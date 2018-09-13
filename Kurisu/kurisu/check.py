import asyncio
import kurisu.prefs
import salieri.core
from discord.ext import commands


def is_upa():
	async def pred(ctx):
		if kurisu.prefs.Roles.get('dev') not in ctx.author.roles:
			if ctx.author.guild_permissions.administrator:
				return True
			else:
				raise salieri.core.NoPerms('Ты не можешь это сделать, ты не модератор/администратор.')
		else:
			return True

	return commands.check(pred)


def is_senpai():
	async def pred(ctx):
		if ctx.author.id != 185459415514742784:
			raise salieri.core.NoPerms('Ты не можешь это сделать, ты не сенпай.')
		else:
			return True

	return commands.check(pred)