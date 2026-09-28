# -*- coding: utf-8 -*-
"""Envio de texto para o aplicativo em foco (ex: WhatsApp Web).

Estratégia escolhida: usar a área de transferência (mais rápido e 100%
confiável com acentuação/emoji) só durante a colagem, e restaurar
imediatamente o conteúdo que o usuário tinha copiado antes - assim o
clipboard não fica "sujo" com as mensagens do sistema.
"""

import time
from typing import Optional

import pyperclip
import pyautogui

from .config import PASTE_DELAY, CLIPBOARD_RESTORE_DELAY, BACKSPACE_DELAY


class ClipboardSender:
    """Envia texto colando via área de transferência, restaurando o
    conteúdo original do usuário logo em seguida."""

    def __init__(self, paste_delay: float = PASTE_DELAY, restore_delay: float = CLIPBOARD_RESTORE_DELAY):
        self._paste_delay = paste_delay
        self._restore_delay = restore_delay

    def send(self, *parts: str) -> None:
        """Cola, em sequência, cada texto de `parts` no campo em foco e
        restaura o clipboard original do usuário ao final."""
        original_clipboard = self._safe_get_clipboard()
        try:
            for msg in parts:
                texto = self._normalizar(msg)
                pyperclip.copy(texto)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(self._paste_delay)
        finally:
            # Aguarda a colagem terminar de ser processada pelo app de
            # destino antes de trocar o clipboard de volta.
            time.sleep(self._restore_delay)
            self._safe_set_clipboard(original_clipboard)

    @staticmethod
    def apagar_comando(tamanho: int, delay: float = BACKSPACE_DELAY) -> None:
        """Apaga do campo de texto os caracteres do comando digitado."""
        for _ in range(tamanho):
            pyautogui.press("backspace")
            time.sleep(delay)

    @staticmethod
    def _normalizar(msg) -> str:
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8", errors="ignore")
        try:
            # Corrige encoding bugado vindo de fontes externas (compatibilidade
            # com o comportamento do script original).
            return msg.encode("latin1").decode("utf-8")
        except Exception:
            return msg

    @staticmethod
    def _safe_get_clipboard() -> Optional[str]:
        try:
            return pyperclip.paste()
        except Exception:
            return ""

    @staticmethod
    def _safe_set_clipboard(content: Optional[str]) -> None:
        try:
            pyperclip.copy(content or "")
        except Exception:
            pass
