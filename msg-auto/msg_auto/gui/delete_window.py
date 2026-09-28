# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from ..command_service import CommandNotFoundError
from .window_utils import setup_window_keyboard
from .confirm_dialog import ConfirmDialog
from .focus_navigation import enable_arrow_navigation


class DeleteWindow(tk.Toplevel):
    """Lista os comandos existentes e permite excluir o selecionado.

    Totalmente operável por teclado: ↑/↓ navegam pela lista, Enter
    aciona a exclusão do item selecionado (com confirmação) e ESC fecha
    a tela (equivalente a Voltar)."""

    def __init__(self, master, command_service):
        super().__init__(master)
        self.command_service = command_service

        self.title("Excluir mensagem")
        self.geometry("300x420")

        tk.Label(self, text="Selecione um comando para excluir (Enter para excluir):").pack(pady=5)
        self.listbox = tk.Listbox(self, exportselection=False)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.listbox.bind("<Return>", lambda e: self._excluir())
        self.listbox.bind("<KP_Enter>", lambda e: self._excluir())
        self._preencher_lista()

        self.excluir_btn = tk.Button(self, text="Excluir selecionado", command=self._excluir)
        self.excluir_btn.pack(pady=5)
        self.voltar_btn = tk.Button(self, text="Voltar (ESC)", command=self.destroy)
        self.voltar_btn.pack(pady=5)

        enable_arrow_navigation([self.listbox, self.excluir_btn, self.voltar_btn])
        setup_window_keyboard(self, on_escape=self.destroy, focus_widget=self.listbox)

    def _preencher_lista(self) -> None:
        self.listbox.delete(0, "end")
        for cmd in self.command_service.get_all():
            marca = " [padrão]" if cmd.is_default else ""
            self.listbox.insert("end", f"{cmd.trigger}{marca}")
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def _excluir(self) -> None:
        selecao = self.listbox.curselection()
        if not selecao:
            return
        trigger = self.listbox.get(selecao[0]).split(" ")[0]

        def ao_confirmar(sim: bool) -> None:
            if not sim:
                return
            try:
                self.command_service.excluir(trigger)
            except CommandNotFoundError as e:
                messagebox.showerror("Erro", str(e))
                return
            self._preencher_lista()

        ConfirmDialog(self, f"Excluir o comando '{trigger}'?", ao_confirmar)
