from discord.ext import commands
import kurisu.prefs, traceback

class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
 	  	 #if message.channel.id != "446333540381229066":
    	   #return

		if message.content == 'Nullpo':
			await self.bot.send_message(message.channel, 'Gah!')

	async def on_command_error(self, error: Exception, ctx: commands.Context):
		ignored = (commands.CommandNotFound, commands.UserInputError)

		if isinstance(error, ignored):
			return

		tmpEmbed = kurisu.prefs.Embeds.new('error')
		tb = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__, limit=5)
		tmpEmbed.add_field(name="Вызвал", value=ctx.message.author.mention)
		tmpEmbed.add_field(name="Сообщение", value=ctx.message.content)
		tmpEmbed.add_field(name="Traceback", value='%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))
		await self.bot.send_message(kurisu.prefs.Channels.log, embed=tmpEmbed)

		if isinstance(error, commands.BadArgument):
			await self.bot.send_message(ctx.message.channel, 'Ошибка в аргументе')
			return
		elif isinstance(error, commands.MissingRequiredArgument):
			await self.bot.send_message(ctx.message.channel, 'Недостаточно аргументов')
			return
		else:
			await self.bot.send_message(ctx.message.channel, 'Упс... Информация об ошибке в %s' % kurisu.prefs.Channels.log.mention)

	async def on_error(self, event, *args, **kwargs):
		print('Mew')
		tmpEmbed = kurisu.prefs.Embeds.new('error')
		tb = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__, limit=5)
		tmpEmbed.add_field(name="Вызвал", value=event)

		argsF = ['[%s] %s' % (i, val) for i, val in args]
		argsF = (len(argsF) == 0) and '*Нет*' or '\n'.join(argsF)
		kwargsF = ['[%s] %s' % (i, kwargs[i]) for i in kwargs]
		argsF = (len(kwargsF) == 0) and '*Нет*' or '\n'.join(kwargsF)

		tmpEmbed.add_field(name="Позиционные аргументы:", value=argsF, inline=True)
		tmpEmbed.add_field(name="Именованные аргументы:", value=argsF, inline=True)

		tmpEmbed.add_field(name="Traceback", value='%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))
		await self.bot.send_message(kurisu.prefs.Channels.log, embed=tmpEmbed)

def setup(bot):
	bot.add_cog(Events(bot))
