import discord, copy, os, datetime

def parse_time(dt):
    months = ['янв.', 'фев.', 'мар.', 'апр.', 'мая', 'июня', 'июля', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']
    
    return ['%s %s %s' % (dt[2], months[dt[1]-1], dt[0]),  '%s:%s:%s' % (str(dt[3]).zfill(2), str(dt[4]).zfill(2), str(dt[5]).zfill(2))]

def parse_delta(dt):
	s, d = dt.seconds, dt.days
	if d == 1:
		ds = "день"
	else:
		ds = "дней"
	h, s = s//3600, s%3600
	m, s = s//60, s%60

	return '%s %s, %s:%s:%s' % (tuple([str(d), ds, str(h).zfill(2), str(m).zfill(2), str(s).zfill(2)]))
	
def avatar_url(member):
	return 'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.{1}'.format(member, 'png')

def info():
	info = []
	info.append(str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2)))
	info.extend(map(str, os.popen('free -t -m').readlines()[-1].split()[1:]))
	info.append(os.popen('vcgencmd measure_temp').readline())
	info[4] = info[4][info[4].index('=') + 1:info[4].rindex("'")]
	info.append(parse_delta(datetime.datetime.now()-startup))

	return info

discordClient = None
startup = None

class Servers:
	FGL = discord.Server(id='380104197267521537')

class Embeds:
	error = discord.Embed(colour = discord.Colour.red())
	alert = discord.Embed(colour = discord.Colour.gold())
	normal = discord.Embed(colour = discord.Colour.dark_red())

	welcome = discord.Embed(colour = discord.Colour.green())
	welcome.title = "Новый Лабмем"

	goodbye = discord.Embed(colour = discord.Colour.red())
	goodbye.title = "Лабмем вышел"

	nyaa = discord.Embed(colour = discord.Colour.dark_red())
	dsgt = discord.Embed(colour = discord.Colour.dark_red())

	SG0 = discord.Embed(colour = discord.Colour.dark_red())

	def new(name):
		try:
			return copy.deepcopy(getattr(Embeds, name))
		except:
			return False

class Channels:
	news = discord.Channel(id='430365781721743362', server=Servers.FGL)
	lab = discord.Channel(id='380104197837815811', server=Servers.FGL)
	log = discord.Channel(id='474683293304881175', server=Servers.FGL)
	dev = discord.Channel(id='446333540381229066', server=Servers.FGL)

class Roles:
	alpaca = discord.Role(id = "474224730245955584", server=Servers.FGL)

def init():
	Embeds.error.set_author(name = "Я ОШИБКА!!", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")
	Embeds.alert.set_author(name = "Amadeus Systems", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")
	Embeds.normal.set_author(name = "Amadeus Systems", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")

	Embeds.nyaa.set_thumbnail(url = 'https://sun9-6.userapi.com/c840635/v840635891/7bad7/o7JkD2yf8lg.jpg')
	Embeds.nyaa.set_author(name = 'Новые раздачи')

	Embeds.dsgt.set_author(name = 'Amadeus System || Трансляция', icon_url='https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg')
	Embeds.dsgt.set_thumbnail(url = 'https://pp.userapi.com/c846520/v846520774/54eed/7GAYm3VeAkk.jpg')
	Embeds.dsgt.add_field(name = 'Disgusting Otaku', value = 'В 19:00 начинается трансляция нового эпизода на [dsgstng.com](https://dsgstng.com).\nНе пропустите! <:LeskisMirk:443050078047830018>')

	Embeds.SG0.set_thumbnail(url = 'https://sun9-6.userapi.com/c840635/v840635891/7bad7/o7JkD2yf8lg.jpg')
