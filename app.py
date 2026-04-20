import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Logística Inteligente")

# --- CONFIGURAÇÃO GEOGRÁFICA ---
COORDS_RJ = [(-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
             (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850), (-43.795, -23.025)]
POLIGONO = Polygon(COORDS_RJ)

def rodar_pipeline_operacional(n=2000):
    dados = []
    for i in range(n):
        perfil = random.choice(['Adulto', 'Criança'])
        qtd_vacinas = random.randint(1, 5)
        qtd_coletas = random.randint(0, 5)
        
        # --- MATRIZ DE TEMPO REALISTA (EM MINUTOS) ---
        # Tempo base de deslocamento + setup: 15 min
        # Cada vacina: 5 min | Cada coleta: 8 min | Fator Criança: +10 min
        tempo_atendimento = (qtd_vacinas * 5) + (qtd_coletas * 8)
        if perfil == 'Criança': tempo_atendimento += 10
        
        tempo_total = 15 + tempo_atendimento # 15 é o deslocamento médio
        
        dados.append({
            'id': i,
            'hora': random.randint(6, 17),
            'perfil': perfil,
            'vacinas': qtd_vacinas,
            'coletas': qtd_coletas,
            'total_servicos': qtd_vacinas + qtd_coletas,
            'tempo_total_min': tempo_total,
            'lat': round(random.uniform(-23.05, -22.75), 6),
            'lon': round(random.uniform(-43.60, -43.10), 6)
        })
    
    df = pd.DataFrame(dados)
    df['valido'] = df.apply(lambda r: POLIGONO.contains(Point(r['lon'], r['lat'])), axis=1)
    df_v = df[df['valido']].copy()
    
    # --- RELATÓRIO FOCO EM DUPLAS E PRODUTIVIDADE ---
    relatorio = df_v.groupby('hora').agg(
        Total_Pedidos=('id', 'count'),
        Total_Vacinas=('vacinas', 'sum'),
        Total_Coletas=('coletas', 'sum'),
        Soma_Minutos=('tempo_total_min', 'sum')
    ).reset_index()

    # Cálculo: Soma de minutos / 60 min = Duplas necessárias naquela hora
    relatorio['Duplas_Necessarias'] = (relatorio['Soma_Minutos'] / 60).apply(np.ceil).astype(int)
    
    # Média de atendimentos que cada dupla fará por hora (deve girar entre 1.0 e 2.0 p/ bater os 6-12 em 6h)
    relatorio['Atendimentos_por_Dupla_Hora'] = (relatorio['Total_Pedidos'] / relatorio['Duplas_Necessarias']).round(1)

    relatorio.to_csv("dimensionamento.csv", index=False)
    return len(df_v)

# --- ROTAS (Mantidas com a nova lógica) ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Beep Saúde | Gestão de Duplas</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f0f4f3; text-align: center; padding-top: 50px; }
            .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; border-top: 8px solid #00a896; }
            .btn { display: block; padding: 12px 25px; margin: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; color: white; }
            .btn-run { background: #00a896; }
            .btn-down { background: #2c3e50; }
            footer { margin-top: 20px; font-size: 0.8em; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color:#00a896">Beep Saúde</h1>
            <p>Dimensionamento de Duplas (Técnica + Motorista)</p>
            <a href="/processar" class="btn btn-run">⚙️ Processar Escala Diária</a>
            <a href="/download-relatorio" class="btn btn-down">📂 Baixar Relatório Detalhado</a>
        </div>
        <footer>Repositório: <a href="https://github.com/Josehenriqueprogramador/beep-app.git">josehenriqueprogramador/beep-app.git</a></footer>
    </body>
    </html>
    """

@app.get("/processar")
def processar():
    qtd = rodar_pipeline_operacional()
    return {"status": "sucesso", "pedidos": qtd}

@app.get("/download-relatorio")
def download():
    if os.path.exists("dimensionamento.csv"):
        return FileResponse("dimensionamento.csv", media_type="text/csv", filename="escala_duplas_beep.csv")
    raise HTTPException(status_code=404)
