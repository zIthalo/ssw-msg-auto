# -*- coding: utf-8 -*-
"""Modelos de dados do sistema."""

from dataclasses import dataclass


@dataclass
class Command:
    """Representa um comando de atalho e a mensagem que ele dispara.

    Atributos:
        trigger: texto digitado pelo usuário que aciona o envio (ex: "//0").
        message: conteúdo da mensagem a ser enviada.
        greeting: se True, a saudação (Bom dia / Boa tarde / Boa noite) é
            adicionada automaticamente antes da mensagem.
        is_default: indica se o comando é um dos padrões de fábrica do
            sistema (apenas informativo; pode ser editado ou excluído
            normalmente pelo usuário).
    """

    trigger: str
    message: str
    greeting: bool = False
    is_default: bool = False

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "greeting": self.greeting,
            "is_default": self.is_default,
        }

    @staticmethod
    def from_dict(trigger: str, data: dict) -> "Command":
        return Command(
            trigger=trigger,
            message=data.get("message", ""),
            greeting=bool(data.get("greeting", False)),
            is_default=bool(data.get("is_default", False)),
        )
