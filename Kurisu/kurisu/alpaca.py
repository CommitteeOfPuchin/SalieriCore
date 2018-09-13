import asyncio, datetime, sqlite3, random
from math import floor
import kurisu.prefs


async def alpacaLoop():
	gifs = [
		'https://i.imgur.com/wupSJAh.gif',
		'https://i.imgur.com/Jjzy14a.gif',
		'https://i.imgur.com/GvOWc77.gif'
	]
	lab = kurisu.prefs.Channels.get('lab')
	alpacaRole = kurisu.prefs.Roles.get('alpaca')
	fgl = kurisu.prefs.Servers.get('FGL')
	dealp = [False, 0]
	while True:
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		if dealp[0]:
			cursor.execute('delete from alpaca where userID = %s' % dealp[1])
			u = fgl.get_member(int(dealp[1]))
			try:
				await u.remove_roles(alpacaRole)
				tmpEmbed = kurisu.prefs.Embeds.new('welcome')
				tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(u))
				tmpEmbed.add_field(name="Никнейм", value=u)
				tmpEmbed.title = "Альпакамен стал лабмемом"
				tmpEmbed.set_image(url=random.choice(gifs))
				await lab.send(embed=tmpEmbed)
			except:
				tmpEmbed = kurisu.prefs.Embeds.new('alert')
				tmpEmbed.add_field(name="ID", value=dealp[1])
				tmpEmbed.title = "Альпакамен не смог стать лабмемом"
				tmpEmbed.set_image(url=random.choice(gifs))
				await lab.send(embed=tmpEmbed)
			dealp = [False, '']
			conn.commit()

		cursor.execute('select * from alpaca order by date asc limit 1')
		a = cursor.fetchall()
		if len(a) != 0:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			r = floor((t - datetime.datetime.now()).total_seconds())
			if r <= 60:
				dealp = [True, str(a[0][1])]
				dt = r
				kurisu.prefs.discordClient.log('Alpaca', 'Next unalpaca: %s' % r)
			else:
				dt = 60
		else:
			dt = 60
		conn.close()
		await asyncio.sleep(dt)
