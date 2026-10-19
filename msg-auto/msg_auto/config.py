# -*- coding: utf-8 -*-
"""Configurações e constantes globais do sistema."""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolver_data_dir() -> str:
    """Define onde ficam os dados do usuário (comandos.json e log).

    Os dados NÃO ficam mais ao lado do programa. Pastas como Área de
    Trabalho, Documentos e Imagens costumam ser protegidas pelo "Acesso
    controlado a pastas" do Windows Defender (antirransomware), que pode
    bloquear silenciosamente a gravação feita por programas não
    confiáveis - o programa parece salvar (mantém tudo em memória), mas
    nada chega ao disco e tudo some ao reiniciar o computador.

    Por isso usamos a pasta padrão do Windows para dados de aplicativos
    (%APPDATA%\\MensagensAutoSAC), que normalmente não é protegida. Em
    outros sistemas, usa-se uma pasta oculta na pasta pessoal.
    """
    appdata = os.getenv("APPDATA")
    if appdata:
        return os.path.join(appdata, "MensagensAutoSAC")
    return os.path.join(os.path.expanduser("~"), ".mensagens_auto_sac")


DATA_DIR = _resolver_data_dir()
COMMANDS_FILE = os.path.join(DATA_DIR, "comandos.json")
LOG_FILE = os.path.join(DATA_DIR, "sac11.log")
WINDOW_STATE_FILE = os.path.join(DATA_DIR, "janela.json")

os.makedirs(DATA_DIR, exist_ok=True)


def _migrar_dados_antigos() -> None:
    """Versões anteriores guardavam os dados em `msg_auto/data/` (ao lado
    do programa). Se existir um arquivo lá e ainda não existir nenhum na
    nova pasta, copia uma única vez, para não perder nada na atualização."""
    antigo = os.path.join(BASE_DIR, "data", "comandos.json")
    if os.path.exists(antigo) and not os.path.exists(COMMANDS_FILE):
        try:
            shutil.copyfile(antigo, COMMANDS_FILE)
        except OSError:
            pass


_migrar_dados_antigos()

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
