from discord.ext import commands
import datetime, sqlite3, random
import kurisu.prefs, kurisu.check
import salieri.tasks


def unixTime(dt):
	return (dt - datetime.datetime(1970, 1, 1)).total_seconds()


class Upa(commands.Cog, name='zalUPA'):
	"""Команды, доступные только администраторам и модераторам"""

	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	@kurisu.check.is_upa()
	async def alpaca(self, ctx):
		"""Временный мут"""
		if ctx.invoked_subcommand is None:
			await ctx.send('У `!alpaca` нет подкоманды %s. Посмотри `!help alpaca`.' % ctx.subcommand_passed)

	@alpaca.command()
	async def add(self, ctx, user: str, time: str, *reas):
		"""Делает пользователя Альпакаменом

		Аргументы:
		-----------
		user : `discord.Member`
			Упоминание пользователя. Не ID. Не ник. Именно упоминание.
		time : `str`
			Время, на которое пользователь станет Альпакаменом. По дефолту 2 года.
			Минимум: 2 минуты. Максимум: 2 года.
			Формат: "??s:??m:??h" или "??с:??м:??ч". Пожалуйста, не используйте их вместе.
			Интересный факт. 2 года ~ 17520 часов.
		"""
		reas = ' '.join(reas)
		user = user.replace('!', '')
		if not kurisu.prefs.Channels.get('lab').permissions_for(ctx.author).view_audit_log:
			return
		u = ctx.guild.get_member(int(user[2:-1]))
		if kurisu.prefs.Roles.get('alpaca') in u.roles:
			await ctx.send("%s и так Альпакамен." % u.mention)
			return

		now = datetime.datetime.now()
		end = now
		time = time.split(':')
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
					if not 'kurisu.alpaca.alpacaLoop' in salieri.tasks.allTasks:
						await ctx.send("Я не могу это сделать, так как задача `alpaca.alpacaLoop` не запущена. Прости.")
						return

				if end < now + datetime.timedelta(minutes=2):
					end = now + datetime.timedelta(minutes=2)
		except:
			await ctx.send("%s, ты точно указал время ЧИСЛАМИ?" % ctx.message.author.mention)
			return

		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('insert into alpaca (userID, date) values (%s, %s)' % (u.id, unixTime(end)))
		await u.add_roles(kurisu.prefs.Roles.get('alpaca'), reason=str(reas))
		pt = kurisu.prefs.parse_time(end.timetuple())
		pt = '%s %s' % (pt[0], pt[1])
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(u))
		tmpEmbed.add_field(name="Причина", value=reas, inline=False)
		tmpEmbed.add_field(name="Никнейм", value=u)
		tmpEmbed.add_field(name="Дата/время до", value=pt)
		tmpEmbed.title = "Лабмем стал Альпакаменом"
		tmpEmbed.set_image(url='https://i.imgur.com/YxaYHWy.gif')
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)
		conn.commit()
		conn.close()

	@alpaca.command()
	async def remove(self, ctx, *users: str):
		"""Делает Альпакамена пользователем
		
		Аргументы:
		-----------
		users : [`discord.Member`]
			Массив упоминаний Альпакаменов. Не ID. Не ников. Именно упоминаний.
		"""
		if not kurisu.prefs.Channels.get('lab').permissions_for(ctx.author).view_audit_log:
			return
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		for u in ctx.message.mentions:
			if not (kurisu.prefs.Roles.get('alpaca') in u.roles):
				await ctx.send("%s и так просто пользователь." % u.mention)
				return
			cursor.execute('delete from alpaca where userID = %s' % u.id)
			await u.remove_roles(kurisu.prefs.Roles.get('alpaca'))

			gifs = [
				'https://i.imgur.com/wupSJAh.gif',
				'https://i.imgur.com/Jjzy14a.gif',
				'https://i.imgur.com/GvOWc77.gif'
			]

			tmpEmbed = kurisu.prefs.Embeds.new('welcome')
			tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(u))
			tmpEmbed.add_field(name="Никнейм", value=u)
			tmpEmbed.title = "Альпакамен стал лабмемом"
			tmpEmbed.set_image(url=random.choice(gifs))
			await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)
		conn.commit()
		conn.close()


def setup(bot):
	bot.add_cog(Upa(bot))
