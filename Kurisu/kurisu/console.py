import discord
from aioconsole import ainput

import kurisu.prefs

async def consoleIO():
	client = kurisu.prefs.discordClient
	channels = ['', '', '', '', '', '', '', '', '', '', '']
	channelID = await ainput('Channel ID: ')
	test = False
	if channelID == '':
		print('Режим только тестового канала активирован')
		test = True
	else:
		channels[0] = discord.Channel(id=channelID, server=discord.Server(id='380104197267521537'))
	
	channels[10] = discord.Channel(id='446333540381229066', server=discord.Server(id='380104197267521537'))
	while True:
		stdin = await ainput('>> ')
		if stdin[0] == '/':
			if stdin[1] == '!':
				preset = [
									'446333540381229066',
									'380104197837815811',
									'430365781721743362',
									'380110041526829076'
								]
				i = 0
				for c in preset:
					channels[i] = client.get_channel(c)
					i += 1
					
				test = False
				print('Пресет "Steins;Gate" установлен')

			if stdin[1] == 'g':
				await client.change_presence(game=discord.Game(name=stdin[3:], type=3))
				print('Game Presence изменен на %s' % stdin[3:])

			if stdin[1] == 'c':
				attr = stdin[3:].split()
				if len(attr) == 1:
					attr = [attr[0], '0']
				attr[1] = int(attr[1])
				
				channels[attr[1]] = client.get_channel(attr[0])
				if channels[attr[1]] is None:
					print('Канал с ID %s не найден' % attr[0])
				else:
					print('Канал %s изменен на #%s (%s)' % (attr[1], channels[attr[1]].name, attr[0]))

				if test:
					test = False
					print('Режим только тестового канала деактивирован')

			if stdin[1] == 't':
				await client.send_message(channels[10], stdin[3:])

			if stdin[1] == 'a':
				for i in range(10):
					channels[i] = ''
				
				test = True
				print('Режим только тестового канала активирован')

			if stdin[1] == 'l':
				for i in range(10):
					print('%s | #%s' % (i, channels[i] == '' and '---' or channels[i].name))

			continue

		if test:
			await client.send_message(channels[10], stdin)
		else:
			if stdin[0].isdigit():
				channel = channels[int(stdin[0])]
				text = stdin[2:]
			else:
				channel = channels[0]
				text = stdin

			await client.send_message(channel, text)
