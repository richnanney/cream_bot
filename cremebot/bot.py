import discord
import cremebot.responses as responses
import asyncio
import datetime

DEFAULT_CHANNEL_ID = 1070809323296526419

class Bot():
    def __init__(self):
        self.token = open("data/discord_bot_token.txt", encoding="utf8").read()
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def send_message(self, content, channel):
        try:
            response = responses.handle_response(content)
            if response:
                await channel.send(response)
        except Exception as e:
            print(e)
        
    async def schedule_daily_message(self):
        last_checked = ""
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            now = datetime.datetime.now()
            next_time = datetime.datetime(
                now.year, now.month, now.day, hour=9, minute=0, second=0
            )
            wait_time = (next_time - now).total_seconds()
            await asyncio.sleep(wait_time)
            channel = self.client.get_channel(DEFAULT_CHANNEL_ID)

            if last_checked != now.day:
                await self.send_message("!checkbirthday", channel)
                last_checked = now.day

    async def on_ready(self):
        print(f"{self.client.user} is now running!")
        self.client.loop.create_task(self.schedule_daily_message())

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        id = str(message.id)
        server = str(message.guild.id)
        server_name = str(message.guild.name)
        print(f"{username} said: '{user_message}' ({channel}) id: {id} server: {server} server_name: {server_name}")
        if user_message:
            await self.send_message(user_message, message.channel)

    def run(self):
        self.client.run(self.token)