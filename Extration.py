import pandas as pd
from demoparser2 import DemoParser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

# Continue with your initial code to extract data...
parser = DemoParser("match1.dem")

# Parse bomb plant, defuse, and explode events
planted = parser.parse_event("bomb_planted", player=["X", "Y"])
defused = parser.parse_event("bomb_defused", player=["X", "Y"])
exploded = parser.parse_event("bomb_exploded", player=["X", "Y"])

# Parse all ticks for players X and Y
ticks_df = parser.parse_ticks(["X", "Y"])

# For each bomb plant event, find the ticks until bomb defuse or bomb explode
tick_ranges = []
for _, plant_event in planted.iterrows():
    # Filter the first defuse or explode event after the plant
    defuse_event = defused[defused["tick"] > plant_event["tick"]].head(1)
    explode_event = exploded[exploded["tick"] > plant_event["tick"]].head(1)
    
    if not defuse_event.empty:
        end_tick = defuse_event["tick"].values[0]
    elif not explode_event.empty:
        end_tick = explode_event["tick"].values[0]
    else:
        continue  # If there's no defuse or explode after planting, ignore

    # Filter the ticks between the plant and the final event (defuse or explode)
    tick_range = ticks_df[(ticks_df["tick"] >= plant_event["tick"]) & (ticks_df["tick"] <= end_tick)]
    tick_ranges.append(tick_range)

# Concatenate all resulting DataFrames to get the final result
result_df = pd.concat(tick_ranges)

# Load the map image and flip it horizontally
map_image = mpimg.imread("dust2.webp")
map_image_flipped = np.fliplr(map_image)  # Flip the image along the x-axis

# Filter for the specific player
player_name = "Let isgo" 
player_df = result_df[result_df["name"] == player_name]

# Extract the X and Y coordinates of the ticks for the player
x_coords = player_df["X"].values
y_coords = player_df["Y"].values

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(map_image_flipped, extent=[0, 3060, 0, 3060])  # Adjust to the actual dimensions of the map

# Create a heatmap with seaborn
sns.kdeplot(
    x=x_coords, 
    y=y_coords, 
    ax=ax, 
    cmap='Reds',  # Choose a color palette
    fill=True, 
    thresh=0, 
    levels=100, 
    alpha=0.6  # Adjust transparency to see the background image
)

# Additional settings
ax.set_xlim(0, 3060)  # Set X limits to match the map
ax.set_ylim(0, 3060)  # Set Y limits to match the map
ax.set_title(f"Spatial Heatmap for player {player_name} between 'bomb_planted' and 'bomb_defused/exploded'")
ax.axis('off')  # Remove axes for better visualization

# Invert the Y-axis to match the standard map representation
ax.invert_yaxis()

# Show the plot
plt.show()
