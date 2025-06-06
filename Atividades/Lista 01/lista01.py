import pandas as pd
import matplotlib.pyplot as plt


# 1) Leitura do CSV com a biblioteca pandas
df = pd.read_csv('estoque.csv')

# 2) Adiciona coluna de valor em estoque e agrupa por produto e calcula o valor por cada tipo de produto
df['Valor_Estoque'] = df['Quantidade'] * df['Preco_Unitario']
preco_total_por_produto = df.groupby(['Produto'])['Valor_Estoque'].sum().reset_index()


# 3) Filtra todos os produtos cujo estoque seja abaixo de 10 e coloca no data frame baixo_estoque
baixo_estoque = df[df['Quantidade'] < 10].copy()


# 4) Exporta os produtos com baixo estoque para um csv
baixo_estoque.to_csv('estoque_baixo.csv', index=False)
# Exporta os valores por produto em planilhas por categoria
with pd.ExcelWriter('valor_total_estoque.xlsx', engine='xlsxwriter') as writer:
    for categoria, grupo in df.groupby('Categoria'):
        grupo_filtrado = grupo[['Data_Atualizacao','Produto', 'Quantidade', 'Preco_Unitario', 'Valor_Estoque']]
        grupo_filtrado.to_excel(writer, sheet_name=categoria[:31], index=False)
print(f"Planilha criada com sucesso")


# 5)  Encontra o produto com maior valor_estoque por categoria
produtos_top = (
    df.loc[df.groupby("Categoria")['Valor_Estoque'].idxmax()]
    [['Categoria', 'Produto', 'Valor_Estoque']]
    .reset_index(drop=True)
)
# print(produtos_top)

# 6) Calcular o valor total do estoque por categoria
valor_total_por_categoria = (
    df.groupby("Categoria")['Valor_Estoque'].sum().sort_values(ascending=False).reset_index().rename(columns={"Valor_Estoque": "Valor_Total_Categoria"})
)

plt.figure(figsize=(10,6))
plt.bar(valor_total_por_categoria['Categoria'], valor_total_por_categoria['Valor_Total_Categoria'], color='skyblue')
plt.title('Valor Total de Estoque por Categoria')
plt.ylabel('Valor Total R$')
plt.xlabel('Categoria')
plt.xticks(rotation = 45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

valor_total_por_categoria.to_csv('Valor_total_por_categoria.csv', index=False)

# 7) Classificar nivel do estoque
def classificar_nivel(quantidade):
    if quantidade < 10:
        return 'Baixo'
    elif 10 < quantidade <= 50:
        return 'Médio'
    else:
        return 'Alto'

df['Nivel_Estoque'] = df['Quantidade'].apply(classificar_nivel)

contagem_niveis = df['Nivel_Estoque'].value_counts().reset_index()
contagem_niveis.columns = ['Nivel_Estoque', 'Quantidade']

print(contagem_niveis)
# Exibe os resultados
# print(maior_por_categoria)
# print(df)
# print(preco_total_por_produto)
# print(baixo_estoque)