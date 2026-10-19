# -*- coding: utf-8 -*-
"""Posição das janelas.

- A janela principal abre onde o usuário a deixou da última vez
  (`MainWindowPositionKeeper`).
- Todas as demais janelas (configurações, suas subtelas e as
  confirmações) abrem na mesma posição em que a janela principal está
  naquele momento (`abrir_na_posicao_da_principal`).

A persistência é um detalhe de conveniência: qualquer falha ao ler ou
gravar a posição é apenas registrada no log e nunca interrompe o uso.
"""

import json
import logging
import os
import re
import tkinter as tk
from typing import Optional, Tuple

from ..config import WINDOW_STATE_FILE

logger = logging.getLogger("sac11")

# Formato devolvido por Tk: "380x260+100+50" (coordenadas podem ser negativas).
_GEOMETRIA = re.compile(r"^(\d+)x(\d+)\+(-?\d+)\+(-?\d+)$")

# Tolerância para janelas encostadas na borda da tela (no Windows é comum -8).
_TOLERANCIA = 20


def parse_geometry(geometria: str) -> Optional[Tuple[int, int, int, int]]:
    """Converte "LxA+X+Y" em (largura, altura, x, y). None se inválida."""
    m = _GEOMETRIA.match(geometria or "")
    if not m:
        return None
    return tuple(int(v) for v in m.groups())  # type: ignore[return-value]


class WindowPlacement:
    """Persistência da posição (x, y) da janela principal em arquivo JSON."""

    def __init__(self, file_path: str = WINDOW_STATE_FILE):
        self._file_path = file_path

    def load(self) -> Optional[Tuple[int, int]]:
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return int(dados["x"]), int(dados["y"])
        except FileNotFoundError:
            return None
        except (OSError, ValueError, KeyError, TypeError):
            logger.warning("Posição salva da janela inválida; usando a padrão.", exc_info=True)
            return None

    def save(self, x: int, y: int) -> None:
        tmp = self._file_path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({"x": int(x), "y": int(y)}, f)
            os.replace(tmp, self._file_path)
        except OSError:
            logger.warning("Não foi possível salvar a posição da janela.", exc_info=True)

    @staticmethod
    def is_visible(x: int, y: int, limites: Tuple[int, int, int, int]) -> bool:
        """True se (x, y) cai dentro da área de tela (esquerda, topo, direita,
        base). Evita abrir a janela fora da tela se, por exemplo, o monitor
        onde ela estava deixou de existir."""
        esquerda, topo, direita, base = limites
        return (
            esquerda - _TOLERANCIA <= x <= direita - 100
            and topo - _TOLERANCIA <= y <= base - 100
        )


class MainWindowPositionKeeper:
    """Restaura a posição da janela principal ao abrir e a mantém salva."""

    def __init__(self, root: tk.Tk, placement: Optional[WindowPlacement] = None):
        self._root = root
        self._placement = placement or WindowPlacement()
        self._pendente = None

    def geometry_for(self, largura: int, altura: int) -> str:
        """Geometria inicial: na posição salva, se existir e estiver visível."""
        pos = self._placement.load()
        if pos and self._placement.is_visible(pos[0], pos[1], self._limites_da_tela()):
            return f"{largura}x{altura}+{pos[0]}+{pos[1]}"
        return f"{largura}x{altura}"

    def start_tracking(self) -> None:
        """Salva a posição (com pequeno atraso) sempre que a janela é movida,
        para não depender de um fechamento "limpo" do programa."""
        self._root.bind("<Configure>", self._ao_configurar, add="+")

    def save_now(self) -> None:
        if self._pendente is not None:
            self._root.after_cancel(self._pendente)
            self._pendente = None
        try:
            if self._root.state() != "normal":  # minimizada/oculta: posição inútil
                return
            pos = parse_geometry(self._root.geometry())
        except tk.TclError:
            return
        if pos:
            self._placement.save(pos[2], pos[3])

    # -------------------- internos --------------------
    def _ao_configurar(self, event) -> None:
        if event.widget is not self._root:  # ignora eventos dos widgets internos
            return
        if self._pendente is not None:
            self._root.after_cancel(self._pendente)
        self._pendente = self._root.after(500, self.save_now)

    def _limites_da_tela(self) -> Tuple[int, int, int, int]:
        r = self._root
        esquerda = min(0, r.winfo_vrootx())
        topo = min(0, r.winfo_vrooty())
        direita = max(r.winfo_screenwidth(), r.winfo_vrootx() + r.winfo_vrootwidth())
        base = max(r.winfo_screenheight(), r.winfo_vrooty() + r.winfo_vrootheight())
        return esquerda, topo, direita, base


def abrir_na_posicao_da_principal(janela: tk.Toplevel) -> None:
    """Posiciona `janela` no mesmo canto superior esquerdo da janela principal
    (o tamanho definido pela própria janela é mantido). Deve ser chamada
    depois de a janela definir seu `geometry("LxA")`."""
    try:
        principal = janela.nametowidget(".")
        pos = parse_geometry(principal.geometry())
        if pos:
            janela.geometry(f"+{pos[2]}+{pos[3]}")
    except tk.TclError:
        logger.warning("Não foi possível posicionar a janela.", exc_info=True)
