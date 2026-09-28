# -*- coding: utf-8 -*-
import tkinter as tk

from .settings_window import SettingsWindow
from .keyboard_menu import KeyboardMenu


class MainWindow(tk.Tk):
    """Janela principal (tela inicial). Possui 2 opções numeradas:
    1 - Configurações, 2 - Sair. Totalmente navegável por ↑/↓, Enter e
    pelos números 1/2. O ESC não fecha o sistema nesta tela."""

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.title("Mensagens Automáticas - SAC")
        self.geometry("380x260")
        self.resizable(False, False)

        tk.Label(self, text="Sistema ativo", font=("Segoe UI", 12, "bold")).pack(pady=15)
        tk.Label(
            self,
            text="Digite um comando (ex: //0) em qualquer campo de\ntexto para enviar a mensagem correspondente.",
            justify="center",
        ).pack(pady=5)

        self.menu = KeyboardMenu(
            self,
            options=[
                ("Configurações", self.abrir_configuracoes),
                ("Sair", self.sair),
            ],
            on_escape=None,  # ESC não fecha o sistema na tela inicial
            button_width=24,
        )
        self.menu.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.sair)

    def abrir_configuracoes(self) -> None:
        SettingsWindow(self, self.app)

    def sair(self) -> None:
        self.app.shutdown()
        self.destroy()
