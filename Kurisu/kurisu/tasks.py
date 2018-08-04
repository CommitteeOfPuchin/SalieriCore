import asyncio

allTasks = {}

loop = None

async def new(task):
	if asyncio.iscoroutinefunction(task):
		fn = '%s.%s' % (task.__module__, task.__name__)
		allTasks[fn] = loop.create_task(task())

		return True
	else:
		return False

async def cancel(task):
	fn = '%s.%s' % (task.__module__, task.__name__)
	if fn in allTasks:
		allTasks[fn].cancel()

		while not allTasks[fn].cancelled():
			allTasks[fn].cancel()
			await asyncio.sleep(0)

		allTasks.pop(fn)
		return True
	else:
		return False
