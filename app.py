import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Saúde - Inteligência Operacional")

# --- CONFIGURAÇÃO CORS (Permite o React conectar) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

COORDS_RJ = [(-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
             (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850), (-43.795, -23.025)]
POLIGONO = Polygon(COORDS_RJ)

def rodar_pipeline_operacional(n=2000):
    dados = []
    for i in range(n):
        perfil = random.choice(['Adulto', 'Criança'])
        qtd_vacinas = random.randint(1, 5)
        qtd_coletas = random.randint(0, 5)
        tempo_servico = (qtd_vacinas * 5) + (qtd_coletas * 8)
        if perfil == 'Criança': tempo_servico += 10
        tempo_total_casa = 15 + tempo_servico
        dados.append({'id': i, 'hora': random.randint(6, 17), 'perfil': perfil, 'vacinas': qtd_vacinas, 'coletas': qtd_coletas, 'tempo_total_min': tempo_total_casa, 'lat': round(random.uniform(-23.05, -22.75), 6), 'lon': round(random.uniform(-43.60, -43.10), 6)})

    df = pd.DataFrame(dados)
    df['valido'] = df.apply(lambda r: POLIGONO.contains(Point(r['lon'], r['lat'])), axis=1)
    df_v = df[df['valido']].copy()
    relatorio = df_v.groupby('hora').agg(Total_Casas=('id', 'count'), Pacientes_Crianca=('perfil', lambda x: (x == 'Criança').sum()), Pacientes_Adulto=('perfil', lambda x: (x == 'Adulto').sum()), Total_Vacinas=('vacinas', 'sum'), Total_Coletas=('coletas', 'sum'), Minutos_Totais_Trabalho=('tempo_total_min', 'sum')).reset_index()
    relatorio['Duplas_Necessarias'] = (relatorio['Minutos_Totais_Trabalho'] / 60).apply(np.ceil).astype(int)
    relatorio['Atendimentos_em_6h'] = ((relatorio['Total_Casas'] / relatorio['Duplas_Necessarias']) * 6).round(0).astype(int)
    relatorio['Tempo_Medio_por_Casa_Min'] = (relatorio['Minutos_Totais_Trabalho'] / relatorio['Total_Casas']).round(0).astype(int)
    relatorio.to_csv("dimensionamento.csv", index=False)
    return relatorio

@app.get("/api/dados")
def get_dados():
    if not os.path.exists("dimensionamento.csv"):
        rodar_pipeline_operacional()
    df = pd.read_csv("dimensionamento.csv")
    return JSONResponse(content=df.to_dict(orient="records"))

@app.get("/processar")
def processar():
    rel = rodar_pipeline_operacional()
    return {"status": "sucesso", "registros": len(rel)}

@app.get("/")
def home():
    return HTMLResponse("<h1>API Operacional Beep Saúde</h1><p>Acesse /api/dados para o JSON.</p>")
