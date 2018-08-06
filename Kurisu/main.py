discordToken = "<token>"

import discord, asyncio, urllib.request, os.path, sqlite3, copy, time, datetime
import kurisu.nyaa, kurisu.console, kurisu.tips, kurisu.override, kurisu.alpaca, kurisu.prefs, kurisu.tasks
import traceback
from discord.ext import commands

startup_extensions = ["kurisu.cogs.steins", "kurisu.cogs.upa", "kurisu.cogs.fgl", "kurisu.cogs.main"]

client = commands.Bot(command_prefix='!', description='Amadeus Systems', formatter=kurisu.override.newHelpFormatter())

ready = False
taskList = {}
  
@client.event
async def on_ready():
	print('[Discord] | Initializing tips')
	kurisu.tips.init()
	print('[Discord] | Initializing preferences')
	kurisu.prefs.init()
	kurisu.prefs.discordClient = client
	print('[Discord] | Logged in as: %s | %s' % (client.user.name, client.user.id))
	await client.change_presence(game=discord.Game(name='Steins;Gate 0', type=3))
	kurisu.tasks.loop = client.loop
	await kurisu.tasks.new(kurisu.nyaa.fetch)
	await kurisu.tasks.new(kurisu.alpaca.alpacaLoop)
	kurisu.prefs.startup = datetime.datetime.now()
	global ready
	ready = True
    
@client.event
async def on_message(message):
    #if message.channel.id != "446333540381229066":
       #return
	await client.process_commands(message)

	if message.content == 'Nullpo':
		await client.send_message(message.channel, 'Gah!')
      
@client.event
async def on_member_join(member):
	if member.server.id != kurisu.prefs.Servers.FGL.id:
		return
	conn = sqlite3.connect('db.sqlite3')
	cursor = conn.cursor()
	cursor.execute('select * from alpaca where userID = %s limit 1' % member.id)
	a = cursor.fetchall()

	tmpEmbed = kurisu.prefs.Embeds.new('welcome')
	tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
	tmpEmbed.add_field(name="Лабмембер №%s" % str(len(member.server.members)-8), value=member)
	tmpEmbed.add_field(name="ID", value=member.id)
	if len(a) != 0:
		t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
		if t > datetime.datetime.now():
			pt = kurisu.prefs.parse_time(t.timetuple())
			pt = '%s %s' % (pt[0], pt[1])
			tmpEmbed.add_field(name="Альпакамен", value="до %s" % pt)
			await client.add_roles(member, kurisu.prefs.Roles.alpaca)
		else:
			tmpEmbed.add_field(name="Альпакамен", value="Роль снята")
			cursor.execute('delete from alpaca where userID = %s' % member.id)
			conn.commit()
	tmpEmbed.set_image(url="https://i.imgur.com/DcLOkLK.gif")
	await client.send_message(kurisu.prefs.Channels.lab, embed=tmpEmbed)
	conn.close()

@client.event
async def on_member_remove(member):
	if member.server.id != kurisu.prefs.Servers.FGL.id:
		return
	tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
	tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
	tmpEmbed.add_field(name="Никнейм", value=member)
	tmpEmbed.add_field(name="ID", value=member.id)
	tmpEmbed.set_image(url="https://i.imgur.com/wupSJAh.gif")
	await client.send_message(kurisu.prefs.Channels.lab, embed=tmpEmbed)
	
@client.event
async def on_command_error(error: Exception, ctx: commands.Context):
	ignored = (commands.CommandNotFound, commands.UserInputError)
	
	if isinstance(error, ignored):
		return
	
	tmpEmbed = kurisu.prefs.Embeds.new('error')
	tb = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__, limit=5)
	tmpEmbed.add_field(name="Вызвал", value=ctx.message.author)
	tmpEmbed.add_field(name="Сообщение", value=ctx.message.content)
	tmpEmbed.add_field(name="Traceback", value='%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))
	await client.send_message(kurisu.prefs.Channels.log, embed=tmpEmbed)
	
	if isinstance(error, commands.BadArgument):
		await client.send_message(ctx.message.channel, 'Ошибка в аргументе')
		return
	elif isinstance(error, commands.MissingRequiredArgument):
		await client.send_message(ctx.message.channel, 'Недостаточно аргументов')
		return
	else:
		await client.send_message(ctx.message.channel, 'Упс... Информация об ошибке в %s' % kurisu.prefs.Channels.log.mention)
	
# Тут начинаются команды

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(discordToken)
