from discord.ext import commands
import kurisu.prefs
import random, json
import os, math

class KurisuRND(commands.Cog, name='Rundom Nigga Generator'):
  """BETA: Команды для броска кубиков"""
  
  statsEn = ['WS', 'BS', 'S', 'T', 'Ag', 'Int', 'Per', 'WP', 'Fel']
  statsRu = ['Ближний бой', 'Баллистик', 'Сила', 'Выносливость', 'Ловкость', 'Интеллект', 'Восприятие', 'Сила Воли', 'Товарищество']
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def rnd(self, ctx, dice: int, count: int = 1):
    """Рандом несколько раз.

    Аргументы:
    -----------
    dice: `int`
      Максимальное значение кости.
    count: `int` = 1
      Количество костей.
    """
    if count > 32:
      await ctx.send('А не жирно?')
      return
      
    if count < 1:
      await ctx.send('Может хоть один?')
      return
    
    await ctx.send('%s\nРезультат: %s' % (ctx.author.mention, ' / '.join([str(random.randint(1, dice)) for _ in range(count)])))
    
    
  @commands.group()
  async def dh(self, ctx):
    """Dark Heresy"""
    if ctx.invoked_subcommand is None:
      await ctx.send('У `!dh` нет подкоманды %s. Посмотри `!help dh`.' % ctx.subcommand_passed)
  
  @dh.command()
  async def create(self, ctx, name: str, fullname: str, WS: int = 0, BS: int = 0, S: int = 0, T: int = 0, Ag: int = 0, Int: int = 0, Per: int = 0, WP: int = 0, Fel: int = 0):
    """Создает файл Dark Heresy.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    fullname: `str`
      Описательное имя персонажа
    """
    if os.path.isfile('./darkheresy/%s.json' % name):
      await ctx.send('Файл %s уже существует' % name)
      return
      
    stats = {"ID": ctx.author.id, "name": fullname, "WS": WS,"BS": BS,"S": S,"T": T,"Ag": Ag,"Int": Int,"Per": Per,"WP": WP,"Fel": Fel}
    with open('./darkheresy/%s.json' % name, 'w') as file:
      json.dump(stats, file)
      await ctx.send('Файл %s создан.' % name)
      
  @dh.command()
  async def delete(self, ctx, name: str):
    """Удаляет файл Dark Heresy.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    """
    if not os.path.isfile('./darkheresy/%s.json' % name):
      await ctx.send('Файл %s не найден' % name)
      return
      
    with open('./darkheresy/%s.json' % name, 'r') as file:
      stats = json.loads(file.read())
      if ctx.author.id != stats['ID']:
        await ctx.send('Но ты же не хозяин файла %s' % name)
        return
        
    os.remove('./darkheresy/%s.json' % name)
    await ctx.send('Файл %s удален.' % name)
  
  @dh.command()
  async def edit(self, ctx, name: str, stat: str, value: int):
    """Изменение характеристик в файле.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    stat: `str`
      Сокращение характеристики, что надо посчитать.
    value: `int`
      Значение характеристики.
    """
    if not os.path.isfile('./darkheresy/%s.json' % name):
      await ctx.send('Файл %s не найден' % name)
      return
      
    if stat not in self.statsEn:
      await ctx.send('Нет статы %s' % stat)
      return
      
    with open('./darkheresy/%s.json' % name, 'r') as file:
      stats = json.loads(file.read())
      if ctx.author.id != stats['ID']:
        await ctx.send('Но ты же не хозяин файла %s' % name)
        return
      stats[stat] = value
    with open('./darkheresy/%s.json' % name, 'w') as file:
      json.dump(stats, file)
      await ctx.send('Файл %s изменен. %s = %i' % (name, stat, value))
      
  @dh.command()
  async def rename(self, ctx, name: str, fullname: str):
    """Изменение имени в файле.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    fullname: `str`
      Описательное имя персонажа
    """
    if not os.path.isfile('./darkheresy/%s.json' % name):
      await ctx.send('Файл %s не найден' % name)
      return
      
    with open('./darkheresy/%s.json' % name, 'r') as file:
      stats = json.loads(file.read())
      if ctx.author.id != stats['ID']:
        await ctx.send('Но ты же не хозяин файла %s' % name)
        return
      stats['name'] = fullname
    with open('./darkheresy/%s.json' % name, 'w') as file:
      json.dump(stats, file)
      await ctx.send('Файл %s изменен. Новое имя: %s' % fullname)
      
  @dh.command()
  async def stats(self, ctx, name: str):
    """Красиво выводит характеристики.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    """
    if not os.path.isfile('./darkheresy/%s.json' % name):
      await ctx.send('Файл %s не найден' % name)
      return
      
    
    with open('./darkheresy/%s.json' % name, 'r') as file:
      stats = json.loads(file.read())
    
    t = (stats['name'].ljust(17),)
    for stat in self.statsEn:
      t = t + (stats[stat],)
      
    text = """```
+===================+
| %.17s |
+==============+====+
| Ближний Бой  | %2d |
| Баллистик    | %2d |
| Сила         | %2d |
+--------------+----+
| Выносливость | %2d |
| Ловкость     | %2d |
| Интеллект    | %2d |
+--------------+----+
| Восприятие   | %2d |
| Сила Воли    | %2d |
| Товарищество | %2d | 
+--------------+----+
```""" % t
    
    await ctx.send(text)
    
  @dh.command()
  async def dice(self, ctx, name: str, stat: str, bonus: str = '+0', count: int = 1):
    """Бросок кубика для Dark Heresy.

    Аргументы:
    -----------
    name: `str`
      Имя файла.
    stat: `str`
      Сокращение характеристики, что надо посчитать.
    bonus: `str` = '+0'
      Выражение бонуса к базовой характеристике.
    count: `int` = 1
      Количество бросков.
    """
    stats = {}
    try:
      with open('./darkheresy/%s.json' % name) as file:
        stats = json.loads(file.read())
    except:
      await ctx.send('Файл %s не найден' % name)
      return
      
    if stat not in self.statsEn:
      await ctx.send('Нет статы %s' % stat)
      return

    formula = '%s%i%s' % ("(" * bonus.count(')'), stats[stat], bonus)
    val = math.ceil(eval(formula))
    resArr = []
    
    for _ in range(count):
      res = random.randint(1, 100)
      if res > val:
        resArr.append('*%s*, неудача (%i/%i)' % (self.statsRu[self.statsEn.index(stat)], res, val))
      else:
        resArr.append('*%s*, __успех__ (%i/%i)' % (self.statsRu[self.statsEn.index(stat)], res, val))
        
    await ctx.send('**%s**\n%s\n`%s`' % (stats['name'], '\n'.join(resArr), formula))

def setup(bot):
  bot.add_cog(KurisuRND(bot))