import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

anos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
df_total = pd.DataFrame()

for ano in anos:
    try:
        df = pd.read_csv(f'focos_br_todos-sats_{ano}.csv', usecols=[
            'numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp'
        ])
        df_total = pd.concat([df_total, df], ignore_index=True)
    except Exception as e:
        print(f"Erro ao carregar {ano}: {e}")

# Limpa valores ausentes
df_total = df_total.dropna()

# Matriz de correlação
correlacoes = df_total.corr()

# Plot
plt.figure(figsize=(8, 6))
sns.heatmap(correlacoes, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlação entre Fatores Ambientais e Risco de Fogo')
plt.tight_layout()
plt.savefig('matriz_de_correlacao.pdf')
plt.close()
