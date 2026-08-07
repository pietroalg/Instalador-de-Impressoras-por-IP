🖨️ Instalador de Impressoras

Ferramenta com interface gráfica para automatizar a configuração de impressoras de rede (IP direto) no Windows, eliminando o processo manual de criar porta TCP/IP, instalar driver e nomear a impressora.

Problema que resolve

Configurar uma impressora de rede manualmente no Windows envolve vários passos repetitivos: abrir "Impressoras e Scanners", criar uma porta TCP/IP, digitar o IP, escolher o driver certo, nomear a impressora e testar. Multiplicado por dezenas de máquinas, isso consome bastante tempo do time de infraestrutura.

Esta ferramenta reduz esse processo a selecionar a impressora numa lista e clicar em "Instalar".

Como funciona

O usuário escolhe uma impressora pré-cadastrada em um catálogo (catalog.json). Ao clicar em "Instalar", o programa:

Verifica se a porta TCP/IP daquela impressora já existe na máquina
Cria a porta, caso ainda não exista
Registra a impressora no Windows, associando nome, porta e driver
Mostra o resultado (sucesso ou erro) na própria tela
Pré-requisitos
Windows
Python 3.9+
Executar como administrador (necessário para alterar configurações de impressoras no sistema)
Instalação
bash
git clone https://github.com/pietroalg/Instalador-de-Impressoras-por-IP.git
cd impressoras-tool
pip install -r requirements.txt
Uso
bash
python main.py

Rode o terminal/IDE como administrador antes de executar, ou a instalação da impressora vai falhar por permissão.

Cadastrando novas impressoras

Basta editar o catalog.json e adicionar um novo item, sem precisar mexer no código:

json
{"nome": "Impressora Marketing", "ip": "192.168.1.52", "driver": "HP Universal Printing PCL 6"}
Estrutura do projeto

Veja ARCHITECTURE.md para detalhes sobre a arquitetura e organização do código.

Roadmap
 Empacotar como .exe standalone (PyInstaller)
 Log de instalações em SQLite (quem instalou, quando, em qual máquina)
 Detecção automática de driver por modelo
 Botão de teste de impressão integrado na tela
Motivação

Projeto criado durante estágio em infraestrutura, como iniciativa pessoal para automatizar uma tarefa manual recorrente do dia a dia do time.
