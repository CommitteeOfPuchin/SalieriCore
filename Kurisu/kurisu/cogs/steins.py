import kurisu.nyaa, kurisu.tips, kurisu.prefs
import sqlite3, time, os.path
from discord.ext import commands


class SteinsGate(commands.Cog, name='Штаны Гея'):
	"""Команды, связанные с Steins;Gate"""
	client = None

	def __init__(self, bot):
		self.client = bot

	@commands.command(name='sub')
	async def sg_sub(self, ctx):
		"""Подписка на события, связанные с трансляциями и торрентами S;G 0.

		`Команда не принимает аргументы.`
		"""

		u = ctx.message.author
		r = kurisu.prefs.Roles.get('sub')

		if r not in u.roles:
			await u.add_roles(r, reason='Желание %s' % u.display_name)
			await ctx.message.channel.send('Вы подписались на уведомления.')

		else:
			await ctx.message.channel.send('Вы уже подписались на уведомления.')

	@commands.command(name='unsub')
	async def sg_unsub(self, ctx):
		"""Отписка от событий, связанных с трансляциями и торрентами S;G 0.

		`Команда не принимает аргументы.`
		"""

		u = ctx.message.author
		r = kurisu.prefs.Roles.get('sub')

		if r in u.roles:
			await u.remove_roles(r, reason='Желание %s' % u.display_name)
			await ctx.message.channel.send('Вы отписались от уведомлений.')

		else:
			await ctx.message.channel.send('Вы и так не подписаны на уведомления.')

	@commands.command()
	async def tips(self, ctx, *tip: str):
		"""Поиск по TIPS Steins;Gate.

		Аргументы:
		-----------
		tip: `str`
			TIP, который нужно найти.
		"""
		tip = ' '.join(tip)
		await kurisu.tips.search(tip, ctx)

	@commands.command()
	async def sg0(self, ctx, episode: int):
		"""Выводит список .torrent файлов.

		Аргументы:
		-----------
		episide: `int`
			Номер запрашиваемого эпизода.
		"""
		tmpEmbed = kurisu.prefs.Embeds.new('SG0')

		# Nyaa
		res = {}
		conn = sqlite3.connect('torr_db.sqlite3')
		cursor = conn.cursor()

		cursor.execute("select title from episodes where id = %s" % episode)
		ep = cursor.fetchall()
		if len(ep) == 0:
			await ctx.send('```Такой серии нет и не будет.```')
			return "Fuck"

		for dl in kurisu.nyaa.nyaa_dls:
			cursor.execute('select dl, link, seeders, leechers from torrents where episode = %s and dl = "%s"' % (episode, dl))
			res[dl] = cursor.fetchall()

		conn.close()
		nyaaField = []
		for tmp in list(res.values()):
			if len(tmp) > 0:
				tmp = tmp[0]
				nyaaField.append('[%s](https://nyaa.si/download/%s.torrent) | %s/%s' % (tmp[0], tmp[1], tmp[2], tmp[3]))

			if len(nyaaField) == 0:
				nyaaField.append('Эпизода еще нет на nyaa.si')

		tmpEmbed.add_field(name='nyaa.si', value='\n'.join(nyaaField), inline = True)
		tmpEmbed.title = ep[0][0]
		pt = kurisu.prefs.parse_time(time.localtime(os.path.getmtime('torr_db.sqlite3')))
		pt = '%s в %s' % (pt[0], pt[1][:-3])
		tmpEmbed.set_footer(text='Последнее обновление БД: %s' % pt)
		await ctx.send(embed=tmpEmbed)

	@commands.command()
	async def tips0(self, ctx, *tip: str):
		"""Поиск по TIPS Steins;Gate 0.

		Аргументы:
		-----------
		tip: `str`
			TIP, который нужно найти.
		"""
		tip = ' '.join(tip)
		await kurisu.tips.search(tip, ctx, 0)


def setup(bot):
	bot.add_cog(SteinsGate(bot))
