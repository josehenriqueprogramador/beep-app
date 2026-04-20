# 🚀 Beep Saúde - Logística Inteligente & Gestão de Duplas

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![Status](https://img.shields.io/badge/Status-Produção_MVP-green.svg)

Este projeto implementa um **Motor de Dimensionamento Logístico** de alta precisão para operações de saúde domiciliar. Diferente de modelos lineares, este algoritmo calcula a necessidade de frota baseada na **Matriz de Complexidade de Atendimento**.

## 🧠 Inteligência do Negócio: Matriz de Complexidade
O sistema abandona a métrica fixa de "atendimentos por hora" e adota uma visão baseada em carga de trabalho real (Workload Capacity):

1.  **Variáveis de Perfil:** Identifica pacientes **Crianças**, adicionando um tempo de manejo de +10 min para garantir a qualidade e o cuidado no atendimento pediátrico.
2.  **Multisserviços:** Calcula o tempo incremental para cada item adicional (Vacinas vs. Coletas), permitindo que um chamado com 5 itens seja dimensionado de forma diferente de um chamado simples.
3.  **Jornada Real:** Calibrado para a realidade operacional da Beep, onde uma dupla (Técnica + Motorista) realiza entre **6 a 12 atendimentos em uma jornada de 6 horas**.

---

## 🛠️ Arquitetura Técnica
* **Motor Geográfico:** Validação via `Shapely` para garantir cobertura na Região Metropolitana do Rio de Janeiro.
* **Cálculo de Capacidade:** Algoritmo que converte minutos totais (Atendimento + Deslocamento) em **Duplas Necessárias** por faixa horária.
* **Output Operacional:** Gera relatórios em CSV com métricas de produtividade prontas para tomada de decisão gerencial.

---

## 📊 Estrutura do Relatório (CSV)
O sistema exporta os seguintes indicadores críticos:
* **Total_Casas:** Volume de paradas necessárias.
* **Pacientes_Crianca/Adulto:** Justificativa da complexidade da hora.
* **Duplas_Necessarias:** Quantidade de equipes para cobrir a demanda sem atrasos.
* **Atendimentos_em_6h:** Produtividade real estimada para a jornada da dupla.
* **Tempo_Medio_por_Casa:** KPI que explica o "gargalo" operacional de cada faixa horária.

---

## 🏁 Como Operar

### 1. Instalação e Execução
```bash
pip install -r requirements.txt
uvicorn app:app --reload
