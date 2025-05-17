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

# Dicionário acumulando o total de ocorrências por estado
ocorrencias_estado = {}

for ano in anos:
    try:
        df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv',usecols=['estado'])
        contagem = df['estado'].value_counts()
        for estado, qtd in contagem.items():
            ocorrencias_estado[estado] = ocorrencias_estado.get(estado, 0) + qtd
    except Exception as e:
        print(f"Erro no ano {ano}: {e}")

# Transforma em DataFrame
df_ocorrencias = pd.DataFrame(list(ocorrencias_estado.items()), columns=['Estado', 'Ocorrências'])

# Ordena pelo total
df_ocorrencias = df_ocorrencias.sort_values(by='Ocorrências', ascending=False)

# Plotando o gráfico
plt.figure(figsize=(14, 7))
plt.bar(df_ocorrencias['Estado'], df_ocorrencias['Ocorrências'], color='dodgerblue')
plt.title('Número de Ocorrências de Incêndios por Estado')
plt.xlabel('Estado')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=60, ha='right')  # Rota os rótulos dos estados para melhor visualização
plt.tight_layout()
plt.savefig('Ocorrencias_incendio_por_estado.pdf')
plt.close()
