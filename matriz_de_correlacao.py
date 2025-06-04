import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import gdown

# Crie a pasta de saída, se ainda não existir
os.makedirs("data", exist_ok=True)

# ID do Google Drive e nome do arquivo de saída
file_id = "1gZXQqDWEJ00Goo91KwIOvRg66Hl5SXuv"
filename = "dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv"
output = f"data/{filename}"

# Verifica se o arquivo já existe antes de baixar
if os.path.exists(output):
    print(f"{filename} já existe. Pulando download.")
else:
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Baixando {filename}...")
    gdown.download(url, output, quiet=False)

# Leitura dos arquivos
# Incêndios e desmatamento (mesmo arquivo)
incendios = pd.read_csv("data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv", sep=";")
desmatamento = pd.read_csv("data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv", sep=";")

# Clima: concatenar arquivos de 2021 a 2024
lista_df = []
for ano in range(2021, 2025):
    caminho_arquivo = f"data/focos_br_todos-sats_{ano}.csv"
    if os.path.isfile(caminho_arquivo):
        df_temp = pd.read_csv(caminho_arquivo)
        df_temp.columns = df_temp.columns.str.strip()
        lista_df.append(df_temp)
    else:
        print(f"Aviso: Arquivo {caminho_arquivo} não encontrado.")
clima = pd.concat(lista_df, ignore_index=True)

#  2. Limpeza de colunas
for df in [incendios, clima, desmatamento]:
    df.columns = df.columns.str.strip()

# 3. Datas e criação de 'ano_mes'
clima['data_pas'] = pd.to_datetime(clima['data_pas'], errors='coerce')
clima['ano_mes'] = clima['data_pas'].dt.to_period('M').astype(str)

incendios['date'] = pd.to_datetime(incendios['date'], errors='coerce')
incendios['ano_mes'] = incendios['date'].dt.to_period('M').astype(str)

desmatamento['date'] = pd.to_datetime(desmatamento['date'], errors='coerce')
desmatamento['ano_mes'] = desmatamento['date'].dt.to_period('M').astype(str)

# 4. Agregação

# Incêndios por estado e mês
incendios_agg = incendios.groupby(['uf', 'ano_mes'])['focuses'].sum().reset_index()
incendios_agg.rename(columns={'uf': 'estado'}, inplace=True)

# Clima por estado e mês
clima_agg = clima.groupby(['estado', 'ano_mes']).agg({
    'numero_dias_sem_chuva': 'mean',
    'precipitacao': 'mean',
    'risco_fogo': 'mean'
}).reset_index()

# Desmatamento por estado, mês e classe
desmatamento_agg = desmatamento.groupby(['uf', 'ano_mes', 'class'])['focuses'].sum().reset_index()
desmatamento_pivot = desmatamento_agg.pivot_table(
    index=['uf', 'ano_mes'],
    columns='class',
    values='focuses',
    fill_value=0
).reset_index()
desmatamento_pivot.rename(columns={'uf': 'estado'}, inplace=True)

# 5. Unir todos os dados
df = pd.merge(incendios_agg, clima_agg, on=['estado', 'ano_mes'], how='inner')
df = pd.merge(df, desmatamento_pivot, on=['estado', 'ano_mes'], how='left')
df = df.dropna()  # Remove registros com valores nulos

# 6. Heatmap com variáveis selecionadas
variaveis_relevantes = [
    'focuses',
    'Fogo em áreas de desmatamento consolidado',
    'Fogo em áreas de desmatamento recente',
    'Fogo em áreas de vegetação nativa',
    'Fogo em outras áreas',
    'numero_dias_sem_chuva',
    'precipitacao',
    'risco_fogo'
]

df_corr_relevantes = df[variaveis_relevantes].corr(method='pearson')

plt.figure(figsize=(10, 8))
sns.heatmap(df_corr_relevantes, annot=True, cmap='coolwarm', fmt=".2f", center=0)
plt.title('Correlação (Pearson) entre Focos de Incêndio, Clima e Uso da Terra')
plt.tight_layout()
plt.savefig('graficos/Correlação entre Focos de Incêndio, Clima e Uso da Terra.png')
plt.close()
