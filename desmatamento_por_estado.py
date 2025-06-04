import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats  # Nova importação necessária
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

# Dicionário de nomes de estados para siglas
estado_para_sigla = {
    'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPÁ': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA',
    'CEARÁ': 'CE', 'DISTRITO FEDERAL': 'DF', 'ESPÍRITO SANTO': 'ES', 'GOIÁS': 'GO',
    'MARANHÃO': 'MA', 'MATO GROSSO': 'MT', 'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG',
    'PARÁ': 'PA', 'PARAÍBA': 'PB', 'PARANÁ': 'PR', 'PERNAMBUCO': 'PE', 'PIAUÍ': 'PI',
    'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN', 'RIO GRANDE DO SUL': 'RS',
    'RONDÔNIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SÃO PAULO': 'SP',
    'SERGIPE': 'SE', 'TOCANTINS': 'TO'
}
sigla_para_estado = {v: k.title() for k, v in estado_para_sigla.items()}

# 1. Leitura do arquivo CSV com o caminho correto
caminho_arquivo = 'data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv'
if not os.path.isfile(caminho_arquivo):
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()
df = pd.read_csv(caminho_arquivo, sep=';')

# 2. Padronização dos nomes das colunas
df.columns = [col.strip().lower() for col in df.columns]

# 3. Criar coluna auxiliar para nomes completos dos estados
uf_upper = df['uf'].str.upper()
df['estado_completo'] = uf_upper.map(sigla_para_estado).fillna(df['uf'])

# 4. Criar coluna de siglas ANTES de criar o DataFrame desmatamento
df['uf_sigla'] = uf_upper.map(estado_para_sigla).fillna(uf_upper)

# 5. Conversão dos tipos de dados e extração de ano/mês
df['focuses'] = pd.to_numeric(df['focuses'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], format='%Y/%m')
df['ano'] = df['date'].dt.year
df['mes'] = df['date'].dt.month

# Criar DataFrame desmatamento após criação da coluna uf_sigla
desmatamento = df[df['class'].str.contains('desmatamento', case=False)]


# 6. Focos de incêndio por estado x áreas de desmatamento (barras agrupadas) - SIGLAS
focos_total_estado = df.groupby('uf_sigla')['focuses'].sum().reset_index()
focos_desmatamento_estado = desmatamento.groupby('uf_sigla')['focuses'].sum().reset_index()
focos_total_estado = focos_total_estado.rename(columns={'focuses':'Total de Focos'})
focos_desmatamento_estado = focos_desmatamento_estado.rename(columns={'focuses':'Focos em Desmatamento'})

comparativo = pd.merge(focos_total_estado, focos_desmatamento_estado, on='uf_sigla', how='left').fillna(0)
comparativo = comparativo.sort_values('Total de Focos', ascending=False)
comparativo_melt = comparativo.melt(id_vars='uf_sigla', value_vars=['Total de Focos', 'Focos em Desmatamento'],
                                    var_name='Tipo', value_name='Focos')

plt.figure(figsize=(14, 7))
sns.barplot(data=comparativo_melt, x='uf_sigla', y='Focos', hue='Tipo')
plt.title('Focos de Incêndio por Estado (Sigla) x Áreas de Desmatamento (2021-2024)')
plt.xlabel('Estado (Sigla)')
plt.ylabel('Quantidade de Focos')
plt.legend(title='Tipo')
plt.tight_layout()
plt.savefig('graficos/Focos de Incêndio por Estado (Sigla) x Áreas de Desmatamento.png')
plt.close()
