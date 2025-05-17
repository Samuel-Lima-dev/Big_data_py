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

# Dicionário: {estado: {ano: ocorrências}}
dados = {}

for ano in anos:
    try:
        df = pd.read_csv(f'data/focos_br_todos-sats_{ano}.csv', usecols=['estado'])
        contagem = df['estado'].value_counts()
        for estado, qtd in contagem.items():
            if estado not in dados:
                dados[estado] = {}
            dados[estado][ano] = qtd
    except Exception as e:
        print(f"Erro no ano {ano}: {e}")

# Transforma o dicionário em DataFrame
df_estados = pd.DataFrame(dados).fillna(0).astype(int)
df_estados = df_estados.T  # Estados nas linhas, anos nas colunas

# Soma total de ocorrências por estado para selecionar os top 10
top_10_estados = df_estados.sum(axis=1).sort_values(ascending=False).head(10).index
df_top10 = df_estados.loc[top_10_estados]

# Transpõe para ter os anos no eixo X e os estados como colunas
df_plot = df_top10.T

# Plotando o gráfico
plt.figure(figsize=(12, 7))
for estado in df_plot.columns:
    plt.plot(df_plot.index, df_plot[estado], marker='o', label=estado)

plt.title('Top 10 Estados com Mais Ocorrências de Incêndios por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Ocorrências')
plt.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('Top10_ocorrencias_por_estado_ano.pdf')
plt.close()
