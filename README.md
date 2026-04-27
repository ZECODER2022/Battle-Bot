# Battle Bot

This is a discord bot that is a fun interactive game for a server! Everytime you chat you earn points which can be used for Boxes! Packs can unlock different cubes with different abilities! These Cubes can we fought for points on the line!

**Features:**
- Points 
- Boxes 
- Cubes
- Battling
- Cube selling
- Dueling
- Trading

**Commands:**
- /points - Shows amount of points the user that triggered the command has
- /shop - Open the menu to buy boxes to unclock cubes!
- /ping - Test the ping/connection of the bot
- /sell - sell extra cubes for some extra points
- /duel - invite a player to a duel
- /help - learn how to use and play the bot
- /trade - trade cubes with other users
- /randomduel - send a command looking for someone to duel
- /inventory - Shows all of your cubes
- /allinventory - show a collections of all users
- /givecube (DEV ONLY) - gives selectect user inputed cube
- /givepoints (DEV ONLY) - gives selected user inputed points
- More in Development...

**Current Boxes:**
- Basic Box - 250 points with standard color lootpool
- Gaming Box - 500 points with gaming title lootpool

**How it works:**
- Points - Every message send by a user instantly gets a random amount of points (5-25) - When the amount is randomly choosen it is stored inside a data.json that has the points as a variable along with the following: User ID, Username, Characters (cubes). This allow all future data to be ready and set up to be saved along with allowing data to be retreieved and read by the bot. 
- Shop - The shop menu is the spot where users can purchase boxes to unlock cubes! Each box has different cubes and rariety for unboxing. These are stored inside a .json for storage and are retrieved and read by the bot everytime you purchase a new box!
- Sell - When a user runes the sell command they select a cube they would like to sell then get to choose from 4 amounts; 1, 5, 10, Max. Once you select a cube and amount the bot will remove the segments from the .json deleting the cubes from your inventory
- Inventory - When you run the inventory command the bot goes into the .json and pull all the cubes that you currently have and listes them in amounts. Once it has gathered all the cubes it will send a message showing all of your cubes and amount.
- Trading - When ran the person who ran it choses a cube they want and the other user choses one they want if they agree it switches them from users in the .json and sends a message saying it was successful!


# **How to install**

To find out how to create, set up, and adding to your server please follow the offical discord Guide here: https://docs.discord.com/developers/quick-start/getting-started

Once you connect the bot to your server via the token you need to add some highup permission roles id to the bracket (seen below)

<img width="288" height="28" alt="Screenshot 2026-04-21 at 8 19 03 AM" src="https://github.com/user-attachments/assets/5da208fe-2ef2-41b3-becb-cd92781ade05" />

This feild allows the bots commands /givecube and /givepoints to be used by server administrators!

Once that it in the bot should be able to be ran and if all steps are done right it should work!

# **DataBase**

The code uses a .json file to store user data like; cubes, points and username. This .json can be manually edited while the bot is running to fix a issue or give other players cubes or points without running commands!

**How to edit:**

To edit a users points under there name you can just edit the points value and save, the bot will instantly update with the new data without having to restart the bot!

<img width="199" height="77" alt="Screenshot 2026-04-26 at 3 22 51 PM" src="https://github.com/user-attachments/assets/832090e0-a6b2-40ca-963f-f41b542e425b" />

To edit what cubes a user has you can just copy the section (seen in photo below) to another user or get them from the CUEBS.md found in the files

<img width="189" height="123" alt="Screenshot 2026-04-26 at 3 23 56 PM" src="https://github.com/user-attachments/assets/17c17a5a-1403-4b2a-9b8a-005188456ea0" />

# **Adding your own stuff**

Since the bot is open sourced anyone can create their own versions! To create your own versions its important to understand how the base code works. This section will be all about how it works and some ideas for new features!

**Cubes:**
Cubes work by having different data groups for each box (See image below) These can have more Cubes added or removed from them will impact the boxes! To create a new box you will need to Add another section with Cubes in it will the same data found in the others. 

<img width="681" height="118" alt="Screenshot 2026-04-26 at 3 26 16 PM" src="https://github.com/user-attachments/assets/c4109851-fa1b-4d8a-a123-6936069f8466" />

To Update the /Shop command with the new Box button you need to go to Line 777 (V Beta-1.5) and add a new box code example below: Along with that you will need to add a new class im not gonna get into how to here but its pretty simple and in the code near the top you can pretty much copy and paste it and change it around and it should work. Thats what i did with the gaming box

Example:

<img width="681" height="28" alt="Screenshot 2026-04-26 at 3 25 46 PM" src="https://github.com/user-attachments/assets/a709a12f-8035-457c-b7c4-bebe45560dfe" />

New Box Code:
- "embed.add_field(name="📦 Basic Box", value='**250 points**\nContains a mystery Cube!', inline=False)" 

