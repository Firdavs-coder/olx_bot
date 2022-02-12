import requests
from bs4 import BeautifulSoup
from requests.api import get
import telebot
from telebot import types
import random

# bot = telebot.TeleBot("5042865364:AAH4Tndi4n_vawDY9sXyEUlS4omPIePaVT4", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2143029358:AAEUMfcLE7mUigh5NRrzJbWc75MGtLaPySk", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
# 0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
numbers = {
    '0':'0️⃣',
    '1':'1️⃣',
    '2':'2️⃣',
    '3':'3️⃣',
    '4':'4️⃣',
    '5':'5️⃣',
    '6':'6️⃣',
    '7':'7️⃣',
    '8':'8️⃣',
    '9':'9️⃣',
}



@bot.message_handler(commands=['subs'])
def start(message):
    if message.from_user.username == 'shavkatNor':
        res = requests.get("https://telegrambotbazasi.pythonanywhere.com//view_olx_users")
        subs = res.json()['subscribes_count']
        bot.send_message(message.chat.id, f"Obunachilaringiz <b>{subs}</b> ta", parse_mode='HTML')

# @bot.message_handler(content_types=['sticker'])
# def video(message):
#     print(message.sticker.file_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if check(message):
        if message.text != '/start':
            text = (message.text).replace(' ','-')
            # print(text)
            
            bot.send_message(message.chat.id,'🔎')
            filtering_products(text,message.chat.id,message.message_id)
        else:
            save_users(message)
            markup = types.InlineKeyboardMarkup(row_width=1)
            itembtna = types.InlineKeyboardButton('Kanalga o\'tish', url='https://t.me/python_flutter_uz')
            itembtnv = types.InlineKeyboardButton('Tekshirish', callback_data='check')
            markup.add(itembtna, itembtnv)
            bot.send_message(message.chat.id, 'Assalomu alaykum. Olx ning norasmiy botiga xush kelibsiz.\nBu botda siz hech qanday qiyinchiliklarsiz olx dan bir qancha mahsulotlarni topishingiz mumkin.\n<a href="https://www.olx.uz/oz/">Web Sayt</a>', parse_mode='HTML', reply_markup=markup)
    

def filtering_products(text,id,message_id):
    # for j, i in enumerate(news):
        bot.delete_message(id,message_id)
        sahifa = f"https://www.olx.uz/oz/list/q-{text}/"
        r = requests.get(sahifa)
        soup = BeautifulSoup(r.text, 'html.parser')
        news = soup.select('tr[class="wrap"]')
        jami = len(news)
        tavakkal = random.randrange(0,jami)
        i = news[tavakkal]
        try:
            price = i.select('p[class="price"] strong')[0].text
        except:
            price = None
        try:
            pic = i.select('img[class="fleft"]')[0]['src']
        except:
            pic = None
        try:
            title = i.select('img[class="fleft"]')[0]['alt']
        except:
            title = None
        try:
            address = i.select('i[data-icon="location-filled"]')[0].parent.text
        except:
            address = None
        try:
            date = i.select('i[data-icon="clock"]')[0].parent.text
        except:
            date = None
        general = f"{address} {date}"
        try:
            get_link = i.select('img[class="fleft"]')[0].parent['href']
        except:
            get_link = None
        markup = types.InlineKeyboardMarkup(row_width=1)
        itembtnv = types.InlineKeyboardButton('Boshqasini tanlash', callback_data = text)
        markup.add(itembtnv)
        
        # id = None
        # if len(str(j)) ==3:
        #     id = f"{numbers[str(j)[0]]} {numbers[str(j)[1]]} {numbers[str(j)[2]]}"
        # elif len(str(j)) == 2:
        #     id = f"{numbers[str(j)[0]]}{numbers[str(j)[1]]}"
        # else:
        #     id = f"{numbers[str(j)[0]]}"
        text = f'''

✅{title}

💰{price}

🏘 🕔{general}

🌐 <a href="{get_link}">Web Sayt</a>

        '''
        bot.send_photo(id, pic, caption=text, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check":
        subscribe = bot.get_chat_member(chat_id=-1001373178208, user_id=call.from_user.id).status
        if subscribe == 'creator' or subscribe == 'member' or subscribe == 'administrator':
            bot.send_message(call.from_user.id, "✅ Botimizdan bemalol foydalanishingiz mumkin!\n🔍 Foydalanish uchun so'z yuboring.",)
        else:
            bot.send_message(call.from_user.id, "👉Iltimos. kanalga a'zo bo'ling\n@python_flutter_uz")
    else:
        filtering_products(call.data,call.from_user.id,call.message.id)   

def add_recline(message):
    if message.from_user.username == 'shavkatNor' and message.caption:
        res = requests.get("https://telegrambotbazasi.pythonanywhere.com/view_olx_users")
        users = res.json()['data']
        for i in users:
            id = i['name']
            try:
                bot.forward_message(int(id),message.chat.id,message.message_id)
            except:
                res = requests.get(f"https://telegrambotbazasi.pythonanywhere.com/olx/delete/{id}")

@bot.message_handler(content_types=['video'])
def video(message):
    if message.from_user.username == 'shavkatNor' and message.caption:
        add_recline(message)



@bot.message_handler(content_types=['photo'])
def img(message):
    save_users(message)
    if message.from_user.username == 'shavkatNor' and message.caption:
        add_recline(message)

def check(message):
    subscribe = bot.get_chat_member(chat_id=-1001373178208, user_id=message.from_user.id).status
    if subscribe == 'creator' or subscribe == 'member' or subscribe == 'administrator':
        return True
    else:
        bot.send_message(message.chat.id, "Iltimos. kanalga a'zo bo'ling\n👉@python_flutter_uz") 
        return False

def save_users(message):
    id = message.from_user.id
    ok = requests.get(f"https://telegrambotbazasi.pythonanywhere.com/olx/add/{id}")

bot.infinity_polling()