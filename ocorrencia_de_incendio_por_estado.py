import pandas as pd
import matplotlib.pyplot as plt

anos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Dicionário acumulando o total de ocorrências por estado
ocorrencias_estado = {}

for ano in anos:
    try:
        df = pd.read_csv(f'focos_br_todos-sats_{ano}.csv', usecols=['estado'])
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
