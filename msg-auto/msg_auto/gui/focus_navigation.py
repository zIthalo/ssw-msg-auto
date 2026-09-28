# -*- coding: utf-8 -*-
"""Navegação por ↑/↓ entre os campos e botões de uma tela.

Usado nas telas de cadastro, edição e exclusão de mensagens: apenas as
setas para cima/baixo movem o foco entre os elementos da tela, na
ordem em que forem informados - sem atalhos numéricos, mantendo essas
telas simples.
"""

import tkinter as tk
from typing import List


def enable_arrow_navigation(widgets: List[tk.Widget]) -> None:
    """Habilita a navegação por ↑/↓ entre os `widgets`, na ordem dada.

    - Em `Entry`, `Checkbutton` e `Button`: a seta sempre move o foco
      para o widget anterior/seguinte da lista.
    - Em `Text` (campo de mensagem, multilinha): as setas continuam
      movendo o cursor dentro do texto normalmente; o foco só passa
      para o widget anterior/seguinte quando o cursor já está na
      primeira linha (seta para cima) ou na última linha (seta para
      baixo) do texto.
    - Em `Listbox` (lista de comandos): as setas continuam navegando
      entre os itens normalmente; o foco só passa para o widget
      anterior/seguinte quando a seleção já está no primeiro item
      (seta para cima) ou no último item (seta para baixo).
    """
    n = len(widgets)
    if n < 2:
        return

    for i, widget in enumerate(widgets):
        anterior = widgets[i - 1]
        seguinte = widgets[(i + 1) % n]

        if isinstance(widget, tk.Text):
            widget.bind("<Up>", _make_text_handler(widget, anterior, topo=True))
            widget.bind("<Down>", _make_text_handler(widget, seguinte, topo=False))
        elif isinstance(widget, tk.Listbox):
            widget.bind("<Up>", _make_listbox_handler(widget, anterior, topo=True))
            widget.bind("<Down>", _make_listbox_handler(widget, seguinte, topo=False))
        else:
            widget.bind("<Up>", lambda e, alvo=anterior: _focar(alvo))
            widget.bind("<Down>", lambda e, alvo=seguinte: _focar(alvo))


def _focar(widget: tk.Widget) -> str:
    widget.focus_set()
    return "break"


def _make_text_handler(widget: tk.Text, alvo: tk.Widget, topo: bool):
    def handler(event):
        linha_atual = int(widget.index("insert").split(".")[0])
        if topo:
            if linha_atual <= 1:
                return _focar(alvo)
        else:
            ultima_linha = int(widget.index("end-1c").split(".")[0])
            if linha_atual >= ultima_linha:
                return _focar(alvo)
        return None  # deixa o comportamento padrão (mover o cursor) acontecer

    return handler


def _make_listbox_handler(widget: tk.Listbox, alvo: tk.Widget, topo: bool):
    def handler(event):
        selecao = widget.curselection()
        indice = selecao[0] if selecao else 0
        if topo and indice <= 0:
            return _focar(alvo)
        if not topo and indice >= widget.size() - 1:
            return _focar(alvo)
        return None  # deixa a navegação padrão da lista acontecer

    return handler
