# -*- coding: utf-8 -*-
"""Atalhos de edição de texto (Ctrl+Z, Ctrl+Backspace, Ctrl+Delete)
aplicáveis a qualquer campo `Entry` ou `Text` do sistema.

A navegação com as setas do teclado já é nativa do Tkinter; o que
impedia seu funcionamento correto nas telas de cadastro era o hook
global de teclado do `HotkeyListener` competindo com a digitação (ver
`SettingsWindow`, que agora pausa o listener enquanto essas telas estão
abertas). Este módulo garante, adicionalmente, os atalhos de edição de
texto que o Tkinter não oferece prontos por padrão.
"""

import tkinter as tk


def enable_edit_shortcuts(widget) -> None:
    """Habilita Ctrl+Z (desfazer), Ctrl+Backspace (apaga a palavra
    anterior ao cursor) e Ctrl+Delete (apaga a palavra seguinte ao
    cursor) no `widget` informado. Funciona tanto em `tk.Entry` quanto
    em `tk.Text`."""

    is_text = isinstance(widget, tk.Text)

    if is_text:
        try:
            widget.configure(undo=True, autoseparators=True, maxundo=-1)
        except tk.TclError:
            pass
        widget.bind("<Control-z>", lambda e: _undo_text(widget))
        widget.bind("<Control-Z>", lambda e: _undo_text(widget))
    else:
        _attach_entry_undo(widget)

    widget.bind("<Control-BackSpace>", lambda e: _apagar_palavra(widget, is_text, para_tras=True))
    widget.bind("<Control-Delete>", lambda e: _apagar_palavra(widget, is_text, para_tras=False))


def _undo_text(widget: tk.Text) -> str:
    try:
        widget.edit_undo()
    except tk.TclError:
        pass
    return "break"


def _attach_entry_undo(entry: tk.Entry) -> None:
    """`tk.Entry` não possui pilha de undo nativa; mantemos um histórico
    simples de valores para permitir Ctrl+Z também no campo de comando."""
    historico = [entry.get()]

    def registrar(_event=None):
        valor = entry.get()
        if not historico or historico[-1] != valor:
            historico.append(valor)

    def desfazer(_event=None):
        if len(historico) > 1:
            historico.pop()
            entry.delete(0, "end")
            entry.insert(0, historico[-1])
        return "break"

    entry.bind("<KeyRelease>", registrar, add="+")
    entry.bind("<Control-z>", desfazer)
    entry.bind("<Control-Z>", desfazer)


def _apagar_palavra(widget, is_text: bool, para_tras: bool) -> str:
    if is_text:
        pos = widget.index("insert")
        if para_tras:
            texto_ate_cursor = widget.get("1.0", pos)
            offset_inicio = _indice_palavra_anterior(texto_ate_cursor)
            widget.delete(f"1.0+{offset_inicio}c", pos)
        else:
            texto_apos_cursor = widget.get(pos, "end")
            offset_fim = _indice_palavra_seguinte(texto_apos_cursor)
            widget.delete(pos, f"{pos}+{offset_fim}c")
    else:
        pos = widget.index("insert")
        texto = widget.get()
        if para_tras:
            antes = texto[:pos]
            nova_pos = _indice_palavra_anterior(antes)
            widget.delete(nova_pos, pos)
            widget.icursor(nova_pos)
        else:
            depois = texto[pos:]
            offset = _indice_palavra_seguinte(depois)
            widget.delete(pos, pos + offset)
    return "break"


def _indice_palavra_anterior(texto: str) -> int:
    i = len(texto)
    while i > 0 and texto[i - 1].isspace():
        i -= 1
    while i > 0 and not texto[i - 1].isspace():
        i -= 1
    return i


def _indice_palavra_seguinte(texto: str) -> int:
    i, n = 0, len(texto)
    while i < n and texto[i].isspace():
        i += 1
    while i < n and not texto[i].isspace():
        i += 1
    # Também consome o espaço até o início da próxima palavra, como a
    # maioria dos editores faz no Ctrl+Delete.
    while i < n and texto[i].isspace():
        i += 1
    return i
