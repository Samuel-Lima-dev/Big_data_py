import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import gdown
import os
from scipy.stats import pearsonr

# Cria a pasta data se não existir
os.makedirs("data", exist_ok=True)

# IDs dos arquivos CSV no Google Drive
csv_arquivos = [
    ("1L0JxbK8tNmx0IUcWdgpL4MVsYKMio1Ku", "focos_br_todos-sats_2021.csv"),
    ("1lXGaKuj0N1YGT0rivQO_gOzZF4L89opT", "focos_br_todos-sats_2022.csv"),
    ("1qZKbnUqC7d2TFjlr0xoDkR9WibUy8VJH", "focos_br_todos-sats_2023.csv"),
    ("1AcOXYotLjrxMVMt8C41uBo82cBRwg0DJ", "focos_br_todos-sats_2024.csv")
]

# IDs dos arquivos XLSX no Google Sheets
xlsx_arquivos = [
    ("1T0aF1o4_BdL5iBr4NwidBlfAZq-Llffh", "IIS3_IIS6_2021.xlsx"),
    ("1Go1a8MnjNe80lBUgureo1Eqohu7OWWwd", "IIS3_IIS6_2022.xlsx"),
    ("1YwZPMgNR-CdJV9mNeoFDce35RUstvbKG", "IIS3_IIS6_2023.xlsx"),
    ("1NbEGpRw0fYL0kZ4Cw20HcsixL3JI713_", "IIS3_IIS6_2024.xlsx")
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

# Função para baixar arquivos XLSX do Google Sheets exportando para Excel
def baixar_arquivos_xlsx():
    for file_id, filename in xlsx_arquivos:
        output = f"data/{filename}"
        if os.path.exists(output):
            print(f"{filename} já existe. Pulando download.")
        else:
            url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
            print(f"Baixando {filename}...")
            r = requests.get(url)
            with open(output, 'wb') as f:
                f.write(r.content)

# Baixar todos os arquivos necessários
baixar_arquivos_csv()
baixar_arquivos_xlsx()

# Dicionário de conversão de nomes completos para siglas dos estados
estado_para_uf = {
    "ACRE": "AC", "ALAGOAS": "AL", "AMAPÁ": "AP", "AMAPA": "AP", "AMAZONAS": "AM",
    "BAHIA": "BA", "CEARÁ": "CE", "CEARA": "CE", "DISTRITO FEDERAL": "DF",
    "ESPÍRITO SANTO": "ES", "ESPIRITO SANTO": "ES", "GOIÁS": "GO", "GOIAS": "GO",
    "MARANHÃO": "MA", "MARANHAO": "MA", "MATO GROSSO": "MT", "MATO GROSSO DO SUL": "MS",
    "MINAS GERAIS": "MG", "PARÁ": "PA", "PARA": "PA", "PARAÍBA": "PB", "PARAIBA": "PB",
    "PARANÁ": "PR", "PARANA": "PR", "PERNAMBUCO": "PE", "PIAUÍ": "PI", "PIAUI": "PI",
    "RIO DE JANEIRO": "RJ", "RIO GRANDE DO NORTE": "RN", "RIO GRANDE DO SUL": "RS",
    "RONDÔNIA": "RO", "RONDONIA": "RO", "RORAIMA": "RR", "SANTA CATARINA": "SC",
    "SÃO PAULO": "SP", "SAO PAULO": "SP", "SERGIPE": "SE", "TOCANTINS": "TO"
}
def estado_para_sigla(estado):
    if pd.isnull(estado):
        return ""
    return estado_para_uf.get(str(estado).strip().upper(), "")

# Arquivos de entrada (agora na pasta data)
csv_files = [
    'data/focos_br_todos-sats_2021.csv',
    'data/focos_br_todos-sats_2022.csv',
    'data/focos_br_todos-sats_2023.csv',
    'data/focos_br_todos-sats_2024.csv'
]
xlsx_files = [
    'data/IIS3_IIS6_2021.xlsx',
    'data/IIS3_IIS6_2022.xlsx',
    'data/IIS3_IIS6_2023.xlsx',
    'data/IIS3_IIS6_2024.xlsx'
]

# Leitura dos dados
df_focos = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
df_seca = pd.concat([pd.read_excel(f, sheet_name=0) for f in xlsx_files], ignore_index=True)

# Classes de seca
seca_classes = {6: "Excepcional", 5: "Extrema", 4: "Severa"}
seca_cols = [col for col in df_seca.columns if col.startswith('IIS6_')]
df_seca['seca_max_val'] = df_seca[seca_cols].max(axis=1)
df_seca['classe_seca'] = df_seca['seca_max_val'].map(seca_classes)
df_seca = df_seca[df_seca['classe_seca'].notnull()]

# Conversão dos nomes dos estados para siglas
df_focos['UF'] = df_focos['estado'].apply(estado_para_sigla)

# Obter a região por UF da tabela de seca filtrada
regiao_uf = df_seca[['UF', 'Regiao']].drop_duplicates()
df_focos = pd.merge(df_focos, regiao_uf, on='UF', how='inner')

# Agrupar total de focos por região e bioma
focos_regiao_bioma = df_focos.groupby(['Regiao', 'bioma']).size().reset_index(name='total_focos')

# Calcular índice médio de seca por região
df_seca['seca_media'] = df_seca[seca_cols].mean(axis=1)
seca_regiao = df_seca.groupby('Regiao')['seca_media'].mean().reset_index()

# Pivotar focos para matriz região x bioma
pivot_focos = focos_regiao_bioma.pivot(index='Regiao', columns='bioma', values='total_focos').fillna(0)

# Juntar índice de seca médio (região) com focos por bioma
df_corr = pd.merge(seca_regiao, pivot_focos, on='Regiao', how='inner')

# Correlação de Pearson entre seca_media e cada bioma
for bioma in pivot_focos.columns:
    coef, pval = pearsonr(df_corr['seca_media'], df_corr[bioma])
    plt.figure(figsize=(7,5))
    sns.regplot(x=df_corr['seca_media'], y=df_corr[bioma], scatter_kws={'s':80}, line_kws={'color':'red'})
    plt.xlabel('Índice Médio de Seca (por Região)')
    plt.ylabel(f'Total de Focos de Incêndio ({bioma})')
    plt.title(f'Região: Seca x Focos de Incêndio ({bioma})\nPearson: {coef:.2f} (p={pval:.4f})')
    plt.tight_layout()
    plt.savefig('graficos/Região: Seca x Focos de Incêndio.png')
    plt.close()