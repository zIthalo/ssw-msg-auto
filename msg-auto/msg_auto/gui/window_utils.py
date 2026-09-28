# -*- coding: utf-8 -*-
"""Utilitário comum para as janelas secundárias do sistema (todas
exceto a inicial): associa o ESC à ação de Voltar/Fechar e garante que
o foco inicial vá para o widget certo, para que a navegação por
teclado funcione desde o primeiro instante em que a tela abre, sem
exigir nenhum clique do mouse."""

import tkinter as tk
from typing import Callable, Optional


def setup_window_keyboard(
    window: tk.Toplevel,
    on_escape: Optional[Callable[[], None]] = None,
    focus_widget: Optional[tk.Widget] = None,
) -> None:
    """
    on_escape: ação equivalente a Voltar/Fechar desta janela. Toda tela
        secundária deve informar isto (apenas a tela inicial do sistema
        não usa este utilitário / passa on_escape=None).
    focus_widget: widget que deve receber o foco inicial (ex: o primeiro
        campo de um formulário, ou a lista de comandos). Quando não
        informado, o foco vai para a própria janela.
    """
    try:
        window.transient(window.master)
    except tk.TclError:
        pass

    if on_escape is not None:
        window.bind("<Escape>", lambda e: on_escape())

    alvo = focus_widget or window
    window.after(10, alvo.focus_set)
