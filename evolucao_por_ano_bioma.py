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

def analise_de_queimadas_por_bioma(anos):
    # Lista para armazenar DataFrames de cada ano
    lista_dfs = []

    for ano in anos:
        try:
            df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv', usecols=['bioma'])
            df = df.dropna(subset=['bioma'])  # remove valores nulos
            df['ano'] = ano  # adiciona coluna ano
            lista_dfs.append(df)
        except Exception as e:
            print(f"Erro ao ler {ano}: {e}")

    if not lista_dfs:
        print("Nenhum dado carregado. Verifique os arquivos CSV.")
        return

    # Concatenar todos os DataFrames
    df_completo = pd.concat(lista_dfs, ignore_index=True)

    # Ordenar biomas pela contagem total
    ordem_biomas = df_completo['bioma'].value_counts().index

    # Gráfico com colunas separadas por ano
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df_completo, x='bioma', hue='ano', order=ordem_biomas)
    plt.title('Evolução de focos de incêndio por bioma (2021-2024)')
    plt.ylabel('Quantidade de focos')
    plt.xlabel('Bioma')
    plt.xticks(rotation=30)
    plt.legend(title='Ano')
    plt.tight_layout()
    plt.savefig('evolucao_biomas_anos_2021_-_2024.pdf', format='pdf')
    plt.close()

# Executar a função
analise_de_queimadas_por_bioma(anos)
