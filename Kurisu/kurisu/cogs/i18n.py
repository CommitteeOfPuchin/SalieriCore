from discord.ext import commands
import kurisu.prefs
import datetime, sqlite3


class i18n(commands.Cog, name='Internationalization'):
	"""Интернационализация - и17я"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def locale(self, ctx, loc):
		if loc in kurisu.prefs.supported_locales:
			kurisu.prefs.locale = loc
			await ctx.send(kurisu.prefs.i18n(self, 'success') % loc)
		else:
			await ctx.send(kurisu.prefs.i18n(self, 'av') % ', '.join(kurisu.prefs.supported_locales))

def setup(bot):
	bot.add_cog(i18n(bot))