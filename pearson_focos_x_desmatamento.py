import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import os
from scipy import stats

# Cria a pasta data se não existir
os.makedirs("data", exist_ok=True)

# Lista de arquivos CSV para download (ID do Google Drive, nome do arquivo)
csv_arquivos = [
    ("1WllWCyc13YsLErZ96I2G4QDupZKhZD7L", "dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv")
]

# Função para baixar arquivos CSV do Google Drive
def baixar_arquivos_csv():
    for file_id, filename in csv_arquivos:
        output = f"data/{filename}"
        if os.path.exists(output):
            print(f"{filename} já existe. Pulando download.")
        else:
            url = f"https://drive.google.com/uc?id={file_id}"
            print(f"Baixando {filename}...")
            gdown.download(url, output, quiet=False)

# Baixar o arquivo necessário
baixar_arquivos_csv()

# Caminho do arquivo baixado
caminho_arquivo = "data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv"

# Leitura do arquivo CSV
if not os.path.isfile(caminho_arquivo):
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()
df = pd.read_csv(caminho_arquivo, sep=';')

# Padronização das colunas
df.columns = [col.strip().lower() for col in df.columns]
df['uf'] = df['uf'].str.upper()
df['focuses'] = pd.to_numeric(df['focuses'], errors='coerce')

# Filtrar áreas de desmatamento
desmatamento = df[df['class'].str.contains('desmatamento', case=False)]

# Agrupar dados
focos_total_estado = df.groupby('uf')['focuses'].sum().reset_index()
focos_desmatamento_estado = desmatamento.groupby('uf')['focuses'].sum().reset_index()
comparativo = pd.merge(focos_total_estado, focos_desmatamento_estado, on='uf', how='left').fillna(0)
comparativo = comparativo.rename(columns={'focuses_x':'Total de Focos','focuses_y':'Focos em Desmatamento'})
comparativo = comparativo.sort_values('Total de Focos', ascending=False)

# Correlação de Pearson e gráfico
correlacao, p_value = stats.pearsonr(comparativo['Total de Focos'], comparativo['Focos em Desmatamento'])
plt.figure(figsize=(10, 6))
sns.regplot(data=comparativo, x='Total de Focos', y='Focos em Desmatamento', 
            scatter_kws={'s': 100, 'alpha': 0.5}, line_kws={'color': 'red'})
plt.title(f'Correlação entre Focos Totais e Focos em Desmatamento (Pearson = {correlacao:.2f})')
plt.xlabel('Total de Focos de Incêndio')
plt.ylabel('Focos em Áreas de Desmatamento')
plt.grid(True)
plt.annotate(f'Correlação Pearson: {correlacao:.2f}\nValor-p: {p_value:.4f}', 
             xy=(0.7, 0.1), xycoords='axes fraction',
             bbox=dict(boxstyle="round", fc="white", ec="gray"))
plt.tight_layout()
plt.show()