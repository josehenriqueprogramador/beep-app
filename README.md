# 🚀 Beep Saúde - Pipeline de Dimensionamento Logístico
Este projeto implementa o **Core Lógico** de uma operação logística para serviços de saúde domiciliar. O sistema processa pedidos de vacinação, valida a viabilidade geográfica na região metropolitana do Rio de Janeiro e calcula o dimensionamento ideal da frota de motoristas/técnicos.
## 🧠 O Motor do Projeto
O sistema foi construído sobre três pilares fundamentais de engenharia de dados:
 1. **Motor de Cálculo:** Algoritmo de inteligência para predição de necessidade de pessoal baseado em janelas horárias.
 2. **Validação Geoespacial:** Filtro de precisão matemática utilizando polígonos (biblioteca Shapely) para garantir que 100% dos pedidos estejam dentro da área de cobertura operacional.
 3. **Interface de API:** Exposição dos resultados através de endpoints FastAPI, permitindo integração com outras ferramentas de BI.
## 🛠️ Tecnologias Utilizadas
 * **Python 3.10+**
 * **Pandas & Numpy:** Manipulação e análise de dados volumosos.
 * **Shapely:** Geoprocessamento e álgebra geoespacial.
 * **FastAPI & Uvicorn:** Infraestrutura de microserviços.
## 📈 Evolução: Do Protótipo à Produção (Roadmap)
Este repositório contém o **MVP (Minimum Viable Product)** funcional. Abaixo, descrevo a transição da simulação para o sistema real da Beep Saúde:
### 1. Camada de Dados
 * **Hoje:** Geração de dados sintéticos via Faker.
 * **Produção:** Integração direta via **SQL/PostgreSQL** com o banco de dados de agendamentos reais da Beep.
### 2. Dinâmica Geográfica
 * **Hoje:** Polígono estático de atendimento do Rio de Janeiro.
 * **Produção:** Integração com **Google Maps API** para ajuste de polígono em tempo real (considerando interdições, clima e zonas de risco).
### 3. Inteligência de Tráfego
 * **Hoje:** Capacidade fixa de 2 atendimentos/hora por motorista.
 * **Produção:** Algoritmo adaptativo que ajusta a produtividade baseada no **histórico de trânsito** e tempo médio de aplicação de cada tipo de vacina.
### 4. Observabilidade e Segurança
 * **Hoje:** Execução aberta em ambiente de teste.
 * **Produção:** Implementação de **OAuth2/API Keys** para segurança e **Sentry/Loguru** para monitoramento de erros em tempo real.
## 🏁 Como Rodar o Projeto
 1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   
   ```
 2. Inicie o servidor:
   ```bash
   uvicorn app:app --reload
   
   ```
 3. Acesse http://localhost:8000/processar para rodar o pipeline.
> **Visão Executiva:** > "Este projeto representa o **Motor Lógico (Core)** da operação. Ele já valida a viabilidade geográfica e calcula o dimensionamento de frota. Para escala industrial, a arquitetura foi desenhada para facilitar a substituição de entradas simuladas por conectores de dados em tempo real (ETL)."
http://localhost:8000/download-relatorio
estará o relatório logo após o processamento.


