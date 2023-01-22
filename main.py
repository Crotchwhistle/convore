import discord
from dotenv import load_dotenv
load_dotenv()
import os

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()

class myClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}.")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

client = myClient(intents=intents)
client.run(TOKEN)