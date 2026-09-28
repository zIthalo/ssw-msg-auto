# -*- coding: utf-8 -*-
"""Serviço responsável por determinar a saudação conforme o horário."""

from datetime import datetime
from typing import Optional


class GreetingService:
    """Gera a saudação de acordo com o horário do sistema.

    - Antes das 12h: "Bom dia."
    - Das 12h às 17h59: "Boa tarde."
    - A partir das 18h: "Boa noite."
    """

    @staticmethod
    def obter_saudacao(hora: Optional[int] = None) -> str:
        h = hora if hora is not None else datetime.now().hour
        if h < 12:
            return "Bom dia."
        elif h < 18:
            return "Boa tarde."
        return "Boa noite."
