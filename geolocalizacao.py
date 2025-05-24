import pandas as pd
import matplotlib.pyplot as plt
import gdown
import os
from pathlib import Path

# Crie a pasta de saída, se não existir
os.makedirs("data", exist_ok=True)

# Lista de arquivos: (ID do Google Drive, nome de saída)
arquivos = [
    ("1dHDGXDjHbbPe6QE6QDiuy8VwtP7XMFPP", "focos_br_todos-sats_2024.csv"),
    ("15Nik8kNDKH-hpAHk26UROH9vxTGJXhBD", "focos_br_todos-sats_2023.csv"),
    ("1U38lVunPdtpcaQ8IVFQlN7LWLhdSPETx", "focos_br_todos-sats_2022.csv"),
    ("1CUwf5L3W7L2TtQwX55bzLfkhbYJq7f00", "focos_br_todos-sats_2021.csv"),
]

# Baixar arquivos se não existirem
for file_id, filename in arquivos:
    output = f"data/{filename}"
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

anos = [2021, 2022, 2023, 2024] 

# Carregar e concatenar os dados dos anos em um único DataFrame
frames = []
for ano in anos:
    try:
        df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv', usecols=['data_pas', 'latitude', 'longitude'])
        df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
        df = df.dropna(subset=['data_pas', 'latitude', 'longitude'])
        frames.append(df)
    except Exception as e:
        print(f"Erro ao carregar dados do ano {ano}: {e}")

if len(frames) == 0:
    raise ValueError("Nenhum dado carregado. Verifique os arquivos CSV.")

# Concatenar todos os dados
focos_df = pd.concat(frames, ignore_index=True)

# Amostragem para não sobrecarregar o gráfico
if len(focos_df) > 20000:
    focos_df = focos_df.sample(20000, random_state=42)

# Visualização de todos os anos
plt.figure(figsize=(14, 10))
plt.scatter(focos_df['longitude'], focos_df['latitude'], alpha=0.5, c='red', s=10)
plt.xlim(-75, -35)
plt.ylim(-35, 5)
plt.title('Distribuição Geográfica dos Focos de Incêndio (2021-2024)', fontsize=16)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('geolocalizacao_todos_anos.pdf')
plt.show()
