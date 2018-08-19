discordToken = "<token>"
webhook = '<url>'

import discord, asyncio, urllib.request, os.path, sqlite3, copy, time, datetime

import kurisu.nyaa, kurisu.tips, kurisu.override, kurisu.alpaca, kurisu.prefs, kurisu.tasks
import traceback

from discord.ext import commands

startup_extensions = ["kurisu.cogs.steins", "kurisu.cogs.upa", "kurisu.cogs.fgl", "kurisu.cogs.main"]
startup_system = ["kurisu.system.messages", "kurisu.system.members"]

client = commands.Bot(command_prefix='!', description='Amadeus Systems', formatter=kurisu.override.newHelpFormatter())

ready = False
taskList = {}


def sigint_handler(sig, frame):
	req = requests.post(webhook, json={'embeds': [{'color': '15158332', 'title': 'Процесс `Amadeus` был закрыт.', 'description': 'Причина: Keyboard Interrupt'}]})
	sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

@client.event
async def on_ready():
	global ready

	desc = '{u.mention} готова к работе'.format(u=client.user)
	req = requests.post(webhook, json={'embeds': [{'color': '3066993', 'title': 'Процесс `Amadeus` запущен.', 'description': desc}]})
	ready = True

# Тут начинаются команды

if __name__ == "__main__":
	for extension in startup_system:
		try:
			client.load_extension(extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load system extension {}\n{}'.format(extension, exc))

	for extension in startup_extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(discordToken)
