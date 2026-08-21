# Arquitetura

## Visão geral

O projeto segue uma separação simples entre **interface**, **lógica de negócio** e **dados**, mesmo sendo uma aplicação pequena. Essa divisão facilita manutenção e futuras extensões (ex: trocar a GUI, adicionar banco de dados, criar uma versão CLI).

```
impressoras-tool/
├── main.py              # Camada de apresentação (GUI)
├── printer_manager.py   # Camada de lógica de negócio (integração com Windows)
├── catalog.json          # Camada de dados (catálogo de impressoras)
└── requirements.txt      # Dependências do projeto
```

## Componentes

### `main.py` — Camada de apresentação

Responsável apenas pela interface com o usuário: desenhar a janela, capturar cliques e exibir resultados. Não contém lógica de negócio — toda chamada ao sistema operacional é delegada ao `printer_manager.py`.

Construído com **PySimpleGUI**, escolhido por permitir montar uma interface funcional rapidamente sem exigir conhecimento de front-end.

### `printer_manager.py` — Camada de lógica

Concentra toda a comunicação com o Windows, feita via **PowerShell** (chamado através do módulo `subprocess` do Python). Principais funções:

| Função | Responsabilidade |
|---|---|
| `add_printer(nome, ip, driver)` | Cria a porta TCP/IP (se não existir) e cadastra a impressora |
Essa camada foi isolada da interface propositalmente: se no futuro a GUI for trocada (por uma versão web, CLI, etc.), a lógica de instalação não precisa ser reescrita.

### `catalog.json` — Camada de dados

Lista de impressoras disponíveis (nome, IP, driver), em formato JSON. Foi separado do código para que o time de infraestrutura possa cadastrar novas impressoras sem precisar editar Python — apenas adicionar um novo item ao arquivo.

## Fluxo de execução

```
Usuário abre main.py
        │
        ▼
Carrega catalog.json → popula lista de impressoras na tela
        │
        ▼
Usuário seleciona impressora e clica "Instalar"
        │
        ▼
main.py chama printer_manager.add_printer(nome, ip, driver)
        │
        ▼
printer_manager verifica se a porta IP já existe (Get-PrinterPort)
        │
        ├── Não existe → cria a porta (Add-PrinterPort)
        │
        ▼
printer_manager cadastra a impressora (Add-Printer)
        │
        ▼
main.py exibe resultado (sucesso/erro) na tela
```

## Decisões técnicas

**Por que PowerShell via `subprocess` em vez de uma biblioteca Python nativa?**
O Windows não expõe uma API Python oficial e completa para gerenciamento de impressoras. `Add-Printer` e `Add-PrinterPort` são cmdlets nativos do PowerShell, mantidos pela própria Microsoft — chamar essas ferramentas prontas é mais confiável do que reimplementar a lógica via APIs de baixo nível (Win32).

**Por que separar o catálogo em JSON em vez de deixar no código?**
Permite que pessoas sem conhecimento de programação (outros integrantes do time de infra) atualizem a lista de impressoras disponíveis.

**Por que checar a porta antes de criar?**
`Add-PrinterPort` falha com erro se a porta já existir (ex: reinstalação, ou porta criada manualmente antes). A verificação prévia torna a operação idempotente — pode ser executada múltiplas vezes com segurança.

## Possíveis evoluções

- **Persistência**: trocar o log em tela por um SQLite, registrando histórico de instalações (impressora, máquina, usuário, data/hora)
- **Distribuição**: empacotar com PyInstaller (`--onefile --windowed`) para gerar um `.exe` distribuível sem exigir Python instalado
- **Permissões**: adicionar manifesto de elevação para solicitar admin automaticamente, em vez de depender do usuário abrir como administrador
- **Testes**: separar chamadas ao `subprocess` atrás de uma interface, permitindo mockar em testes unitários
- **Upgrade no Front-End**: A versão atual usa `PySimpleGUI`, escolhida propositalmente pela velocidade de desenvolvimento — mas ela tem limitações visuais e não é ideal para um portfólio mais robusto.
