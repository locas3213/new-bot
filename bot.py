import discord
import re
from discord.ext import commands

# Enable intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot
bot = commands.Bot(command_prefix=None, intents=intents)

# Set channel IDs
TAX_CHANNEL_ID = 1338229910514176092  # 🔴 Replace with the tax calculation channel ID
GENERAL_CHANNEL_ID = 1323666511428194458  # 🔴 Replace with the other channel ID
TAX_RESULT_IMAGE_URL = "https://media.discordapp.net/attachments/1137468852251394141/1324053860695675001/New_Project.png?ex=67aa2b40&is=67a8d9c0&hm=7002f8c78eb5bedd7a750d46ccdc3c5865ff07222a22924a319befb8135d9400&=&format=webp&quality=lossless&width=1260&height=63"  # 🔴 Replace with tax result image URL
GENERAL_IMAGE_URL = "https://media.discordapp.net/attachments/1137468852251394141/1324053860695675001/New_Project.png?ex=67aa2b40&is=67a8d9c0&hm=7002f8c78eb5bedd7a750d46ccdc3c5865ff07222a22924a319befb8135d9400&=&format=webp&quality=lossless&width=1260&height=63"  # 🔴 Replace with general image URL

def parse_amount(amount_str):
    """Convert shorthand values like 1k, 1m, 1b to full numbers."""
    amount_str = amount_str.lower().replace(",", "")  # Remove commas and lowercase
    multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}

    match = re.match(r"(\d+(?:\.\d+)?)([kmb]?)$", amount_str)
    if match:
        number, suffix = match.groups()
        number = float(number)  # Convert to float to handle decimals (e.g., 1.5k = 1500)
        return int(number * multipliers.get(suffix, 1))  # Convert to full number
    return None  # Invalid input

@bot.event
async def on_ready():
    print(f'✅ Bot is online! Logged in as {bot.user}')

@bot.event
async def on_message(message):
    """Handles ProBot tax calculation and general message image sending."""
    if message.author.bot:
        return  # Ignore bot messages

    # ✅ If the message is in the tax calculation channel, calculate tax and send image
    if message.channel.id == TAX_CHANNEL_ID:
        target_amount = parse_amount(message.content)
        if target_amount is not None:
            tax_rate = 5  # ProBot tax percentage
            required_amount = target_amount / (1 - tax_rate / 100)  # Calculate amount to send
            
            await message.channel.send(f'{int(required_amount)}')  # Send only the whole number
            await message.channel.send(TAX_RESULT_IMAGE_URL)  # Send image after the result

    # ✅ If the message is in the general channel, send an image
    elif message.channel.id == GENERAL_CHANNEL_ID:
        await message.channel.send(GENERAL_IMAGE_URL)

    await bot.process_commands(message)  # Ensure other commands still work

# Run the bot (replace 'YOUR_BOT_TOKEN' with your actual bot token)
bot.run('MTMzODMzNzI4NDIxODY4NzUyOA.G5ZVuO.6Hg0gOdU8yqVBpbcmmLFFnv5HfOYq_eXXtr5dU')
