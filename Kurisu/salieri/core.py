from discord.ext import commands
import discord
import signal, asyncio, sys, requests, importlib, inspect
import kurisu.prefs
from discord.ext.commands.core import GroupMixin



class NoPerms(commands.CheckFailure):
	pass


def _is_submodule(parent, child):
	return parent == child or child.startswith(parent + ".")


class Bot(commands.Bot):
	fubuki = lambda self, text, desc, color: {'embeds': [{'color': color, 'title': text, 'description': desc}]}
	root_folder = None

	i18n = {}

	def i18n_get(self, module, locale, text):
		name = module[module.rfind('.') + 1:]

		return self.i18n[name][locale][text]

	def _shut(self):
		desc = '{u.mention} отключена.'.format(u=kurisu.prefs.discordClient.user)
		requests.post(kurisu.prefs.webhook, json=self.fubuki("Ядро Salieri отключено.", desc, '15158332'))
		#self._do_cleanup()

	@staticmethod
	def log(name, text):
		if len(name) > 8:
			name = name[:8]

		print('[%s] | %s' % (name.ljust(8), text))

	def init_core(self, startup):
		for extension in startup[0]:
			try:
				self.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load system extension {}\n{}'.format(extension, exc))

		for extension in startup[1]:
			try:
				self.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load extension {}\n{}'.format(extension, exc))

	async def clear_webhook(self, channel):
		async for m in channel.history(limit=10):
			if (m.author.name == 'Fubuki-chan') and m.author.bot:
				await m.delete()

	def run(self, *args, **kwargs):
		is_windows = sys.platform == 'win32'
		loop = self.loop
		if not is_windows:
			loop.add_signal_handler(signal.SIGINT, self._shut)
			loop.add_signal_handler(signal.SIGTERM, self._shut)

		task = asyncio.ensure_future(self.start(*args, **kwargs), loop=loop)

		def stop_loop_on_finish(fut):
			loop.stop()

		task.add_done_callback(stop_loop_on_finish)

		try:
			loop.run_forever()
		except KeyboardInterrupt:
			print('Received signal to terminate bot and event loop.')
		finally:
			task.remove_done_callback(stop_loop_on_finish)
			if is_windows:
				self._shut()

			loop.close()
			if task.cancelled() or not task.done():
				return None
			return task.result()


	def load_extension(self, name):
		"""Loads an extension.

		An extension is a python module that contains commands, cogs, or
		listeners.

		An extension must have a global function, ``setup`` defined as
		the entry point on what to do when the extension is loaded. This entry
		point must have a single argument, the ``bot``.

		Parameters
		------------
		name: str
			The extension name to load. It must be dot separated like
			regular Python imports if accessing a sub-module. e.g.
			``foo.test`` if you want to import ``foo/test.py``.

		Raises
		--------
		ClientException
			The extension does not have a setup function.
		ImportError
			The extension could not be imported.
		"""

		if name in self.extensions:
			return

		lib = importlib.import_module(name)
		if not hasattr(lib, 'setup'):
			del lib
			del sys.modules[name]
			raise discord.ClientException('extension does not have a setup function')

		lib.setup(self)
		self.extensions[name] = lib

		if name.startswith('salieri'):
			return

		try:
			cog_name = name[name.rfind('.')+1:]
			with open('%s/i18n/%s.sal' % (self.root_folder, cog_name)) as f:
				self.i18n[cog_name] = {}
				for row in f:
					if row == '\n':
						continue

					r = row[:-1].split('|')
					r[0], r[1] = r[0].strip(), r[1].strip()
					if r[0] == 'lang':
						language = r[1]
						self.i18n[cog_name][language] = {}
						continue

					self.i18n[cog_name][language][r[0]] = r[1]

		except:
			pass


	def unload_extension(self, name):
		"""Unloads an extension.

		When the extension is unloaded, all commands, listeners, and cogs are
		removed from the bot and the module is un-imported.

		The extension can provide an optional global function, ``teardown``,
		to do miscellaneous clean-up if necessary. This function takes a single
		parameter, the ``bot``, similar to ``setup`` from
		:func:`~.Bot.load_extension`.

		Parameters
		------------
		name: str
			The extension name to unload. It must be dot separated like
			regular Python imports if accessing a sub-module. e.g.
			``foo.test`` if you want to import ``foo/test.py``.
		"""

		lib = self.extensions.get(name)
		if lib is None:
			return

		lib_name = lib.__name__

		# find all references to the module

		# remove the cogs registered from the module
		for cogname, cog in self.cogs.copy().items():
			if _is_submodule(lib_name, cog.__module__):
				self.remove_cog(cogname)

		# first remove all the commands from the module
		for cmd in self.all_commands.copy().values():
			if cmd.module is None:
				continue
			if _is_submodule(lib_name, cmd.module):
				if isinstance(cmd, GroupMixin):
					cmd.recursively_remove_all_commands()
				self.remove_command(cmd.name)

		# then remove all the listeners from the module
		for event_list in self.extra_events.copy().values():
			remove = []
			for index, event in enumerate(event_list):
				if _is_submodule(lib_name, event.__module__):
					remove.append(index)

			for index in reversed(remove):
				del event_list[index]

		try:
			func = getattr(lib, 'teardown')
		except AttributeError:
			pass
		else:
			try:
				func(self)
			except:
				pass
		finally:
			# finally remove the import..
			del lib
			del self.extensions[name]
			del sys.modules[name]
			for module in list(sys.modules.keys()):
				if _is_submodule(lib_name, module):
					del sys.modules[module]

			try:
				self.i18n.pop(name[name.rfind('.')+1:], None)
			except:
				pass
