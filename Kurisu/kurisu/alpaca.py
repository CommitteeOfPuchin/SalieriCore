import discord, asyncio, time, datetime, sqlite3
from math import floor
import kurisu.prefs

ibn = kurisu.prefs.Channels.dev
alpacaRole = kurisu.prefs.Roles.alpaca
dealp = [False,'']

async def alpacaLoop():
	client = kurisu.prefs.discordClient
	dealp = [False, 0]
	while True:
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		if dealp[0]:
			cursor.execute('delete from alpaca where userID = %s' % dealp[1])
			s = client.get_server('380104197267521537')
			u = s.get_member(dealp[1])
			try:
				await client.remove_roles(u, alpacaRole)
				await client.send_message(ibn, "%s больше не Альпакамен." % u.mention)
			except:
				await client.send_message(ibn, "Пользователь с ID %s покинул сервер до снятия роли." % dealp[1])
			dealp = [False, '']
			conn.commit()

		cursor.execute('select * from alpaca order by date asc limit 1')
		a = cursor.fetchall()
		if len(a) != 0:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			r = floor((t - datetime.datetime.now()).total_seconds())
			if r <= 60:
				dealp =  [True, str(a[0][1])]
				dt = r
				print(r)
			else:
				dt = 60
		else:
			dt = 60
		conn.close()
		await asyncio.sleep(dt)
