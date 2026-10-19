# -*- coding: utf-8 -*-
"""Camada de persistência dos comandos/mensagens.

O sistema depende apenas da interface `CommandRepository`. Hoje ela é
implementada em arquivo JSON local (`JsonCommandRepository`), mas o
serviço de comandos (`CommandService`) não sabe disso - ele só conhece a
interface. Isso permite, no futuro, criar uma `MySQLCommandRepository`
(usando por exemplo `mysql-connector-python` ou `SQLAlchemy`) e trocar a
implementação em um único lugar (em `app.py`), sem alterar o restante do
sistema.

Gravação segura contra desligamentos/encerramentos abruptos
-------------------------------------------------------------
Se o computador for desligado (ou o processo for encerrado à força pelo
Windows) exatamente durante a gravação do arquivo, uma escrita "ingênua"
(abrir o arquivo e escrever por cima) pode deixar um arquivo pela metade
no disco. Para evitar isso, toda gravação aqui é:

1. Escrita primeiro em um arquivo temporário (`comandos.json.tmp`);
2. Sincronizada fisicamente com o disco (`os.fsync`);
3. Só então promovida ao arquivo definitivo com uma operação atômica do
   sistema operacional (`os.replace`), que nunca deixa o arquivo
   definitivo num estado parcialmente escrito.

Além disso, antes de sobrescrever o arquivo principal, uma cópia de
segurança (`comandos.json.bak`) é atualizada. Se, por qualquer motivo,
o arquivo principal aparecer ausente ou corrompido na próxima leitura,
o sistema recupera automaticamente a partir desse backup, em vez de
"resetar" silenciosamente para os padrões de fábrica.
"""

import json
import logging
import os
import shutil
import threading
from abc import ABC, abstractmethod
from typing import Dict, Optional

from .models import Command

logger = logging.getLogger("sac11")


class CommandRepository(ABC):
    """Interface de persistência de comandos."""

    @abstractmethod
    def load_all(self) -> Dict[str, Command]:
        """Carrega todos os comandos armazenados."""
        raise NotImplementedError

    @abstractmethod
    def save_all(self, commands: Dict[str, Command]) -> None:
        """Persiste todos os comandos informados."""
        raise NotImplementedError


class JsonCommandRepository(CommandRepository):
    """Persistência em arquivo JSON local, com escrita atômica e
    backup/recuperação automática."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._backup_path = file_path + ".bak"
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            self._escrever_arquivo(file_path, {})

    def load_all(self) -> Dict[str, Command]:
        with self._lock:
            raw = self._ler_arquivo(self._file_path)
            if raw is None:
                logger.warning(
                    "Arquivo principal de comandos ausente/corrompido (%s); tentando o backup.",
                    self._file_path,
                )
                raw = self._ler_arquivo(self._backup_path)
                if raw is not None:
                    logger.warning(
                        "Comandos recuperados a partir do backup (%s) - %d comando(s).",
                        self._backup_path,
                        len(raw),
                    )
                    # Restaura o arquivo principal a partir do backup íntegro,
                    # já usando a escrita atômica.
                    self._escrever_arquivo(self._file_path, raw)
                else:
                    logger.error(
                        "Backup também ausente/corrompido; iniciando com lista vazia "
                        "(os padrões de fábrica serão recriados)."
                    )
                    raw = {}

        commands = {trigger: Command.from_dict(trigger, data) for trigger, data in raw.items()}
        logger.info("Carregados %d comando(s) de %s", len(commands), self._file_path)
        return commands

    def save_all(self, commands: Dict[str, Command]) -> None:
        raw = {trigger: cmd.to_dict() for trigger, cmd in commands.items()}
        with self._lock:
            self._atualizar_backup()
            self._escrever_arquivo(self._file_path, raw)
            self._verificar_gravacao(raw)
        logger.info("Salvos %d comando(s) em %s", len(raw), self._file_path)

    # -------------------- auxiliares --------------------
    def _atualizar_backup(self) -> None:
        """Copia o arquivo principal atual (antes de sobrescrevê-lo) para
        o backup, desde que ele exista e esteja íntegro."""
        if not os.path.exists(self._file_path):
            return
        if self._ler_arquivo(self._file_path) is None:
            # Não sobrescreve um backup bom com um arquivo já corrompido.
            return
        try:
            shutil.copyfile(self._file_path, self._backup_path)
        except OSError:
            logger.exception("Não foi possível atualizar o backup de comandos.")

    @staticmethod
    def _escrever_arquivo(path: str, raw: dict) -> None:
        """Grava `raw` em `path` de forma atômica (ver docstring do módulo)."""
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)

    def _verificar_gravacao(self, esperado: dict) -> None:
        """Relê o arquivo recém-gravado e confirma que o conteúdo bate com
        o esperado. Se a gravação foi bloqueada ou não chegou ao disco
        (ex: antivírus/Acesso controlado a pastas), levanta um erro
        explícito em vez de deixar o usuário achar que foi salvo."""
        lido = self._ler_arquivo(self._file_path)
        if lido is None or set(lido.keys()) != set(esperado.keys()):
            raise OSError(
                "A gravação não foi confirmada no disco em "
                f"'{self._file_path}'. Verifique se o Windows Defender "
                "(Acesso controlado a pastas) ou outro antivírus está "
                "bloqueando o programa."
            )

    @staticmethod
    def _ler_arquivo(path: str) -> Optional[dict]:
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            logger.exception("Falha ao ler %s", path)
            return None
