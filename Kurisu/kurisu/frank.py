import discord, time, asyncio
import kurisu.prefs


async def loop():
  client = kurisu.prefs.discordClient
  channel = kurisu.prefs.Channels.lab
  frankEmbed = discord.Embed(colour = discord.Colour.blue())
  frankEmbed.title = "День рождения Frank-kun'а"
  while time.localtime()[6] == 3:
    i = 1 + (time.localtime()[3]) + (1 if time.localtime()[4] >= 30 else 0)
    frankEmbed.description = "Поздравляю тебя, Франк, %sй раз" % i
    
    await client.send_message(channel, '<@300386245349998605>')
    await client.send_message(channel, embed = frankEmbed)
    
    await asyncio.sleep(60*30)