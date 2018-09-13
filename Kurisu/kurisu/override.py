from discord.ext import commands
import discord
import itertools, inspect


class newHelpFormatter(commands.formatter.HelpFormatter):
	def category(tup):
		cog = tup[1].cog_name
		return cog + ':' if cog is not None else '\u200bБез категории:'

	def get_ending_note(self):
		command_name = self.context.invoked_with
		return "Набери {0}{1} <команда>, чтобы получить больше информации о команде.\n" \
					"Также ты можешь набрать {0}{1} <категория>, чтобы получить больше информации о категории".format(self.clean_prefix, command_name)

	def format(self):
		helpEmbed = discord.Embed(colour=discord.Colour.dark_red())
		command_name = self.context.invoked_with
		helpEmbed.set_author(name="%s%s" % (self.clean_prefix, command_name), icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")

		description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

		if description:
			helpEmbed.description = description

		if isinstance(self.command, commands.Command):
			# <signature portion>
			signature = self.get_command_signature()
			helpEmbed.title = signature

			# <long doc> section
			if self.command.help:
				helpEmbed.add_field(name="Описание:", value=self.command.help)

			# end it here if it's just a regular command
			if not self.has_subcommands():
				return helpEmbed

		def category(tup):
			cog = tup[1].cog_name
			return cog + ':' if cog is not None else '\u200bБез категории:'

		if self.is_bot():
			helpEmbed.title = "Makise Kurisu"
			data = sorted(self.filter_command_list(), key=category)
			for ctg, cmds in itertools.groupby(data, key=category):
				if ctg == "Amadeus:":
					continue

				cmds = list(cmds)
				if len(cmds) > 0:
					subs = []
					for name, cmd in cmds:
						if name in cmd.aliases:
							continue

						subs.append("%s: %s" % (name, cmd.short_doc))

				helpEmbed.add_field(name=ctg, value='\n'.join(subs))
		else:
			subs = []
			for name, cmd in self.filter_command_list():
				subs.append("%s: %s" % (name, cmd.short_doc))
			
			helpEmbed.add_field(name="Команды:", value='\n'.join(subs))

		ending_note = self.get_ending_note()
		helpEmbed.add_field(name="Также:", value=ending_note)
		return helpEmbed
