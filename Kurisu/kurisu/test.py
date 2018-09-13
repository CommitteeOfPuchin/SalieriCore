import asyncio
import kurisu.prefs

test = True


async def loop():
	"""Просто пишет Hello World

	Больше ничего
	"""
	client = kurisu.prefs.discordClient
	i = 0
	while True:
		await client.send_message(kurisu.prefs.Channels.lab, "Hello World #%s" % str(i))
		i = i + 1
		await asyncio.sleep(10)
