import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Leitura do arquivo CSV
caminho_arquivo = 'data/dashboard-fires-month-29-05-2025-19_50_13(com filtro) 2021 - 2024.csv'
if not os.path.isfile(caminho_arquivo):
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit()
df = pd.read_csv(caminho_arquivo, sep=';')

# 2. Padronização dos nomes das colunas
df.columns = [col.strip().lower() for col in df.columns]

# 3. Conversão dos tipos de dados e extração de ano/mês
df['focuses'] = pd.to_numeric(df['focuses'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], format='%Y/%m')
df['ano'] = df['date'].dt.year

# 4. Filtro para anos de interesse
df = df[df['ano'].between(2021, 2024)]

# 5. Mapeamento simplificado de estados para biomas
uf_para_bioma = {
    # Amazônia
    'AMAZONAS': 'Amazônia', 'PARÁ': 'Amazônia', 'RORAIMA': 'Amazônia', 'AMAPÁ': 'Amazônia',
    'ACRE': 'Amazônia', 'RONDÔNIA': 'Amazônia', 'TOCANTINS': 'Cerrado', 'MATO GROSSO': 'Amazônia',
    'MARANHÃO': 'Amazônia',
    # Cerrado
    'GOIÁS': 'Cerrado', 'DISTRITO FEDERAL': 'Cerrado', 'MATO GROSSO DO SUL': 'Cerrado',
    'TOCANTINS': 'Cerrado', 'PIAUÍ': 'Cerrado', 'BAHIA': 'Cerrado', 'MINAS GERAIS': 'Cerrado',
    # Caatinga
    'CEARÁ': 'Caatinga', 'RIO GRANDE DO NORTE': 'Caatinga', 'PARAÍBA': 'Caatinga',
    'PERNAMBUCO': 'Caatinga', 'ALAGOAS': 'Caatinga', 'SERGIPE': 'Caatinga',
    # Mata Atlântica
    'ESPÍRITO SANTO': 'Mata Atlântica', 'RIO DE JANEIRO': 'Mata Atlântica',
    'SÃO PAULO': 'Mata Atlântica', 'PARANÁ': 'Mata Atlântica', 'SANTA CATARINA': 'Mata Atlântica',
    'RIO GRANDE DO SUL': 'Mata Atlântica',
    # Pantanal
    'MATO GROSSO DO SUL': 'Pantanal', 'MATO GROSSO': 'Pantanal',
    # Pampa
    'RIO GRANDE DO SUL': 'Pampa'
}
df['bioma'] = df['uf'].map(lambda x: uf_para_bioma.get(str(x).upper(), 'Outro'))

# 6. Filtrar apenas áreas de desmatamento
mascara_desmatamento = df['class'].str.contains('desmatamento', case=False, na=False)
df_desmatamento = df[mascara_desmatamento].copy()

# 7. Classificar tipo de desmatamento
def tipo_desmatamento(classe):
    if 'consolidado' in classe.lower():
        return 'Consolidado'
    elif 'recente' in classe.lower():
        return 'Recente'
    else:
        return 'Outro'
df_desmatamento['tipo_desmatamento'] = df_desmatamento['class'].apply(tipo_desmatamento)

# 8. Agrupar dados para o gráfico
dados_grafico = df_desmatamento.groupby(['bioma', 'tipo_desmatamento'])['focuses'].sum().reset_index()

# 9. Ordenar biomas pelo total de focos
ordem_biomas = dados_grafico.groupby('bioma')['focuses'].sum().sort_values(ascending=False).index

# 10. Gráfico
plt.figure(figsize=(12, 7))
sns.barplot(
    data=dados_grafico,
    x='bioma', y='focuses', hue='tipo_desmatamento',
    order=ordem_biomas
)
plt.title('Focos de Incêndio por Bioma x Áreas de Desmatamento (2021-2024)')
plt.xlabel('Bioma')
plt.ylabel('Total de Focos em Desmatamento')
plt.legend(title='Tipo de Desmatamento')
plt.tight_layout()
plt.savefig('graficos/Focos de Incêndio por Bioma x Áreas de Desmatamento.png')
plt.close()