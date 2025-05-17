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

def ocorrencias_por_mes(anos):
    # Inicializa um contador mensal
    ocorrencias_mensais = {mes: 0 for mes in range(1, 13)}

    for ano in anos:
        try:
            df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv',usecols=['data_pas'])
            df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')
            df = df.dropna(subset=['data_pas'])  # remove datas inválidas
            df['mes'] = df['data_pas'].dt.month
            contagem = df.groupby('mes').size()
            for mes, valor in contagem.items():
                ocorrencias_mensais[mes] += valor
        except Exception as e:
            print(f"Erro em {ano}: {e}")

    # Criação do gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(list(ocorrencias_mensais.keys()), list(ocorrencias_mensais.values()), 
             marker='o', color='coral')
    plt.title('Ocorrências de Incêndios por Mês (Soma de Todos os Anos)')
    plt.xlabel('Mês')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Ocorrencia_por_mes.pdf', format='pdf')
    plt.close()

# Executar a função
ocorrencias_por_mes(anos)
