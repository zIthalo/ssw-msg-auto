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

    # -------------------- Endereços das demais filiais --------------------
    Command(
        "/tub",
        "Rua Arlete Teresinha Orlandi da Silva, 200\n"
        "Bairro: - São João Margem Esquerda\n"
        "Cep: - 88708-418\n"
        "Cidade: - Tubarão/SC\n"
        "Contato: - (48) 3626-6526 - (48) 98802-5500 - (48) 3626-6526",
        greeting=False, is_default=True,
    ),
    Command(
        "/sao",
        "Rua da Despedida, 111\n"
        "Bairro: - Vila dos Remédios\n"
        "Cep: - 05102-050\n"
        "Cidade: - São Paulo/SP\n"
        "Contato: - (11) 3641-0166 - (11) 98449-1171 - (11) 99417-8663",
        greeting=False, is_default=True,
    ),
    Command(
        "/cpn",
        "Rua do Parque, 300\n"
        "Bairro: - Parque Villa Flores\n"
        "Cep: - 13175-660\n"
        "Cidade: - Sumaré / SP\n"
        "Contato: - (19) 99836-1476",
        greeting=False, is_default=True,
    ),
    Command(
        "/san",
        "Av Joaquim Norberto de Souza, 241\n"
        "Bairro: - Ribeiropolis\n"
        "Cep: - 11714-420\n"
        "Cidade: - Praia Grande / SP\n"
        "Contato: - (13) 3592-3745",
        greeting=False, is_default=True,
    ),
    Command(
        "/cwb",
        "Rua Alexandre Zanchetta,110\n"
        "Bairro: - Campina\n"
        "Cep: - 83325-070\n"
        "Cidade: - São José dos Pinhais/PR\n"
        "Contato: - (41) 3283-5505 - (41) 3283-5505 - (41) 98855 8886",
        greeting=False, is_default=True,
    ),
    Command(
        "/jvl",
        "Rodovia BR 101 - km 046\n"
        "Bairro: - Nova Brasilia\n"
        "Cep: - 89213-205\n"
        "Cidade: - Joinville/SC\n"
        "Contato: - (47) 3440-0240 - (47) 98843-7690 - (47) 98865-7876",
        greeting=False, is_default=True,
    ),
    Command(
        "/cri",
        "Rua Dilnei Luiz Piovesan, S/N\n"
        "Bairro: - Cristo Redentor\n"
        "Cep: - 88816-300\n"
        "Cidade: - Criciúma/SC\n"
        "Contato: - (48) 3442-0765 - (48) 98855-4029 - (48) 99818-0033",
        greeting=False, is_default=True,
    ),
    Command(
        "/fln",
        "Rua Roney Henrique Heiderscheidt, 60\n"
        "Bairro: - Cond CEIP - Jardim Eldorado\n"
        "Cep: - 88133-500\n"
        "Cidade: - Palhoça/SC\n"
        "Contato: - (48) 3285-6413 - (48) 98866-5979 - (48) 99665-3667",
        greeting=False, is_default=True,
    ),
    Command(
        "/jgs",
        "Av Pref. Waldemar Grubba, 1896\n"
        "Bairro: - Vila Lalau\n"
        "Cep: - 89256-501\n"
        "Cidade: - Jaraguá do Sul/SC\n"
        "Contato: - (47) 3208-9538",
        greeting=False, is_default=True,
    ),
    Command(
        "/sbs",
        "Rua Eduardo Liebl, 72\n"
        "Bairro: - Serra Alta\n"
        "Cep: - 88133-515\n"
        "Cidade: - São Bento do Sul/SC\n"
        "Contato: - (47) 3633-2892",
        greeting=False, is_default=True,
    ),
    Command(
        "/ibm",
        "Rua dos Veradores, 440\n"
        "Bairro: - Itoupava\n"
        "Cep: - 89162-850\n"
        "Cidade: - Rio do Sul/SC\n"
        "Contato: - (47) 3525-1611",
        greeting=False, is_default=True,
    ),
    Command(
        "/lgs",
        "Avenida Belem, 1270\n"
        "Bairro: - Santa Helena\n"
        "Cep: - 88504-480\n"
        "Cidade: - Lages/SC\n"
        "Contato: - (49) 3222-4619",
        greeting=False, is_default=True,
    ),
    Command(
        "/jcb",
        "Rua Odete Aquino Dallaio, 113\n"
        "Bairro: -\n"
        "Cep: - 89600-000\n"
        "Cidade: - Joaçaba/SC\n"
        "Contato: - (49) 3521-0172",
        greeting=False, is_default=True,
    ),
    Command(
        "/xap",
        "Rua Humaita, 2679\n"
        "Bairro: - Dom Geronimo\n"
        "Cep: - 89805-295\n"
        "Cidade: - Chapecó/SC\n"
        "Contato: - (49) 3324-2343",
        greeting=False, is_default=True,
    ),
    Command(
        "/smd",
        "Rua São Pedro, 147 D\n"
        "Bairro: - Centro\n"
        "Cep: - 89801-300\n"
        "Cidade: - Chapecó/SC\n"
        "Contato: - (49) 99988-8874",
        greeting=False, is_default=True,
    ),
    Command(
        "/poa",
        "Estrada José Zingano, 846 - Pavilhão 11 e 12\n"
        "Bairro: - Dist. Industrial\n"
        "Cep: - 94930-280\n"
        "Cidade: - Cachoeirinha/RS\n"
        "Contato: - (51) 3251-0683 - (51) 3251-0683 - (51) 3251-0683",
        greeting=False, is_default=True,
    ),
    Command(
        "/nhb",
        "Rua Dr. Karl Wilhelm Schinke, 69\n"
        "Bairro: - Rondonia\n"
        "Cep: - 93415-240\n"
        "Cidade: - Novo Hamburgo / RS\n"
        "Contato: - (51) 3527-3122",
        greeting=False, is_default=True,
    ),
    Command(
        "/igr",
        "Rua Ruberto Alfredo Brocker, 83\n"
        "Bairro: - Sander\n"
        "Cep: - 95666-000\n"
        "Cidade: - Três Coroas/RS\n"
        "Contato: - (51) 3546-5014",
        greeting=False, is_default=True,
    ),
    Command(
        "/cax",
        "Rua Domingos Chies, 982\n"
        "Bairro: - Interlagos\n"
        "Cep: - 95052-160\n"
        "Cidade: - Caxias do Sul/RS\n"
        "Contato: - (54) 3533-4735 - (54) 3533-4735 - (54) 3533-4735",
        greeting=False, is_default=True,
    ),
    Command(
        "/oso",
        "Av. Angelo Gabriel Boff Guasseli, 1494\n"
        "Bairro: - Parque do Sol\n"
        "Cep: - 95520-000\n"
        "Cidade: - Osório / RS\n"
        "Contato: - (51) 3160-0130",
        greeting=False, is_default=True,
    ),
]
