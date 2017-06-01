from transitions.extensions import GraphMachine
import telegram
from flask import Flask, request, send_file

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_user(self, update):
        text = update.message.text
        return text.lower() == '/start'
    

    def is_going_to_state11(self, update):
        text = update.message.text
        return text.lower() == '1'

    def is_backgoing_to_state11(self, update):
        text = update.message.text
        return text.lower() == 'no'

    def is_going_to_state12(self, update):
        text = update.message.text
        return text.lower() != 'yes' and text.lower() != 'no'

    def is_going_to_state13(self, update):
        text = update.message.text
        return text.lower() == 'yes'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == '2'

    def is_going_to_check1(self, update):
        text = update.message.text
        return text.lower() == 'check'

    def is_going_to_check2(self, update):
        text = update.message.text
        return text.lower() != 'back'

    def is_going_to_delete1(self, update):
        text = update.message.text
        return text.lower() == 'delete'

    def is_going_to_deleteday1(self, update):
        text = update.message.text
        return text.lower() == '某天'

    def back_user(self, update):
        text = update.message.text
        return text.lower() == 'back'

    def is_going_to_deleteday2(self, update):
        text = update.message.text
        return text.lower() != '某天'

    def is_going_to_deleteall(self, update):
        text = update.message.text
        return text.lower() == '全部'

    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == '3'

    def is_going_to_state3yes(self, update):
        text = update.message.text
        return text.lower() == 'yes' 

    def is_going_to_state3no(self, update):
        text = update.message.text
        return text.lower() == 'no' 

    def on_enter_user(self,update):
        update.message.reply_text("1.登記帳務\n2.查詢或刪除帳目\n3.妙蛙種子feat.體育新聞\n*輸入back可回首頁")

    def on_enter_state11(self, update):
        update.message.reply_text("請輸入 日期 項目 金額（請在中間空格）")

    def on_exit_state11(self, update):
        print('Leaving state11')

    def on_enter_state12(self, update):
        update.message.reply_text("SURE?")

    def on_exit_state12(self, update):
        print('Leaving state12')

    def on_enter_state13(self, update):
        update.message.reply_photo(open('3.jpg','rb'))
        update.message.reply_text("登記成功囉！")
        #self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_check1(self, update):
        update.message.reply_text("以下為歷史記帳（日期,項目,金額）")

    def on_exit_check1(self, update):
        print('Leaving check1')

    def on_enter_check2(self, update):
        update.message.reply_text("記帳再接再厲～～")
        self.go_back(update)

    def on_exit_check2(self, update):
        print('Leaving check2')

    def on_enter_delete1(self, update):
        update.message.reply_text("希望刪除的資料？")

    def on_exit_delete1(self, update):
        print('Leaving delete1')

    def on_enter_deleteall(self, update):
        update.message.reply_text("已刪除全部紀錄")

    def on_exit_deleteall(self, update):
        print('Leaving deleteall')

    def on_enter_deleteday1(self, update):
        update.message.reply_text("請問需刪除何天資料")

    def on_exit_deleteday1(self, update):
        print('Leaving deleteday1')

   # def on_enter_deleteday2(self, update):
        

    def on_exit_deleteday2(self, update):
        print('Leaving deleteday2')

    def on_enter_state3(self, update):
        update.message.reply_photo(open('3.jpg','rb'))
        update.message.reply_text("妙蛙種子為草屬性及毒屬性的種子寶可夢，有如青蛙般的身體上背著大顆充滿營養的種子，與種子是共生關係。這顆種子從出生時開始種植，出生後暫時由種子中獲取養分成長。成為妙蛙草後由中生長出草，成為妙蛙花後開花。")
        update.message.reply_text("想要妙蛙播報新聞嗎？")

    def on_exit_state3(self, update):
        print('Leaving state3')

    def on_exit_state3yes(self, update):
        print('Leaving state3yes')

    def on_enter_state3no(self, update):
        update.message.reply_text("我才不理你哩")
        self.toyes(update)
