from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Operacional API")

# --- CONFIGURAÇÕES TÉCNICAS ---
COORDS_RJ = [
    (-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
    (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850),
    (-43.795, -23.025)
]
POLIGONO = Polygon(COORDS_RJ)

# --- FUNÇÕES DE LÓGICA (SEUS SCRIPTS) ---

def rodar_pipeline():
    # Fase 1: Geração
    vacinas = ['Gripe', 'BCG', 'Hepatite B', 'Tríplice Viral', 'Febre Amarela']
    dados = []
    for i in range(1000):
        hora = random.randint(6, 17)
        dados.append({
            'id_pedido': f'BEEP-{2000 + i}',
            'vacina': random.choice(vacinas),
            'horario_inicio': f"{hora:02d}:00",
            'latitude': round(random.uniform(-23.05, -22.75), 6),
            'longitude': round(random.uniform(-43.60, -43.10), 6),
        })
    df = pd.DataFrame(dados)

    # Fase 2: Validação Geográfica
    df['valido'] = df.apply(lambda r: POLIGONO.contains(Point(r['longitude'], r['latitude'])), axis=1)
    df_limpo = df[df['valido']].copy()

    # Fase 3: Dimensionamento
    df_limpo['hora'] = df_limpo['horario_inicio'].str.split(':').str[0].astype(int)
    pico = df_limpo['hora'].value_counts().sort_index()
    dimensionamento = (pico / 2).apply(np.ceil).astype(int)
    
    relatorio = pd.DataFrame({
        'pedidos': pico,
        'motoristas_necessarios': dimensionamento
    })
    
    # Salva os resultados temporariamente no servidor
    df_limpo.to_csv("pedidos_validados.csv", index=False)
    relatorio.to_csv("dimensionamento.csv")
    
    return {"status": "sucesso", "pedidos_validos": len(df_limpo)}

# --- ENDPOINTS (COMANDOS DA API) ---

@app.get("/")
def home():
    return {"mensagem": "API Beep Operacional Online. Use /processar para rodar o pipeline."}

@app.get("/processar")
def processar():
    """Executa todo o pipeline e gera os arquivos no servidor"""
    resultado = rodar_pipeline()
    return resultado

@app.get("/download-relatorio")
def download():
    """Baixa o arquivo de dimensionamento gerado"""
    if os.path.exists("dimensionamento.csv"):
        return FileResponse("dimensionamento.csv", media_type="text/csv", filename="relatorio_beep.csv")
    raise HTTPException(status_code=404, detail="Arquivo não encontrado. Rode /processar primeiro.")
