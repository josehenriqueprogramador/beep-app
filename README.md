# 🚀 Beep Saúde - Inteligência Operacional

API desenvolvida com **FastAPI** para dimensionamento automático de duplas (Técnica + Motorista) e gestão de escala na Região Metropolitana do Rio de Janeiro.

---

## 📌 Visão Geral

O projeto automatiza o planejamento de jornada da Beep Saúde, convertendo demanda em decisões de escala baseadas em regras reais:

- **Matriz de Tempo:** Cálculo por item (Vacina 5min / Coleta 8min) + 15min fixos de deslocamento.
- **Complexidade Pediátrica:** Adicional de +10min para manejo infantil.
- **Geofencing:** Filtro via `Shapely` para validar operações dentro do polígono do Rio de Janeiro.
- **Capacidade:** Dimensionamento baseado em jornadas reais de 6 horas.

---

## 🧠 Tecnologias

- Python 3.10+
- FastAPI
- Pandas & NumPy
- Shapely

---

## 📁 Estrutura do App

/
├── main.py              # Script principal (API e Cálculo)
├── dimensionamento.csv  # Relatório gerado (Output)
└── requirements.txt     # Dependências

---

## 🧱 Lógica de Processamento

Entrada (Simulação) → Filtro Geográfico → Matriz de Complexidade → Cálculo de Minutos → Escala de Duplas

---

## 📊 Indicadores Gerados (KPIs)

- **Total de Casas:** Volume de paradas por hora.
- **Duplas Necessárias:** Equipes necessárias para a demanda.
- **Atendimentos em 6h:** Produtividade real por dupla.
- **Tempo Médio/Casa:** Eficiência da rota.

---

## 🚀 Como Executar

pip install -r requirements.txt

uvicorn main:app --reload

**Interface:** http://localhost:8000

---

## 👨‍💻 Autor

José Henrique Jardim

https://github.com/Josehenriqueprogramador/beep-app.git

---

## 📺 Processo de Desenvolvimento

[![Assista no YouTube](https://img.youtube.com/vi/36UTnlklR-8/0.jpg)](https://youtu.be/36UTnlklR-8)

---

## 📜 Licença

MIT License
