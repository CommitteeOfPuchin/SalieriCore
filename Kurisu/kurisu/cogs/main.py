from discord.ext import commands
import kurisu.tasks, discord, importlib, importlib.util, asyncio
import kurisu.prefs
from sys import modules

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
			if ctx.subcommand_passed == None:
				mods = [i for i in modules if i.startswith('kurisu.cogs.')]
				emb = kurisu.prefs.Embeds.new('normal')
				emb.add_field(name="Зубцы", value="\n".join(mods))
				await self.bot.say(embed=emb)
			else:
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

		await self.bot.say("Зубец {} перезагружен.".format(ext))

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

		await self.bot.say("Зубец {} подключен.".format(ext))

	@cog.command(pass_context=True)
	async def unload(self, ctx, ext: str):
		"""Отключает зубец"""
		if ctx.message.author.id != "185459415514742784" :
			return
		if ext.find('kurisu.cogs') == -1:
			ext = "kurisu.cogs.%s" % ext
		self.bot.unload_extension(ext)

		await self.bot.say("Зубец {} отключен.".format(ext))

	@commands.group(pass_context=True)
	async def module(self, ctx):
		"""Управление модулями"""
		if ctx.message.author.id != "185459415514742784" :
			await self.bot.say("Ты не можешь это сделать, ты не сенпай.")
			return
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed == None:
				mods = [i for i in modules if (i.startswith('kurisu.') and not (i.startswith('kurisu.cogs')))]
				emb = kurisu.prefs.Embeds.new('normal')
				emb.add_field(name="Модули", value="\n".join(mods))
				await self.bot.say(embed=emb)
			else:
				await self.bot.say('У `!module` нет подкоманды %s. Посмотри `!help module`.' % ctx.subcommand_passed)

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

		if module in modules:
			await self.bot.say("Модуль `%s` уже импортирован" % module)
			return

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Импорт модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)")
		emb.set_footer(text = "Ожидание ввода...")
		mess = await self.bot.say(embed=emb)

		def check(m):
			return m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']

		m = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=10)
		if m == None:
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Импорт модуля", value="Импорт модуля %s отменен." % module)
			emb.set_footer(text = "Время ожидания вышло.")
			await self.bot.edit_message(mess, embed=emb)
			return
		if m.content.lower() in ['д', 'да', 'y', 'yes']:
			await self.bot.delete_message(m)
			try:
				__import__(module, globals=globals())
			except:
				emb.clear_fields()
				emb.colour = discord.Colour.red()
				emb.add_field(name="Импорт модуля", value="Не удалось импортировать модуль `%s`." % module)
				emb.set_footer(text = "Произошла ошибка.")
				await self.bot.edit_message(mess, embed=emb)
				return
			emb.clear_fields()
			emb.colour = discord.Colour.green()
			emb.add_field(name="Импорт модуля", value="Модуль `%s` успешно импортирован." % module)
			emb.set_footer(text = "Операция выполнена успешно.")
			await self.bot.edit_message(mess, embed=emb)
		else:
			await self.bot.delete_message(m)
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Импорт модуля", value="Импорт модуля %s отменен." % module)
			emb.set_footer(text = "Операция отменена пользователем.")
			await self.bot.edit_message(mess, embed=emb)

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

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Перезапуск модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)\nТакже хочу отметить, что __все задачи__, относящиеся к данному модулю будут перезапущены.")
		emb.set_footer(text = "Ожидание ввода...")
		mess = await self.bot.say(embed=emb)

		def check(m):
			return m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']

		m = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=10)
		if (m == None) or (m.content.lower() in ['n', 'н', 'no', 'нет']):
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Перезапуск модуля", value="Перезапуск модуля %s отменен." % module)
			
			if m != None:
				await self.bot.delete_message(m)
				emb.set_footer(text = "Операция отменена пользователем.")
			else:
				emb.set_footer(text = "Время ожидания вышло.")

			await self.bot.edit_message(mess, embed=emb)
			return
		await self.bot.delete_message(m)

		m = getattr(globals()['kurisu'], module)
		mPath = m.__name__

		emb.clear_fields()
		emb.add_field(name='Вывод', value='```\n\n```')
		emb.set_footer(text = "Выполняется операция...")
		embout = []

		tasks = kurisu.tasks.allTasks.keys()
		mTasks = []
		for task in tasks:
			if task.startswith(mPath):
				mTasks.append(task)

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await kurisu.tasks.cancel(task):
				embout.append("Задача `%s.%s` отменена." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				mess = await self.bot.edit_message(mess, embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Перезапуск модуля", value="Не удалось отменить задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text = "Произошла ошибка.")
				await self.bot.edit_message(mess, embed=emb)
				return

		try:
			importlib.reload(m)
			embout.append("Модуль `%s` перезагружен." % mPath)
			emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			mess = await self.bot.edit_message(mess, embed=emb)
		except:
			emb.colour = discord.Colour.red()
			emb.set_field_at(0, name="Произошла ошибка во время перезагрузки модуля `%s`." % mPath)
			emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			emb.set_footer(text = "Произошла ошибка.")
			await self.bot.edit_message(mess, embed=emb)
			return

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await kurisu.tasks.new(task):
				embout.append("Задача `%s.%s` создана." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				mess = await self.bot.edit_message(mess, embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Перезапуск модуля", value="Не удалось создать задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text = "Произошла ошибка.")
				await self.bot.edit_message(mess, embed=emb)
				return

		emb.colour = discord.Colour.green()
		emb.set_field_at(0, name="Перезапуск модуля", value="Модуль `%s` успешно перезапущен." % mPath)
		emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
		emb.set_footer(text = "Операция выполнена успешно.")
		await self.bot.edit_message(mess, embed=emb)

	@module.command(pass_context=True, name="del")
	async def module_del(self, ctx, module: str):
		"""Выгружает модуль"""
		if ctx.message.author.id != "185459415514742784" :
			return
		importlib.invalidate_caches()
		if module.startswith('kurisu.'):
			module = module.replace('kurisu.', '')

		if not module in dir(globals()['kurisu']):
			await self.bot.say("А модуль `%s` точно импортирован?" % module)
			return

		emb = kurisu.prefs.Embeds.new('alert')
		emb.add_field(name="Выгрузка модуля", value="Сенпай, ты же в курсе, что это опасно? Пожалуйста, подтверди действие (Д/н)\nТакже хочу отметить, что __все задачи__, относящиеся к данному модулю будут отменены.")
		emb.set_footer(text = "Ожидание ввода...")
		mess = await self.bot.say(embed=emb)

		def check(m):
			return m.content.lower() in ['д', 'н', 'да', 'нет', 'yes', 'no', 'y', 'n']

		m = await self.bot.wait_for_message(author=ctx.message.author, check=check, timeout=10)
		if (m == None) or (m.content.lower() in ['n', 'н', 'no', 'нет']):
			emb.clear_fields()
			emb.colour = discord.Colour.red()
			emb.add_field(name="Выгрузка модуля", value="Выгрузка модуля %s отменена." % module)
			
			if m != None:
				await self.bot.delete_message(m)
				emb.set_footer(text = "Операция отменена пользователем.")
			else:
				emb.set_footer(text = "Время ожидания вышло.")

			await self.bot.edit_message(mess, embed=emb)
			return
		await self.bot.delete_message(m)

		m = getattr(globals()['kurisu'], module)
		mPath = m.__name__

		emb.clear_fields()
		emb.add_field(name='Вывод', value='```\n\n```')
		emb.set_footer(text = "Выполняется операция...")
		embout = []

		tasks = kurisu.tasks.allTasks.keys()
		mTasks = []
		for task in tasks:
			if task.startswith(mPath):
				mTasks.append(task)

		for mTask in mTasks:
			t = mTask.split('.')[1:]
			task = getattr(getattr(kurisu, t[0]), t[1])
			if await kurisu.tasks.cancel(task):
				embout.append("Задача `%s.%s` отменена." % (t[0], t[1]))
				emb.set_field_at(0, name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				mess = await self.bot.edit_message(mess, embed=emb)
				await asyncio.sleep(0.5)
			else:
				emb.colour = discord.Colour.red()
				emb.set_field_at(0, name="Выгрузка модуля", value="Не удалось отменить задачу `%s.%s`." % (t[0], t[1]))
				emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
				emb.set_footer(text = "Произошла ошибка.")
				await self.bot.edit_message(mess, embed=emb)
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
			mess = await self.bot.edit_message(mess, embed=emb)
		except:
			emb.colour = discord.Colour.red()
			emb.set_field_at(0, name="Произошла ошибка во время выгрузки модуля `%s`." % mPath)
			emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
			emb.set_footer(text = "Произошла ошибка.")
			await self.bot.edit_message(mess, embed=emb)
			return

		emb.colour = discord.Colour.green()
		emb.set_field_at(0, name="Выгрузка модуля", value="Модуль `%s` успешно выгружен." % mPath)
		emb.add_field(name='Вывод', value='```\n%s\n```' % '\n'.join(embout))
		emb.set_footer(text = "Операция выполнена успешно.")
		await self.bot.edit_message(mess, embed=emb)

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
			await self.bot.say("Ты точно уверен, что в модуле `kurisu` есть `%s.%s`?" % (t[0], t[1]))
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
