# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from ..command_service import CommandAlreadyExistsError, CommandNotFoundError
from .text_shortcuts import enable_edit_shortcuts
from .window_utils import setup_window_keyboard
from .focus_navigation import enable_arrow_navigation
from .window_placement import abrir_na_posicao_da_principal


class EditWindow(tk.Toplevel):
    """Lista os comandos existentes (padrão e personalizados) e permite
    editar comando, mensagem e saudação de qualquer um deles.

    Totalmente operável por teclado: ↑/↓ navegam pela lista (padrão do
    próprio Listbox), Enter abre o editor do item selecionado e ESC
    fecha a tela (equivalente a Voltar)."""

    def __init__(self, master, command_service):
        super().__init__(master)
        self.command_service = command_service

        self.title("Editar mensagem")
        self.geometry("300x420")
        abrir_na_posicao_da_principal(self)

        tk.Label(self, text="Selecione um comando (Enter ou duplo clique para editar):").pack(pady=5)
        self.listbox = tk.Listbox(self, exportselection=False)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.listbox.bind("<Return>", lambda e: self._abrir_editor())
        self.listbox.bind("<KP_Enter>", lambda e: self._abrir_editor())
        self.listbox.bind("<Double-Button-1>", self._on_duplo_clique)
        self._preencher_lista()

        self.editar_btn = tk.Button(self, text="Editar selecionado", command=self._abrir_editor)
        self.editar_btn.pack(pady=5)
        self.voltar_btn = tk.Button(self, text="Voltar (ESC)", command=self.destroy)
        self.voltar_btn.pack(pady=5)

        enable_arrow_navigation([self.listbox, self.editar_btn, self.voltar_btn])
        setup_window_keyboard(self, on_escape=self.destroy, focus_widget=self.listbox)

    def _preencher_lista(self) -> None:
        self.listbox.delete(0, "end")
        for cmd in self.command_service.get_all():
            marca = " [padrão]" if cmd.is_default else ""
            self.listbox.insert("end", f"{cmd.trigger}{marca}")
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def _on_duplo_clique(self, event) -> str:
        """Duplo clique em um comando abre o editor (comando, mensagem e
        saudação) desse item. Cliques fora de qualquer item são ignorados."""
        indice = self.listbox.nearest(event.y)
        caixa = self.listbox.bbox(indice) if indice >= 0 else None
        if caixa and caixa[1] <= event.y <= caixa[1] + caixa[3]:
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(indice)
            self.listbox.activate(indice)
            self._abrir_editor()
        return "break"

    def _abrir_editor(self) -> None:
        selecao = self.listbox.curselection()
        if not selecao:
            return
        trigger = self.listbox.get(selecao[0]).split(" ")[0]
        cmd = self.command_service.get(trigger)
        if not cmd:
            return
        _EditForm(self, self.command_service, cmd, self._preencher_lista)


class _EditForm(tk.Toplevel):
    def __init__(self, master, command_service, cmd, on_saved):
        super().__init__(master)
        self.command_service = command_service
        self.trigger_atual = cmd.trigger
        self.on_saved = on_saved

        self.title(f"Editando {cmd.trigger}")
        self.geometry("380x480")
        abrir_na_posicao_da_principal(self)

        tk.Label(self, text="Comando").pack(pady=(10, 0))
        self.cmd_entry = tk.Entry(self)
        self.cmd_entry.insert(0, cmd.trigger)
        self.cmd_entry.pack(fill="x", padx=10)
        enable_edit_shortcuts(self.cmd_entry)

        tk.Label(self, text="Mensagem").pack(pady=(10, 0))
        tk.Label(
            self,
            text="Tudo o que for digitado (espaços, Enter, símbolos) é enviado exatamente como está. "
                 "Com saudação marcada, ela vem antes do texto: comece com Enter para pular linha.",
            fg="gray", wraplength=350, justify="left",
        ).pack(padx=10)
        self.msg_text = tk.Text(self, height=12)
        self.msg_text.insert("1.0", cmd.message)
        self.msg_text.pack(fill="both", expand=True, padx=10)
        enable_edit_shortcuts(self.msg_text)

        self.greeting_var = tk.BooleanVar(value=cmd.greeting)
        self.greeting_check = tk.Checkbutton(
            self,
            text="Iniciar com saudação (Bom dia / Boa tarde / Boa noite)",
            variable=self.greeting_var,
        )
        self.greeting_check.pack(pady=10)

        if cmd.is_default:
            tk.Label(self, text="Este é um comando padrão de fábrica.", fg="gray").pack()

        botoes = tk.Frame(self)
        botoes.pack(pady=5)
        self.salvar_btn = tk.Button(botoes, text="Salvar", command=self.salvar)
        self.salvar_btn.pack(side="left", padx=5)
        self.cancelar_btn = tk.Button(botoes, text="Cancelar (ESC)", command=self.destroy)
        self.cancelar_btn.pack(side="left", padx=5)

        enable_arrow_navigation(
            [self.cmd_entry, self.msg_text, self.greeting_check, self.salvar_btn, self.cancelar_btn]
        )
        setup_window_keyboard(self, on_escape=self.destroy, focus_widget=self.cmd_entry)

    def salvar(self) -> None:
        novo_trigger = self.cmd_entry.get().strip()
        # "end-1c" descarta apenas o \n extra que o Tk sempre acrescenta; nada
        # do que o usuário digitou (espaços, Enter, símbolos) é removido.
        message = self.msg_text.get("1.0", "end-1c")
        greeting = self.greeting_var.get()

        if not novo_trigger or not message:
            messagebox.showwarning("Atenção", "Preencha o comando e a mensagem.")
            return

        try:
            self.command_service.editar(self.trigger_atual, novo_trigger, message, greeting)
        except (CommandAlreadyExistsError, CommandNotFoundError) as e:
            messagebox.showerror("Erro", str(e))
            return

        messagebox.showinfo("Sucesso", "Comando atualizado.")
        self.on_saved()
        self.destroy()
