"""
Instalador de Impressoras - Tela principal (GUI)

Interface gráfica que permite ao usuário selecionar uma impressora
de um catálogo pré-cadastrado e instalá-la automaticamente no Windows.
"""

import sys
import os
import PySimpleGUI as sg
import json
from printer_manager import add_printer


def resource_path(relative_path):
    """Retorna o caminho correto do arquivo, tanto rodando via python
    quanto rodando como .exe empacotado pelo PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        # Rodando como .exe: os arquivos ficam numa pasta temporária
        return os.path.join(sys._MEIPASS, relative_path)
    # Rodando normalmente via python main.py
    return os.path.join(os.path.abspath("."), relative_path)


# Carrega o catálogo de impressoras cadastradas
with open(resource_path("catalog.json"), encoding="utf-8") as f:
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
            add_printer(escolhida["nome"], escolhida["ip"])
            window["-LOG-"].print(f"✅ {escolhida['nome']} instalada com sucesso!")
        except Exception as e:
            window["-LOG-"].print(f"❌ Erro: {e}")

window.close()
