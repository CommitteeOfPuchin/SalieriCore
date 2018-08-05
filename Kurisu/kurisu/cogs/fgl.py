import inspect, re
from discord.ext import commands
import discord
import kurisu.prefs

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

def setup(bot):
	bot.remove_command("help")
	bot.add_cog(FGL(bot))
