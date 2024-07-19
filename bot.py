import http.client
from typing import Dict, List
import discord
import os
import json

from dotenv import load_dotenv

load_dotenv()

DISCORD_API_KEY: str = os.getenv("DISCORD_API_KEY")
DOMAINR_API_KEY: str = os.getenv("DOMAINR_API_KEY")

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

client: discord.Client = discord.Client(intents=intents)


def get_domain_registration_status(domain: str) -> str:
    conn: http.client.HTTPSConnection = http.client.HTTPSConnection(
        "domainr.p.rapidapi.com"
    )

    headers: Dict[str, str] = {
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
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("/"):
        tokens: List[str] = message.content.split(" ")
        command: str = tokens[0][1:]
        if command == "checkdomain":
            if len(tokens) > 1:
                domain = tokens[1]
                status = get_domain_registration_status(domain)
                status_data = json.loads(status)
                registration_status = status_data["status"][0]["status"]
                await message.channel.send(
                    f"Domain {domain} is {registration_status}."
                )
            else:
                await message.channel.send("Please provide a domain to check.")
        else:
            await message.channel.send(f"Unknown command: {command}")

client.run(DISCORD_API_KEY)
