from discord.ext import commands
import kurisu.prefs, sqlite3, datetime

class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_member_join(self, member):
		if member.server.id != kurisu.prefs.Servers.FGL.id:
			return
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('select * from alpaca where userID = %s limit 1' % member.id)
		a = cursor.fetchall()

		tmpEmbed = kurisu.prefs.Embeds.new('welcome')
		tmpEmbed.set_thumbnail(url=member.avatar_url)
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		if len(a) != 0:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			if t > datetime.datetime.now():
				pt = kurisu.prefs.parse_time(t.timetuple())
				pt = '%s %s' % (pt[0], pt[1])
				tmpEmbed.add_field(name="Альпакамен", value="до %s" % pt)
				await client.add_roles(member, kurisu.prefs.Roles.alpaca)
			else:
				tmpEmbed.add_field(name="Альпакамен", value="Роль снята")
				cursor.execute('delete from alpaca where userID = %s' % member.id)
				conn.commit()
		tmpEmbed.set_image(url="https://i.imgur.com/DcLOkLK.gif")
		await self.bot.send_message(kurisu.prefs.Channels.lab, embed=tmpEmbed)
		conn.close()

	async def on_member_remove(self, member):
		if member.server.id != kurisu.prefs.Servers.FGL.id:
			return
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.set_thumbnail(url=member.avatar_url)
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		tmpEmbed.set_image(url="https://i.imgur.com/wupSJAh.gif")
		await self.bot.send_message(kurisu.prefs.Channels.lab, embed=tmpEmbed)


def setup(bot):
	bot.add_cog(Events(bot))
