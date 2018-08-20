from lxml import html
import asyncio, sqlite3, urllib.request, discord
import time, datetime, copy, os.path, aiohttp

templates = {'HorribleSubs': ['[HorribleSubs] Steins Gate 0 - ', ' [1080p].mkv'], 'Erai-raws': ['[Erai-raws] Steins;Gate 0 - ', ' [1080p].mkv']}
nyaa_dls = ['HorribleSubs', 'Erai-raws']

import kurisu.prefs

dsgt = False

async def getPage(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch():
    channel = kurisu.prefs.Channels.news
    client = kurisu.prefs.discordClient
    dsgtEmbed = kurisu.prefs.Embeds.dsgt
    global dsgt
    while True:
      new = []
      if dsgt:
        pt = kurisu.prefs.parse_time(time.localtime(os.path.getmtime('torr_db.sqlite3')))
        pt = '%s в %s' % (pt[0], pt[1][:-3])
        dsgtEmbed.set_footer(text = 'Последнее обновление БД: %s' % pt)

        await client.send_message(channel, '@here')
        await client.send_message(channel, embed = dsgtEmbed)
        dsgt = False

      for dl in nyaa_dls:
        new.extend(await nyaa(dl))

      if len(new) > 0:
        nyaa_field = []
        nyaaEmbed = kurisu.prefs.Embeds.new('nyaa')
        for tor in new:
            nyaa_field.append('[%s](https://nyaa.si/download/%s.torrent) || %s/%s' % tor)

        nyaaEmbed.add_field(name = 'Nyaa', value = '\n'.join(nyaa_field))
        t = kurisu.prefs.parse_time(time.localtime(os.path.getmtime('torr_db.sqlite3')))
        t = '%s в %s' % (t[0], t[1][:-3])
        nyaaEmbed.set_footer(text = 'Последнее обновление БД: %s' % t)

        await client.send_message(channel, '@here')
        await client.send_message(channel, embed = nyaaEmbed)

      t = time.localtime()
      if (t[6] == 2 and t[3] >= 19) or (t[6] == 3 and t[3] < 6):
        dt = 1*60
      else:
        dt = 10*60
        print('[Nyaa]    | Peers and leechs are up to date')

      if (t[6] == 2 and t[3] == 18 and t[4] < 55 and t[4] >= 45):
        dt = (59 - t[4])*60 + (60 - t[5]) - 300
        print('[Nyaa]    | Alert in: %s' % dt)
        dsgt = True

      await asyncio.sleep(dt)

async def nyaa(dl):
    # TODO: Перепилить на aiohttp + в ссылку пихать магнет
    try:
        page = html.fromstring(await getPage('https://nyaa.si/?f=0&c=1_2&q=steins+gate+0+%s+1080p' % dl))
    except:
        print('[Nyaa]    | Error')
        return []

    conn = sqlite3.connect('torr_db.sqlite3')
    cursor = conn.cursor()
    result = []

    table = page.xpath('//table[contains(@class, "torrent-list")]//tr')[1:]
    for tr in table[::-1]:
        if time.mktime(datetime.datetime.strptime(tr.xpath('./td')[4].xpath('./text()')[0], "%Y-%m-%d %H:%M").timetuple()) < 1522540800:
            continue
        name = tr.xpath('./td')[1].xpath('./a/text()')[-1:][0]
        episode = name.replace(templates[dl][0], '').replace(templates[dl][1], '')
        tFile = tr.xpath('./td')[2].xpath('./a/@href')[0]
        tFile = tFile[tFile.rfind('/')+1:tFile.find('.')]
        seed = tr.xpath('./td')[5].xpath('./text()')[0]
        leech = tr.xpath('./td')[6].xpath('./text()')[0]

        cursor.execute('SELECT id FROM torrents WHERE link = %s' % tFile)

        db_id = None

        for tmp in cursor.fetchall():
            db_id = tmp[0]

        if db_id == None:
            print('[Nyaa]    | New nyaa torrent: %s' % name)
            cursor.execute('insert into torrents (link, seeders, leechers, dl, episode) values (%s, %s, %s, "%s", %s)' % (tFile, seed, leech, dl, episode))
            result.append((name, tFile, seed, leech))
        else:
            cursor.execute('update torrents SET seeders = %s, leechers = %s WHERE id = %s' % (seed, leech, db_id))
        conn.commit()

    conn.close()
    return result
