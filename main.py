import discord
from discord.ext import commands
import json
import random
from pathlib import Path
import asyncio

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = Path('data.json')

DEVELOPER_ROLE_ID = PUT_ADMIN_ROLE_HERE!!!!

CUBES = [
    {'name': 'Red Cube', 'color': '🔴', 'rarity': 'common', 'weight': 50, 'hp': 100, 'damage': 25},
    {'name': 'Blue Cube', 'color': '🔵', 'rarity': 'uncommon', 'weight': 25, 'hp': 150, 'damage': 35},
    {'name': 'Green Cube', 'color': '🟢', 'rarity': 'rare', 'weight': 15, 'hp': 175, 'damage': 45},
    {'name': 'Yellow Cube', 'color': '🟡', 'rarity': 'epic', 'weight': 5, 'hp': 200, 'damage': 65},
    {'name': 'Black Cube', 'color': '⚫', 'rarity': 'legendary', 'weight': 1, 'hp': 250, 'damage': 80}
]

GAMING_CUBES = [
    {'name': 'Steam', 'color': '⚫', 'rarity': 'common', 'weight': 50, 'hp': 100, 'damage': 25},
    {'name': 'Portal 1', 'color': '🔵', 'rarity': 'uncommon', 'weight': 25, 'hp': 150, 'damage': 35},
    {'name': 'Portal 2', 'color': '🟠', 'rarity': 'rare', 'weight': 15, 'hp': 175, 'damage': 45},
    {'name': 'Half-Life', 'color': '🟢', 'rarity': 'Epic', 'weight': 5, 'hp': 200, 'damage': 65},
    {'name': 'Half-Life 2', 'color': '🟣', 'rarity': 'legendary', 'weight': 1, 'hp': 250, 'damage': 75},
    {'name': 'Companion Cube', 'color': '🩷', 'rarity': 'SECRETE', 'weight': 0.10, 'hp': 500, 'damage': 100}
]

TRADE_WARNINGS = {
    'Black Cube': 'This is a **LEGENDARY** cube! Are you sure you want to sell it?',
    'Half-Life 2': 'This is a **LEGENDARY** cube! Are you sure you want to sell it?',
    'Companion Cube': 'This is the **RAREST CUBE** in the entire game! ARE YOU SURE you want to sell it?'
}

SELL_PRICES = {
    'Red Cube': 50,
    'Blue Cube': 100,
    'Green Cube': 175,
    'Yellow Cube': 350,
    'Black Cube': 500,
    'Steam': 50,
    'Portal 1': 100,
    'Portal 2': 175,
    'Half-Life': 300,
    'Half-Life 2': 500,
    'Companion Cube': 1500
}

CUBE_LOOKUP = {cube['name']: cube for cube in CUBES + GAMING_CUBES}

def roll_gaming_cube():
    weights = [cube['weight'] for cube in GAMING_CUBES]
    result = random.choices(GAMING_CUBES, weights=weights, k=1)[0]
    return result.copy()

def roll_cube():
    weights = [cube['weight'] for cube in CUBES]
    result = random.choices(CUBES, weights=weights, k=1)[0]
    return result.copy()

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def coin_flip(user1_id, user2_id):
    return random.choice([user1_id, user2_id])

async def run_battle(channel, challenger, challenged, cube1, cube2, wager, data):
    hp1 = cube1.get('hp', 100)
    hp2 = cube2.get('hp', 100)
    damage1 = cube1.get('damage', 25)
    damage2 = cube2.get('damage', 25)

    first = coin_flip(challenger.id, challenged.id)
    if first == challenger.id:
        flip_msg = f"🪙 Coin Flip! **{challenger.name}** goes first!"
    else:
        flip_msg = f"🪙 Coin Flip! **{challenged.name}** goes first!"
    
    await channel.send(flip_msg)
    await asyncio.sleep(2)

    round_num = 1 
    while hp1 > 0 and hp2 > 0:
        await channel.send(f"**--- Round {round_num} ---**")
        await asyncio.sleep(1)

        if first == challenger.id:
            hp2 -= damage1
            await challenger.send(f"⚔️ You attacked **{challenged.name}** for **{damage1}** damage!")
            await challenged.send(f"💥 You were attacked by **{challenger.name}** for **{damage1}** damage! Your HP: {max(hp2, 0)}")
            await asyncio.sleep(1.5)

            if hp2 > 0:
                hp1 -= damage2
                await challenged.send(f"⚔️ You attacked **{challenger.name}** for **{damage2}** damage!")
                await challenger.send(f"💥 You were attacked by **{challenged.name}** for **{damage2}** damage! Your HP: {max(hp1, 0)}")
                await asyncio.sleep(1.5)
            
            round_num += 1
        else:
            hp1 -= damage2
            await challenged.send(f"⚔️ You attacked **{challenger.name}** for **{damage2}** damage!")
            await challenger.send(f"💥 You were attacked by **{challenged.name}** for **{damage2}** damage! Your HP: {max(hp1, 0)}")
            await asyncio.sleep(1.5)

            if hp1 > 0:
                hp2 -= damage1
                await challenger.send(f"⚔️ You attacked **{challenged.name}** for **{damage1}** damage!")
                await challenged.send(f"💥 You were attacked by **{challenger.name}** for **{damage1}** damage! Your HP: {max(hp2, 0)}")
                await asyncio.sleep(1.5)
            
            round_num += 1

        if hp1 > 0 and hp2 <= 0:
            winner, loser = challenger, challenged
            winning_cube = cube1
        elif hp2 > 0 and hp1 <= 0:
            winner, loser = challenged, challenger
            winning_cube = cube2
        else:
            continue

        data = load_data()
        data['users'][str(winner.id)]['points'] += wager
        data['users'][str(loser.id)]['points'] -= wager
        save_data(data)

        embed = discord.Embed(title="Duel over!", color=discord.Color.gold())
        embed.add_field(name="Winner", value=f"{winner.mention} wins **{wager}** points!", inline=False)
        embed.add_field(name="Winning Cube", value=f"{winning_cube['color']} {winning_cube['name']}", inline=False)
        await channel.send(embed=embed)
        break

class TradeSelect(discord.ui.Select):
    def __init__(self, user_cubes):
        seen = {}
        options = []
        for cube in user_cubes:
            name = cube['name']
            if name not in seen:
                seen[name] = {'cube': cube, 'count': 0}
            seen[name]['count'] += 1

        for name, entry in seen.items():
            cube = entry['cube']
            options.append(
                discord.SelectOption(
                    label=cube['name'],
                    emoji=cube['color'],
                    description=f"Owned: {entry['count']} | {cube['name']}"
                )
            )

        super().__init__(placeholder='Choose a cube to trade...', options=options)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.choosen_cube = self.values[0]
        self.disabled = True
        self.view.stop()
        await interaction.response.edit_message(content=f"You selected **({self.values[0]}**! Now confirm the trade)", view=self.view)

class TradeSelectedView(discord.ui.View):
    def __init__(self, user_cubes):
        super().__init__(timeout=60)
        self.choosen_cube = None
        self.add_item(TradeSelect(user_cubes))



class SellSelect(discord.ui.Select):
    def __init__(self, user_cubes, sell_prices):
        seen = {}
        options = []
        for cube in user_cubes:
            name = cube['name']
            if name not in seen:
                seen[name] = {'cube': cube, 'count': 0}
            seen[name]['count'] += 1

        for name, entry in seen.items():
            cube = entry['cube']
            price = sell_prices.get(cube['name'], 0 )
            options.append(
                discord.SelectOption(
                    label=cube['name'],
                    emoji=cube['color'],
                    description=f"Owned: {entry['count']} | Sell for: {price} pts each"
                )
            )
        super().__init__(placeholder='Choose a cube to sell...', options=options)
        self.user_cubes = user_cubes
        self.sell_prices = sell_prices
        self.seen = seen
    
    async def callback(self, interaction: discord.Interaction):
        self.view.choosen_cube = self.values[0]
        self.view.max_owned = self.seen[self.values[0]]['count']
        self.disabled = True
        await interaction.response.edit_message(content=f"You selected **{self.values[0]}**! Now choose how many to sell.", view=self.view)
        self.view.show_quantity_buttons()
        self.view.stop()

class SellView(discord.ui.View):
    def __init__ (self, user_cubes, sell_prices):
        super().__init__(timeout=60)
        self.choosen_cube = None
        self.max_owned = 0
        self.sell_prices = sell_prices
        self.add_item(SellSelect(user_cubes, sell_prices))

    def show_quantity_buttons(self):
        pass

class SellQuantityView(discord.ui.View):
    def __init__(self, cube_name, max_owned, sell_prices, user_id):
        super().__init__(timeout=60)
        self.cube_name = cube_name
        self.max_owned = max_owned
        self.sell_prices = sell_prices
        self.user_id = user_id
        self.quantity = 0

        amounts = [1, 5, 10, max_owned]
        seen_amounts = set()
        for amount in amounts: 
            if amount <= max_owned and amount not in seen_amounts: 
                seen_amounts.add(amount)
                self.add_item(SellQuantityButton(amount, cube_name, sell_prices, user_id))

class SellQuantityButton(discord.ui.Button):
    def __init__(self, amount, cube_name, sell_prices, user_id):
        price = sell_prices.get(cube_name, 0)
        total = price * amount
        super().__init__(
            label=f"Sell {amount} for {total} pts",
            style=discord.ButtonStyle.green
        )

        self.amount = amount
        self.cube_name = cube_name
        self.sell_prices = sell_prices
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("This isn't your sale!", ephemeral=True)
            return
        
        data = load_data()
        user = data['users'].get(self.user_id)
        
        owned = [c for c in user['characters'] if c['name'] == self.cube_name]
        if len(owned) < self.amount: 
            await interaction.response.send_message("You don't have that many to sell!", ephemeral=True)
            return
        
        removed = 0
        new_characters = []
        for cube in user['characters']:
            if cube['name'] == self.cube_name and removed < self.amount:
                removed += 1
            else:
                new_characters.append(cube)

        user['characters'] = new_characters

        price = self.sell_prices.get(self.cube_name, 0)
        total_earned = price * self.amount
        user['points'] += total_earned
        save_data(data)

        for item in self.view.children:
            item.disabled = True
        
        await interaction.response.edit_message(content=f"Sold **{self.amount}x {self.cube_name}** for **{total_earned}** points!", view=self.view)
        self.view.stop()

class GamingBoxButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Gaming Box - 500 PTS",
            style=discord.ButtonStyle.green,
            emoji="🎮"
        )

    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        data = load_data()

        if user_id not in data['users']:
            await interaction.response.send_message("You have **0** points! Send a message to earn some!", ephemeral=True)
            return
        
        user = data['users'][user_id]

        if user['points'] < 500:
            await interaction.response.send_message(
                f"Not enought points! You need **500** but have **{user['points']}**",
                ephemeral=True
            )
            return
        
        user['points'] -= 500

        cube = roll_gaming_cube()
        user['characters'].append(cube)
        save_data(data)

        await interaction.response.send_message(
            f"You bought a **Gaming Box**! 🎮\nYou got a {cube['color']} {cube['name']}! ({cube['rarity']})",
            ephemeral=True
        )

        if cube['name'] == 'Companion Cube':
            await interaction.response.send_message("🎉 Congratulations! You got the SECRET Companion Cube! 🎉", ephemeral=True)

class CubeSelect(discord.ui.Select):
    def __init__(self, user_cubes):
        seen = set()
        options = []
        for cube in user_cubes:
            if cube['name'] not in seen:
                seen.add(cube['name'])
                hp = cube.get('hp', 100)
                damage = cube.get('damage', 25)
                rarity = cube.get('rarity', 'unknown')
                options.append(
                    discord.SelectOption(
                        label=cube['name'],
                        emoji=cube['color'],
                        description=f"HP: {hp} | DMG: {damage} | {rarity}"
                    )
                )
        super().__init__(placeholder='Choose your cube...', options=options)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.chosen_cube_name = self.values[0]
        self.disabled = True
        await interaction.response.edit_message(content=f"You chose **{self.values[0]}**! Waiting for opponent...", view=self.view)
        self.view.stop()

class CubeSelectView(discord.ui.View):
    def __init__(self, user_cubes):
        super().__init__(timeout=60)
        self.chosen_cube_name = None
        self.add_item(CubeSelect(user_cubes))

class GamingBoxView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GamingBoxButton())

class DuelView(discord.ui.View):
    def __init__(self, challenger, challenged, wager):
        super().__init__(timeout=60)
        self.challenger = challenger
        self.challenged = challenged
        self.wager = wager

    @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenged.id:
            await interaction.response.send_message("Only the challenged user can accept this duel!", ephemeral=True)
            return
        
        data = load_data()
        challenger_data = data['users'].get(str(self.challenger.id))
        challenged_data = data['users'].get(str(self.challenged.id))
        
        if challenger_data['points'] < self.wager or challenged_data['points'] < self.wager:
            await interaction.response.send_message("Someone no longer has enough points to duel!", ephemeral=True)
            return

        await interaction.response.send_message("Duel accepted! Both players, please select your cubes in DMs!")

        view1 = CubeSelectView(challenger_data['characters'])
        view2 = CubeSelectView(challenged_data['characters'])

        try:
            await self.challenger.send("Pick your cube for the duel!", view=view1)
        except discord.Forbidden:
            await interaction.channel.send(f"⚠️ Could not send DM to {self.challenger.name}! Enable DMs from server members.")
            return
        
        try:
            await self.challenged.send("Pick your cube for the duel!", view=view2)
        except discord.Forbidden:
            await interaction.channel.send(f"⚠️ Could not send DM to {self.challenged.name}! Enable DMs from server members.")
            return

        await asyncio.gather(view1.wait(), view2.wait())

        if not view1.chosen_cube_name or not view2.chosen_cube_name:
            await interaction.channel.send("Duel cancelled - a player didn't pick a cube in time!")
            return
        
        cube1 = next(c for c in challenger_data['characters'] if c['name'] == view1.chosen_cube_name)
        cube2 = next(c for c in challenged_data['characters'] if c['name'] == view2.chosen_cube_name)

        await run_battle(interaction.channel, self.challenger, self.challenged, cube1, cube2, self.wager, data)
        self.stop()

    @discord.ui.button(label="Decline Duel", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenged.id:
            await interaction.response.send_message("Only the challenged user can decline this duel!", ephemeral=True)
            return
        await interaction.response.send_message("Duel declined!")
        self.stop()

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
        self.add_item(GamingBoxButton())

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
    points = random.randint(5, 25)
    
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

@bot.tree.command(name='duel', description='Challenge another user to a duel!')
@discord.app_commands.describe(opponent='Who do you want to duel?', wager='How many points do you want to wager?')
async def duel(interaction: discord.Interaction, opponent: discord.Member, wager: int):
    data = load_data()
    challenger_id = str(interaction.user.id)
    challenged_id = str(opponent.id)

    if opponent.id == interaction.user.id:
        await interaction.response.send_message("You can't duel yourself!", ephemeral=True)
        return
    if opponent.bot:
        await interaction.response.send_message("You can't duel bots!", ephemeral=True)
        return
    if wager <= 0:
        await interaction.response.send_message("Wager must be more than 0!", ephemeral=True)
        return

    challenger_data = data['users'].get(challenger_id)
    challenged_data = data['users'].get(challenged_id)

    if not challenger_data or challenger_data['points'] < wager:
        await interaction.response.send_message("You don't have enough points to make this wager!", ephemeral=True)
        return
    if not challenged_data or challenged_data['points'] < wager:
        await interaction.response.send_message(f"{opponent.name} doesn't have enough points!", ephemeral=True)
        return
    
    view = DuelView(interaction.user, opponent, wager)
    await interaction.response.send_message("Duel request sent!", view=view)

@bot.tree.command(name='givecube', description='Give a cube to a user')
@discord.app_commands.describe(user='Who do you to give the cube?', cube_name='Name of the cube to give')
async def givecube(interaction: discord.Interaction, user: discord.Member, cube_name: str):
    if not any(role.id == DEVELOPER_ROLE_ID for role in interaction.user.roles): 
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    cube = next((c for c in CUBES if c['name'].lower() == cube_name.lower()), None)
    if not cube:
        await interaction.response.send_message("Cube not found! Check the shop for available cubes.", ephemeral=True)
        return

    data = load_data()
    user_id = str(user.id)

    if user_id not in data['users']:
        data['users'][user_id] = {'username': user.name, 'points': 0, 'characters': []}

    data['users'][user_id]['characters'].append(cube.copy())
    save_data(data)

    await interaction.response.send_message(f"Gave {cube['color']} **{cube['name']}** to **{user.mention}**!", ephemeral=True)

@bot.tree.command(name='givepoints', description='Give points to a user')
@discord.app_commands.describe(user='Who do you want to give points to?', amount='How many points?')
async def givepoints(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not any(role.id == DEVELOPER_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be more thab 0!", ephemeral=True)
        return
    
    data = load_data()
    user_id = str(user.id)

    if user_id not in data['users']:
        data['users'][user_id] = {'username': user.name, 'points': 0, 'characters': []}

    data['users'][user_id]['points'] += amount
    save_data(data)

    await interaction.response.send_message(f"Gave {amount} points to **{user.mention}**!", ephemeral=True)

@bot.tree.command(name='totalinventory', description='See the cubes of all users!')
async def totalinventory(interaction: discord.Interaction):
    data = load_data()

    counts = {}
    for user_data in data['users'].values():
        for cube in user_data['characters']:
            name = cube['name']
            if name not in counts:
                counts[name] = {'cube': cube, 'count': 0}
            counts[name]['count'] += 1

    if not counts:
        await interaction.response.send_message("No cubes found in any inventories!", ephemeral=True)
        return
    
    embed = discord.Embed(title="Total Inventory", color=discord.Color.dark_gold())
    for name, entry in counts.items():
        cube = entry['cube']
        embed.add_field(
            name=f"{cube['color']} {cube['name']} - {cube['rarity']}",
            value=f"Total Owned: **{entry['count']}*",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='randomduel', description='challenge a random oppenent to a duel!')
@discord.app_commands.describe(wager='How many points do you want to wager?')
async def random_duel(interaction: discord.Interaction, wager: int):
    data = load_data()
    challenger_id = str(interaction.user.id)

    if wager <= 0:
        await interaction.response.send_message("Wager must be more than 0!", ephemeral=True)
        return
    
    challenger_data = data['users'].get(challenger_id)
    if not challenger_data or challenger_data['points'] < wager:
        await interaction.response.send_message("You don't have enough points to make this wager!", ephemeral=True)
        return
    
    eligible = [
        uid for uid, udata in data['users'].items()
        if uid != challenger_id
        and udata['points'] >= wager
        and udata['characters']
    ]

    if not eligible:
        await interaction.response.send_message("No eligible opponents found!", ephemeral=True)
        return
    
    random_id = random.choice(eligible)
    opponent = await bot.fetch_user(int(random_id))

    embed = discord.Embed(
        title="Random Duel Challenge!",
        description=f"You have been randomly challenged to a duel by **{interaction.user.name}** for **{wager}** points!",
        color=discord.Color.orange()
    
    )

    view = DuelView(interaction.user, opponent, wager)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name='help', description='Learn how to use the bot!')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="How to Play",
        description=("Welcome to the Battle BOT! Here what you need to know:"),
        color=discord.Color.blurple()
    )

    embed.add_field(name="Earning Points", value="Send message in any channel and earn 5-25 points randomly!", inline=False)
    embed.add_field(name="Buying Boxes", value="Use '/shop' to buy boxes with your points! Each box contains a random cube!", inline=False)
    embed.add_field(name="Dueling", value="Challenge other users to duels using '/duel @user wager_amount' then pick your cube in your DMs!", inline=False)
    embed.add_field(name="Inventory", value="Use '/inventory' to see your cubes and '/totalinventory' to see all the cubes in the server owned by members!", inline=False)
    embed.add_field(name="Points", value="Use '/points' to check how many points you have!", inline=False)

    await interaction.response.send_message(embed=embed)



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

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='sell', description='Sell cubes for points!')
async def sell(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data['users'] or not data['users'][user_id]['characters']:
        await interaction.response.send_message('Your inventory is empty! Buy some boxes to get characters!', ephemeral=True)
        return
    
    user_cubes = data['users'][user_id]['characters']

    view = SellView(user_cubes, SELL_PRICES)
    await interaction.response.send_message("Select a cube to sell:", view=view, ephemeral=True)

    await view.wait()

    if not view.choosen_cube:
        return
    
    Quantity_view = SellQuantityView(view.choosen_cube, view.max_owned, SELL_PRICES, user_id)
    await interaction.followup.send("Select quantity to sell:", view=Quantity_view, ephemeral=True)

class StatsSelect(discord.ui.Select):
    def __init__(self, user_cubes):
        seen = set()
        options = []
        self.cube_stats = {}
        for cube in user_cubes:
            cube_name = cube.get('name', 'Unknown Cube')
            if cube_name not in seen:
                seen.add(cube_name)
                template = CUBE_LOOKUP.get(cube_name, {})
                hp = cube.get('hp', template.get('hp', 100))
                damage = cube.get('damage', template.get('damage', 25))
                rarity = cube.get('rarity', template.get('rarity', 'unknown'))
                color = cube.get('color', template.get('color', '⬜'))
                self.cube_stats[cube_name] = {
                    'hp': hp,
                    'damage': damage,
                    'rarity': rarity,
                    'color': color,
                }
                options.append(
                    discord.SelectOption(
                        label=cube_name,
                        emoji=color,
                        description=f"HP: {hp} | DMG: {damage} | {rarity}"
                    )
                )
        super().__init__(placeholder='Choose a cube...', options=options)
    
    async def callback(self, interaction: discord.Interaction):
        cube_name = self.values[0]
        stats = self.cube_stats.get(cube_name, {'hp': 100, 'damage': 25, 'rarity': 'unknown', 'color': '⬜'})
        embed = discord.Embed(title=f"{stats['color']} {cube_name} Stats", color=discord.Color.blue())
        embed.add_field(name="HP", value=str(stats['hp']), inline=True)
        embed.add_field(name="Damage", value=str(stats['damage']), inline=True)
        embed.add_field(name="Rarity", value=str(stats['rarity']).title(), inline=True)
        await interaction.response.defer()
        await interaction.followup.send(embed=embed, ephemeral=True)

class StatsView(discord.ui.View):
    def __init__(self, user_cubes):
        super().__init__(timeout=60)
        self.add_item(StatsSelect(user_cubes))

@bot.tree.command(name='ping', description='Responds with Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

@bot.tree.command(name='stats', description='Check cube stats')
async def stats(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data['users'] or not data['users'][user_id]['characters']:
        await interaction.followup.send('Your inventory is empty! Buy some boxes to get characters!')
        return
    
    user_cubes = data['users'][user_id]['characters']
    view = StatsView(user_cubes)
    await interaction.followup.send("Select a cube to see stats:", view=view)

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
    embed.add_field(name="🎮 Gaming Box", value='**500 points**\nContains a gaming-themed Cube!', inline=False)
    view = discord.ui.View()
    view.add_item(BasicBoxButton())
    view.add_item(GamingBoxButton())
    await interaction.response.send_message(embed=embed, view=ShopView())

bot.run('Token_here')
