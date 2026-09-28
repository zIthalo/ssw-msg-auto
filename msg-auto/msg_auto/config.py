# -*- coding: utf-8 -*-
"""Configurações e constantes globais do sistema."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

COMMANDS_FILE = os.path.join(DATA_DIR, "comandos.json")
LOG_FILE = os.path.join(DATA_DIR, "sac11.log")

# Garante que a pasta de dados exista assim que o módulo é importado,
# independentemente de qual componente é inicializado primeiro.
os.makedirs(DATA_DIR, exist_ok=True)

# Quantidade máxima de caracteres mantidos em memória para
# reconhecer um comando digitado pelo usuário.
KEY_BUFFER_MAX = 50

# Intervalo entre a tecla "backspace" ao apagar o comando digitado.
BACKSPACE_DELAY = 0.01

# Intervalo entre o Ctrl+V e a próxima ação, para dar tempo do
# aplicativo de destino (ex: WhatsApp Web) processar a colagem.
PASTE_DELAY = 0.05

# Tempo de espera antes de restaurar o conteúdo original da área de
# transferência do usuário, garantindo que o "Ctrl+V" já foi processado
# pelo aplicativo de destino antes de trocarmos o clipboard de volta.
CLIPBOARD_RESTORE_DELAY = 0.35
