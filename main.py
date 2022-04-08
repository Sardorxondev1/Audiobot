import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
import keyboard as kb
from onesec_api import Mailbox
import json
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def texthandler(m: types.Message):
	if m.text != '✉️ Получить почту':
		await m.answer(f'👋Приветствую тебя.\n🙂Этот бот создан для быстрого получения временной почты\n\n ✅Подписывайся: @chop_bots', reply_markup=kb.menu)
	elif m.text == '✉️ Получить почту':
		ma = Mailbox('')
		email = f'{ma._mailbox_}@1secmail.com'
		await m.answer(f'📫 Твоя почта: {email}\n\n📩Почта проверяется автоматически каждые 5 секунд, если придет новое письмо, мы вас об этом оповестим!\n\n⚠️На 1 почту можно получить только - 1 письмо⚠️')
		while True:
			mb = ma.filtred_mail()
			if isinstance(mb, list):
				mf = ma.mailjobs('read',mb[0])
				js = mf.json()
				fromm = js['from']
				theme = js['subject']
				mes = js['textBody']
				await m.answer(f'📩Новое письмо:\n<b>От</b>: {fromm}\n<b>Тема</b>: {theme}\n<b>Сообщение</b>: {mes}', reply_markup=kb.menu, parse_mode='HTML')
				break
			else:
				pass
			await asyncio.sleep(5)
 

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True) # Запуск
