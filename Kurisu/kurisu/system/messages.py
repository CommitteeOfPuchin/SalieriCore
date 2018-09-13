from discord.ext import commands
from discord.ext.commands import errors
import kurisu.prefs, traceback
import salieri.core


class Events(commands.Cog, name='System.messages'):
	def __init__(self, bot):
		self.bot = bot
    
	async def on_message(self, message):
		# if message.channel.id != "446333540381229066":
			# return

		if message.content == 'Nullpo':
			await message.channel.send('Gah!')
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		ignored = (commands.errors.CommandNotFound, commands.errors.UserInputError)

		if isinstance(error, ignored):
			return

		tmpEmbed = kurisu.prefs.Embeds.new('error')
		tb = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__, limit=5)
		tmpEmbed.add_field(name="Вызвал", value=ctx.message.author.mention)
		tmpEmbed.add_field(name="Сообщение", value=ctx.message.content)
		tmpEmbed.add_field(name="Traceback", value='%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))

		if isinstance(error, commands.errors.BadArgument):
			await ctx.send('Ошибка в аргументе')
			return
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send('Недостаточно аргументов')
			return
		elif isinstance(error, salieri.core.NoPerms):
			await ctx.send(error)
		else:
			#await ctx.send('Упс... Информация об ошибке в %s' % kurisu.prefs.Channels.log.mention)
			await ctx.send(embed=tmpEmbed)


def setup(bot):
	bot.add_cog(Events(bot))
