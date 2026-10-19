# -*- coding: utf-8 -*-
import tkinter as tk

from .window_utils import setup_window_keyboard
from .window_placement import abrir_na_posicao_da_principal


class ListWindow(tk.Toplevel):
    """Exibe todos os comandos cadastrados (padrão e personalizados),
    com o texto da mensagem, se usa saudação e a origem do comando.
    ESC fecha a tela (equivalente a Voltar)."""

    def __init__(self, master, command_service):
        super().__init__(master)

        self.title("Todas as mensagens")
        self.geometry("480x460")
        abrir_na_posicao_da_principal(self)

        text = tk.Text(self, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)

        for cmd in command_service.get_all():
            origem = "Padrão" if cmd.is_default else "Personalizado"
            saudacao = "Sim" if cmd.greeting else "Não"
            text.insert(
                "end",
                f"Comando: {cmd.trigger}   |   Origem: {origem}   |   Saudação: {saudacao}\n"
                f"{cmd.message}\n"
                f"{'-' * 60}\n\n",
            )

        text.config(state="disabled")

        tk.Button(self, text="Voltar (ESC)", command=self.destroy).pack(pady=5)

        setup_window_keyboard(self, on_escape=self.destroy, focus_widget=self)
