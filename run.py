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
version = "0.3.3"
totalgc = 4

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
    btnContactOwner = types.InlineKeyboardButton('Pamsky.',url='t.me/impamsky')
    
    #assign tata letak keyboard
    markup.row(btnContactOwner)
    bot.reply_to(message,'Hallo, Sapu terbang siap mengantar pesan ke Group sebelah. \n/help untuk melihat bantuan.\nKalo masi bingung tanya creator',reply_markup=markup)

@bot.message_handler(commands=['version'])
def show_bot_version(message):
    log(message,'version')
    bot.reply_to(message,'Sekarang bot di versi\nv{}'.format(version))

@bot.message_handler(commands=['help'])
def send_help(message):
    log(message,'help')
    bot.reply_to(message,'Command yang dapat di gunakan :\n\n/role <Code> <Mode> <Host>\n/version')

@bot.message_handler(commands=['role'])
def send_role(message):
    log(message,'role')
    texts = message.text.split(' ')
    code = texts[1]
    mode = texts[2]
    host = texts[3]
    bot.reply_to(message,'Pesan di kirim ke {} group terdaftar.'.format(totalgc))

    #gc pam
    bot.send_message(chat_id=-1001734121931,text='**`{code}` `{code}`\n`{code}` `{code}`**\n☝Click code to copy☝\n\nMode : {mode}\nHost : {host}'.format(code=code,mode=mode,host=host),parse_mode='MarkdownV2')
    #gc au indo gc
    bot.send_message(chat_id=-1001746697467,text='**`{code}` `{code}`\n`{code}` `{code}`**\n☝Click code to copy☝\n\nMode : {mode}\nHost : {host}'.format(code=code,mode=mode,host=host),parse_mode='MarkdownV2')
    #gc cucing
    bot.send_message(chat_id=-1001765155506,text='**`{code}` `{code}`\n`{code}` `{code}`**\n☝Click code to copy☝\n\nMode : {mode}\nHost : {host}'.format(code=code,mode=mode,host=host),parse_mode='MarkdownV2')
    #gc idn -1001607301547
    bot.send_message(chat_id=-1001607301547,text='**`{code}` `{code}`\n`{code}` `{code}`**\n☝Click code to copy☝\n\nMode : {mode}\nHost : {host}'.format(code=code,mode=mode,host=host),parse_mode='MarkdownV2')

@bot.message_handler(commands=['roletest'])
def send_roletest(message):
    log(message,'roletest')
    
    texts = message.text.split(' ')
        
    code = str(texts[1])
    mode = str(texts[2])
    host = str(texts[3])
       
    bot.send_message(chat_id=-1001734121931,text='**`{code}` `{code}`\n`{code}` `{code}`**\n☝Click code to copy☝\n\nMode : {mode}\nHost : {host}'.format(code=code,mode=mode,host=host),parse_mode='MarkdownV2')

@bot.message_handler(commands=['register'])
def register(message):
    log(message,'register')
    #mengambil data char
    chat_id=message.chat.id #id group
    
    #check id if has registered
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    data = cur.execute('''
        SELECT * FROM "group" where id_gc="{chat_id}"
    '''.format(chat_id=chat_id))
    if data.fetchone():
        print("Record ada")
        #for row in data:
        #   print('=============1')
        #    print(row)
        #    print('=============2')
        bot.send_message(chat_id,'Group sudah terdaftar sebelumnya')
        
    else:
        print("Record tidak ada")
        nama_gc = message.chat.title

        #if not register inserting query database
        query = 'INSERT INTO "group" (id_gc,nama_gc) values({chat_id},"{nama_gc}");'.format(chat_id=chat_id,nama_gc=nama_gc)
        run_query(query)
            
        #send massage if succes
        bot.send_message(chat_id,'Group ID : {} berhasil di daftarkan'.format(chat_id))
    conn.close()

@bot.message_handler(commands=['groupinfo'])
def info(message):
    log(message,'groupinfo')
    chat_id=message.chat.id
    bot.reply_to(message,'Group ID : {}'.format(chat_id))

print('Bot Start Running')
bot.polling()