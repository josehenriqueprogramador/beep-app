# 🚀 Beep Saúde - Gestão de Duplas & Performance

Sistema especializado em dimensionamento de escala para operações de saúde domiciliar, focado em transformar volume de atendimentos em necessidade real de pessoal.

---

## 📌 Visão Geral

O foco central deste projeto é a otimização da escala operacional. Ele processa a base de chamados e aplica regras de negócio para definir a eficiência das equipes:

- **Dimensionamento de Duplas:** Cálculo exato de quantos técnicos e motoristas são necessários.
- **Matriz de Complexidade:** Ajuste automático de tempo para casos pediátricos (+10 min).
- **Cálculo de Jornada:** Planejamento baseado em turnos de 6 horas.
- **Performance:** Estimativa de produtividade entre 6 a 12 atendimentos por equipe.

---

## 🧠 Regras de Negócio

- **Perfil Pediátrico:** Identificação de pacientes infantis para ajuste do tempo médio de atendimento.
- **Gestão de Itens:** Diferenciação entre volume de vacinas e coletas por domicílio.
- **Métrica de Escala:** Conversão de carga horária total em número de duplas operacionais.

---

## 📁 Estrutura do App

/
├── main.py              # Script principal de processamento
├── complexidade.py      # Lógica da Matriz de Complexidade
├── escala.py            # Motor de cálculo de duplas
├── data/                # Inputs e Outputs (CSV)
└── requirements.txt     # Dependências

---

## 📊 Indicadores Gerados

O sistema processa os dados e entrega um relatório detalhado com:

- **Total de Casas:** Volume bruto de paradas no dia.
- **Duplas Necessárias:** Quantidade de equipes para cobrir a demanda sem atrasos.
- **Tempo Médio/Casa:** KPI que identifica a complexidade da rota.
- **Capacidade Operacional:** Projeção de atendimentos possíveis dentro da jornada.

---

## 🚀 Como Executar

python main.py

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
