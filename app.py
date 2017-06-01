import sys
from io import BytesIO

import sqlite3
import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('database')
print("Opened database successfully")
'''
conn.execute('CREATE TABLE items (date TEXT,item TEXT,money TEXT)')
print("Table created successfully")
#conn.close()
'''
API_TOKEN = '359802451:AAGxmX8GrItYk3chamGXXSFWlx9DQ3WbrvA'
WEBHOOK_URL = 'https://065afd93.ngrok.io/hook'

re_data=None

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state11',
        'state12',
        'state13',
        'state2',
        'delete1',
        'deleteall',
        'deleteday1',
        'deleteday2',
        'check1',
        'check2',
        'state3',
        'state3yes',
        'state3no'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': [
                'state11',
                'state12',
                'state13',
                'state2',
                'delete1',
                'deleteall',
                'deleteday1',
                'deleteday2',
                'check1',
                'check2',
                'state3',
                'state3yes',
                'state3no'
            ],
            'dest': 'user',
            'conditions': 'back_user'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state11',
            'conditions': 'is_going_to_state11'
        },
        {
            'trigger': 'advance',
            'source': 'state11',
            'dest': 'state12',
            'conditions': 'is_going_to_state12'
        },
        {
            'trigger': 'advance',
            'source': 'state12',
            'dest': 'state13',
            'conditions': 'is_going_to_state13'
        },
        {
            'trigger': 'advance',
            'source': 'state12',
            'dest': 'state11',
            'conditions': 'is_backgoing_to_state11'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },  
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'check1',
            'conditions': 'is_going_to_check1'
        }, 
        {
            'trigger': 'advance',
            'source': 'check1',
            'dest': 'check2',
            'conditions': 'is_going_to_check2'
        },   
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'delete1',
            'conditions': 'is_going_to_delete1'
        },       
        {
            'trigger': 'advance',
            'source': 'delete1',
            'dest': 'deleteday1',
            'conditions': 'is_going_to_deleteday1'
        },  
        {
            'trigger': 'advance',
            'source': 'deleteday1',
            'dest': 'deleteday2',
            'conditions': 'is_going_to_deleteday2'
        },
        {
            'trigger': 'advance',
            'source': 'delete1',
            'dest': 'deleteall',
            'conditions': 'is_going_to_deleteall'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
        },
        {
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state3yes',
            'conditions': 'is_going_to_state3yes'
        },
        {
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state3no',
            'conditions': 'is_going_to_state3no'
        },   
        {
            'trigger': 'toyes',
            'source': 'state3no',
            'dest': 'state3yes'
        },         
        {
            'trigger': 'go_back',
            'source': [
                'check2'
            ],
            'dest': 'user'
        },
        {
            'trigger': 'back',
            'source':'state13',
            'dest': 'user'
        },
        {
            'trigger': 'back',
            'source':'deleteall',
            'dest': 'user'
        },
        {
            'trigger': 'back',
            'source':'deleteday2',
            'dest': 'user'
        },
        {
            'trigger': 'back',
            'source':'state3yes',
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=True,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    state_do(update, machine.state)
    print(machine.state)
    return 'ok'

def state_do(update, state):
    if state=='state12':
        global re_data
        re_data=update.message.text
        print(re_data)
        custom_keyboard = [['yes','no']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, 
                         text="(if press no,you will be back)", 
                         reply_markup=reply_markup)

    elif state=='state13': #insert
        stmt = "INSERT INTO items (d,item,money) VALUES (?,?,?)"
        words=re_data.split()
        args = (str(words[0]),str(words[1]),str(words[2]),)
        conn.execute(stmt, args)        
        #args = (update.message.text,)
        #conn.execute(stmt, args)
        conn.commit()
        print ("insert ok")

        machine.back(update)
    
    elif state=='state2':
        custom_keyboard = [['delete', 'check']] 
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, 
                         text="刪除or查詢?", 
                         reply_markup=reply_markup) 

    elif state=='check1': #search/check
        stmt = "SELECT d,item,money from items"
        cursor=conn.execute(stmt)
        for row in cursor:
            
            update.message.reply_text(repr(row[0])+","+repr(row[1])+","+repr(row[2]))    

        conn.commit()
        update.message.reply_text("輸入任意文字離開") 

    elif state=='delete1':
        custom_keyboard = [['全部', '某天']] 
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, 
                         text="全部or某天?", 
                         reply_markup=reply_markup)         
    
    elif state=='deleteall':
        stmt = "DELETE from items"
        cursor=conn.execute(stmt)
        conn.commit()
        machine.back(update)
    
    elif state=='deleteday1': #search/check
        stmt = "SELECT d,item,money from items"
        cursor=conn.execute(stmt)
        for row in cursor:
            
            update.message.reply_text(repr(row[0])+","+repr(row[1])+","+repr(row[2]))    

        conn.commit()

    elif state=='deleteday2':
        print(update.message.text)
        stmt = "DELETE from items WHERE d ="+repr(update.message.text)
        cursor=conn.execute(stmt)
        conn.commit()
        update.message.reply_text("已成功刪除該天資料") 
        machine.back(update)
 
    elif state=='state3':
        custom_keyboard = [['yes', 'no']] 
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, 
                         text="yes or no?", 
                         reply_markup=reply_markup)
    
    elif state=='state3yes':
        req=requests.get("http://www.tsna.com.tw")
        #print (req.text.encode('utf-8'))
        soup=BeautifulSoup(req.text, "html.parser")
        #print(soup)

        count=0
        for line in soup.select('.pic_iten'):
            count=count+1
            if count==3:
                break
         #   update.message.reply_text(line)
         #   update.message.reply_text(str(line.find('a').text))
         #   update.message.reply_text(soup.find('a'))
            update.message.reply_text(str(line.select('.text')[0].text))
        machine.back(update)

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
    
