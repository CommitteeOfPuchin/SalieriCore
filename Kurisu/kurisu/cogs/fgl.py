import inspect, re
from discord.ext import commands
import discord
import kurisu.prefs
import datetime

_mentions_transforms = {
	'@everyone': '@\u200beveryone',
	'@here': '@\u200bhere'
	}

_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

class FGL:
	"""Просто все подряд, десу"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def help(self, ctx, *cmd: str):
		"""Показывает данное сообщение"""
		bot = ctx.bot
		destination = ctx.message.author if bot.pm_help else ctx.message.channel

		def repl(obj):
			return _mentions_transforms.get(obj.group(0), '')

		# help by itself just lists our own commands.
		if len(cmd) == 0:
			helpEmbed = bot.formatter.format_help_for(ctx, bot)
		elif len(cmd) == 1:
			# try to see if it is a cog name
			name = _mention_pattern.sub(repl, cmd[0])
			command = None
			if name in bot.cogs:
				command = bot.cogs[name]
			else:
				command = bot.commands.get(name)
				if command is None:
					await bot.send_message(destination, "Команда %s не найдена." % name)
					return

			helpEmbed = bot.formatter.format_help_for(ctx, command)
		else:
			name = _mention_pattern.sub(repl, cmd[0])
			command = bot.commands.get(name)
			if command is None:
				await bot.send_message(destination, "Команда %s не найдена." % name)
				return

			for key in cmd[1:]:
				try:
					key = _mention_pattern.sub(repl, key)
					command = command.commands.get(key)
					if command is None:
						await bot.send_message(destination, "Подкоманда %s не найдена." % key)
						return
				except AttributeError:
					await bot.send_message(destination, "Команда %s не имеет подкоманд." % name)
					return

			helpEmbed = bot.formatter.format_help_for(ctx, command)

		if bot.pm_help is None:
			characters = sum(map(lambda l: len(l), pages))
			# modify destination based on length of pages.
			if characters > 1000:
				destination = ctx.message.author

		await bot.send_message(destination, embed=helpEmbed)

	@commands.command()
	async def status(self):
		stats = kurisu.prefs.info()

		emb = kurisu.prefs.Embeds.new('normal')
		emb.add_field(name = 'Статистика', value='CPU: {d[0]}%\nRAM Total: {d[1]}MB\nRAM Used: {d[2]}MB\nTemp: {d[4]}`C\nUptime: {d[5]}'.format(d=stats))

		await self.bot.say(embed = emb)

	@commands.command(pass_context=True)
	async def info(self, ctx):
		if len(ctx.message.mentions) == 0:
			users = [ctx.message.author]
		else:
			users = ctx.message.mentions

		for u in users:
			emb = kurisu.prefs.Embeds.new('normal')
			emb.colour = u.colour
			emb.title = '%s%s%s' % (u,  "" if (u.name == u.display_name) else (" a.k.a %s" % u.display_name), u.bot and " [BOT]" or '')
			emb.add_field(name="ID:", value=u.id)
			embDays = (datetime.datetime.now() - u.joined_at).days
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

			emb.add_field(name="На сервере:", value=dateParse(embDays))
			r, g, b = u.top_role.colour.to_tuple()
			emb.add_field(name="Основная роль:", value='%s (#%02x%02x%02x)' % ((u.top_role.name == "@everyone" and "Без роли" or u.top_role.name), r, g, b))
			roles = [r.name for r in u.roles[::-1][:-1] if r != u.top_role]
			if len(roles) > 0:
				emb.add_field(name="Остальные роли", value=", ".join(roles))
			emb.set_thumbnail(url=u.avatar_url)
			await self.bot.say(embed=emb)

def setup(bot):
	bot.remove_command("help")
	bot.add_cog(FGL(bot))
