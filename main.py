import requests
from bs4 import BeautifulSoup
from requests.api import get
import telebot
from telebot import types

bot = telebot.TeleBot("2143029358:AAHWODHfo7Q0WFQv73MsScR4XJhVENKuRK8", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
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
# {numbers[j+1]}
# price = news[0].select('p[class="price"] strong')[0].text
# pic = news[0].select('img[class="fleft"]')[0]['src']
# title = news[0].select('img[class="fleft"]')[0]['alt']
# address = news[0].select('i[data-icon="location-filled"]')[0].parent.text
# date = news[0].select('i[data-icon="clock"]')[0].parent.text
# general = f"{address} {date}"
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text != '/start':
        text = (message.text).replace(' ','-')
        # print(text)
        sahifa = f"https://www.olx.uz/oz/list/q-{text}/"
        r = requests.get(sahifa)
        soup = BeautifulSoup(r.text, 'html.parser')
        news = soup.select('tr[class="wrap"]') # mahsulotlar
        print(len(news))
        bot.send_message(message.chat.id,'🕔')
        filtering_products(news,message)
    else:
        bot.send_message(message.chat.id, 'Assalomu alaykum. Olx ning norasmiy botiga xush kelibsiz.\nBu botda siz hech qanday qiyinchiliklarsiz olx dan bir qancha mahsulotlarni topishingiz mumkin.\n<a href="https://www.olx.uz/oz/">Web Sayt</a>', parse_mode='HTML')
    

def filtering_products(news,message):
    for j, i in enumerate(news):
        
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
        
        id = None
        # print(numbers[str(j)[0]])
        if len(str(j)) ==3:
            id = f"{numbers[str(j)[0]]} {numbers[str(j)[1]]} {numbers[str(j)[2]]}"
        elif len(str(j)) == 2:
            id = f"{numbers[str(j)[0]]}{numbers[str(j)[1]]}"
        else:
            id = f"{numbers[str(j)[0]]}"
        text = f'''
{id}

✅{title}

💰{price}

🏘 🕔{general}

🌐 <a href="{get_link}">Web Sayt</a>

        '''
        # bot.send_message(message.chat.id, text)
        markup = types.InlineKeyboardMarkup(row_width=2,)
        itembtna = types.InlineKeyboardButton('Tavsif', callback_data=str(get_link))
        phone = types.InlineKeyboardButton('📞 Web', callback_data=str(get_link))
        markup.add(itembtna, phone)
        bot.send_photo(message.chat.id, pic, caption=text, parse_mode='HTML')

bot.infinity_polling()