import kurisu.nyaa, kurisu.tips, kurisu.prefs
import sqlite3, copy, time, os.path
from discord.ext import commands

class SteinsGate:
	"""Команды, связанные с Steins;Gate"""
	client = None

	def __init__(self, bot):
		self.client = bot

	@commands.command()
	async def tips(self, *tip: str):
		"""Поиск по TIPS Steins;Gate."""
		tip = ' '.join(tip)
		await kurisu.tips.search(tip, self.client)

	@commands.command()
	async def sg0(self, episode: int):
		"""Выводит список .torrent файлов."""
		tmpEmbed = kurisu.prefs.Embeds.new('SG0')
	
		# Nyaa
		res = {}
		conn = sqlite3.connect('torr_db.sqlite3')
		cursor = conn.cursor()

		cursor.execute("select title from episodes where id = %s" % episode)
		ep = cursor.fetchall()
		if len(ep) == 0:
 			await self.client.say('```Такой серии нет и не будет.```')
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
              
		tmpEmbed.add_field(name = 'nyaa.si', value = '\n'.join(nyaaField), inline = True)
		tmpEmbed.set_author(name = ep[0][0], icon_url='https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg')
		pt = kurisu.prefs.parse_time(time.localtime(os.path.getmtime('torr_db.sqlite3')))
		pt = '%s в %s' % (pt[0], pt[1][:-3])
		tmpEmbed.set_footer(text = 'Последнее обновление БД: %s' % pt)
		await self.client.say(embed = tmpEmbed)

	@commands.command()
	async def tips0(self, *tip: str):
		"""Поиск по TIPS Steins;Gate 0."""
		tip = ' '.join(tip)
		await kurisu.tips.search(tip, self.client, 0)

def setup(bot):
	bot.add_cog(SteinsGate(bot))
