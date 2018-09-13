import re, os
from discord.ext import commands
import discord
import kurisu.prefs
import datetime, sqlite3

_mentions_transforms = {
	'@everyone': '@\u200beveryone',
	'@here': '@\u200bhere'
	}

_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))


def cache_size():
	try:
		stdout = os.popen('du -h /home/pi/MusicBot/audio_cache').readline()
		return "%s" % stdout.split()[0].replace(',', '.')
	except:
		return "недоступен"


class FGL(commands.Cog, name='FGL Cog'):
	"""Просто все подряд, десу"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, *commands: str):
		"""Возвращает данное сообщение"""
		bot = ctx.bot
		destination = ctx.message.channel

		def repl(obj):
			return _mentions_transforms.get(obj.group(0), '')

		#help by itself just lists our own commands.
		if len(commands) == 0:
			helpEmbed = await bot.formatter.format_help_for(ctx, bot)
		elif len(commands) == 1:
			#try to see if it is a cog name
			name = _mention_pattern.sub(repl, commands[0])
			command = None
			if name in bot.cogs:
				command = bot.cogs[name]
			else:
				command = bot.all_commands.get(name)
				if command is None:
					await destination.send("Команда %s не найдена." % name)
					return

			helpEmbed = await bot.formatter.format_help_for(ctx, command)
		else:
			name = _mention_pattern.sub(repl, commands[0])
			command = bot.all_commands.get(name)
			if command is None:
				await destination.send("Команда %s не найдена." % name)
				return

			for key in commands[1:]:
				try:
					key = _mention_pattern.sub(repl, key)
					command = command.all_commands.get(key)
					if command is None:
						await destination.send("Подкоманда %s не найдена." % key)
						return
				except AttributeError:
					await destination.send("Команда %s не имеет подкоманд." % name)
					return

			helpEmbed = await bot.formatter.format_help_for(ctx, command)

		await destination.send(embed=helpEmbed)

	@commands.command()
	async def status(self, ctx):
		"""Возвращает информацию о хост-машине"""
		stats = kurisu.prefs.info()

		emb = kurisu.prefs.Embeds.new('normal')
		emb.add_field(name=kurisu.prefs.i18n(self, 'stats'),
    	value='CPU All: {d[0]}\nCPU 1: {d[1][0]}\nCPU 2: {d[1][1]}\nCPU 3: {d[1][2]}\nCPU 4: {d[1][3]}\nRAM Total: {d[2]}MB\nRAM Used: {d[3]}MB\nTemp: {d[5]}`C\nUptime: {d[6]}'.format(d=stats))
		emb.add_field(name=kurisu.prefs.i18n(self, 'bot'), value=kurisu.prefs.i18n(self, 'root') % self.bot.root_folder)
		emb.add_field(name=kurisu.prefs.i18n(self, 'moeka'), value=kurisu.prefs.i18n(self, 'cache') % cache_size())

		await ctx.send(embed=emb)

	@commands.command()
	async def info(self, ctx, *users: str):
		"""Возвращает информацию о пользователе

		Аргументы:
		-----------
		users: [`discord.Member`]
			Массив упоминаний пользователей.
			Если нет ни одного упоминания, используется автор сообщения.
		"""
		if len(ctx.message.mentions) == 0:
			users = [ctx.message.author]
		else:
			users = ctx.message.mentions

		for u in users:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			emb = kurisu.prefs.Embeds.new('normal')
			norole = u.top_role.name == "@everyone"
			color = (255, 255, 255) if norole else u.colour.to_rgb()
			emb.colour = discord.Colour.from_rgb(*color)
			emb.title = '%s%s%s' % (u,  "" if (u.name == u.display_name) else (" a.k.a %s" % u.display_name), u.bot and " [BOT]" or '')
			emb.add_field(name="ID:", value=u.id, inline=False)

			if not u.bot:
				cursor.execute('select * from committee where userID = %s limit 1' % u.id)
				a = cursor.fetchall()

				if a:
					join_date = datetime.datetime.fromtimestamp(a[0][2])
					emb.description = "Член Комитета №%s" % a[0][1]

				else:
					cursor.execute('select * from labmembers where userID = %s limit 1' % u.id)
					a = cursor.fetchall()
					if a:
						join_date = datetime.datetime.fromtimestamp(a[0][2])
						emb.description = "Лабмембер №%s" % a[0][0]
					else:
						join_date = datetime.datetime.now()
						emb.description = "Лабмембер №`<N/A>`"

				embDays = (datetime.datetime.now() - join_date).days

				def isYa(num):
					return (num%10 > 1) and (num%10 < 5) and ((num//10 == 0) or (num//10 > 1))

				def dateParse(days):
					res = ''
					years, days = days//365, days%365
					if years > 0:
						if years == 1:
							res = "1 год"
						elif (years > 1) and (years < 5):
							res = "%s года" % years
						else:
							res = "%s лет" % years
					months, days = days//30, days%30
					if months > 0:
						if months == 1:
							res = ', '.join([res, "1 месяц"])
						elif isYa(months):
							res = ', '.join([res, "%s месяца" % months])
						else:
							res = ', '.join([res, "%s месяцев" % months])
					if days > 0:
						if days == 1:
							res = ', '.join([res, "1 день"])
						elif isYa(days):
							res = ', '.join([res, "%s дня" % days])
						else:
							res = ', '.join([res, "%s дней" % days])

					if res.startswith(', '):
						res = res[2:]
						if res.startswith(', '):
							res = res[2:]

					if res == '':
						res = 'Ни одного дня'
					return res

				emb.add_field(name="На сервере:", value=dateParse(embDays), inline=False)
			else:
				cursor.execute('select * from labbots where botID = %s limit 1' % u.id)
				a = cursor.fetchall()
				if a:
					emb.description = "Бот №%s" % a[0][1]
				else:
					emb.description = "Бот №`<N/A>`"

			emb.add_field(name="Основная роль:", value='%s (#%02x%02x%02x)' % (norole and "Без роли" or u.top_role.name, *color), inline=True)
			if kurisu.prefs.Roles.get('alpaca') in u.roles:
				cursor.execute('select * from alpaca where userID = %s limit 1' % u.id)
				a = cursor.fetchall()
				t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
				pt = kurisu.prefs.parse_time(t.timetuple())
				pt = '%s %s' % (pt[0], pt[1])
				emb.add_field(name="Альпакамен", value="до %s" % pt, inline=True)
			roles = [r.name for r in u.roles[::-1][:-1] if r != u.top_role]
			if len(roles) > 0:
				emb.add_field(name="Остальные роли", value=", ".join(roles), inline=False)
			emb.set_thumbnail(url=kurisu.prefs.avatar_url(u))
			await ctx.send(embed=emb)

			conn.close()


def setup(bot):
	bot.remove_command("help")
	bot.add_cog(FGL(bot))
