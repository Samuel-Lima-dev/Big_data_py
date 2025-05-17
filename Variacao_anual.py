import pandas as pd
import matplotlib.pyplot as plt

anos = (2018, 2019, 2020, 2021, 2022, 2023, 2024)

def contar_ocorrencias_por_ano(anos):
    ocorrencias_por_ano = {}

    for ano in anos:
        try:
            # Carrega apenas a coluna de data (mais leve)
            df = pd.read_csv(f'focos_br_todos-sats_{ano}.csv', usecols=['data_pas'])
            df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
            df = df.drop_duplicates(subset='data_pas')  # remove duplicadas
            ocorrencias_por_ano[ano] = df.shape[0]  # conta linhas válidas
        except Exception as e:
            print(f"Erro ao processar {ano}: {e}")
            ocorrencias_por_ano[ano] = 0

    return ocorrencias_por_ano

def gerar_grafico_barras(ocorrencias_dict):
    plt.figure(figsize=(12, 6))
    plt.bar(ocorrencias_dict.keys(), ocorrencias_dict.values(), color='skyblue')
    plt.title('Ocorrências de Incêndios por Ano (2018-2024)')
    plt.xlabel('Ano')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(list(ocorrencias_dict.keys()))
    for ano, qtd in ocorrencias_dict.items():
        plt.text(ano, qtd + 100, str(qtd), ha='center', va='bottom')  # rótulo nas barras
    plt.tight_layout()
    plt.savefig('Variacao_anual.pdf', format='pdf')
    plt.close()

# Executa tudo:
ocorrencias = contar_ocorrencias_por_ano(anos)
gerar_grafico_barras(ocorrencias)
