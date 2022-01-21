from .. import loader		
from asyncio import sleep

class IrisBotMod(loader.Module):
	"""Я рекомендую создать вам чат ,где вы будете использовать данный модуль, чтобы вас не беспокоили лишнии уведомления и тд. Так же можно это делать в лс Iris-а."""
	strings = {"name": "IrisBot"}
	
	def __init__(self):
		self.farm = True
		self.virys = True
		
	async def farmcmd(self, message):
		"""Включает команду "Ферма". Чтобы остановить, используйте "ирисфарм стоп"."""
		while self.farm:
			await message.reply("Ферма\n\n<b>Следующая команда будет произведена через 4 часа.\n\nIrisBot by @Gkpole</b>")
			await sleep(14500)
			
	async def virysncmd(self, message):
		"""Включает команду "Заразить =" (Заражает равного по силе соперника). Чтобы остановить, используйте "ирисвирус стоп"."""
		while self.virys:
			await message.reply("Заразить =\n\n<b>Следующая команда будет произведена через 1 час.\n\nIrisBot by @Gkpole</b>")
			await sleep(3600)
			
	async def virysecmd(self, message):
		"""Включает команду "Заразить -" (Заражает слабого соперника). Чтобы остановить, используйте "ирисвирус стоп"."""
		while self.virys:
			await message.reply("Заразить -\n\n<b>Следующая команда будет произведена через 1 час.\n\nIrisBot by @Gkpole</b>")
			await sleep(3600)
			
	async def viryshcmd(self, message):
		"""Включает команду "Заразить +" (Заражает сильного соперника) . Чтобы остановить, используйте "ирисвирус стоп"."""
		while self.virys:
			await message.reply("Заразить +\n\n<b>Следующая команда будет произведена через 1 час.\n\nIrisBot by @Gkpole</b>")
			await sleep(3600)
			
	async def watcher(self, message):
		me = (await message.client.get_me())
		if message.sender_id == me.id:
			if message.text.lower() == "ирисфарм стоп":
				self.farm = False
				await message.reply("<b>Ирисфарм остановлен.</b>")
			if message.text.lower() == "ирисвирус стоп":
				self.virys = False
				await message.reply("<b>Ирисвирус остановлен.</b>")
				
	async def linkcmd(self, message):
		"""Если у вас не работают команды,используйте данную команду, чтобы заново установить модуль."""
		await message.edit("<code>.dlmod https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/d/42wBTBiz5WJdwQ</code>\n\n<b>IrisBot by Gkpole")
		
			
			

		
			
