import pandas as pd
import matplotlib.pyplot as plt
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

def calcular_ocorrencias_por_ano(anos):
    ocorrencias = []

    for ano in anos:
        try:
            df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv',usecols=['data_pas'])
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
    plt.savefig('graficos/Variacao_percentual_anual.png')
    plt.close()

# Chamar a função
variacao_percentual(anos)
