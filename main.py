import PySimpleGUI as sg
import json
from printer_manager import add_printer, list_installed_printers

with open("catalog.json", encoding="utf-8") as f:
    catalog = json.load(f)

nomes = [p["nome"] for p in catalog]

layout = [
    [sg.Text("Selecione a impressora:")],
    [sg.Combo(nomes, key="-IMPRESSORA-", size=(40, 1))],
    [sg.Button("Instalar"), sg.Button("Sair")],
    [sg.Multiline(size=(50, 10), key="-LOG-", disabled=True)]
]

window = sg.Window("Instalador de Impressoras", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Sair"):
        break
    if event == "Instalar":
        escolhida = next(p for p in catalog if p["nome"] == values["-IMPRESSORA-"])
        try:
            add_printer(escolhida["nome"], escolhida["ip"], escolhida["driver"])
            window["-LOG-"].print(f"✅ {escolhida['nome']} instalada com sucesso!")
        except Exception as e:
            window["-LOG-"].print(f"❌ Erro: {e}")

window.close()