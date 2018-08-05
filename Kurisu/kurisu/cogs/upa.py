from discord.ext import commands
import discord, time, datetime, sqlite3
import kurisu.prefs
import kurisu.tasks

def unixTime(dt):
	return (dt - datetime.datetime(1970,1,1)).total_seconds()

class Upa:
	"""Команды, доступные только администраторам и модераторам"""

	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def alpaca(self, ctx):
		"""Временный мут"""
		if not ctx.message.author.server_permissions.view_audit_logs:
			await self.bot.say("Ты не можешь это сделать, ты не модератор/администратор.")
			return
		if ctx.invoked_subcommand is None:
			await self.bot.say('У `!alpaca` нет подкоманды %s. Посмотри `!help alpaca`.' % ctx.subcommand_passed)

	@alpaca.command(pass_context=True)
	async def add(self, ctx, user: str, *time: str):
		"""Делает пользователя Альпакаменом

		Аргументы:
		-----------
		user : `discord.Member`
			Упоминание пользователя. Не ID. Не ник. Именно упоминание.
		time : `str`
			Время, на которое пользователь станет Альпакаменом. По дефолту 2 года.
			Минимум: 2 минуты. Максимум: 2 года.
			Формат: "??s ??m ??h" или "??с ??м ??ч". Пожалуйста, не используйте их вместе.
			Интересный факт. 2 года ~ 17520 часов.
		"""
		if not ctx.message.author.server_permissions.view_audit_logs:
			return

		u = ctx.message.server.get_member(user[2:-1])
		if kurisu.prefs.Roles.alpaca in u.roles:
			await self.bot.say("%s и так Альпакамен." % u.mention)
			return

		now = datetime.datetime.now()
		end = now
		if len(time) == 0:
			time = ['17520h']
		
		try:
			for t in time:
				if (t[-1] == 's') or (t[-1] == 'с'):
					end = end + datetime.timedelta(seconds=int(t[:-1]))
				if (t[-1] == 'm') or (t[-1] == 'м'):
					end = end + datetime.timedelta(minutes=int(t[:-1]))
				if (t[-1] == 'h') or (t[-1] == 'ч'):
					end = end + datetime.timedelta(hours=int(t[:-1]))

				if end >= now + datetime.timedelta(hours=17520):
					end = now + datetime.timedelta(hours=17520)
				else:
					if not 'kurisu.alpaca.alpacaLoop' in kurisu.tasks.allTasks:
						await self.bot.say("Я не могу это сделать, так как задача `alpaca.alpacaLoop` не запущена. Прости.")
						return

				if end < now + datetime.timedelta(minutes=2):
					end = now + datetime.timedelta(minutes=2)
		except:
			await self.bot.say("%s, ты точно указал время ЧИСЛАМИ?" % ctx.message.author.mention)
			return

		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('insert into alpaca (userID, date) values (%s, %s)' % (u.id, unixTime(end)))
		await self.bot.add_roles(u, kurisu.prefs.Roles.alpaca)
		pt = kurisu.prefs.parse_time(end.timetuple())
		pt = '%s %s' % (pt[0], pt[1])
		await self.bot.say("%s стал Альпакаменом до *%s (МСК)*." % (u.mention, pt))
		conn.commit()
		conn.close()

	@alpaca.command(pass_context=True)
	async def remove(self, ctx, *users: str):
		"""Делает Альпакамена пользователем
		
		Аргументы:
		-----------
		users : [`discord.Member`]
			Массив упоминаний Альпакаменов. Не ID. Не ников. Именно упоминаний.
		"""
		if not ctx.message.author.server_permissions.view_audit_logs:
			return
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		for u in ctx.message.mentions:
			if not (kurisu.prefs.Roles.alpaca in u.roles):
				await self.bot.say("%s и так просто пользователь." % u.mention)
				return
			cursor.execute('delete from alpaca where userID = %s' % u.id)
			await self.bot.remove_roles(u, kurisu.prefs.Roles.alpaca)
			await self.bot.say("%s больше не Альпакамен." % u.mention)
		conn.commit()
		conn.close()

def setup(bot):
	bot.add_cog(Upa(bot))
