import discord, datetime
from discord.ext import commands

import kurisu.nyaa, kurisu.tips, kurisu.alpaca, kurisu.prefs
import salieri.tasks, salieri.core
import requests

startup_extensions = ["kurisu.cogs.steins", "kurisu.cogs.upa", "kurisu.cogs.fgl", "salieri.main", "kurisu.cogs.rnd"]
startup_system = ["kurisu.system.messages"]

client = commands.Bot(command_prefix='!', description='Salieri Systems')
#client.root_folder = 'kurisu'

ready = False
taskList = {}
fubuki = lambda text, desc, color: {'embeds': [{'color': color, 'title': text, 'description': desc}]}

def log(name, text):
	if len(name) > 8:
		name = name[:8]

	print('[%s] | %s' % (name.ljust(8), text))
  
def init_core(client, startup):
		for extension in startup[0]:
			try:
				client.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load system extension {}\n{}'.format(extension, exc))

		for extension in startup[1]:
			try:
				client.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load extension {}\n{}'.format(extension, exc))

@client.event
async def on_ready():
	global ready
	if ready:
		await kurisu.prefs.Channels.get('dev').send("Переподключение...")
	else:
		log('Discord', 'Initializing tips')
		kurisu.tips.init()
		log('Discord', 'Initializing preferences')
		kurisu.prefs.discordClient = client
		kurisu.prefs.init()
		log('Salieri', 'Initializing core')
		init_core(client, [startup_system, startup_extensions])
		#client.log('Salieri', 'Clearing Fubuki')
		#await client.clear_webhook(kurisu.prefs.Channels.get('dev'))
		log('Discord', 'Logged in as: %s | %s' % (client.user.name, client.user.id))
		await client.change_presence(activity=discord.Activity(application_id='444126412270600202',
																name='Steins;Gate 0',
															   	type=3))
		salieri.tasks.loop = client.loop
		await salieri.tasks.new(kurisu.alpaca.alpacaLoop)
		kurisu.prefs.startup = datetime.datetime.now()

	desc = '{u.mention} готова к работе.'.format(u=client.user)
	requests.post(kurisu.prefs.webhook, json=fubuki("Ядро Salieri запущено.", desc, '3066993'))
	ready = True

client.run(kurisu.prefs.discordToken)
