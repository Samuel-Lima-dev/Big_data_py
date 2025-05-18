import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
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
    contagem_bioma = Counter()

    for ano in anos:
        try:
            df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv', usecols=['bioma'])
            df = df.dropna(subset=['bioma'])  # remove valores nulos
            contagem_ano = df['bioma'].value_counts().to_dict()
            contagem_bioma.update(contagem_ano)
        except Exception as e:
            print(f"Erro ao ler {ano}: {e}")

    # Converter contagem para DataFrame
    bioma_df = pd.DataFrame.from_dict(contagem_bioma, orient='index', columns=['ocorrencias'])
    bioma_df = bioma_df.sort_values('ocorrencias', ascending=False)

    # Gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x=bioma_df.index, y=bioma_df['ocorrencias'], color='forestgreen')
    plt.title('Número de Ocorrências de Incêndios por Bioma (2021–2024)')
    plt.xlabel('Bioma')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('Ocorrencias_por_bioma.pdf', format='pdf')
    plt.close()

# Executar a função
analise_de_queimadas_por_bioma(anos)
