-- Tarefa 1: Listar nome do produto, categoria e soma total de vendas, ordenado do maior para o menor. [cite: 40, 41]
-- Lógica: Calculamos o total multiplicando a quantidade pelo preço dentro da função de agregação SUM. Usamos GROUP BY para consolidar as métricas por produto e categoria, e ORDER BY DESC para ranquear os maiores faturamentos no topo. 

SELECT 
    Produto, 
    Categoria, 
    SUM(Quantidade * Preço) AS Valor_Total_Vendas [cite: 40]
FROM 
    vendas
GROUP BY 
    Produto, 
    Categoria
ORDER BY 
    Valor_Total_Vendas DESC; [cite: 41]

-- Tarefa 2: Identificar os produtos que venderam menos no mês de junho de 2023. [cite: 42]
-- Lógica: Assumindo erro de digitação no ano de "2024" para se alinhar aos dados gerados em "2023", filtramos as transações de junho na cláusula WHERE. Agrupamos os dados por produto e ordenamos as vendas de forma crescente (ASC) com limite de 3 registros para destacar os piores desempenhos. 

SELECT
    Produto, 
    SUM(Quantidade) AS Total_Itens_Vendidos,
    SUM(Quantidade * Preço) AS Valor_Total_Vendas
FROM 
    vendas
WHERE 
    Data >= '2023-06-01' AND Data <= '2023-06-30' [cite: 42]
GROUP BY 
    Produto
ORDER BY 
    Valor_Total_Vendas ASC
LIMIT 3;