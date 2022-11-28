import telebot
from telebot import types
import datetime
import logging
import os
from dotenv import load_dotenv,find_dotenv
import sqlite3

#Load .env variables
load_dotenv(find_dotenv())
#print(os.getenv('TOKEN'))

#bot identity
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
version = "0.4.0"
totalgc = 1

#sqlite
#db_name = 'database.db'
def run_query(query):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()

'''
cur.excute()
from row in data:
    print(row)

#coomit buat manipulasi data
conn.commit()
conn.close()
'''

#setting log
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def log(message,commandText):
    tanggal = datetime.datetime.now()
    tanggal = tanggal.strftime('[%d %B %Y]')
    firstName = message.chat.first_name
    lastName = message.chat.last_name
    text_log='{},{},{},{}\n'.format(tanggal,firstName,lastName,commandText)
    log_bot = open('log.txt','a')
    log_bot.write(text_log)
    log_bot.close

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log(message,'start')
    #memanggil inline keyboard
    markup = types.InlineKeyboardMarkup()
    btnContactOwner = types.InlineKeyboardButton('Berdonasi',url='https://t.me/BottyCu/79')
    
    #assign tata letak keyboard
    markup.row(btnContactOwner)
    bot.reply_to(message,'Bot ini Membutuhkan Biaya Untuk Beroperasi Lagi , Kirim Donasi Untuk Mengaktifkannya Kembali... Cek /logs_donation untuk melihat baru berapa yang berdonasi.',reply_markup=markup)

@bot.message_handler(commands=['logs_donation'])
def show_bot_version(message):
    log(message,'version')
    bot.reply_to(message,'===========================\n🔒LOGS DONATION🔒\n===========================\n\n-Kosong\n\n==========================='.format(version))

@bot.message_handler(commands=['groupinfo'])
def info(message):
    log(message,'groupinfo')
    chat_id=message.chat.id
    bot.reply_to(message,'Group ID : {}'.format(chat_id))

@bot.message_handler(commands=['list'])
def show_instagram_profile(message):
    log(message,'list')
    chat_id=message.chat.id

    #check id chat
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    data = cur.execute('''
        SELECT * from "room" WHERE from_gc="{chat_id}";
    '''.format(chat_id=chat_id))
    record = data.fetchall()

    if record:
        print("Record ada")
        bot.send_message(chat_id,'Kode Di Group Ini Saja\n')  
        for row in record:
            print(row)
            bot.send_message(chat_id,'{} /public /delete\n'.format(row[1]))        
        print("Done loop")
        

    else:
        print("Record tidak ada")
        nama_gc = message.chat.title
    
    conn.close()

    
    

    

print('Bot Start Running')
bot.polling()
