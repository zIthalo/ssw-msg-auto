# -*- coding: utf-8 -*-
"""Camada de serviço: regras de negócio de cadastro, edição, exclusão
e disparo de comandos/mensagens. Não depende de Tkinter nem de teclado -
pode ser testada isoladamente."""

from typing import Dict, List, Optional

from .models import Command
from .repository import CommandRepository
from .seed_data import DEFAULT_COMMANDS
from .greeting import GreetingService
from .sender import ClipboardSender


class CommandAlreadyExistsError(Exception):
    """Levantado ao tentar cadastrar um comando que já existe."""


class CommandNotFoundError(Exception):
    """Levantado ao tentar editar/excluir um comando inexistente."""


class CommandService:
    def __init__(self, repository: CommandRepository, sender: ClipboardSender, greeting_service: GreetingService):
        self._repository = repository
        self._sender = sender
        self._greeting_service = greeting_service
        self._commands: Dict[str, Command] = {}
        self._load()

    # -------------------- carregamento / seed --------------------
    def _load(self) -> None:
        stored = self._repository.load_all()
        if not stored:
            stored = {c.trigger: Command(c.trigger, c.message, c.greeting, c.is_default) for c in DEFAULT_COMMANDS}
            self._repository.save_all(stored)
        self._commands = stored

    def restaurar_padrao(self) -> None:
        """Recoloca os textos padrão de fábrica (sem remover comandos
        personalizados já cadastrados pelo usuário)."""
        for c in DEFAULT_COMMANDS:
            self._commands[c.trigger] = Command(c.trigger, c.message, c.greeting, is_default=True)
        self._repository.save_all(self._commands)

    # -------------------- consultas --------------------
    def get_all(self) -> List[Command]:
        return sorted(self._commands.values(), key=lambda c: c.trigger)

    def get(self, trigger: str) -> Optional[Command]:
        return self._commands.get(trigger)

    def all_triggers_by_length(self) -> List[str]:
        """Gatilhos ordenados do mais longo para o mais curto, para que
        o reconhecimento de comandos priorize sempre o casamento mais
        específico."""
        return sorted(self._commands.keys(), key=len, reverse=True)

    # -------------------- CRUD --------------------
    def criar(self, trigger: str, message: str, greeting: bool) -> None:
        trigger = trigger.strip()
        if not trigger:
            raise ValueError("O comando não pode ser vazio.")
        if trigger in self._commands:
            raise CommandAlreadyExistsError(f"O comando '{trigger}' já existe.")
        self._commands[trigger] = Command(trigger, message, greeting, is_default=False)
        self._repository.save_all(self._commands)

    def editar(self, trigger_atual: str, novo_trigger: str, message: str, greeting: bool) -> None:
        if trigger_atual not in self._commands:
            raise CommandNotFoundError(f"O comando '{trigger_atual}' não existe.")

        novo_trigger = novo_trigger.strip()
        if not novo_trigger:
            raise ValueError("O comando não pode ser vazio.")
        if novo_trigger != trigger_atual and novo_trigger in self._commands:
            raise CommandAlreadyExistsError(f"O comando '{novo_trigger}' já existe.")

        existente = self._commands.pop(trigger_atual)
        self._commands[novo_trigger] = Command(
            trigger=novo_trigger,
            message=message,
            greeting=greeting,
            is_default=existente.is_default,
        )
        self._repository.save_all(self._commands)

    def excluir(self, trigger: str) -> None:
        if trigger not in self._commands:
            raise CommandNotFoundError(f"O comando '{trigger}' não existe.")
        del self._commands[trigger]
        self._repository.save_all(self._commands)

    # -------------------- execução --------------------
    def executar(self, trigger: str) -> None:
        cmd = self._commands.get(trigger)
        if not cmd:
            return
        if cmd.greeting:
            self._sender.send(self._greeting_service.obter_saudacao(), cmd.message)
        else:
            self._sender.send(cmd.message)
