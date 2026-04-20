import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from shapely.geometry import Point, Polygon
import random
import os

app = FastAPI(title="Beep Logística Inteligente")

# --- CONFIGURAÇÃO GEOGRÁFICA (RIO DE JANEIRO) ---
COORDS_RJ = [(-43.795, -23.025), (-43.365, -23.010), (-43.160, -22.990),
             (-43.120, -22.850), (-43.300, -22.750), (-43.650, -22.850), (-43.795, -23.025)]
POLIGONO = Polygon(COORDS_RJ)

def rodar_pipeline_complexo(n=1000):
    dados = []
    tipos_servico = ['Vacina', 'Coleta']
    perfis = ['Adulto', 'Criança']
    
    for i in range(n):
        # Sorteio de variáveis de complexidade
        servico = random.choice(tipos_servico)
        perfil = random.choice(perfis)
        itens = random.randint(1, 3)
        
        # Lógica de Tempo (Regra de Negócio)
        tempo_base = 25 if servico == 'Coleta' else 15
        adicional_itens = (itens - 1) * 10
        adicional_perfil = 15 if perfil == 'Criança' else 0
        
        tempo_atendimento = tempo_base + adicional_itens + adicional_perfil
        deslocamento_estimado = 15  # minutos entre casas
        
        dados.append({
            'id_pedido': f'BEEP-{2000 + i}',
            'servico': servico,
            'perfil': perfil,
            'itens': itens,
            'tempo_total': tempo_atendimento + deslocamento_estimado,
            'hora': random.randint(6, 17),
            'lat': round(random.uniform(-23.05, -22.75), 6),
            'lon': round(random.uniform(-43.60, -43.10), 6)
        })
    
    df = pd.DataFrame(dados)
    
    # Validação Geográfica
    df['valido'] = df.apply(lambda r: POLIGONO.contains(Point(r['lon'], r['lat'])), axis=1)
    df_validado = df[df['valido']].copy()
    
    # Dimensionamento Inteligente por Carga Horária
    # Soma de todos os minutos necessários / 60 minutos (1 hora de trabalho)
    resumo = df_validado.groupby('hora')['tempo_total'].sum() / 60
    relatorio = pd.DataFrame({
        'Hora': [f"{int(h):02d}:00" for h in resumo.index],
        'Pedidos': df_validado['hora'].value_counts().sort_index().values,
        'Motoristas_Necessarios': resumo.apply(np.ceil).astype(int).values
    })
    
    relatorio.to_csv("dimensionamento.csv", index=False)
    df_validado.to_csv("pedidos_detalhados.csv", index=False)
    return len(df_validado)

# --- ROTAS DA API ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beep Logística | Dimensionamento</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f0f4f3; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); text-align: center; margin-top: 60px; max-width: 450px; border-top: 8px solid #00a896; }
            h1 { color: #00a896; margin-bottom: 5px; }
            p { color: #555; font-size: 0.9em; margin-bottom: 25px; }
            .btn { display: block; padding: 12px 25px; margin: 10px auto; border-radius: 6px; text-decoration: none; font-weight: 600; transition: 0.2s; border: none; width: 80%; }
            .btn-run { background: #00a896; color: white; }
            .btn-run:hover { background: #008f7f; transform: scale(1.02); }
            .btn-down { background: #2c3e50; color: white; }
            .btn-down:hover { background: #1a252f; transform: scale(1.02); }
            .footer { margin-top: auto; padding: 20px; font-size: 0.85em; color: #777; }
            a { color: #00a896; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Beep Saúde</h1>
            <p>Algoritmo de Dimensionamento de Frota<br><b>Variáveis:</b> Pediatria, Multisserviços e Logística RJ</p>
            <a href="/processar" class="btn btn-run">⚙️ Processar Demanda</a>
            <a href="/download-relatorio" class="btn btn-down">📂 Baixar Relatório (CSV)</a>
        </div>
        <div class="footer">
            Desenvolvido por José Henrique Jardim | 
            <a href="https://github.com/Josehenriqueprogramador/beep-app.git" target="_blank">GitHub Repo</a>
        </div>
    </body>
    </html>
    """

@app.get("/processar")
def processar():
    qtd = rodar_pipeline_complexo()
    return {"status": "sucesso", "pedidos_processados": qtd, "mensagem": "Relatório gerado com sucesso!"}

@app.get("/download-relatorio")
def download():
    if os.path.exists("dimensionamento.csv"):
        return FileResponse("dimensionamento.csv", media_type="text/csv", filename="dimensionamento_beep.csv")
    raise HTTPException(status_code=404, detail="Execute o processamento primeiro.")
