# Teste de Analytics - Quod
Resolução do Teste para Estagiário de Analytics da Quod. O projeto contempla a simulação e limpeza de dados com Python (Pandas) , extração de métricas com consultas SQL e um relatório de insights voltado para estratégias de negócios.

Este repositório contém os códigos, análises e relatórios desenvolvidos como resolução do Teste para Estagiário de Analytics da Quod.

## Estrutura do Repositório
O projeto foi dividido em três etapas principais, refletidas nos arquivos abaixo:
- `analise_vendas.py`: Script em Python responsável por gerar os dados simulados, realizar a limpeza (tratamento de nulos e duplicatas) e executar a análise exploratória.
- `data_clean.csv`: Base de dados final e tratada, gerada automaticamente pelo script Python.
- `tendencia_vendas.png`: Visualização gráfica em linha demonstrando a tendência mensal de vendas.
- `consultas_sql.sql`: Arquivo contendo as instruções SQL para extração de métricas de faturamento e desempenho de produtos, acompanhadas da explicação lógica.
- `relatorio_insights.md`: Relatório executivo apontando os principais insights observados nos dados e sugerindo estratégias comerciais acionáveis.

## Como Executar o Projeto
1. Certifique-se de ter o Python 3.x instalado em sua máquina.
2. Instale as bibliotecas necessárias rodando o seguinte comando no terminal:
   ```bash
   pip install pandas numpy matplotlib
