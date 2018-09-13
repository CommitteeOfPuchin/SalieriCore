import kurisu.nyaa, kurisu.tips, kurisu.prefs
import sqlite3, time, os.path
from discord.ext import commands
import kurisu.check


class RolePlay(commands.Cog, name='ERP Core'):
	"""Команды, связанные с ролплеем"""

	def __init__(self, bot):
		self.client = bot
		self.dev = kurisu.prefs.Channels.get('dev')
		self.guild = kurisu.prefs.Servers.get('FGL')

	@commands.group()
	async def rp(self, ctx):
		"""Ролплей

		Оставить заявку на ролплей
		"""

		u = ctx.message.author
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				conn = sqlite3.connect('db.sqlite3')
				cursor = conn.cursor()
				cursor.execute('SELECT status FROM roleplay WHERE userID = %s' % u.id)

				cf = cursor.fetchall()
				if cf:
					u_status = int(cf[0][0])
					if u_status == 0:
						await ctx.send('Ваша заявка на рассмотрении.')
					elif u_status == -1:
						await ctx.send('Ваша заявка отклонена/вы заблокированы в РП.')
					else:
						await ctx.send('Ваша заявка принята.')

				else:
					cursor.execute('insert into roleplay (userID, status) values (%s, 0)' % u.id)
					await ctx.send('Заявка принята на рассмотрение.')
					conn.commit()

				conn.close()
			else:
				await ctx.send('У `!rp` нет подкоманды %s. Посмотри `!help rp`.' % ctx.subcommand_passed)

	@rp.command()
	@kurisu.check.is_upa()
	async def a(self, ctx):
		"""Принять заявку

		Аргументы:
		-----------
		users: [`discord.Member`]
			Массив упоминаний пользователей.
			Если нет ни одного упоминания, используется автор сообщения.
		"""

		if len(ctx.message.mentions) == 0:
			await ctx.send('Приведи пользователей.')
			return
		else:
			users = ctx.message.mentions

		for u in users:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			cursor.execute('SELECT status FROM roleplay WHERE userID = %s' % u.id)

			cf = cursor.fetchall()
			if cf:
				u_status = int(cf[0][0])
				if u_status == 0:
					cursor.execute('update roleplay set status = 1 where userID = %s' % u.id)
					await u.add_roles(kurisu.prefs.Roles.get('RP'))
					await ctx.send('Заявка %s принята.' % u.mention)
					await self.dev.send('%s, ваша заявка принята. Добро пожаловать.' % u.mention)
				else:
					await ctx.send('У нас нет заявки от %s' % u.mention)
			else:
				await ctx.send('У нас нет заявки от %s' % u.mention)
			conn.commit()
			conn.close()

	@rp.command()
	@kurisu.check.is_upa()
	async def d(self, ctx):
		"""Отклонить заявку/Заблокировать

		Аргументы:
		-----------
		users: [`discord.Member`]
			Массив упоминаний пользователей.
			Если нет ни одного упоминания, используется автор сообщения.
		"""

		if len(ctx.message.mentions) == 0:
			await ctx.send('Приведи пользователей.')
			return
		else:
			users = ctx.message.mentions

		for u in users:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			cursor.execute('SELECT status FROM roleplay WHERE userID = %s' % u.id)

			cf = cursor.fetchall()
			if cf:
				u_status = int(cf[0][0])
				if u_status > -1:
					cursor.execute('update roleplay set status = -1 where userID = %s' % u.id)

					if kurisu.prefs.Roles.get('RP') in u.roles:
						await u.remove_roles(kurisu.prefs.Roles.get('RP'))
						await ctx.send('%s заблокирован в РП.' % u.mention)
						await self.dev.send('%s, вы заблокированы в РП.' % u.mention)
					else:
						await ctx.send('Заявка %s отклонена.' % u.mention)
						await self.dev.send('%s, ваша заявка отклонена.' % u.mention)

				else:
					await ctx.send('У нас нет заявки от %s' % u.mention)
			else:
				await ctx.send('У нас нет заявки от %s' % u.mention)
			conn.commit()
			conn.close()

	@rp.command()
	async def list(self, ctx):
		"""Возвращает списки участников"""
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('SELECT userID, status FROM roleplay')
		cf = cursor.fetchall()

		tmpEmbed = kurisu.prefs.Embeds.new('normal')

		if cf:
			def u_sel(y):
				tmp = [str(self.guild.get_member(id)) for id in [i[0] for i in cf if eval(y)]]
				return [i for i in tmp if str(i) != 'None']

			u_approved = u_sel('i[1] > 0')
			u_block = u_sel('i[1] == -1')
			u_pending = u_sel('i[1] == 0')

			if u_approved:
				tmpEmbed.add_field(name='Принято', value='\n'.join(u_approved), inline=True)

			if u_pending:
				tmpEmbed.add_field(name='Заявки', value='\n'.join(u_pending), inline=True)

			if u_block:
				tmpEmbed.add_field(name='Отклонено', value='\n'.join(u_block), inline=True)
		else:
			tmpEmbed.add_field(name='Заявки', value='`Пусто`')

		await ctx.send(embed=tmpEmbed)


def setup(bot):
	bot.add_cog(RolePlay(bot))
