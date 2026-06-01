import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Saúde - Inteligência Operacional")

# --- CONFIGURAÇÃO GEOGRÁFICA (RIO DE JANEIRO) ---
COORDS_RJ = [(-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
             (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850), (-43.795, -23.025)]
POLIGONO = Polygon(COORDS_RJ)

def rodar_pipeline_operacional(n=2000):
    dados = []
    for i in range(n):
        perfil = random.choice(['Adulto', 'Criança'])
        qtd_vacinas = random.randint(1, 5)
        qtd_coletas = random.randint(0, 5)
        
        # --- MATRIZ DE TEMPO (REGRAS REAIS) ---
        # Deslocamento + Preparação: 15 min fixos por casa
        # Tempo por item: Vacina (5 min) | Coleta (8 min)
        # Complexidade: Criança soma +10 min pelo tempo de manejo
        
        tempo_servico = (qtd_vacinas * 5) + (qtd_coletas * 8)
        if perfil == 'Criança': 
            tempo_servico += 10
            
        tempo_total_casa = 15 + tempo_servico
        
        dados.append({
            'id': i,
            'hora': random.randint(6, 17),
            'perfil': perfil,
            'vacinas': qtd_vacinas,
            'coletas': qtd_coletas,
            'tempo_total_min': tempo_total_casa,
            'lat': round(random.uniform(-23.05, -22.75), 6),
            'lon': round(random.uniform(-43.60, -43.10), 6)
        })
    
    df = pd.DataFrame(dados)
    # Filtro geográfico
    df['valido'] = df.apply(lambda r: POLIGONO.contains(Point(r['lon'], r['lat'])), axis=1)
    df_v = df[df['valido']].copy()
    
    # --- GERAÇÃO DO RELATÓRIO OPERACIONAL (SEM DECIMAIS) ---
    relatorio = df_v.groupby('hora').agg(
        Total_Casas=('id', 'count'),
        Pacientes_Crianca=('perfil', lambda x: (x == 'Criança').sum()),
        Pacientes_Adulto=('perfil', lambda x: (x == 'Adulto').sum()),
        Total_Vacinas=('vacinas', 'sum'),
        Total_Coletas=('coletas', 'sum'),
        Minutos_Totais_Trabalho=('tempo_total_min', 'sum')
    ).reset_index()

    # 1. Cálculo de Duplas (Sempre arredonda para cima para não faltar gente)
    relatorio['Duplas_Necessarias'] = (relatorio['Minutos_Totais_Trabalho'] / 60).apply(np.ceil).astype(int)
    
    # 2. Produtividade Real: Quantos atendimentos a dupla faz na jornada de 6h (Número Inteiro)
    # Calculamos a média e arredondamos para o inteiro mais próximo
    relatorio['Atendimentos_em_6h'] = ((relatorio['Total_Casas'] / relatorio['Duplas_Necessarias']) * 6).round(0).astype(int)
    
    # 3. Tempo Médio gasto em cada casa (incluindo o deslocamento)
    relatorio['Tempo_Medio_por_Casa_Min'] = (relatorio['Minutos_Totais_Trabalho'] / relatorio['Total_Casas']).round(0).astype(int)

    relatorio.to_csv("dimensionamento.csv", index=False)
    return len(df_v)

# --- INTERFACE E ROTAS ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Beep Saúde | Gestão de Frota</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f4f9f8; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; border-top: 10px solid #00a896; }
            h1 { color: #00a896; margin-bottom: 5px; }
            p { color: #666; margin-bottom: 30px; line-height: 1.5; }
            .btn { display: block; padding: 15px 30px; margin: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; transition: 0.3s; }
            .btn-run { background: #00a896; color: white; }
            .btn-down { background: #2c3e50; color: white; }
            .btn:hover { opacity: 0.9; transform: translateY(-2px); }
            footer { margin-top: 30px; font-size: 0.85em; color: #999; }
            a { color: #00a896; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Beep Saúde</h1>
            <p><b>Painel de Dimensionamento de Duplas</b><br>
            Cálculo baseado em Perfil (Adulto/Criança) e Volume de Serviços.</p>
            <a href="/processar" class="btn btn-run">⚙️ Gerar Escala do Dia</a>
            <a href="/download-relatorio" class="btn btn-down">📂 Descarregar Relatório CSV</a>
        </div>
        <footer>Desenvolvido por José Henrique Jardim | <a href="https://github.com/Josehenriqueprogramador/beep-app.git">GitHub</a></footer>
    </body>
    </html>
    """

@app.get("/processar")
def processar():
    qtd = rodar_pipeline_operacional()
    return {"status": "sucesso", "pedidos_validos": qtd, "mensagem": "Escala calculada com base na jornada de 6h."}

@app.get("/download-relatorio")
def download():
    if os.path.exists("dimensionamento.csv"):
        return FileResponse("dimensionamento.csv", media_type="text/csv", filename="escala_duplas_beep.csv")
    raise HTTPException(status_code=404, detail="Gere o processamento primeiro.")
