import http
from typing import List
import discord
import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_API_KEY: str = os.getenv("DISCORD_API_KEY")
DOMAINR_API_KEY: str = os.getenv('DOMAINR_API_KEY')

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

client: discord.Client = discord.Client(intents=intents)


def get_domain_registration_status(domain: str) -> str:
    conn = http.client.HTTPSConnection("domainr.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': DOMAINR_API_KEY,
        'x-rapidapi-host': "domainr.p.rapidapi.com"
    }

    conn.request("GET", f"/v2/status?domain={domain}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


@client.event
async def on_ready() -> None:
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message: str) -> None:
    if message.author == client.user:
        return

    if message.content.startswith('/domain'):
        message_tokens: List[str] = message.content.split(" ")
        response = get_domain_registration_status(message_tokens[1])
        await message.channel.send(response)

client.run(DISCORD_API_KEY)
