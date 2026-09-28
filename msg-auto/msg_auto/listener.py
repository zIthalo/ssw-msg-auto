# -*- coding: utf-8 -*-
"""Captura global de teclado: identifica quando o usuário digitou um
comando cadastrado, apaga o texto digitado e envia o comando para a
fila de execução."""

import threading
from queue import Queue

import keyboard

from .config import KEY_BUFFER_MAX
from .command_service import CommandService
from .sender import ClipboardSender


class HotkeyListener:
    def __init__(self, command_service: CommandService, sender: ClipboardSender, command_queue: Queue):
        self._command_service = command_service
        self._sender = sender
        self._queue = command_queue
        self._buffer = ""
        self._pause_count = 0
        self._pause_lock = threading.Lock()
        self._hook = None

    def pause(self) -> None:
        """Pausa o reconhecimento de comandos. Reentrante: pode ser
        chamado por mais de um lugar ao mesmo tempo (ex: a thread que
        executa o envio E uma tela de cadastro aberta); o listener só
        volta a ficar ativo quando todos os chamadores tiverem chamado
        `resume()`. Isso evita que o hook global de teclado interfira
        enquanto o usuário digita dentro das próprias telas do sistema
        (o que antes corrompia o texto sendo digitado nos cadastros)."""
        with self._pause_lock:
            self._pause_count += 1
        self._buffer = ""

    def resume(self) -> None:
        with self._pause_lock:
            self._pause_count = max(0, self._pause_count - 1)

    @property
    def _is_paused(self) -> bool:
        with self._pause_lock:
            return self._pause_count > 0

    def start(self) -> None:
        self._hook = keyboard.on_press(self._on_press)

    def stop(self) -> None:
        if self._hook:
            keyboard.unhook(self._hook)
            self._hook = None

    def _on_press(self, event) -> None:
        if self._is_paused:
            return

        nome = event.name
        if nome is None:
            return

        if len(nome) == 1:
            ch = nome
        elif nome in ("slash", "/"):
            ch = "/"
        elif nome == "backspace":
            self._buffer = self._buffer[:-1]
            return
        else:
            return

        self._buffer = (self._buffer + ch)[-KEY_BUFFER_MAX:]

        for trigger in self._command_service.all_triggers_by_length():
            if trigger in self._buffer:
                self.pause()
                self._sender.apagar_comando(len(trigger))
                self._queue.put(trigger)
                self._buffer = ""
                self.resume()
                return
