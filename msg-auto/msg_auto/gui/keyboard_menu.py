# -*- coding: utf-8 -*-
"""Menu de opções numeradas, totalmente navegável pelo teclado.

Usado nas telas que apresentam uma lista fixa e pequena de opções
(tela inicial, configurações, confirmações). Suporta:

- ↑ / ↓: move o foco entre as opções (com destaque visual).
- Enter (inclusive o Enter do teclado numérico): confirma a opção
  atualmente focada.
- Teclas numéricas 1-9 (linha superior OU numpad, quando o NumLock
  está ativo): acessam diretamente a opção correspondente, sem
  precisar navegar pelas setas. A tecla 0 aciona a 10ª opção, se
  existir.
"""

import tkinter as tk
from typing import Callable, List, Optional, Tuple

FOCUS_BG = "#3B6EC7"
FOCUS_FG = "#FFFFFF"


class KeyboardMenu:
    def __init__(
        self,
        master: tk.Widget,
        options: List[Tuple[str, Callable[[], None]]],
        on_escape: Optional[Callable[[], None]] = None,
        button_width: int = 32,
    ):
        """
        options: lista de tuplas (rótulo, callback), na ordem em que
            devem aparecer e ser numeradas (1, 2, 3, ...).
        on_escape: função chamada quando o usuário pressiona ESC. Se for
            None, ESC não executa nenhuma ação (usado na tela inicial).
        """
        self.master = master
        self._options = options
        self._buttons: List[tk.Button] = []
        self._index = 0
        self._normal_bg = None

        self.frame = tk.Frame(master)

        for i, (label, _callback) in enumerate(options, start=1):
            numero = i if i <= 9 else (0 if i == 10 else None)
            texto = f"{numero} - {label}" if numero is not None else label
            btn = tk.Button(
                self.frame,
                text=texto,
                width=button_width,
                anchor="w",
                relief="raised",
                command=self._make_activator(i - 1),
            )
            btn.pack(pady=3, fill="x", padx=4)
            if self._normal_bg is None:
                self._normal_bg = btn.cget("bg")
            self._buttons.append(btn)

        top = master.winfo_toplevel()
        top.bind("<Up>", self._mover_cima, add="+")
        top.bind("<Down>", self._mover_baixo, add="+")
        top.bind("<Return>", self._confirmar, add="+")
        top.bind("<KP_Enter>", self._confirmar, add="+")
        top.bind("<Key>", self._tecla_numerica, add="+")
        if on_escape is not None:
            top.bind("<Escape>", lambda e: on_escape(), add="+")

        if self._buttons:
            self.frame.after(10, lambda: self._focar(0))

    def pack(self, **kwargs) -> None:
        self.frame.pack(**kwargs)

    # -------------------- callbacks internos --------------------
    def _make_activator(self, idx: int):
        def _ativar():
            self._focar(idx)
            self._options[idx][1]()

        return _ativar

    def _focar(self, idx: int) -> None:
        if not self._buttons:
            return
        idx = max(0, min(idx, len(self._buttons) - 1))
        for i, btn in enumerate(self._buttons):
            if i == idx:
                btn.configure(bg=FOCUS_BG, fg=FOCUS_FG, relief="sunken")
            else:
                btn.configure(bg=self._normal_bg, fg="black", relief="raised")
        self._index = idx
        self._buttons[idx].focus_set()

    def _mover_cima(self, event) -> str:
        self._focar((self._index - 1) % len(self._buttons))
        return "break"

    def _mover_baixo(self, event) -> str:
        self._focar((self._index + 1) % len(self._buttons))
        return "break"

    def _confirmar(self, event) -> str:
        self._make_activator(self._index)()
        return "break"

    def _tecla_numerica(self, event) -> Optional[str]:
        ch = event.char
        if not ch or not ch.isdigit():
            return None
        n = int(ch)
        idx = 9 if n == 0 else n - 1
        if 0 <= idx < len(self._buttons):
            self._make_activator(idx)()
            return "break"
        return None
