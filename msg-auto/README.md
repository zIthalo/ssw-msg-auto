# Mensagens Automáticas - SAC

Sistema para agilizar o atendimento via WhatsApp Web (ou qualquer campo de
texto) através de **comandos de atalho** digitados pelo teclado. Ao digitar
um comando cadastrado (ex.: `//0`), o sistema apaga automaticamente o que
foi digitado e envia a mensagem correspondente no campo em foco - sem
precisar copiar e colar manualmente.

---

## Sumário

1. [Requisitos](#1-requisitos)
2. [Instalação](#2-instalação)
3. [Como executar](#3-como-executar)
4. [Como usar no dia a dia](#4-como-usar-no-dia-a-dia)
5. [Tela de Configurações](#5-tela-de-configurações)
6. [Comandos padrão de fábrica](#6-comandos-padrão-de-fábrica)
7. [Saudação automática](#7-saudação-automática)
8. [Como os dados são armazenados](#8-como-os-dados-são-armazenados)
9. [Sobre a área de transferência (clipboard)](#9-sobre-a-área-de-transferência-clipboard)
10. [Arquitetura do projeto](#10-arquitetura-do-projeto)
11. [Solução de problemas](#11-solução-de-problemas)
12. [Evoluções futuras](#12-evoluções-futuras)

---

## Novidades desta versão

- **Mensagens enviadas exatamente como digitadas**: espaços, linhas em
  branco, Enter, tabs e símbolos no início, meio e fim da mensagem agora
  são preservados no cadastro e na edição (antes eram removidos nas
  pontas, o que juntava a saudação ao texto). Com a saudação marcada,
  ela é colocada antes do texto; para separar, comece a mensagem com
  Enter (ou espaço). Mensagens já salvas antes desta versão podem ter
  perdido esses espaços nas pontas: basta editá-las novamente.
- **Duplo clique na tela "Editar mensagem"** abre a edição do comando
  (comando, mensagem e saudação) clicado.
- **Posição das janelas**: a janela principal abre onde foi fechada da
  última vez (a posição fica em `janela.json`, na pasta de dados; se
  ela estiver fora da tela, usa a posição padrão). Configurações, suas
  subtelas e as confirmações abrem na mesma posição da janela
  principal.

- **Correção definitiva da perda de mensagens ao reiniciar o computador**:
  - Os dados agora ficam em `%APPDATA%\MensagensAutoSAC` (no Windows:
    `C:\Users\<usuário>\AppData\Roaming\MensagensAutoSAC`), e não
    mais ao lado do programa. Pastas como Área de Trabalho/Documentos
    costumam ser protegidas pelo **"Acesso controlado a pastas"** do
    Windows Defender, que pode bloquear a gravação sem avisar.
    Instalações antigas são **migradas automaticamente** na primeira
    abertura (nada se perde).
  - **Nunca mais "salva de mentira"**: o sistema relê o arquivo após
    gravar e só atualiza a tela depois que o disco confirmou. Se a
    gravação falhar, aparece uma mensagem de erro clara e nada é
    alterado.
  - Qualquer erro inesperado em qualquer tela agora é mostrado ao
    usuário e registrado no log.

- **Robustez contra desligamento abrupto do computador**: se o Windows
  encerrar o programa à força durante um desligamento/reinício (algo
  que pode acontecer exatamente durante a gravação do arquivo de
  comandos), o arquivo de dados **não fica mais corrompido nem
  esvaziado**:
  - A gravação agora é **atômica** (grava em um arquivo temporário,
    força a sincronização física com o disco e só então substitui o
    arquivo definitivo) - nunca existe um estado "gravado pela
    metade".
  - Um **backup automático** (`comandos.json.bak`) é mantido a cada
    gravação. Se o arquivo principal aparecer ausente ou corrompido na
    próxima abertura, o sistema **recupera sozinho** a partir do
    backup, em vez de resetar silenciosamente para os padrões de
    fábrica.
  - O log (`%APPDATA%\MensagensAutoSAC\sac11.log`) agora registra cada carregamento,
    gravação, criação, edição e exclusão de comando - útil para
    diagnosticar qualquer problema de persistência que venha a ocorrer.

## Novidades de versões anteriores

- **Navegação por setas nas telas de cadastro, edição e exclusão**: nas
  telas de **Nova mensagem**, **Editar mensagem** (lista e formulário)
  e **Excluir mensagem**, as setas **↑ / ↓** movem o foco entre os
  campos e botões da tela, sem atalhos numéricos (essas telas
  permanecem simples, ao contrário dos menus de Configurações):
  - No campo **Comando**, no **Checkbutton** de saudação e nos
    **botões**, ↑/↓ sempre movem o foco para o campo anterior/seguinte
    (dando a volta do último para o primeiro).
  - No campo **Mensagem** (multilinha): as setas continuam movendo o
    cursor dentro do texto normalmente; só passam o foco para o campo
    anterior/seguinte quando o cursor já está na primeira linha (seta
    para cima) ou na última linha (seta para baixo).
  - Na **lista de comandos** (telas de editar/excluir): as setas
    continuam navegando entre os itens normalmente; só passam o foco
    para o botão seguinte/anterior quando a seleção já está no
    primeiro ou no último item da lista.
- **Navegação completa por teclado** nas telas de menu (Inicial e
  Configurações): ↑/↓ com destaque visual, Enter confirma, números 1-9
  acessam direto, ESC volta (exceto na tela inicial). A confirmação de
  "Restaurar padrões de fábrica" e a de exclusão de comando usam um
  diálogo próprio Sim/Não (1-Sim / 2-Não), também navegável.
- **Correção de persistência**: comandos e mensagens novas (ou com o
  comando alterado) agora permanecem salvos corretamente após fechar e
  reabrir o sistema. A causa era o hook global de teclado interferindo
  na digitação dentro das próprias telas de cadastro/edição - ele agora
  é pausado automaticamente sempre que a tela de **Configurações** (ou
  qualquer tela aberta a partir dela) está ativa.
- **Atalhos de edição em todos os campos**: `Ctrl+Z` (desfazer),
  `Ctrl+Backspace` (apaga a palavra anterior ao cursor) e `Ctrl+Delete`
  (apaga a palavra seguinte ao cursor) já funcionam nos campos de
  "Comando" e "Mensagem" das telas de cadastro e edição.
- **20 novos comandos padrão de fábrica** com os endereços das demais
  filiais (`/tub`, `/sao`, `/cpn`, `/san`, `/cwb`, `/jvl`, `/cri`,
  `/fln`, `/jgs`, `/sbs`, `/ibm`, `/lgs`, `/jcb`, `/xap`, `/smd`,
  `/poa`, `/nhb`, `/igr`, `/cax`, `/oso`).

## 1. Requisitos

- Windows, macOS ou Linux com interface gráfica.
- Python 3.9 ou superior.
- No Linux, a biblioteca `keyboard` normalmente exige execução como
  `root` (ou configuração de permissões) para capturar teclas globalmente.

## 2. Instalação

```bash
# 1. Extraia/clonar o projeto em uma pasta de sua preferência
cd msg-auto

# 2. (Recomendado) crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt
```

## 3. Como executar

```bash
python main.py
```

Uma pequena janela "Sistema ativo" será exibida. **Deixe essa janela aberta**
em segundo plano enquanto usa o WhatsApp Web (ou outro aplicativo) - é ela
que mantém o monitoramento do teclado ativo.

> No Windows pode ser necessário executar como Administrador para que a
> captura global de teclado funcione corretamente em algumas janelas.

## 4. Como usar no dia a dia

1. Abra o WhatsApp Web (ou o campo de texto desejado) e clique na caixa de
   digitação da conversa.
2. Digite um dos comandos cadastrados, por exemplo `//0`.
3. Assim que o comando é reconhecido, o sistema:
   - apaga os caracteres digitados do comando;
   - cola a mensagem correspondente (com a saudação, se configurada) no
     campo de texto.
4. Revise a mensagem e pressione Enter para enviar - o sistema **não envia
   sozinho**, apenas preenche o campo.

## 5. Tela de Configurações

Clique em **⚙️ Configurações** na janela principal para acessar:

| Opção | O que faz |
|---|---|
| **Nova mensagem** | Cadastra um novo comando e sua respectiva mensagem. |
| **Editar mensagem** | Lista todos os comandos (padrão e personalizados) e permite alterar o texto do comando, a mensagem e a saudação. |
| **Excluir mensagem** | Remove um comando/mensagem cadastrado. |
| **Listar todas** | Mostra todos os comandos cadastrados, a mensagem, se usa saudação e a origem (Padrão/Personalizado). |
| **Restaurar padrões de fábrica** | Recoloca o texto original das mensagens padrão, caso tenham sido alteradas. Não afeta mensagens personalizadas. |

### Cadastrando uma nova mensagem

1. **Comando**: texto que irá disparar o envio (ex.: `//9`, `**z`, `--a`).
   Evite reaproveitar um comando já existente - o sistema avisa em caso de
   conflito.
2. **Mensagem**: o texto que será enviado. Pressione Enter dentro do campo
   para quebrar linha normalmente.
3. **Saudação**: marque a caixa "Iniciar com saudação" para que o sistema
   insira automaticamente "Bom dia.", "Boa tarde." ou "Boa noite." antes da
   mensagem, de acordo com o horário do computador.
4. Clique em **Salvar**.

### Editando ou renomeando um comando

Na tela **Editar mensagem**, selecione o comando na lista e clique em
**Editar selecionado**. É possível alterar o texto do comando (ex.: trocar
`//9` por `//ok`), o conteúdo da mensagem e a opção de saudação. Isso vale
tanto para mensagens personalizadas quanto para as mensagens **padrão de
fábrica** - elas também podem ser totalmente editadas.

### Excluindo um comando

Na tela **Excluir mensagem**, selecione o comando e clique em **Excluir
selecionado**. A exclusão pede confirmação antes de ser efetivada.

## 6. Comandos padrão de fábrica

O sistema já vem com os comandos abaixo pré-cadastrados (idênticos aos do
script original). Todos podem ser editados ou excluídos livremente pela
tela de configurações:

| Comando | Descrição resumida | Saudação |
|---|---|---|
| `//0` | Tudo bem? Como posso ajudar você? | Sim |
| `//1` | Tudo bem por aqui. E você? Verificando... | Sim |
| `//2` | Verificando, só um momento. | Sim |
| `//3` | Preciso de auxílio com a NF | Sim |
| `//4` | Segue e-mail referente à NF | Sim |
| `//5` | Como posso ajudar você hoje? | Sim |
| `//6` | Poderia enviar o PDF/número da NF? | Sim |
| `//+` | Agradecimento (por nada) | Não |
| `//.` | Muito obrigado! | Não |
| `**.` | Previsão de entrega para o dia... | Sim |
| `**0` | Vou verificar e já retorno. | Não |
| `**1` | E-mail do SAC (sac2.blu@arletetransportes.com.br) | Não |
| `**2` | Mercadoria entregue, segue comprovante. | Não |
| `**3` | Mercadoria em rota de entrega hoje. | Não |
| `**5` | Cliente acionado, aguardando retorno. | Não |
| `**6` | Verificando / Cobrando retorno. | Não |
| `**7` | Base acionada, aguardando retorno. | Não |
| `--1` | Reentrega em sistema, nova previsão. | Sim |
| `--2` | Reentrega e CC-e em sistema. | Sim |
| `--3` | Gentileza verificar (menção @). | Sim |
| `--4` | Estamos conversando sobre a NF... | Não |
| `//d` | Solicita dados de quem irá retirar a mercadoria. | Não |
| `//b` | Endereço completo da filial Blumenau. | Não |

Use **Listar todas** para ver o texto completo de cada mensagem.

## 7. Saudação automática

Quando a opção "saudação" está marcada em um comando, o sistema insere
automaticamente, antes da mensagem, o texto conforme o horário do
computador no momento do envio:

- Antes das 12h → **"Bom dia."**
- Das 12h às 17h59 → **"Boa tarde."**
- A partir das 18h → **"Boa noite."**

## 8. Como os dados são armazenados

Todos os comandos (padrão e personalizados) ficam salvos localmente em:

```
%APPDATA%\MensagensAutoSAC\comandos.json
```

Não é necessário instalar ou configurar nenhum servidor de banco de dados
(o sistema **não usa MySQL nem qualquer servidor externo**) - tudo funciona
em arquivo local, de forma simples e portátil. Basta copiar essa pasta
`MensagensAutoSAC` para levar suas mensagens para outro computador.

Os registros de execução (log) ficam em `%APPDATA%\MensagensAutoSAC\sac11.log`.

> **Extensibilidade**: internamente existe uma interface `CommandRepository`
> (em `msg_auto/repository.py`). Hoje só há a implementação em JSON, mas se
> no futuro for necessário migrar para SQLite ou outro banco, basta criar
> uma nova classe implementando essa interface - o restante do sistema não
> precisa ser alterado.

## 9. Sobre a área de transferência (clipboard)

O envio das mensagens utiliza a área de transferência do sistema (Ctrl+C /
Ctrl+V) por ser o método mais confiável para textos com acentuação e
caracteres especiais. Para **não deixar rastro** do que foi enviado:

1. O sistema salva o conteúdo que já estava na sua área de transferência
   **antes** de colar a mensagem.
2. Copia e cola a mensagem do comando.
3. Assim que a colagem é processada, **restaura automaticamente** o
   conteúdo original que você tinha copiado antes.

Ou seja, ao pressionar Ctrl+V logo depois de usar um comando, você
recupera o que você mesmo havia copiado - não o texto do sistema.

## 10. Arquitetura do projeto

O projeto segue separação de responsabilidades (cada camada com uma única
função), facilitando manutenção e testes:

```
main.py                        # ponto de entrada
msg_auto/
├── app.py                     # composition root: liga todas as camadas
├── config.py                  # constantes e caminhos
├── models.py                  # entidade Command
├── greeting.py                # regra da saudação por horário
├── repository.py              # interface + implementação JSON de persistência
├── seed_data.py                # mensagens padrão de fábrica
├── sender.py                  # envio via clipboard com salvar/restaurar
├── command_service.py         # regras de negócio (CRUD + execução)
├── listener.py                # captura global de teclado
├── data/
│   ├── comandos.json          # dados persistidos
│   └── sac11.log              # log de execução
└── gui/
    ├── main_window.py         # janela principal (menu numerado: Configurações/Sair)
    ├── settings_window.py     # menu de configurações (6 opções numeradas)
    ├── keyboard_menu.py       # componente reutilizável de menu navegável por teclado
    ├── confirm_dialog.py      # diálogo Sim/Não numerado e navegável por teclado
    ├── focus_navigation.py    # navegação por ↑/↓ entre campos/botões (cadastro, edição, exclusão)
    ├── window_utils.py        # ESC e foco inicial para as telas secundárias
    ├── text_shortcuts.py      # Ctrl+Z / Ctrl+Backspace / Ctrl+Delete nos campos de texto
    ├── register_window.py     # tela de cadastro
    ├── edit_window.py         # tela de edição (lista + formulário)
    ├── delete_window.py       # tela de exclusão
    └── list_window.py         # tela de listagem
```

**Fluxo de execução de um comando:**

1. `HotkeyListener` observa as teclas digitadas em qualquer aplicativo.
2. Ao reconhecer um comando cadastrado, apaga o texto digitado e coloca o
   comando em uma fila (`Queue`).
3. Uma thread `worker` (em `app.py`) retira o comando da fila e chama
   `CommandService.executar()`.
4. `CommandService` monta a mensagem (com ou sem saudação, via
   `GreetingService`) e delega o envio ao `ClipboardSender`.
5. `ClipboardSender` cola o texto e restaura o clipboard original.

Cada camada tem uma responsabilidade única (Princípio da Responsabilidade
Única) e depende apenas de interfaces/abstrações necessárias, o que
facilita testar `CommandService` isoladamente, sem depender de Tkinter,
teclado ou clipboard reais.

**Por que os comandos "sumiam" antes:** o `HotkeyListener` usa um hook
*global* de teclado - ele recebe todo evento de tecla do sistema
operacional, mesmo quando o foco está em uma janela do próprio
aplicativo. Sem uma pausa explícita, ao digitar a mensagem no formulário
de cadastro o listener continuava tentando casar o texto digitado com
algum comando; se por coincidência aparecesse um trecho como `**` ou
`//` dentro da própria mensagem sendo escrita, ele apagava caracteres e
colava texto automaticamente **dentro do campo em edição**, corrompendo
o que estava sendo digitado antes de salvar. A correção foi fazer
`SettingsWindow` chamar `listener.pause()` ao abrir e `listener.resume()`
ao fechar (contando com um contador reentrante em `HotkeyListener`, que
também é usado pela thread de envio - ver `gui/settings_window.py` e
`listener.py`).

## 11. Solução de problemas

**O comando não é reconhecido.**
Verifique se o campo de texto do aplicativo está realmente em foco e se o
comando não colide com outro maior (ex.: `//` sozinho nunca deve ser
cadastrado como comando, pois qualquer comando começando com `//`
"vazaria" para ele - prefira sempre comandos com pelo menos 2-3
caracteres além do prefixo).

**Nada acontece ao digitar (Linux).**
Rode o programa com permissões elevadas (`sudo python main.py`) ou
configure as permissões de acesso a `/dev/input` exigidas pela biblioteca
`keyboard`.

**A mensagem colada veio com acentos estranhos.**
Isso geralmente indica um problema de configuração de encoding do
aplicativo de destino; o sistema já tenta corrigir automaticamente
encodings mal interpretados, mas alguns aplicativos legados podem exigir
ajustes manuais.

**Perdi mensagens depois de desligar/reiniciar o computador.**
A partir desta versão, isso não deve mais ocorrer: a gravação é atômica
e há um backup automático (`comandos.json.bak`) com recuperação
automática. Se ainda assim acontecer, verifique o arquivo
`%APPDATA%\MensagensAutoSAC\sac11.log` logo após reabrir o programa - ele registra
se o arquivo principal foi encontrado corrompido e se a recuperação a
partir do backup foi usada. Guarde esse trecho do log para diagnóstico.

**Apareceu "A gravação não foi confirmada no disco" ou "Acesso negado".**
Algo está impedindo o programa de gravar em
`%APPDATA%\MensagensAutoSAC`. Verifique o antivírus e o Windows
Defender (Segurança do Windows > Proteção contra vírus e ameaças >
Proteção contra ransomware > Acesso controlado a pastas) e permita o
Python (`python.exe`/`pythonw.exe`) ou desative o recurso para essa
pasta. Para abrir a pasta de dados, digite `%APPDATA%\MensagensAutoSAC`
na barra de endereço do Explorador de Arquivos.

**Quero apagar tudo e recomeçar do zero.**
Feche o programa e apague o arquivo `%APPDATA%\MensagensAutoSAC\comandos.json`. Ele
será recriado automaticamente com as mensagens padrão de fábrica na
próxima execução.

## 12. Evoluções futuras

Algumas ideias que se encaixam naturalmente na arquitetura atual, caso o
projeto cresça:

- Criar uma `SQLiteCommandRepository` para bancos de dados mais robustos,
  mantendo a mesma interface `CommandRepository`.
- Adicionar atalho de teclado para pausar/retomar o sistema sem precisar
  fechar a janela.
- Categorizar comandos (ex.: "Entrega", "Financeiro", "Saudação") na tela
  de listagem.
- Suporte a múltiplos perfis de atendente, cada um com seu próprio
  conjunto de comandos.
