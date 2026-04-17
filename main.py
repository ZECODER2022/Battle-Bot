import discord
from discord.ext import commands
import json
import random
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = Path('data.json')
#cube data
CUBES = [
    {'name': 'Red Cube', 'color': '🔴', 'rarity': 'common', 'weight': 50},
    {'name': 'Blue Cube', 'color': '🔵', 'rarity': 'uncommon', 'weight': 25},
    {'name': 'Green Cube', 'color': '🟢', 'rarity': 'rare', 'weight': 15},
    {'name': 'Yellow Cube', 'color': '🟡', 'rarity': 'epic', 'weight': 5}
]
# data and more boring stuff...

def roll_cube():
    weights = [cube['weight']for cube in CUBES]
    result = random.choices(CUBES, weights=weights, k=1)[0]
    return result

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class BasicBoxButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Basic Box - 250 PTS",
            style=discord.ButtonStyle.blurple,
            emoji="📦"
        )
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        data = load_data()

        if user_id not in data['users']:
            await interaction.response.send_message("You have **0** points! Send a message to earn some!", ephemeral=True)
            return
        user = data['users'][user_id]

        if user['points'] < 250:
            await interaction.response.send_message(
                f"Not enought points! You need **250** but have **{user['points']}**",
                ephemeral=True
            )
            return
        
        user['points'] -= 250

        cube = roll_cube()
        user['characters'].append(cube)

        save_data(data)

        await interaction.response.send_message(
            f"You bought a **Basic Box**! 📦\nYou got a {cube['color']} **{cube['name']}** ({cube['rarity']})",
            ephemeral=True
        )

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(BasicBoxButton())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    print('Slash commands synced')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    user_id = str(message.author.id)
    points = random.randint(1, 10)
    
    data = load_data()

    if user_id not in data['users']:
        data['users'][user_id] = {
            'username': message.author.name,
            'points': 0,
            'characters': []
        }
    
    data['users'][user_id]['points'] += points
    save_data(data)
    
    await bot.process_commands(message)
# everything under here is commands!!! 
@bot.tree.command(name='inventory', description='See your inventory!')
async def inventory(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data['users'] or not data['users'][user_id]['characters']:
        await interaction.response.send_message('Your inventory is empty! Buy some boxes to get characters!', ephemeral=True)
        return
    
    cubes = data['users'][user_id]['characters']

    counts = {}
    for cube in cubes:
        name = cube['name']
        if name not in counts:
            counts[name] = {'cube': cube, 'count': 0}
        counts[name]['count'] += 1

        embed = discord.Embed(title=f"{interaction.user.name}'s Inventory", color=discord.Color.blurple())

        for name, entry in counts.items():
            cube = entry['cube']
            embed.add_field(name=f"{cube['color']}{cube['name']} - {cube['rarity']}", value=f"Quantity: {entry['count']}", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='ping', description='Responds with Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

@bot.tree.command(name='points', description='Check your points')
async def points(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_data()
    if user_id in data['users']:
        points = data['users'][user_id]['points']
        await interaction.response.send_message(f'You have **{points}** points!')
    else:
        await interaction.response.send_message('You have **0** points! Send a message to earn some!')

@bot.tree.command(name='shop', description='Buy boxes for cubes!')
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(
    title='🛒 Shop',
    description='Spend your points on boxes!',
    color=discord.Color.gold() 
)
    embed.add_field(name="📦 Basic Box", value='**250 points**\nContains a mystery Cube!', inline=False)
    await interaction.response.send_message(embed=embed, view=ShopView())

bot.run('Token Here!!!')
