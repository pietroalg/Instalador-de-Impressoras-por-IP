import subprocess

def add_printer(nome, ip, driver):
    port_name = f"IP_{ip}"

    # Verifica se a porta já existe
    check_port = subprocess.run(
        ["powershell", "-Command", f'Get-PrinterPort -Name "{port_name}" -ErrorAction SilentlyContinue'],
        capture_output=True, text=True
    )

    # Só cria a porta se ela NÃO existir ainda
    if not check_port.stdout.strip():
        subprocess.run([
            "powershell", "-Command",
            f'Add-PrinterPort -Name "{port_name}" -PrinterHostAddress "{ip}"'
        ], check=True)

    # Adiciona a impressora usando essa porta (isso pode rodar de novo sem problema)
    subprocess.run([
        "powershell", "-Command",
        f'Add-Printer -Name "{nome}" -PortName "{port_name}" -DriverName "{driver}"'
    ], check=True)

def test_print(nome):
    subprocess.run([
        "powershell", "-Command",
        f'Get-Printer -Name "{nome}" | Invoke-Expression "rundll32 printui.dll,PrintUIEntry /k /n \\"{nome}\\""'
    ])

def list_installed_printers():
    result = subprocess.run(
        ["powershell", "-Command", "Get-Printer | Select-Object Name | ConvertTo-Json"],
        capture_output=True, text=True
    )
    return result.stdout