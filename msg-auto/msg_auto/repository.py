# -*- coding: utf-8 -*-
"""Camada de persistência dos comandos/mensagens.

O sistema depende apenas da interface `CommandRepository`. Hoje ela é
implementada em arquivo JSON local (`JsonCommandRepository`), mas o
serviço de comandos (`CommandService`) não sabe disso - ele só conhece a
interface. Isso permite, no futuro, criar uma `MySQLCommandRepository`
(usando por exemplo `mysql-connector-python` ou `SQLAlchemy`) e trocar a
implementação em um único lugar (em `app.py`), sem alterar o restante do
sistema.
"""

import json
import os
import threading
from abc import ABC, abstractmethod
from typing import Dict

from .models import Command


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
    """Persistência simples em arquivo JSON local."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load_all(self) -> Dict[str, Command]:
        with self._lock:
            with open(self._file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        return {trigger: Command.from_dict(trigger, data) for trigger, data in raw.items()}

    def save_all(self, commands: Dict[str, Command]) -> None:
        raw = {trigger: cmd.to_dict() for trigger, cmd in commands.items()}
        with self._lock:
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(raw, f, indent=2, ensure_ascii=False)
