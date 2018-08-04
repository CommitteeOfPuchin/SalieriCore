
from discord.ext import commands

# The permission system of the bot is based on a "just works" basis
# You have permissions and the bot has permissions. If you meet the permissions
# required to execute the command (and the bot does as well) then it goes through
# and you can execute the command.
# Certain permissions signify if the person is a moderator (Manage Server) or an
# admin (Administrator). Having these signify certain bypasses.
# Of course, the owner will always be able to execute commands.

def check_permissions(ctx, perms, *, check=all):
    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_permissions(*, check=all, **perms):
    def pred(ctx):
        return check_permissions(ctx, perms, check=check)
    return commands.check(pred)

def check_guild_permissions(ctx, perms, *, check=all):
    if len(ctx.message.author.roles) == 0:
        return False

    resolved = ctx.message.author.server_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_guild_permissions(*, check=all, **perms):
    def pred(ctx):
        return check_guild_permissions(ctx, perms, check=check)
    return commands.check(pred)

# These do not take channel overrides into account

def is_mod():
    def pred(ctx):
        return check_guild_permissions(ctx, {'manage_guild': True})
    return commands.check(pred)

def is_admin():
    def pred(ctx):
        return check_guild_permissions(ctx, {'administrator': True})
    return commands.check(pred)

def mod_or_permissions(**perms):
    perms['manage_guild'] = True
    def predicate(ctx):
        return check_guild_permissions(ctx, perms, check=any)
    return commands.check(predicate)

def admin_or_permissions(**perms):
    perms['administrator'] = True
    def predicate(ctx):
        return check_guild_permissions(ctx, perms, check=any)
    return commands.check(predicate)

def is_in_guilds(*guild_ids):
    def predicate(ctx):
        guild = ctx.guild
        if guild is None:
            return False
        return guild.id in guild_ids
    return commands.check(predicate)
