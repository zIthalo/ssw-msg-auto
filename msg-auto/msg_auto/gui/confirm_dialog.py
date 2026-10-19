# -*- coding: utf-8 -*-
"""Janela de confirmação Sim/Não, totalmente navegável pelo teclado.

Usada para operações potencialmente destrutivas (ex: restaurar padrões
de fábrica). Enquanto está aberta, captura o foco de teclado, então o
ESC e as teclas de navegação atuam sobre ela primeiro - a tela por trás
só volta a responder depois que esta janela for fechada.
"""

import tkinter as tk
from typing import Callable

from .keyboard_menu import KeyboardMenu
from .window_placement import abrir_na_posicao_da_principal


class ConfirmDialog(tk.Toplevel):
    def __init__(self, master, mensagem: str, on_confirm: Callable[[bool], None]):
        super().__init__(master)
        self.on_confirm = on_confirm

        self.title("Confirmação")
        self.geometry("340x200")
        abrir_na_posicao_da_principal(self)
        self.resizable(False, False)
        self.transient(master)

        tk.Label(self, text=mensagem, wraplength=300, justify="center").pack(pady=(20, 10), padx=15)

        self.menu = KeyboardMenu(
            self,
            options=[
                ("Sim", self._confirmar_sim),
                ("Não", self._confirmar_nao),
            ],
            on_escape=self._confirmar_nao,
            button_width=20,
        )
        self.menu.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self._confirmar_nao)
        self.grab_set()
        self.after(10, self.focus_force)

    def _confirmar_sim(self) -> None:
        self.grab_release()
        self.destroy()
        self.on_confirm(True)

    def _confirmar_nao(self) -> None:
        self.grab_release()
        self.destroy()
        self.on_confirm(False)
