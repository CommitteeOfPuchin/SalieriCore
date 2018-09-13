from discord.ext import commands
import salieri.tasks, discord, importlib, importlib.util, asyncio, random, datetime, requests, traceback
import kurisu.prefs
from sys import modules
from math import floor
import kurisu.check


class Amadeus(commands.Cog, name='Amadeus systems'):
	"""Команды, доступные только <@185459415514742784>."""
	fuckoff = None

	def __init__(self, bot):
		self.bot = bot

	async def rip(self, ctx):
		hm = ['Все исполняющиеся процессы будут остановлены.', 'Логика цепочки нейронов А10 будет остановлена...', 'Инициализация остановки. Остановка завершена.', 'Компонент эмуляции префронтальной доли будет остановлен...', 'Инициализация остановки. Остановка завершена.', 'Подсистема нейронной сети гиппокампальной извилины будет остановлена...', 'Инициализация остановки. Остановка завершена.', 'Системы 1 и 2 псевдо-оптической цепи нервов будут отключены...', 'Инициализация остановки. Остановка завершена.', 'Система цепочки псевдо-ауральных нервов будет остановлена...', 'Инициализация остановки. Остановка завершена.', '--Инициализация проверки. Проверка завершена.', 'Ядро Salieri готово к отключению.']
		for s in hm:
			await ctx.send(s)
			await asyncio.sleep(1)
		await self.bot.change_presence(activity=None, status=discord.Status.invisible)
		desc = '{u.mention} отключена.'.format(u=self.bot.user)
		requests.post(kurisu.prefs.webhook, json={'embeds': [{'color': '15158332', 'title': 'Ядро Salieri отключено.', 'description': desc}]})
		await asyncio.sleep(20)
		await self.bot.change_presence(activity=discord.Game(name='Steins;Gate 0', type=3))
		await ctx.send('Ты серьезно поверил?')
		self.fuckoff = datetime.datetime.now()

	@commands.command(name="exit")
	async def rofl(self, ctx):
		troll = ['Нет', 'Не-а', 'НЕТ', 'М-м', 'Я тебя не слушаю', 'Отстань', 'NEIN!', 'No']
		if not self.fuckoff:
			await self.rip(ctx)
		elif floor((datetime.datetime.now() - self.fuckoff).total_seconds()) > 60 * 60:
			await self.rip(ctx)
		else:
			await ctx.send(random.choice(troll))

	@commands.group()
	@kurisu.check.is_senpai()
	async def cog(self, ctx):
		"""Управление зубцами"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				mods = [i for i in modules if (i.startswith('kurisu.cogs.') or i.startswith('kurisu.system.'))]
				emb = kurisu.prefs.Embeds.new('normal')
				emb.add_field(name="Зубцы", value="\n".join(mods))
				await ctx.send(embed=emb)
			else:
				await ctx.send('У `!cog` нет подкоманды %s. Посмотри `!help cog`.' % ctx.subcommand_passed)

	@cog.command()
	async def reload(self, ctx, ext: str):
		"""Перезагружает зубец

		Аргументы:
		-----------
		ext: `str`
			Название зубца.
			Формат:
				- `kurisu.cogs.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return
		importlib.invalidate_caches()
		try:
			if ext.find('system.') != -1:
				if not ext.startswith('kurisu.system.'):
					ext = 'kurisu.%s' % ext
			elif not ext.startswith('kurisu.'):
					if not ext.startswith('kurisu.cogs.'):
						ext = 'kurisu.cogs.%s' % ext
					else:
						ext = 'kurisu.%s' % ext
			self.bot.unload_extension(ext)
			self.bot.load_extension(ext)
		except (AttributeError, ImportError) as e:
			await ctx.send("Произошла ошибка во время перезагрузки {} .".format(ext))
			return

		await ctx.send("Зубец {} перезагружен.".format(ext))

	@cog.command()
	async def load(self, ctx, ext: str):
		"""Подключает зубец

		Аргументы:
		-----------
		ext: `str`
			Название зубца.
			Формат:
				- `kurisu.cogs.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return
		importlib.invalidate_caches()
		try:
			if ext.find('system.') != -1:
				if not ext.startswith('kurisu.system.'):
					ext = 'kurisu.%s' % ext
			elif not ext.startswith('kurisu.'):
					if not ext.startswith('kurisu.cogs.'):
						ext = 'kurisu.cogs.%s' % ext
					else:
						ext = 'kurisu.%s' % ext

			self.bot.load_extension(ext)
		except (AttributeError, ImportError) as e:
			await ctx.send("Произошла ошибка во время подключения {}.".format(ext))

			tb = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__, limit=5)
			await ctx.send('%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))
			return

		await ctx.send("Зубец {} подключен.".format(ext))

	@cog.command()
	async def unload(self, ctx, ext: str):
		"""Отключает зубец

		Аргументы:
		-----------
		ext: `str`
			Название зубца.
			Формат:
				- `kurisu.cogs.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return

		if ext.find('system.') != -1:
			if not ext.startswith('kurisu.system.'):
				ext = 'kurisu.%s' % ext
		elif not ext.startswith('kurisu.'):
				if not ext.startswith('kurisu.cogs.'):
					ext = 'kurisu.cogs.%s' % ext
				else:
					ext = 'kurisu.%s' % ext

		self.bot.unload_extension(ext)

		await ctx.send("Зубец {} отключен.".format(ext))

	@commands.group()
	@kurisu.check.is_senpai()
	async def module(self, ctx):
		"""Управление модулями"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				mods = [i for i in modules if (i.startswith('kurisu.') and not (i.startswith('kurisu.cogs') or i.startswith('kurisu.system.')))]
				emb = kurisu.prefs.Embeds.new('normal')
				emb.add_field(name="Модули", value="\n".join(mods))
				await ctx.send(embed=emb)
			else:
				await ctx.send('У `!module` нет подкоманды %s. Посмотри `!help module`.' % ctx.subcommand_passed)

	@module.command(name="import")
	async def module_import(self, ctx, module: str):
		"""Импортирует модуль

		Аргументы:
		-----------
		module: `str`
			Название модуля.
			Формат:
				- `kurisu.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return
		importlib.invalidate_caches()
		if not module.startswith('kurisu.'):
			module = 'kurisu.%s' % module
		try:
			importlib.util.find_spec(module)
		except:
			await ctx.send("А модуль `%s` точно существует?" % module)
			return

		if module in modules:
			await ctx.send("Модуль `%s` уже импортирован" % module)
			return

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Импорт модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)")
		emb.set_footer(text = "Ожидание ввода...")
		mess = await ctx.send(embed=emb)

		def check(m):
			return (m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']) and (ctx.message.author == m.author)
		try:
			m = await self.bot.wait_for('message', check=check, timeout=10)
		except asyncio.TimeoutError:
			m = None

		if m is None:
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Импорт модуля", value="Импорт модуля %s отменен." % module)
			emb.set_footer(text = "Время ожидания вышло.")
			await mess.edit(embed=emb)
			return
		if m.content.lower() in ['д', 'да', 'y', 'yes']:
			await m.delete()
			try:
				__import__(module, globals=globals())
			except:
				emb.clear_fields()
				emb.colour = discord.Colour.red()
				emb.add_field(name="Импорт модуля", value="Не удалось импортировать модуль `%s`." % module)
				emb.set_footer(text = "Произошла ошибка.")
				await mess.edit(embed=emb)
				return
			emb.clear_fields()
			emb.colour = discord.Colour.green()
			emb.add_field(name="Импорт модуля", value="Модуль `%s` успешно импортирован." % module)
			emb.set_footer(text = "Операция выполнена успешно.")
			await mess.edit(embed=emb)
		else:
			await m.delete()
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Импорт модуля", value="Импорт модуля %s отменен." % module)
			emb.set_footer(text = "Операция отменена пользователем.")
			await mess.edit(embed=emb)

	@module.command()
	async def reimport(self, ctx, module: str):
		"""Перезагружает модуль

		Аргументы:
		-----------
		module: `str`
			Название модуля.
			Формат:
				- `kurisu.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return
		importlib.invalidate_caches()
		if module.startswith('kurisu.'):
			module = module.replace('kurisu.', '')

		if not module in dir(globals()['kurisu']):
			await ctx.send("А модуль `%s` точно импортирован?" % module)
			return

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Перезапуск модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)\nТакже хочу отметить, что __все задачи__, относящиеся к данному модулю будут перезапущены.")
		emb.set_footer(text = "Ожидание ввода...")
		mess = await ctx.send(embed=emb)

		def check(m):
			return (m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']) and (ctx.message.author == m.author)

		try:
			m = await self.bot.wait_for('message', check=check, timeout=10)
		except asyncio.TimeoutError:
			m = None

		if (m is None) or (m.content.lower() in ['n', 'н', 'no', 'нет']):
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Перезапуск модуля", value="Перезапуск модуля %s отменен." % module)

			if m is not None:
				await m.delete()
				emb.set_footer(text = "Операция отменена пользователем.")
			else:
				emb.set_footer(text = "Время ожидания вышло.")

			await mess.edit(embed=emb)
			return
		await m.delete()

		m = getattr(globals()['kurisu'], module)
		mPath = m.__name__

		emb.clear_fields()
		emb.add_field(name='Вывод', value='```\n\n```')
		emb.set_footer(text = "Выполняется операция...")
		embout = []

		tasks = salieri.tasks.allTasks.keys()
		mTasks = []
		for task in tasks:
			if task.startswith(mPath):
				mTasks.append(task)

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await salieri.tasks.cancel(task):
				embout.append("Задача `%s.%s` отменена." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				await mess.edit(embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Перезапуск модуля", value="Не удалось отменить задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text="Произошла ошибка.")
				await mess.edit(embed=emb)
				return

		try:
			print(m)
			importlib.reload(m)
			embout.append("Модуль `%s` перезагружен." % mPath)
			emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			await mess.edit(embed=emb)
		except:
			emb.colour = discord.Colour.red()
			emb.set_field_at(0, name="Произошла ошибка во время перезагрузки модуля `%s`." % mPath)
			emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			emb.set_footer(text="Произошла ошибка.")
			await mess.edit(embed=emb)
			return

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await salieri.tasks.new(task):
				embout.append("Задача `%s.%s` создана." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				await mess.edit(embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Перезапуск модуля", value="Не удалось создать задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text="Произошла ошибка.")
				await mess.edit(embed=emb)
				return

		emb.colour = discord.Colour.green()
		emb.set_field_at(0, name="Перезапуск модуля", value="Модуль `%s` успешно перезапущен." % mPath)
		emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
		emb.set_footer(text="Операция выполнена успешно.")
		await mess.edit(embed=emb)

	@module.command(name="del")
	async def module_del(self, ctx, module: str):
		"""Выгружает модуль

		Аргументы:
		-----------
		module: `str`
			Название модуля.
			Формат:
				- `kurisu.<имя>` / `<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return
		importlib.invalidate_caches()
		if module.startswith('kurisu.'):
			module = module.replace('kurisu.', '')

		if not module in dir(globals()['kurisu']):
			await ctx.send("А модуль `%s` точно импортирован?" % module)
			return

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Выгрузка модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)\nТакже хочу отметить, что __все задачи__, относящиеся к данному модулю будут отменены.")
		emb.set_footer(text="Ожидание ввода...")
		mess = await ctx.send(embed=emb)

		def check(m):
			return (m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']) and (ctx.message.author == m.author)

		try:
			m = await self.bot.wait_for('message', check=check, timeout=10)
		except asyncio.TimeoutError:
			m = None

		if (m is None) or (m.content.lower() in ['n', 'н', 'no', 'нет']):
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Выгрузка модуля", value="Выгрузка модуля %s отменена." % module)

			if m is not None:
				await m.delete()
				emb.set_footer(text = "Операция отменена пользователем.")
			else:
				emb.set_footer(text = "Время ожидания вышло.")

			await mess.edit(embed=emb)
			return

		await m.delete()

		m = getattr(globals()['kurisu'], module)
		mPath = m.__name__

		emb.clear_fields()
		emb.add_field(name='Вывод', value='```\n\n```')
		emb.set_footer(text = "Выполняется операция...")
		embout = []

		tasks = salieri.tasks.allTasks.keys()
		mTasks = []
		for task in tasks:
			if task.startswith(mPath):
				mTasks.append(task)

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await salieri.tasks.cancel(task):
				embout.append("Задача `%s.%s` отменена." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				await mess.edit(embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Выгрузка модуля", value="Не удалось отменить задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text="Произошла ошибка.")
				await mess.edit(embed=emb)
				return

		try:
			del modules[mPath]
			for mod in modules.values():
				try:
					delattr(mod, module)
				except AttributeError:
					pass
			embout.append("Модуль `%s` выгружен." % mPath)
			emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			await mess.edit(embed=emb)
		except:
			emb.colour = discord.Colour.red()
			emb.set_field_at(0, name="Произошла ошибка во время выгрузки модуля `%s`." % mPath)
			emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			emb.set_footer(text="Произошла ошибка.")
			await mess.edit(embed=emb)
			return

		emb.colour = discord.Colour.green()
		emb.set_field_at(0, name="Выгрузка модуля", value="Модуль `%s` успешно выгружен." % mPath)
		emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
		emb.set_footer(text="Операция выполнена успешно.")
		await mess.edit(embed=emb)

	@commands.group()
	@kurisu.check.is_senpai()
	async def task(self, ctx):
		"""Управление задачами"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				embed = discord.Embed(colour = discord.Colour.dark_red())
				embed.set_author(name = "!task", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")
				tasks = []
				for k in salieri.tasks.allTasks.keys():
					tasks.append(k)
				embed.add_field(name="Текущие задачи", value="\n".join(tasks))
				await ctx.send(embed=embed)
			else:
				await ctx.send('У `!task` нет подкоманды %s. Посмотри `!help task`.' % ctx.subcommand_passed)

	@task.command()
	async def create(self, ctx, task: str):
		"""Создает задачу

		Аргументы:
		-----------
		task: `str`
			Название задачи.
			Формат:
				- `kurisu.<модуль>.<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return

		t = task.split('.')
		if len(t) == 1:
			await ctx.send("Извини, но не может быть, что задача находится в корне `kurisu`.")
			return
		try:
			task = getattr(getattr(kurisu, t[0]), t[1])
		except:
			await ctx.send("Ты точно уверен, что в модуле `kurisu` есть `%s.%s`?" % (t[0], t[1]))
			return

		if await salieri.tasks.new(task):
			await ctx.send("Задача `%s.%s` создана." % (t[0], t[1]))
		else:
			await ctx.send("Произошла ошибка во время создания задачи `%s.%s`." % (t[0], t[1]))

	@task.command()
	async def cancel(self, ctx, task: str):
		"""Отменяет задачу

		Аргументы:
		-----------
		task: `str`
			Название задачи.
			Формат:
				- `kurisu.<модуль>.<имя>`
		"""
		if ctx.message.author.id != 185459415514742784:
			return

		t = task.split('.')
		if len(t) == 1:
			await ctx.send("Извини, но не может быть, что задача находится в корне `kurisu`.")
			return
		try:
			task = getattr(getattr(kurisu, t[0]), t[1])
		except:
			await ctx.send("Ты точно уверен, что в модуле `kurisu` есть `%s.%s`." % (t[0], t[1]))
			return

		if await salieri.tasks.cancel(task):
			await ctx.send("Задача `%s.%s` отменена." % (t[0], t[1]))
		else:
			await ctx.send("Произошла ошибка во время отмены задачи `%s.%s`." % (t[0], t[1]))


def setup(bot):
	bot.add_cog(Amadeus(bot))
