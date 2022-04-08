import os
import requests
import telebot
from telebot import types, apihelper


bot = telebot.TeleBot('5101656331:AAHzdO1JgViYtCFdyn4IUKbBkmpxdpRSbTc')

chat_ids_file = 'user.txt'
users_amount = [0]
def save_chat_id(chat_id):
    chat_id = str(chat_id)
    with open(chat_ids_file,"a+") as ids_file:
        ids_file.seek(0)
        ids_list = [line.split('\n')[0] for line in ids_file]
        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'NEW USER: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
    return

@bot.message_handler(commands=['start'])
def start_message(message):
	save_chat_id(message.chat.id)
	bot.send_message(message.chat.id,'''Assalomu alaykuk Xush kelibsiz menga rasm yuboring men sizga unig Havolasini yuboraman.''',disable_web_page_preview = True,parse_mode='HTML')

@bot.message_handler(content_types=['photo'])
def send_text(message):
	file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open(f'{message.chat.id}.jpg', 'wb') as new_file:
		new_file.write(downloaded_file)
	new_file.close()
	filesfiles = open(f'{message.chat.id}.jpg', "rb")
	files = {"files": filesfiles}
	r = requests.post("https://telegra.ph/upload", files=files)
	info = r.json()
	err = info[0].get("error")
	if err:
		bot.reply_to(message, f"Failed to upload. Reason: {err}")
		return
	url = "https://telegra.ph" + info[0].get("src")
	keyboard = types.InlineKeyboardMarkup()	
    
    
	keyboard.add(types.InlineKeyboardButton(text='Kanalimiz',url=f't.me/off_python))
	bot.reply_to(message, f'''<b>🖼 Surat moffaqiyatli yuklandi :</b>
<b>└Havola:</b> {url}''',disable_web_page_preview = True,parse_mode='HTML',reply_markup=keyboard)
	filesfiles.close()
	os.remove(f'{message.chat.id}.jpg')
    
    

bot.polling(True)
