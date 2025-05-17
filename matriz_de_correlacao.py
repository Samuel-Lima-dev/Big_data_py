import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def carregar_e_tratar_dados(anos):
    # Carrega e concatena os arquivos CSV
    df = pd.concat([pd.read_csv(f'focos_br_todos-sats_{ano}.csv') for ano in anos], ignore_index=True)
    
    # Converte a coluna de data
    df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
    df = df.dropna(subset=['data_pas'])

    return df

def gerar_matriz_correlacao(df):
    ocorrencias = df.groupby(df['data_pas'].dt.year).size().reset_index(name='ocorrencias')
    ocorrencias.rename(columns={'data_pas': 'ano'}, inplace=True)
    ocorrencias['variacao_percentual'] = ocorrencias['ocorrencias'].pct_change() * 100
    ocorrencias['variacao_percentual'] = ocorrencias['variacao_percentual'].fillna(0)

    correlacao = ocorrencias.corr(numeric_only=True)

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Matriz de Correlação - Queimadas por Ano')
    plt.tight_layout()
    plt.savefig('matriz_correlacao_queimadas.pdf')
    plt.close()

# Execução
anos = range(2018, 2025)
df = carregar_e_tratar_dados(anos)
gerar_matriz_correlacao(df)
