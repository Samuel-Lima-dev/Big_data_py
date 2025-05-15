import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

anos = (2018, 2019, 2020, 2021, 2022, 2023, 2024)  

def carregar_e_tratar_dados(anos):
    anos = anos
    # Carregar os dados de todos os arquivos CSV (2018-2024)
    all_data = pd.concat([pd.read_csv(f'focos_br_todos-sats_{ano}.csv') for ano in anos], ignore_index=True)

    # Remover duplicatas com base na coluna 'data_pas'
    all_data = all_data.drop_duplicates(subset=['data_pas'])

    # Converter 'data_pas' para o formato datetime
    all_data['data_pas'] = pd.to_datetime(all_data['data_pas'])

    # Tratar valores ausentes e negativos em 'numero_dias_sem_chuva'
    all_data['numero_dias_sem_chuva'] = all_data['numero_dias_sem_chuva'].fillna(0)

    # Remover valores negativos de 'numero_dias_sem_chuva'
    all_data = all_data[all_data['numero_dias_sem_chuva'] >= 0]

    # Converter 'numero_dias_sem_chuva' para int
    all_data['numero_dias_sem_chuva'] = all_data['numero_dias_sem_chuva'].astype(int)

    # Preencher valores NaN na coluna 'frp' (poder radiativo do fogo) com 0
    all_data['frp'] = all_data['frp'].fillna(0)

    return all_data

# Variável que contém os dados tratados
all_data = carregar_e_tratar_dados(anos)


def ocorrencias_por_ano(all_data):
    # Análise Temporal: Variação Anual
    ocorrencias_por_ano = all_data.groupby(all_data['data_pas'].dt.year).size()
    plt.figure(figsize=(12, 6))
    ocorrencias_por_ano.plot(kind='bar', color='skyblue')
    plt.title('Ocorrências de Incêndios por Ano (2018-2024)')
    plt.xlabel('Ano')
    plt.ylabel('Número de Ocorrências')

    #Salvar resultado em um pdf
    plt.savefig('grafico_ocorrencias_por_ano.pdf', format='pdf')

ocorrencias_por_ano(all_data)