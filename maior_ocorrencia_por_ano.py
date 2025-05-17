import pandas as pd
import matplotlib.pyplot as plt

anos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Dicionário: {estado: {ano: ocorrências}}
dados = {}

for ano in anos:
    try:
        df = pd.read_csv(f'focos_br_todos-sats_{ano}.csv', usecols=['estado'])
        contagem = df['estado'].value_counts()
        for estado, qtd in contagem.items():
            if estado not in dados:
                dados[estado] = {}
            dados[estado][ano] = qtd
    except Exception as e:
        print(f"Erro no ano {ano}: {e}")

# Transforma o dicionário em DataFrame
df_estados = pd.DataFrame(dados).fillna(0).astype(int)
df_estados = df_estados.T  # Estados nas linhas, anos nas colunas

# Soma total de ocorrências por estado para selecionar os top 10
top_10_estados = df_estados.sum(axis=1).sort_values(ascending=False).head(10).index
df_top10 = df_estados.loc[top_10_estados]

# Transpõe para ter os anos no eixo X e os estados como colunas
df_plot = df_top10.T

# Plotando o gráfico
plt.figure(figsize=(12, 7))
for estado in df_plot.columns:
    plt.plot(df_plot.index, df_plot[estado], marker='o', label=estado)

plt.title('Top 10 Estados com Mais Ocorrências de Incêndios por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Ocorrências')
plt.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('Top10_ocorrencias_por_estado_ano.pdf')
plt.close()
