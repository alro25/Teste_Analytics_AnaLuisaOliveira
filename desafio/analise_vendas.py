"""
Teste de Analytics - Quod
Parte 1: Limpeza, Análise de Dados de Vendas e Visualização
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use("Agg") # Evita erros de interface ao gerar gráficos no terminal

# ── Reprodutibilidade ──────────────────────────────────────────────────────────
np.random.seed(42)

# ── 1. Simulação do Dataset com Sazonalidade (2023) ────────────────────────────
NUM_REGISTROS = 600 # Volume suficiente para criar tendências claras [cite: 22]

produtos_categorias = {
    "Notebook":      "Eletrônicos", "Smartphone":    "Eletrônicos", "Tablet":        "Eletrônicos",
    "Cadeira Gamer": "Móveis",      "Mesa Escritório":"Móveis",     "Headset":       "Periféricos",
    "Teclado":       "Periféricos", "Mouse":         "Periféricos", "Monitor":       "Eletrônicos",
    "Impressora":    "Periféricos",
}

precos_base = {
    "Notebook": 3500.0, "Smartphone": 2000.0, "Tablet": 1500.0, "Cadeira Gamer": 1200.0, 
    "Mesa Escritório": 800.0, "Headset": 250.0, "Teclado": 150.0, "Mouse": 80.0, 
    "Monitor": 900.0, "Impressora": 600.0
}
produtos  = list(produtos_categorias.keys())

# Datas cobrindo apenas 2023, conforme exigência do teste 
dias_disponiveis = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
datas_sorteadas = np.random.choice(dias_disponiveis, NUM_REGISTROS)

df = pd.DataFrame({"Data": datas_sorteadas})
df["Mes"] = df["Data"].dt.month

def escolher_produto_sazonal(mes):
    # Picos sazonais focados em eventos de varejo
    if mes in [1, 3, 11, 12]:
        pesos = [0.6 if p == "Smartphone" else 0.4/(len(produtos)-1) for p in produtos]
        return np.random.choice(produtos, p=pesos)
    else:
        return np.random.choice(produtos)

def gerar_quantidade_sazonal(mes, produto):
    base = np.random.randint(1, 6) 
    if mes in [1, 3, 11, 12] and produto == 'Smartphone':
        return base + np.random.randint(10, 30) 
    return base

df["Produto"] = df["Mes"].apply(escolher_produto_sazonal)
df["Categoria"] = df["Produto"].map(produtos_categorias)
df["Quantidade"] = df.apply(lambda row: gerar_quantidade_sazonal(row["Mes"], row["Produto"]), axis=1)

df["Preço"] = df["Produto"].map(precos_base) * np.random.uniform(0.9, 1.1, size=NUM_REGISTROS)
df["Preço"] = np.round(df["Preço"], 2)

df["ID"] = range(1, NUM_REGISTROS + 1)
df = df[["ID", "Data", "Produto", "Categoria", "Quantidade", "Preço"]] 

# ── 2. Imperfeições e 3. Limpeza ───────────────────────────────────────────────
# Inserindo dados faltantes propositais 
for col in ["Quantidade", "Preço"]:
    idx = np.random.choice(df.index, size=15, replace=False)
    df.loc[idx, col] = np.nan

# Inserindo duplicatas propositais [cite: 26]
df = pd.concat([df, df.iloc[[2, 7, 15]]], ignore_index=True) 
df["Data"] = df["Data"].astype(str) 

# Limpeza e conversão de tipos 
df["Data"]       = pd.to_datetime(df["Data"])
df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
df["Preço"]      = pd.to_numeric(df["Preço"], errors="coerce")
df = df.drop_duplicates()

# Tratamento de nulos usando medianas 
df["Quantidade"] = df["Quantidade"].fillna(df["Quantidade"].median()).astype(int)
df["Preço"] = df.groupby("Produto")["Preço"].transform(lambda x: x.fillna(x.median()))
df["Preço"] = df["Preço"].fillna(df["Preço"].median())

# ── 4. Análises e Exportação ───────────────────────────────────────────────────
df["Total_Venda"] = df["Quantidade"] * df["Preço"]
df.to_csv("data_clean.csv", index=False)
print("✅ Arquivo 'data_clean.csv' salvo com sucesso.")

# Identificando o produto com maior número de vendas totais [cite: 30]
vendas_por_produto = df.groupby('Produto')['Total_Venda'].sum().reset_index()
produto_top = vendas_por_produto.loc[vendas_por_produto['Total_Venda'].idxmax()]
print(f"🏆 Produto com maior total de vendas: {produto_top['Produto']} (R$ {produto_top['Total_Venda']:,.2f})") 

# ── 5. Gráfico de Tendência Mensal ─────────────────────────────────────────────
df["Mes_Ano"] = df["Data"].dt.to_period("M")
vendas_mensais = df.groupby("Mes_Ano")["Total_Venda"].sum().reset_index()
vendas_mensais["Mes_dt"] = vendas_mensais["Mes_Ano"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(vendas_mensais["Mes_dt"], vendas_mensais["Total_Venda"], marker="o", linewidth=2.5, color="#2563EB")

# Destacando insights no gráfico [cite: 35]
eventos = {1: "Férias/Ano Novo", 3: "Dia do Consumidor", 11: "Black Friday", 12: "Natal"}
for idx, row in vendas_mensais.iterrows():
    mes_num = row['Mes_Ano'].month
    if mes_num in eventos:
        ax.annotate(f"{eventos[mes_num]}",
                    xy=(row["Mes_dt"], row["Total_Venda"]),
                    xytext=(0, 15), textcoords="offset points",
                    ha="center", fontsize=9, color="#DC2626", fontweight='bold',
                    arrowprops=dict(arrowstyle="->", color="#DC2626"))

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Tendência de Vendas Mensais (2023)", fontsize=14, fontweight="bold")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("tendencia_vendas.png", dpi=150)
print("✅ Gráfico salvo: tendencia_vendas.png")