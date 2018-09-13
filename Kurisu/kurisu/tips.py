import discord, copy

from .search import *

k_ru = [[], []]
k_eng = [[], []]
k = [[], []]
tips = [[], []]
kirill = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

tipsEmbed = discord.Embed(colour = discord.Colour.dark_red())
tipsEmbed.set_thumbnail(url = 'https://pp.userapi.com/c831208/v831208232/1655b0/KlMKUSjaQws.jpg')


def unif(s):
	return s.replace('.', '').replace(' ', '').replace('-', '').lower()


def init():
	with open('tips0.txt', 'r') as f:
		tmp = [row.strip() for row in f]
		for i in range(len(tmp)//3):
			k_ru[0].append(unif(tmp[i*3]))
			k[0].append(tmp[i*3])
			k_eng[0].append(unif(tmp[i*3+1]))
			tips[0].append(tmp[i*3+2])

	with open('tips.txt', 'r') as f:
		tmp = [row.strip() for row in f]
		for i in range(len(tmp)//3):
			k_ru[1].append(unif(tmp[i*3]))
			k[1].append(tmp[i*3])
			k_eng[1].append(unif(tmp[i*3+1]))
			tips[1].append(tmp[i*3+2])


async def search(tip, discordClient, sg=1):
	tip = unif(tip)
	await discordClient.say('Ищу...')
	rus = len([x for x in kirill if x in tip]) > 0 and True or False
	
	s = rus and k_ru[sg] or k_eng[sg]

	try:
		i = s.index(tip)
		tip = tips[sg][i].split('|')
		t = "TIPS"
	except:
		await discordClient.say('Четкий поиск не дал результатов. Запускаю нечеткий поиск...')
		
		test = ['', 99999]
		for t in s:
			tmp = distance_3(t, tip)[0]
			if tmp < test[1]:
				test = [t, tmp]
		
		perc = (1 - float(test[1]) / float(len(test[0])))*100
		if perc < 85:
			if test[1] > 2:
				await discordClient.say('Ничего не найдено. Попробуйте точнее.')
			else:
				await discordClient.say('Я слишком неуверена...\n*Вероятность: %.2f%%*' % perc)
			return False
		t = "TIPS | %.2f%%" % perc
		i = s.index(test[0])
		tip = tips[sg][i].split('|')

	tip[1] = tip[1].replace('[linebreak]', '\n')

	tmpEmbed = copy.deepcopy(tipsEmbed)
	tmpEmbed.set_author(name=t, icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")
	tmpEmbed.add_field(name=k[sg][i], value=tip[1], inline=True)
	tmpEmbed.set_footer(text=tip[0])
	await discordClient.say(embed=tmpEmbed)
