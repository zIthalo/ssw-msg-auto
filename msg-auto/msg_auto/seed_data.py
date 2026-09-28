# -*- coding: utf-8 -*-
"""Mensagens padrão de fábrica do sistema.

Este arquivo preserva, na íntegra, o conteúdo original de mensagens do
script legado (mensagens[] e endereco[]) e os respectivos comandos de
atalho (BUILTIN_COMMANDS). São carregadas automaticamente na primeira
execução e ficam disponíveis para o usuário editar, renomear o comando
ou excluir pela tela de configurações - exatamente como qualquer
mensagem personalizada.

Use `CommandService.restaurar_padrao()` para recolocar estes textos
originais a qualquer momento, sem afetar as mensagens personalizadas.
"""

from .models import Command

_ENDERECO_BASE_BLU = (
    "Arlete Transportes Filial (BLU)  - \n"
    "Rodovia Ingo Henring, 8979 CNPJ: 72.090.442/0009-34\n"
    "Bairro: Margem Esquerda \n\n"
    "Cep: 89116-755 - Gaspar/SC \n"
    "Fone:(47) 3318-0980\n"
    "Contato: blumenau@arletetransportes.com.br \n"
    "https://www.google.com/maps?q=-26.9167197,-48.9699487"
)

DEFAULT_COMMANDS = [
    Command("//0", " Tudo bem?\n\nComo posso ajudar você?", greeting=True, is_default=True),
    Command("//1", "Tudo bem por aqui. E você?\n\nVerificando, só um momento.", greeting=True, is_default=True),
    Command("//2", "\n\nVerificando, só um momento.", greeting=True, is_default=True),
    Command("//3", " Tudo bem?\n\nPreciso de um auxílio com esta NF: ", greeting=True, is_default=True),
    Command("//4", " Tudo bem?\n\nSegue e-mail referente a NF: \n\nPoderia nos auxiliar?", greeting=True, is_default=True),
    Command("//5", " Tudo bem por aqui! E você?\n\nComo posso ajudar você hoje?", greeting=True, is_default=True),
    Command("//6", "Por gentileza, teria o PDF desta NF? \n\nOu teria o número da nota fiscal para eu verificar melhor?", greeting=True, is_default=True),
    Command("//+", "Por nada, eu é quem agradeço! \n\nSe precisar, pode chamar estou à disposição.", greeting=False, is_default=True),
    Command("//.", "Muito obrigado!", greeting=False, is_default=True),
    Command("**.", "A mercadoria está com previsão de entrega para dia ", greeting=True, is_default=True),
    Command("**0", "Vou verificar e já te retorno.", greeting=False, is_default=True),
    Command("**1", "sac2.blu@arletetransportes.com.br", greeting=False, is_default=True),
    Command("**2", "Mercadoria entregue segue comprovante.", greeting=False, is_default=True),
    Command("**3", "Esta mercadoria está em rota de entrega hoje, deve ser finalizada em horário comercial. \n\nSerá entregue no endereço acima.", greeting=False, is_default=True),
    Command("//d", "Vamos precisar dos dados da pessoa que irá retirar:\nNome Completo: \nRG ou CPF: \nPlaca do veículo: ", greeting=False, is_default=True),
    Command("**5", "Cliente acionado, aguardando retorno.", greeting=False, is_default=True),
    Command("**6", "Verificando / Cobrando retorno.", greeting=False, is_default=True),
    Command("**7", "Base acionada, aguardando retorno.", greeting=False, is_default=True),
    Command("--4", "Olá!\n\nEstamos conversando sobre a NF: \n\nVou verificar e já te retorno.", greeting=False, is_default=True),
    Command("--1", "\n\nReentrega em sistema,\n\nGentileza informar a nova previsão", greeting=True, is_default=True),
    Command("--2", "\n\nReentrega e CC-e em sistema.\n\nGentileza informar a nova previsão.", greeting=True, is_default=True),
    Command("--3", "\n\n@\n\nGentileza verificar.", greeting=True, is_default=True),
    Command("//b", _ENDERECO_BASE_BLU, greeting=False, is_default=True),
]
