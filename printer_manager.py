"""
Printer Manager - Lógica de comunicação com o Windows via PowerShell.

Responsável por criar portas TCP/IP e cadastrar impressoras.
"""

import subprocess

# Driver nativo do Windows, presente em qualquer instalação sem precisar
# baixar nada. Usado só pra garantir que a impressora seja criada sem erro -
# o driver correto do fabricante é trocado manualmente depois, em
# Configurações > Impressoras > Propriedades > Driver.

def add_printer(nome, ip):
    """Adiciona uma impressora de rede (IP direto) no Windows.

    Verifica se a porta já existe antes de criar (evita erro de porta
    duplicada em reinstalações). Sempre usa o driver genérico do Windows -
    o driver correto de cada fabricante deve ser instalado manualmente depois.
    """
    port_name = f"IP_{ip}"

    # Verifica se a porta já existe
    check_port = subprocess.run(
        ["powershell", "-Command", f'Get-PrinterPort -Name "{port_name}" -ErrorAction SilentlyContinue'],
        capture_output=True, text=True
    )

    # Só cria a porta se ela ainda não existir
    if not check_port.stdout.strip():
        subprocess.run([
            "powershell", "-Command",
            f'Add-PrinterPort -Name "{port_name}" -PrinterHostAddress "{ip}"'
        ], check=True)

    # Adiciona a impressora usando a porta (idempotente - pode rodar de novo)
    subprocess.run([
        "powershell", "-Command",
        f'Add-Printer -Name "{nome}" -PortName "{port_name}" -DriverName "Microsoft IPP Class Driver"'
    ], check=True)
