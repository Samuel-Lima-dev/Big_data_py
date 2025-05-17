import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import os

# Crie a pasta de saída, se ainda não existir
os.makedirs("data", exist_ok=True)

# Lista de arquivos: (ID do Google Drive, nome de saída)
arquivos = [
    ("1dHDGXDjHbbPe6QE6QDiuy8VwtP7XMFPP", "focos_br_todos-sats_2024.csv"),
    ("15Nik8kNDKH-hpAHk26UROH9vxTGJXhBD", "focos_br_todos-sats_2023.csv"),
    ("1U38lVunPdtpcaQ8IVFQlN7LWLhdSPETx", "focos_br_todos-sats_2022.csv"),
    ("1CUwf5L3W7L2TtQwX55bzLfkhbYJq7f00", "focos_br_todos-sats_2021.csv"),

]

# Loop para verificar e baixar apenas os arquivos que ainda não existem
for file_id, filename in arquivos:
    output = f"data/{filename}"
    if os.path.exists(output):
        print(f"{filename} já existe. Pulando download.")
    else:
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Baixando {filename}...")
        gdown.download(url, output, quiet=False)

anos = [2021, 2022, 2023, 2024]
df_total = pd.DataFrame()

for ano in anos:
    try:
        df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv',usecols=[
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
