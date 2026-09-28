# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from ..command_service import CommandAlreadyExistsError
from .text_shortcuts import enable_edit_shortcuts
from .window_utils import setup_window_keyboard
from .focus_navigation import enable_arrow_navigation


class RegisterWindow(tk.Toplevel):
    """Tela de cadastro de uma nova mensagem/comando."""

    def __init__(self, master, command_service):
        super().__init__(master)
        self.command_service = command_service

        self.title("Nova mensagem")
        self.geometry("380x440")

        tk.Label(self, text="Comando (ex: //9, **a, --z)").pack(pady=(10, 0))
        self.cmd_entry = tk.Entry(self)
        self.cmd_entry.pack(fill="x", padx=10)
        enable_edit_shortcuts(self.cmd_entry)

        tk.Label(self, text="Mensagem").pack(pady=(10, 0))
        self.msg_text = tk.Text(self, height=12)
        self.msg_text.pack(fill="both", expand=True, padx=10)
        enable_edit_shortcuts(self.msg_text)

        self.greeting_var = tk.BooleanVar(value=True)
        self.greeting_check = tk.Checkbutton(
            self,
            text="Iniciar com saudação (Bom dia / Boa tarde / Boa noite)",
            variable=self.greeting_var,
        )
        self.greeting_check.pack(pady=10)

        botoes = tk.Frame(self)
        botoes.pack(pady=5)
        self.salvar_btn = tk.Button(botoes, text="Salvar", command=self.salvar)
        self.salvar_btn.pack(side="left", padx=5)
        self.cancelar_btn = tk.Button(botoes, text="Cancelar", command=self.destroy)
        self.cancelar_btn.pack(side="left", padx=5)

        enable_arrow_navigation(
            [self.cmd_entry, self.msg_text, self.greeting_check, self.salvar_btn, self.cancelar_btn]
        )
        setup_window_keyboard(self, on_escape=self.destroy, focus_widget=self.cmd_entry)

    def salvar(self) -> None:
        trigger = self.cmd_entry.get().strip()
        message = self.msg_text.get("1.0", "end").strip()
        greeting = self.greeting_var.get()

        if not trigger or not message:
            messagebox.showwarning("Atenção", "Preencha o comando e a mensagem.")
            return

        try:
            self.command_service.criar(trigger, message, greeting)
        except CommandAlreadyExistsError as e:
            messagebox.showerror("Erro", str(e))
            return

        messagebox.showinfo("Sucesso", f"Comando '{trigger}' cadastrado.")
        self.destroy()
