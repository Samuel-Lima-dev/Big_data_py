import pandas as pd
import matplotlib.pyplot as plt

anos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

def calcular_ocorrencias_por_ano(anos):
    ocorrencias = []

    for ano in anos:
        try:
            df = pd.read_csv(f'focos_br_todos-sats_{ano}.csv', usecols=['data_pas'])
            df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
            df = df.drop_duplicates(subset='data_pas')
            ocorrencias.append({'ano': ano, 'ocorrencias': len(df)})
        except Exception as e:
            ocorrencias.append({'ano': ano, 'ocorrencias': 0})

    return pd.DataFrame(ocorrencias)

def variacao_percentual(anos):
    df_ocorrencias = calcular_ocorrencias_por_ano(anos)
    df_ocorrencias['variacao_percentual'] = df_ocorrencias['ocorrencias'].pct_change() * 100
    df_ocorrencias['variacao_percentual'] = df_ocorrencias['variacao_percentual'].fillna(0)

    # Gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_ocorrencias['ano'], df_ocorrencias['variacao_percentual'], marker='o', color='green')
    plt.xticks(df_ocorrencias['ano'])
    plt.title('Variação Percentual das Queimadas por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Variação Percentual (%)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Variacao_percentual_anual.pdf', format='pdf')
    plt.close()

# Chamar a função
variacao_percentual(anos)
