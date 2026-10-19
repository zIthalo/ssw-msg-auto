# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from .register_window import RegisterWindow
from .edit_window import EditWindow
from .delete_window import DeleteWindow
from .list_window import ListWindow
from .keyboard_menu import KeyboardMenu
from .confirm_dialog import ConfirmDialog
from .window_placement import abrir_na_posicao_da_principal


class SettingsWindow(tk.Toplevel):
    """Menu de configurações: 6 opções numeradas, navegáveis por
    ↑/↓, Enter e pelos números 1 a 6. ESC equivale à opção 6 - Voltar.

    Enquanto esta janela (e as telas abertas a partir dela) estiver
    aberta, o hook global de teclado do sistema fica pausado. Isso evita
    que o reconhecimento de comandos interfira na digitação dentro dos
    próprios campos de cadastro/edição - era essa interferência que
    fazia comandos e mensagens novas se perderem, além de atrapalhar a
    navegação por teclado.
    """

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.command_service = app.command_service

        self.title("Configurações")
        self.geometry("300x330")
        abrir_na_posicao_da_principal(self)
        self.resizable(False, False)

        self.menu = KeyboardMenu(
            self,
            options=[
                ("Nova mensagem", self.nova),
                ("Editar mensagem", self.editar),
                ("Excluir mensagem", self.deletar),
                ("Listar todas", self.listar),
                ("Restaurar padrões de fábrica", self.restaurar),
                ("Voltar", self._fechar),
            ],
            on_escape=self._fechar,
            button_width=30,
        )
        self.menu.pack(pady=10)

        self.app.listener.pause()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._fechar)

    def _fechar(self) -> None:
        self.app.listener.resume()
        self.destroy()

    def nova(self) -> None:
        RegisterWindow(self, self.command_service)

    def editar(self) -> None:
        EditWindow(self, self.command_service)

    def deletar(self) -> None:
        DeleteWindow(self, self.command_service)

    def listar(self) -> None:
        ListWindow(self, self.command_service)

    def restaurar(self) -> None:
        def ao_confirmar(sim: bool) -> None:
            if sim:
                self.command_service.restaurar_padrao()
                messagebox.showinfo("Pronto", "Mensagens padrão restauradas.")

        ConfirmDialog(
            self,
            "Tem certeza que deseja restaurar os padrões de fábrica?",
            ao_confirmar,
        )
