import pandas as pd
import os
from datetime import datetime

indicadores = ["selic", "ipca", "dolar"]

data_hoje_arquivo = datetime.now().strftime("%Y-%m-%d")

raiz_projeto = os.path.dirname(os.path.abspath(__file__))

pasta_destino_silver = os.path.join(raiz_projeto, "silver")
os.makedirs(pasta_destino_silver, exist_ok=True)

for nome in indicadores:
    print(f"limpando os dados de {nome.upper()}...")
    
    caminho_bronze = os.path.join(raiz_projeto, "bronze", nome, f"{data_hoje_arquivo}.json")
    
    if not os.path.exists(caminho_bronze):
        print(f"Arquivo {caminho_bronze} não encontrado. Pulando {nome.upper()}.\n")
        
        continue
    
    df = pd.read_json(caminho_bronze)
    
    df['data'] = pd.to_datetime(df['data'], format = "%d/%m/%Y")
    
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    
    df['indicador'] = nome
    
    caminho_silver = f"{pasta_destino_silver}/{nome}.parquet"
    try:
        df.to_parquet(caminho_silver, index=False)
        print(f"  -> Sucesso! Arquivo limpo e salvo em: {caminho_silver}")
    except ImportError:
        caminho_csv = os.path.join(pasta_destino_silver, f"{nome}.csv")
        df.to_csv(caminho_csv, index=False)
        print(f"  -> Aviso: lib parquet não instalada. Salvo como CSV em: {caminho_csv}")

print("\nProcessamento da Camada Silver concluído!")