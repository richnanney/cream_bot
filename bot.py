import discord
import responses
import asyncio
import datetime

DEFAULT_CHANNEL_ID = 1070809323296526419


async def send_message(content, channel):
    try:
        if content:  # This will prevent us from sending 'False'.
            await channel.send(content)
    except Exception as e:
        print(f"Error sending response! Error: {e}")


def watch_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    id = str(message.id)
    server = str(message.guild.id)
    server_name = str(message.guild.name)
    print(
        f"{username} said: '{user_message}' ({channel}) id: {id} server: {server} server_name: {server_name}"
    )


def run_discord_bot():
    TOKEN = open("discord_bot_token.txt", encoding="utf8").read()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    async def schedule_daily_message():
        last_checked = ""
        await client.wait_until_ready()
        while not client.is_closed():
            now = datetime.datetime.now()
            next_time = datetime.datetime(
                now.year, now.month, now.day, hour=8, minute=0, second=0
            )
            wait_time = (next_time - now).total_seconds()
            await asyncio.sleep(wait_time)
            channel = client.get_channel(DEFAULT_CHANNEL_ID)

            if last_checked != now.day:
                for server in client.guilds:
                    await send_message(responses.wish_birthday(server.name), channel)
                last_checked = now.day

    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")
        client.loop.create_task(schedule_daily_message())

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        watch_message(message)

        if message.content[0] == "!":
            await send_message(responses.handle_response(message), message.channel)

    client.run(TOKEN)
