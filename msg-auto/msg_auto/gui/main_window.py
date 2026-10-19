# -*- coding: utf-8 -*-
import logging
import traceback
import tkinter as tk
from tkinter import messagebox

from .settings_window import SettingsWindow
from .keyboard_menu import KeyboardMenu
from .window_placement import MainWindowPositionKeeper


class MainWindow(tk.Tk):
    """Janela principal (tela inicial). Possui 2 opções numeradas:
    1 - Configurações, 2 - Sair. Totalmente navegável por ↑/↓, Enter e
    pelos números 1/2. O ESC não fecha o sistema nesta tela."""

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.title("Mensagens Automáticas - SAC")
        # Abre onde o usuário fechou da última vez e continua acompanhando.
        self.position_keeper = MainWindowPositionKeeper(self)
        self.geometry(self.position_keeper.geometry_for(380, 260))
        self.position_keeper.start_tracking()
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

    def report_callback_exception(self, exc_type, exc_value, exc_tb) -> None:
        """Rede de segurança: qualquer erro não tratado em qualquer tela
        (todas compartilham este interpretador Tk) é registrado no log e
        mostrado ao usuário, em vez de sumir silenciosamente. Assim, uma
        falha ao salvar nunca passa despercebida."""
        logging.getLogger("sac11").error(
            "Erro não tratado na interface", exc_info=(exc_type, exc_value, exc_tb)
        )
        detalhe = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
        messagebox.showerror(
            "Ocorreu um erro",
            "A ação NÃO foi concluída (nada foi alterado).\n\n"
            f"Detalhe: {detalhe}\n\n"
            "Mais informações no arquivo de log (sac11.log).",
        )

    def abrir_configuracoes(self) -> None:
        SettingsWindow(self, self.app)

    def sair(self) -> None:
        self.position_keeper.save_now()
        self.app.shutdown()
        self.destroy()
