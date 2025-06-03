import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

# Dicionário de conversão de estado para sigla
estado_para_sigla = {
    'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPÁ': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA',
    'CEARÁ': 'CE', 'DISTRITO FEDERAL': 'DF', 'ESPÍRITO SANTO': 'ES', 'GOIÁS': 'GO',
    'MARANHÃO': 'MA', 'MATO GROSSO': 'MT', 'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG',
    'PARÁ': 'PA', 'PARAÍBA': 'PB', 'PARANÁ': 'PR', 'PERNAMBUCO': 'PE', 'PIAUÍ': 'PI',
    'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN', 'RIO GRANDE DO SUL': 'RS',
    'RONDÔNIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SÃO PAULO': 'SP',
    'SERGIPE': 'SE', 'TOCANTINS': 'TO'
}

# Caminho do arquivo
arquivo_csv = 'data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv'
if not os.path.isfile(arquivo_csv):
    print(f"Arquivo não encontrado: {arquivo_csv}")
    exit()

# Leitura e pré-processamento dos dados
df = pd.read_csv(arquivo_csv, sep=';')
df.columns = df.columns.str.strip().str.lower()
df['uf'] = df['uf'].str.upper()
df['uf_sigla'] = df['uf'].map(estado_para_sigla).fillna(df['uf'])
df['focuses'] = pd.to_numeric(df['focuses'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], format='%Y/%m', errors='coerce')

# Filtra focos relacionados a desmatamento
desmatamento = df[df['class'].str.contains('desmatamento', case=False)]

# Agrupamento e soma dos focos
total_focos = df.groupby('uf_sigla')['focuses'].sum().reset_index(name='Total de Focos')
focos_desmat = desmatamento.groupby('uf_sigla')['focuses'].sum().reset_index(name='Focos em Desmatamento')

# Combinação dos dados
comparativo = pd.merge(total_focos, focos_desmat, on='uf_sigla', how='left').fillna(0)

# Correlação de Pearson
correlacao, p_valor = pearsonr(comparativo['Total de Focos'], comparativo['Focos em Desmatamento'])

# Gráfico de dispersão com linha de regressão
plt.figure(figsize=(10, 6))
sns.regplot(
    data=comparativo,
    x='Total de Focos',
    y='Focos em Desmatamento',
    scatter_kws={'s': 80, 'alpha': 0.6},
    line_kws={'color': 'red'}
)
plt.title(f'Correlação entre Focos Totais e em Desmatamento (Pearson = {correlacao:.2f})')
plt.xlabel('Total de Focos de Incêndio')
plt.ylabel('Focos em Áreas de Desmatamento')
plt.grid(True)
plt.annotate(
    f'Correlação Pearson: {correlacao:.2f}\nValor-p: {p_valor:.4f}',
    xy=(0.65, 0.1), xycoords='axes fraction',
    bbox=dict(boxstyle="round", fc="white", ec="gray")
)
plt.tight_layout()
plt.savefig('graficos/Correlação entre Focos Totais e em Desmatamento.png')
plt.close()
