# -*- coding: utf-8 -*-
"""Ponto de composição do sistema: cria e conecta todas as camadas
(persistência, serviço, envio, listener e interface gráfica)."""

import logging
import os
import threading
from queue import Queue

from .config import COMMANDS_FILE, LOG_FILE, DATA_DIR
from .repository import JsonCommandRepository
from .sender import ClipboardSender
from .greeting import GreetingService
from .command_service import CommandService
from .listener import HotkeyListener


def _configurar_log() -> logging.Logger:
    # Garante que a pasta data/ exista antes do FileHandler tentar abrir
    # o arquivo de log (evita FileNotFoundError em uma instalação nova).
    os.makedirs(DATA_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("sac11")


class Application:
    """Composition root: monta as dependências e mantém a thread
    worker responsável por executar os comandos enfileirados."""

    def __init__(self):
        self.logger = _configurar_log()
        self.running = True
        self.command_queue: Queue = Queue()

        repository = JsonCommandRepository(COMMANDS_FILE)
        self.sender = ClipboardSender()
        greeting_service = GreetingService()
        self.command_service = CommandService(repository, self.sender, greeting_service)
        self.listener = HotkeyListener(self.command_service, self.sender, self.command_queue)

        self._worker_thread = threading.Thread(target=self._worker, daemon=True)

    def _worker(self) -> None:
        while self.running:
            try:
                trigger = self.command_queue.get(timeout=0.5)
            except Exception:
                continue

            # Pausa o listener enquanto o próprio sistema cola o texto,
            # para o Ctrl+V não ser interpretado como digitação do usuário.
            self.listener.pause()
            try:
                self.command_service.executar(trigger)
                self.logger.info("Comando executado: %s", trigger)
            except Exception:
                self.logger.exception("Falha ao executar comando: %s", trigger)
            finally:
                self.listener.resume()
                self.command_queue.task_done()

    def start(self) -> None:
        # Import tardio para não obrigar Tkinter a carregar em testes
        # que usem apenas a camada de serviço.
        from .gui.main_window import MainWindow

        self._worker_thread.start()
        self.listener.start()

        window = MainWindow(self)
        window.mainloop()

    def shutdown(self) -> None:
        self.running = False
        self.listener.stop()
