import requests
import json
import os
from datetime import datetime

# Dicionário com os nomes e códigos das séries que queremos
indicadores = {
    "selic": 432,
    "ipca": 433,
    "dolar": 1
}

hoje = datetime.now()
data_final = hoje.strftime("%d/%m/%Y")
data_inicial = hoje.replace(year=hoje.year - 10).strftime("%d/%m/%Y")

data_hoje_arquivo = hoje.strftime("%Y-%m-%d")

# O laço 'for' vai rodar uma vez para cada indicador
for nome, codigo in indicadores.items():
    
    pasta_destino = f"bronze/{nome}"
    os.makedirs(pasta_destino, exist_ok=True)
    
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final,
    }

    print(f"Baixando dados: {nome.upper()} (Código: {codigo})...")
    resposta = requests.get(url, params=params)

    if resposta.status_code == 200:
        dados_json = resposta.json()
        caminho_arquivo = f"{pasta_destino}/{data_hoje_arquivo}.json"
        
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
            
        print(f"Sucesso! Salvo em: {caminho_arquivo}\n")
    else:
        print(f"Falha ao conectar à API para {nome}. Código: {resposta.status_code}\n")