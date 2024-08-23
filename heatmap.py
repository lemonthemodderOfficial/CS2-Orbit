import seaborn as sns
import matplotlib.pyplot as plt
from demoparser2 import DemoParser

parser = DemoParser("match1.dem")
event_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
ticks_df = parser.parse_ticks(["X", "Y"])
# Exemplo: Suponha que você queira criar um heatmap do número de mortes por jogador (assumindo que 'player_death' retorna isso)
# Vamos contar o número de mortes de cada jogador para cada round

# Primeiro, vamos criar um pivot table que mostre o número de mortes por jogador em cada round
heatmap_data = event_df.pivot_table(
    index='total_rounds_played',  # Eixo Y: número total de rodadas jogadas
    columns='attacker_name',      # Eixo X: nome do atacante (jogador que causou a morte)
    values='user_name',         # Valor: nome da vítima (ou qualquer outra métrica relevante)
    aggfunc='count',              # Função de agregação: contagem
    fill_value=0                  # Preenchendo valores nulos com 0
)

# Agora vamos plotar o heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=.5)
plt.title('Heatmap das Mortes por Jogador')
plt.xlabel('Atacante')
plt.ylabel('Rodada')
plt.show()

# Carregar a imagem de fundo
#img = mpimg.imread('background.png')

# Criar a figura
fig, ax = plt.subplots(figsize=(12, 8))

# Mostrar a imagem de fundo
#ax.imshow(img, aspect='auto', extent=[0, 1, 0, 1], alpha=0.5)

# Adicionar título e rótulos aos eixos
plt.title('Heatmap das Mortes por Jogador com Imagem de Fundo')
plt.xlabel('Atacante')
plt.ylabel('Rodada')

# Mostrar o gráfico
plt.show()
