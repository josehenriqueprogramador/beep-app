# 🚀 Beep Saúde - Logística Inteligente

Plataforma de inteligência logística voltada para dimensionamento de frotas e otimização de atendimento domiciliar, desenvolvida com Python + FastAPI + Docker.

---

## 📌 Visão Geral

O sistema implementa um Motor de Dimensionamento de alta precisão para operações de saúde domiciliar, focado em:

- Cálculo de Complexidade (Pediátrico/Adulto)
- Dimensionamento de Duplas (Técnica + Motorista)
- Otimização de Jornada de 6 Horas
- Gestão de Multisserviços (Vacinas e Coletas)

---

## 🧠 Tecnologias

- Python 3.10+
- FastAPI
- Docker
- Pandas
- Shapely (Geofencing)

---

## 📁 Estrutura

backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── schemas/
│   └── utils/
├── requirements.txt
└── Dockerfile

docker-compose.yml

---

## 🧱 Arquitetura

Requisição (Dados)
↓
Validador Geográfico (RJ)
↓
Motor de Complexidade
↓
Cálculo de Duplas
↓
Relatório (CSV)

---

## 🚀 Rodar Localmente

pip install -r requirements.txt

uvicorn app.main:app --reload

Servidor:

http://localhost:8000

---

## 🐳 Rodar com Docker

docker compose up -d --build

---

## 📡 Endpoints

GET /health

Resposta:

{
  "status": "ok"
}

POST /dimensionar

Resposta:

{
  "message": "processamento concluído"
}

---

## 🧪 Testes

curl http://localhost:8000/health

---

## 🔐 Próximas Features

- Integração Google Maps
- Dashboard Real-time
- Predição de Demanda
- Roteirização Dinâmica

---

## 📈 Roadmap

Fase 1
- Algoritmo Base
- Estrutura Docker

Fase 2
- API FastAPI

Fase 3
- Interface Web

---

## 👨‍💻 Autor

José Henrique Jardim

https://github.com/josehenriqueprogramador

---

## 📺 Processo de Desenvolvimento

[![Assista no YouTube](https://img.youtube.com/vi/36UTnlklR-8/0.jpg)](https://youtu.be/36UTnlklR-8)

---

## 📜 Licença

MIT License
