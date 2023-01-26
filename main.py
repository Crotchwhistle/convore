# importing discord
import discord
from discord import app_commands
# importing .env 
from dotenv import load_dotenv
load_dotenv()
import os


TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()

class myClient(discord.Client):
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=964294311715938308))
        print(f"Logged in as {self.user}.")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

client = myClient(intents=intents)
tree = app_commands.CommandTree(client)

# test ping command
@tree.command(name="ping", description="Pings the bot.", guild=discord.Object("964294311715938308"))
async def ping_command(interaction):
    await interaction.response.send_message("Pong!")

client.run(TOKEN)