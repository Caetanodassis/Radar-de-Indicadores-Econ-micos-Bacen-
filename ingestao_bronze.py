import requests
import json
import os
from datetime import datetime

codigo_serie = 432
pasta_destino = "Radar-de-Indicadores-Econ-micos-Bacen-/bronze/selic"
os.makedirs(pasta_destino, exist_ok=True)

# Para séries diárias, o Bacen exige dataInicial e aceita até 10 anos de janela.
hoje = datetime.now()
data_final = hoje.strftime("%d/%m/%Y")
data_inicial = hoje.replace(year=hoje.year - 10).strftime("%d/%m/%Y")
url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"
params = {
    "formato": "json",
    "dataInicial": data_inicial,
    "dataFinal": data_final,
}

print("conectando a API do Banco Central do Brasil...")
resposta = requests.get(url, params=params)

if resposta.status_code == 200:
    dados_json = resposta.json()
    
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    caminho_arquivo = f"{pasta_destino}/{data_hoje}.json"
    
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! Dados Selic Salvos em: {caminho_arquivo}")
    
else:
    print(f"Falha ao conectar à API. Código de status: {resposta.status_code}") 