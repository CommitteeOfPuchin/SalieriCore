import kurisu.prefs, sqlite3, datetime, random


class Events:
	def __init__(self, bot):
		self.bot = bot
		self.gifs = {'join': [
			'https://i.imgur.com/DcLOkLK.gif',
			'https://i.imgur.com/kVybxun.gif',
			'https://i.imgur.com/eqgYNr4.gif'
		], 'leave':[
			'https://i.imgur.com/72Al5af.gif',
			'https://i.imgur.com/YZ8Vf3B.gif',
			'https://i.imgur.com/kDrO4V7.gif'
		], 'ban':[
			'https://i.imgur.com/HC5ZgV0.gif',
			'https://i.imgur.com/KZXCtFB.gif',
			'https://i.imgur.com/N0zj21G.gif'
		], 'unban':
		[
			'https://i.imgur.com/wupSJAh.gif',
			'https://i.imgur.com/Jjzy14a.gif',
			'https://i.imgur.com/GvOWc77.gif'
		]}

	async def on_member_join(self, member):
		if member.guild != kurisu.prefs.Servers.get('FGL'):
			return
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('select * from alpaca where userID = %s limit 1' % member.id)
		a = cursor.fetchall()

		tmpEmbed = kurisu.prefs.Embeds.new('welcome')

		cursor.execute('select * from labmembers where userID = %s limit 1' % member.id)
		b = cursor.fetchall()
		if b:
			labmember = b[0][0]
			tmpEmbed.title = 'Лабмем №%s вернулся' % labmember
		else:
			cursor.execute('select * from labmembers order by number desc limit 1')
			b = cursor.fetchall()
			labmember = b[0][0] + 1

			cursor.execute('insert into labmembers (userID, number, join_date) values (%s, %s, %s)' % (member.id, labmember, member.joined_at.timestamp()))
			tmpEmbed.title = 'Лабмем №%s присоединился' % labmember
			conn.commit()

		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		if a:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			if t > datetime.datetime.now():
				pt = kurisu.prefs.parse_time(t.timetuple())
				pt = '%s %s' % (pt[0], pt[1])
				tmpEmbed.add_field(name="Альпакамен", value="до %s" % pt)
				await member.add_roles(kurisu.prefs.Roles.get('alpaca'))
			else:
				tmpEmbed.add_field(name="Альпакамен", value="Роль снята")
				cursor.execute('delete from alpaca where userID = %s' % member.id)
				conn.commit()
		tmpEmbed.set_image(url=random.choice(self.gifs['join']))
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)
		conn.close()

	async def on_member_remove(self, member):
		if member.guild != kurisu.prefs.Servers.get('FGL'):
			return
		if kurisu.prefs.ban_check(await kurisu.prefs.Servers.get('FGL').bans(), member):
			return
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		tmpEmbed.set_image(url=random.choice(self.gifs['leave']))
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)

	async def on_member_ban(self, guild, user):
		if guild != kurisu.prefs.Servers.get('FGL'):
			return
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.title = "Лабмем забанен"
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(user))
		tmpEmbed.add_field(name="Никнейм", value=user)
		tmpEmbed.add_field(name="ID", value=user.id)
		tmpEmbed.add_field(name="Причина", value=kurisu.prefs.ban_check(await kurisu.prefs.Servers.get('FGL').bans(), user)[0].reason)
		tmpEmbed.set_image(url=random.choice(self.gifs['ban']))

		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('delete from labmembers where userID = %s' % user.id)
		conn.commit()
		conn.close()

		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)

	async def on_member_unban(self, guild, user):
		if guild != kurisu.prefs.Servers.get('FGL'):
			return
		tmpEmbed = kurisu.prefs.Embeds.new('welcome')
		tmpEmbed.title = "Лабмем разбанен"
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(user))
		tmpEmbed.add_field(name="Никнейм", value=user)
		tmpEmbed.add_field(name="ID", value=user.id)
		tmpEmbed.set_image(url=random.choice(self.gifs['unban']))
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)


def setup(bot):
	bot.add_cog(Events(bot))
