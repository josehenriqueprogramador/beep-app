
# 🚀 Beep Saúde - Logística Inteligente & Dimensionamento de Frota

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![Status](https://img.shields.io/badge/Status-MVP_Funcional-green.svg)

Este projeto implementa o **Core Lógico** de uma operação logística de saúde domiciliar. O sistema resolve um dos maiores desafios do setor: **Como garantir que temos a quantidade certa de profissionais, no lugar certo e na hora certa?**

## 🧠 Arquitetura do Motor Lógico
O sistema processa milhares de pontos de dados para entregar inteligência operacional através de três pilares:

1.  **Validação Geoespacial:** Filtro de precisão matemática via polígonos (`Shapely`). Garante que 100% dos pedidos processados estejam dentro da malha viável de atendimento da Região Metropolitana do Rio de Janeiro.
2.  **Motor de Dimensionamento:** Algoritmo que traduz demanda bruta em necessidade de capital humano, aplicando regras de negócio de produtividade por janela horária.
3.  **Interface de Microserviço:** Exposição via `FastAPI`, pronta para ser consumida por Dashboards de BI ou sistemas de despacho.

---

## 🛠️ Stack Tecnológica
* **Core:** Python 3.10+
* **Análise de Dados:** `Pandas` & `Numpy` (Processamento vetorial).
* **Geoprocessamento:** `Shapely` (Álgebra de pontos em polígonos).
* **Servidor:** `FastAPI` & `Uvicorn`.

---

## 📈 Roadmap: Do Protótipo à Produção
Este repositório é um **MVP (Minimum Viable Product)**. Abaixo, a visão de evolução para escala industrial:

| Funcionalidade | Estado Atual (MVP) | Visão de Produção |
| :--- | :--- | :--- |
| **Fonte de Dados** | Dados sintéticos (`Faker`) | Conexão direta via **SQL/PostgreSQL** |
| **Geolocalização** | Polígono estático | **Google Maps API** (Dinâmico com trânsito/risco) |
| **Produtividade** | Fixa (2 atend./hora) | **Machine Learning** (Predição baseada em clima/trânsito) |
| **Segurança** | Aberta para testes | Autenticação **OAuth2 / API Keys** |

---

## 🏁 Como Rodar e Testar

### 1. Instalação
```bash
pip install -r requirements.txt

```
### 2. Execução
```bash
uvicorn app:app --reload

```
### 3. Fluxo de Operação (Importante ⚠️)
Devido ao uso de **armazenamento efêmero** no ambiente de nuvem (Render Free), o ciclo de uso deve seguir esta ordem:
 * **PASSO 1 (Processar):** Acesse http://localhost:8000/processar
   * *O que ocorre:* O motor gera os dados, valida a geografia e salva o resultado no servidor.
 * **PASSO 2 (Download):** Acesse http://localhost:8000/download-relatorio
   * *O que ocorre:* Você recebe o arquivo dimensionamento.csv com a escala de motoristas pronta.
> **Nota Técnica:** No Render Free, o servidor "dorme" após 15 minutos. Se o download falhar, basta rodar o Passo 1 novamente para reaquecer o motor.
> 
## 🎯 Visão Executiva
> "Este projeto representa o **Cérebro Operacional** da logística. Ele não apenas processa dados, ele valida a viabilidade de negócio. A arquitetura foi desenhada para ser 'plug-and-play', onde a substituição da camada de simulação por dados reais de um banco de dados (ETL) é feita sem alterar a lógica central de cálculo."
