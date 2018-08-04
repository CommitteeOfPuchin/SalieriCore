from discord.ext import commands
import kurisu.tasks, discord, importlib, importlib.util, asyncio

class Amadeus:
	"""Команды, доступные только <@185459415514742784>."""

	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def cog(self, ctx):
		"""Управление зубцами"""
		if ctx.message.author.id != "185459415514742784" :
			await self.bot.say("Ты не можешь это сделать, ты не сенпай.")
			return
		if ctx.invoked_subcommand is None:
			await self.bot.say('У `!cog` нет подкоманды %s. Посмотри `!help cog`.' % ctx.subcommand_passed)

	@cog.command(pass_context=True)
	async def reload(self, ctx, ext: str):
		"""Перезагружает зубец"""
		if ctx.message.author.id != "185459415514742784" :
			return
		try:
			if ext.find('kurisu.cogs') == -1:
				ext = "kurisu.cogs.%s" % ext
			self.bot.unload_extension(ext)
			self.bot.load_extension(ext)
		except (AttributeError, ImportError) as e:
			await self.bot.say("Произошла ошибка во время перезагрузки {} .".format(ext))
			return

		await self.bot.say("Модуль {} перезагружен.".format(ext))

	@cog.command(pass_context=True)
	async def load(self, ctx, ext: str):
		"""Подключает зубец"""
		if ctx.message.author.id != "185459415514742784" :
			return
		try:
			if ext.find('kurisu.cogs') == -1:
				ext = "kurisu.cogs.%s" % ext
			self.bot.load_extension(ext)
		except (AttributeError, ImportError) as e:
			await self.bot.say("Произошла ошибка во время подключения {} .".format(ext))
			return

		await self.bot.say("Модуль {} подключен.".format(ext))

	@cog.command(pass_context=True)
	async def unload(self, ctx, ext: str):
		"""Отключает зубец"""
		if ctx.message.author.id != "185459415514742784" :
			return
		if ext.find('kurisu.cogs') == -1:
			ext = "kurisu.cogs.%s" % ext
		self.bot.unload_extension(ext)

		await self.bot.say("Модуль {} отключен.".format(ext))

	@commands.group(pass_context=True)
	async def module(self, ctx):
		"""Управление модулями"""
		if ctx.message.author.id != "185459415514742784" :
			await self.bot.say("Ты не можешь это сделать, ты не сенпай.")
			return
		if ctx.invoked_subcommand is None:
			await self.bot.say('У `!cog` нет подкоманды %s. Посмотри `!help cog`.' % ctx.subcommand_passed)

	@module.command(pass_context=True, name="import")
	async def module_import(self, ctx, module: str):
		"""Импортирует модуль"""
		if ctx.message.author.id != "185459415514742784" :
			return
		importlib.invalidate_caches()
		if not module.startswith('kurisu.'):
			module = 'kurisu.%s' % module
		try:
			importlib.util.find_spec(module)
		except:
			await self.bot.say("А модуль `%s` точно существует?" % module)
			return

		await self.bot.say("Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)")
		def check(m):
			return m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']

		m = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=10)
		if m == None:
			await self.bot.say("Импорт модуля `%s` отменен." % module)
			return
		if m.content.lower() in ['д', 'да', 'y', 'yes']:
			try:
				__import__(module, globals=globals())
			except:
				await self.bot.say("Не удалось импортировать модуль `%s`" % module)
				return
			await self.bot.say("Модуль `%s` успешно импортирован" % module)
		else:
			await self.bot.say("Импорт модуля `%s` отменен." % module)

	@module.command(pass_context=True)
	async def reimport(self, ctx, module: str):
		"""Перезагружает модуль"""
		if ctx.message.author.id != "185459415514742784" :
			return
		importlib.invalidate_caches()
		if module.startswith('kurisu.'):
			module = module.replace('kurisu.', '')

		if not module in dir(globals()['kurisu']):
			await self.bot.say("А модуль `%s` точно импортирован?" % module)
			return

		await self.bot.say("Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)\n*Также хочу отметить, что все задачи, относящиеся к данному модулю будут перезапущены.*\n*Процесс будет замедлен, чтобы сообщения отсылались корректно.*")
		def check(m):
			return m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']

		m = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=10)
		if (m == None) or (m.content.lower() in ['n', 'н', 'no', 'нет']):
			await self.bot.say("Перезагрузка модуля `%s` отменена." % module)
			return

		m = getattr(globals()['kurisu'], module)
		mPath = m.__name__

		tasks = kurisu.tasks.allTasks.keys()
		mTasks = []
		for task in tasks:
			if task.startswith(mPath):
				mTasks.append(task)

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await kurisu.tasks.cancel(task):
				await self.bot.say("Задача `%s.%s` отменена." % (t[0], t[1]))
				await asyncio.sleep(1)
			else:
				await self.bot.say("Произошла ошибка во время отмены задачи `%s.%s`." % (t[0], t[1]))
				return

		try:
			importlib.reload(m)
			await self.bot.say("Модуль `%s` перезагружен." % mPath)
		except:
			await self.bot.say("Произошла ошибка во время перезагрузки модуля `%s`." % mPath)
			return

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await kurisu.tasks.new(task):
				await self.bot.say("Задача `%s.%s` создана." % (t[0], t[1]))
				await asyncio.sleep(1)
			else:
				await self.bot.say("Произошла ошибка во время создания задачи `%s.%s`." % (t[0], t[1]))
				return

	@commands.group(pass_context=True)
	async def task(self, ctx):
		"""Управление задачами"""
		if ctx.message.author.id != "185459415514742784" :
			await self.bot.say("Ты не можешь это сделать, ты не сенпай.")
			return
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed == None:
				embed = discord.Embed(colour = discord.Colour.dark_red())
				embed.set_author(name = "!task", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")
				tasks = []	
				for k in kurisu.tasks.allTasks.keys():
					tasks.append(k)
				embed.add_field(name="Текущие задачи", value="\n".join(tasks))
				await self.bot.say(embed=embed)
			else:
				await self.bot.say('У `!task` нет подкоманды %s. Посмотри `!help task`.' % ctx.subcommand_passed)

	@task.command(pass_context=True)
	async def create(self, ctx, task: str):
		"""Создает задачу"""
		if ctx.message.author.id != "185459415514742784" :
			return
		
		t = task.split('.')
		if len(t) == 1:
			await self.bot.say("Извини, но не может быть, что задача находится в корне `kurisu`.")
			return
		try:
			task = getattr(getattr(kurisu, t[0]), t[1])
		except:
			await self.bot.say("Ты точно уверен, что в модуле `kurisu` есть `%s.%s`." % (t[0], t[1]))
			return

		if await kurisu.tasks.new(task):
			await self.bot.say("Задача `%s.%s` создана." % (t[0], t[1]))
		else:
			await self.bot.say("Произошла ошибка во время создания задачи `%s.%s`." % (t[0], t[1]))


	@task.command(pass_context=True)
	async def cancel(self, ctx, task: str):
		"""Отменяет задачу"""
		if ctx.message.author.id != "185459415514742784" :
			return

		t = task.split('.')
		if len(t) == 1:
			await self.bot.say("Извини, но не может быть, что задача находится в корне `kurisu`.")
			return
		try:
			task = getattr(getattr(kurisu, t[0]), t[1])
		except:
			await self.bot.say("Ты точно уверен, что в модуле `kurisu` есть `%s.%s`." % (t[0], t[1]))
			return

		if await kurisu.tasks.cancel(task):
			await self.bot.say("Задача `%s.%s` отменена." % (t[0], t[1]))
		else:
			await self.bot.say("Произошла ошибка во время отмены задачи `%s.%s`." % (t[0], t[1]))

def setup(bot):
	bot.add_cog(Amadeus(bot))
