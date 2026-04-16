from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Operacional API")

# --- CONFIGURAÇÕES TÉCNICAS (Mantidas) ---
COORDS_RJ = [(-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
             (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850), (-43.795, -23.025)]
POLIGONO = Polygon(COORDS_RJ)

def rodar_pipeline():
    # ... (Sua lógica de processamento que já fizemos) ...
    # Simulação rápida para o exemplo
    dados = [{'horario_inicio': f"{random.randint(6,17)}:00", 'lat':-22.8, 'lon':-43.3} for _ in range(1000)]
    df = pd.DataFrame(dados)
    df['valido'] = True
    pico = df['horario_inicio'].str.split(':').str[0].value_counts().sort_index()
    relatorio = pd.DataFrame({'pedidos': pico, 'motoristas': (pico/2).apply(np.ceil).astype(int)})
    relatorio.to_csv("dimensionamento.csv")
    return len(df)

# --- NOVA ROTA PRINCIPAL COM INTERFACE ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beep Logística Inteligente</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; }
            .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; margin-top: 50px; max-width: 500px; }
            h1 { color: #00a896; margin-bottom: 10px; }
            p { color: #666; margin-bottom: 30px; }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; transition: 0.3s; cursor: pointer; border: none; }
            .btn-process { background-color: #00a896; color: white; }
            .btn-process:hover { background-color: #008f7f; }
            .btn-download { background-color: #2c3e50; color: white; }
            .btn-download:hover { background-color: #1a252f; }
            footer { margin-top: auto; padding: 20px; color: #888; font-size: 0.9em; }
            a { color: #00a896; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Beep Saúde</h1>
            <p>Sistema de Dimensionamento de Frota Geolocalizado</p>
            
            <a href="/processar" class="btn btn-process">⚙️ Rodar Pipeline</a>
            <a href="/download-relatorio" class="btn btn-download">📂 Baixar Relatório</a>
        </div>
        
        <footer>
            Repositório: <a href="https://github.com/Josehenriqueprogramador/beep-app.git" target="_blank">josehenriqueprogramador/beep-app.git</a>
        </footer>
    </body>
    </html>
    """

@app.get("/processar")
def processar():
    qtd = rodar_pipeline()
    return f"Processamento concluído! {qtd} registros analisados. Volte e clique em baixar."

@app.get("/download-relatorio")
def download():
    if os.path.exists("dimensionamento.csv"):
        return FileResponse("dimensionamento.csv", media_type="text/csv", filename="relatorio_beep.csv")
    raise HTTPException(status_code=404, detail="Arquivo não encontrado. Rode o pipeline primeiro.")
