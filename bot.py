from sql import  mydb, mycursor
from config import token, all_cripts
import telebot

from bs4 import BeautifulSoup
import requests
import re
from time import time


class_curse = "h2 text-semi-bold details-panel-item--price__value"
repeat = False
current_func = "course"
duration_sub = 30
cm = ""
bot = telebot.TeleBot(token)
language = "eng"

rules_eng = "Some rules of writing cryps: \
Instead of space write dash(-) in names of crypts."
rules_rus = "Некоторые правила письма криптовалют:\n\
Писать полное названия допустим Bitcion вместо btc;\n\
Вместо пробелов писать тире(-) в названии крипт."

commands = {"start": "Start using bot",
 "help": "to see all commands", 
 "settings": "Set configuration of this bot",
 "add_list": "You can reate and add your favorite crypts to list",
"price_list": "Check price of crypts from list",
"clear_list": "Clear list"
}
commands_rus = {
"start": "Начните использовать бот.",
 "help": "Чтоби увидеть все команди и их функцию", 
 "settings": "Встановіть конфігурацію цього бота",
 "add_list": "Вы можете создавать и добавлять свои любимые криптовалюту в список",
"price_list": "Проверить цену криптовалюти из списка",
"clear_list": "Очистка списка с криптовалютами"
}
cur_adv = 0
description_eng = "Hi! If you are interested in crypto world ,\
 This bot is for you.\n It was created to simlify your life!\n\
 Write cript to chat and bot will return price value. \n\
One more advantage is that : You can create list of your favourite crypts \
and after check price of crypts from list by one click.\n\
Some rules of writing cryps: \
Instead of space write dash(-) in names of crypts.\n\
You can subscribe to this bot(2 dolars - 1 month).\
 With subscribe your list can contain 15 elements,without subscribe - 4.\
 More detail describe about last changes.\
 And many other beneficial function"
description_rus = "Привет! Если вы заинтересованы в мире криптовалют, \
Тогда етот бот для вас! \n\
Он был создан, чтобы упростить вашу жизнь!\n\
Написать криптовалюту в чат\n\
Еще одно преимущество: вы можете создать список ваших любимых криптовалют \
и после ви сможете проверить цену всех криптовалют из списка одним кликом\
Вы можете подписаться на этого бота (2 доллара - 1 месяц). \
 С подпиской ваш список может содержать 15 элементов, без подписки - 4. \
 Более подробно опишите о последних изменениях. \
 И многие другие полезные функции" + rules_rus
adv_delay = 0 #Delay from last user's advertisment  
duration_sub = 30
advertisments = ["https://www.test.com", "test2 sdfgs","advertisment 3"]

@bot.message_handler(commands=["help"])
def comand_help(message): 
    global cm, commands, mycursor, mydb
    user = str(message.chat.id)
    mycursor.execute("SELECT lang FROM main WHERE id = " + user)
    language = mycursor.fetchall()[0][0]
    cm = ""
    if language == "eng":
        pass
    elif language == "rus":
        commands = commands_rus
    for i in commands:
        cm = str(cm) + "/"+str(i) +" - "+ str(commands[str(i)]) +"\n"
    cm = cm +"\n" + rules_eng
    bot.send_message(message.chat.id, cm)

@bot.message_handler(commands=["start"])
def begin(message):
    global mydb, mycursor, language
    user = str(message.chat.id)
    mycursor.execute("SELECT * FROM main WHERE id = " + user)
    test_exist = mycursor.fetchall()
    if test_exist == []:
        now_date = int(time()/3600/24)
        mycursor.execute("INSERT INTO main(id,lang,subscribe,adv_time) VALUES(" \
        + str(user) + ",'rus', 0" + str(now_date) + ")")
        mydb.commit()
    else:
        pass
    mycursor.execute("SELECT lang FROM main WHERE id = " + user)
    language = mycursor.fetchall()[0][0]  
    print(language)
    if language == "eng":
        bot.send_message(user, description_eng)
    elif language == "rus":
        bot.send_message(user, description_rus)

'''Create table in db with basic crypts for user or change type of bot'''
@bot.message_handler(commands = ["add_list"])
def create_list(message):
    global current_func, language, user_cripts, duration_sub
    user = str(message.chat.id)
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row("Continue", "Cancel")
    current_func = "course"
    mycursor.execute("SELECT crypts FROM main " +"WHERE id="\
    + str(message.chat.id))
    user_cripts = mycursor.fetchall()
    mycursor.execute("SELECT lang, subscribe, date_sub FROM main WHERE id = " + user)
    b = mycursor.fetchall()[0]
    language = b[0]
    subscribe = b[1]
    date = b[2]
    number = True
    if subscribe == 1:
        now_date = int(time()/3600/24)#Convert to days
        if now_date > date + duration_sub:
            mycursor.execute("UPDATE main SET subscribe = 0 WHERE id = " + user)
            mydb.commit()
    print(user_cripts[0][0])
    if not user_cripts[0][0] == None and not user_cripts[0][0] == set():
        print(1)
        if subscribe == 0:
            if len(user_cripts[0][0]) >= 4:
                if language == "eng":
                    created_list_text = "Your list contain max amount of crypts(4): "
                elif language == "rus":
                    created_list_text = "Ваш список заполнен на максимум(4): "
                number = False
            else:
                if language == "eng":
                    created_list_text = "These crypts are in this list : "
                elif language == "rus":
                    created_list_text = "В етом списке уже есть : "
                mycursor.execute("UPDATE main SET cur_func = 2 WHERE id = " + user)
                mydb.commit()
        else:
            if len(user_cripts[0][0]) >= 8:
                if language == "eng":
                    created_list_text = "Your list contain max amount of crypts(8)"
                elif language == "rus":
                    created_list_text = "Ваш список заполнен на максимум(8) "
                number = False
            else:
                if language == "eng":
                    created_list_text = "These crypts are in this list : "
                elif language == "rus":
                    created_list_text = "В етом списке уже есть : "
                mycursor.execute("UPDATE main SET cur_func = 2 WHERE id = " + user)
                mydb.commit()
        for cur_cript in user_cripts[0][0]:
            print(cur_cript)
            created_list_text = created_list_text + cur_cript.title() + ", "
    else:# if user_cripts[0][0] == set():
        if language == "eng":
            created_list_text = "Your list for this moment is empty."
        elif language == "rus":
            created_list_text = "Ваш список на даний момент пустой."
        mycursor.execute("UPDATE main SET cur_func = 2 WHERE id = " + user)
        mydb.commit()
    if number:
        if language == "eng":
            created_list_text = created_list_text + "\n\
Continue or cancel .\n\
Format of introduction : 1cript,2cript..."
        elif language == "rus":
            created_list_text = created_list_text + "\n\
Продолжайте или отмените .\n\
Формат введения : 1cript,2cript..."
    if number:
        bot.send_message(user, created_list_text, reply_markup = markup)
    else:
        bot.send_message(user, created_list_text)

'''Check price of basic user's crypts'''
@bot.message_handler(commands = ["price_list"])
def price_list(message):
    global mydb, mycursor, commands, language, duration_sub
    user = str(message.chat.id) 
    mycursor.execute("SELECT crypts FROM main WHERE id = " + str(message.chat.id))
    user_cripts = mycursor.fetchall()
    mycursor.execute("SELECT lang, subscribe, date_sub FROM main WHERE id = " + user)
    b = mycursor.fetchall()[0]
    language = b[0]
    subscribe = b[1]
    date = b[2]
    print(user)
    print(user_cripts[0][0])
    if subscribe == 1:
        now_date = int(time()/3600/24)#Convert to days
        if now_date > date + duration_sub :
            mycursor.execute("UPDATE main SET subscribe = 0 WHERE id = " + user)
            mydb.commit()   
    msg = ""
    print(user_cripts[0][0])
    if user_cripts[0][0] != [] and user_cripts[0][0] != None:
        n = len(user_cripts)
        for cur_cript_unform in user_cripts[0][0]:#Find all courses
            cur_cript = str(cur_cript_unform)
            url = "https://coinmarketcap.com//currencies/" + cur_cript
            content = requests.get(url)
            soup = BeautifulSoup(content.text, "html.parser")
            curse = soup.find("span", {"class": class_curse})
            print(curse)
            msg += cur_cript.title() + " - " + str(curse.text) + "$ Dolars\n"
            print(msg)
        bot.send_message(message.chat.id, msg)#send message

    else:#Validate empty user list
        if language == "eng":
            empty_list_text = "You didn't add any cript to list"
        elif language == "rus":
            empty_list_text = "Ви не добавили ниодной криптовалюти в список."
        bot.send_message(message.chat.id, empty_list_text)

@bot.message_handler(commands = ["settings"])
def setting(message):
    global current_func, language, duration_sub
    user = str(message.chat.id)
    mycursor.execute("SELECT lang FROM main WHERE id = " + user)
    language = mycursor.fetchall()[0][0]  
    mycursor.execute("UPDATE main SET cur_func = 3 WHERE id = " + user)
    mydb.commit()
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row("Language")
    markup.row("Cancel")
    if language == "eng":
        settings_text = "Choose what you want to change."
    elif language == "rus":
        settings_text = "Виберите что ви хотите изменить."
    bot.send_message(message.chat.id, settings_text, reply_markup = markup)
@bot.message_handler(commands = ["clear_list"])
def delete_list(message):
    global mydb , mycursor, language
    user = str(message.chat.id)
    mycursor.execute("UPDATE main SET crypts=NULL WHERE id = "+str(message.chat.id))
    mydb.commit()
    mycursor.execute("SELECT lang FROM main WHERE id = " + user)
    language = mycursor.fetchall()[0][0]
    if language == "eng":
        bot.send_message(message.chat.id, "Your list was cleared")
    elif language == "rus":
        bot.send_message(message.chat.id, "Ваш список криптовалют бил очищен.")

'''Subscibe command'''
@bot.message_handler(commands = ["subscribe"])
def sub(message):
    global db,cursor, language, duration_sub
    user = str(message.chat.id)
    mycursor.execute("SELECT subscribe, date_sub FROM main WHERE id = " + user)
    b = mycursor.fetchall()[0]
    subscribe = b[0]
    date = b[1]
    now_date = int(time()/3600/24)
    mycursor.execute("UPDATE main SET subscribe = 1, date_sub = " \
+ str(now_date) + " WHERE id ="+str(message.chat.id))
    mydb.commit()


@bot.message_handler(content_types = ["text"])
# Basic function of bot which changed after some commands
def main_func(message):
    global mydb, mycursor, commands, current_func, repeat, language, duration_sub, cur_adv
    user = str(message.chat.id)
    print(str(message.text))
    mycursor.execute("SELECT lang, subscribe, date_sub, cur_func FROM main WHERE id = " + user)
    b = mycursor.fetchall()[0]
    language = b[0]
    subscribe = b[1]
    date = b[2]
    current_func = b[3]
    now_date = int(time()/3600/24)#Convert to days
    if subscribe == 1:
        
        if now_date > date + duration_sub:
            mycursor.execute("UPDATE main SET subscribe = 0 WHERE id = " + user)
            mydb.commit()
    '''main function - check curse of crypts what user send'''
    if current_func == 0 or current_func == None:#If func = course
        #Delete probels and lower register
        crypt = str(message.text).strip().lower()
        print(crypt)
        mycursor.execute("SELECT adv_time FROM main WHERE id="+user)
        b = mycursor.fetchall()[0]
        adv_time = b[0]
        if now_date >= adv_delay + adv_time:
            if subscribe == 0 or subscribe == None:
                bot.send_message(user, advertisments[cur_adv])
                if cur_adv + 1 < len(advertisments):
                    cur_adv += 1
                else:
                    cur_adv = 0
                mycursor.execute("UPDATE main SET adv_time=" + str(now_date) \
                + " WHERE id =" + user)
                mydb.commit()
        if crypt in all_cripts:
            '''Check course by parsing'''
            try:
                url = "https://coinmarketcap.com//currencies/" + str(message.text)
                content = requests.get(url)
                soup = BeautifulSoup(content.text, "html.parser")
                curse = soup.find("span", {"class": class_curse})
                print(curse.text)
                price_text = str(message.text).title() + " - "\
                 + str(curse.text) + "$ Dolars"
                curse_grow = ""
                '''Two classes can be 24hours changes : negative or positive 
                It will check first negative and add to curse_grow after
                positive and add too
                '''
                if subscribe == 1:
                    curse = soup.find_all("span", {"class": "text-semi-bold negative_change"})
                    if curse != []:
                        for i in curse:
                            curse_grow = curse_grow + str(i.text)
                    curse = soup.find_all("span", {"class": "text-semi-bold positive_change"})
                    if curse != []:
                        for i in curse:
                            curse_grow = curse_grow + str(i.text)
                    # Find all 3 args with validation as -or+ demicals and may be %
                    val = re.compile(r'-?\+?[\d.,]{1,25}%?')
                    grows = val.findall(curse_grow)
                    print(grows)
                    # find needed arg in True numiration
                    if "%" in grows[0]:
                        price_text = price_text + ".\n" + "Grow of this \
crypt by last 24 hours: " + str(grows[1]) + "( " + str(grows[2]) + " )"
                    else:
                        price_text = price_text + ".\n" + "Grow of this \
crypt yesterday by last 24 hours: " + str(grows[0]) + "( " + str(grows[1]) + " )"

                bot.send_message(message.chat.id, price_text)
            except:#For any parse problem
                pass
        else:
            '''For not real crypts'''
            if language == "eng":
                fail_text = "We hasn't in base this crypt."
            elif language == "rus":
                fail_text = "Ета криптовалюту не сущесвуєт в базе етого бота."
            bot.send_message(message.chat.id, fail_text)

    elif current_func == 1:#If current func = add to list
        global user_cripts
        user = str(message.chat.id)
        mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
        mydb.commit()
        mycursor.execute("SELECT crypts FROM main " +"WHERE id="\
        + str(message.chat.id))
        user_cripts = mycursor.fetchall()
        mycursor.execute("SELECT lang, subscribe, date_sub FROM main WHERE id = " + user)
        b = mycursor.fetchall()[0]
        language = b[0]
        subscribe = b[1]
        add_cripts_list = message.text.split(",")

        success = True
        false_cripts = []
        print(add_cripts_list)
        crypts = ""
        print(user_cripts)
        if user_cripts[0][0] != None and user_cripts[0][0] != []:
            if subscribe == 0:
                while len(user_cripts[0][0])+len(add_cripts_list)>4:
                    del add_cripts_list[len(add_cripts_list)-1]
            else:
                while len(user_cripts[0][0])+len(add_cripts_list)>5:
                    del add_cripts_list[len(add_cripts_list)-1]

            for cr in user_cripts[0][0]:
                if crypts != "": 
                    crypts = crypts + ',' + cr
                else:
                    crypts = cr
        print(crypts+'1')
        print(add_cripts_list)
        #Start Validate all crypts one by one from add_cripts_list(msg by user)
        for cript in add_cripts_list:
            print(cript)
            cript_formated = cript.lower().strip()
            #Validate one crypt by existing in bot's base of crypts.
            if cript_formated in all_cripts:
                #Validate repiting crips in user cripts list
                for c in user_cripts:
                    c1 = c[0]
                    if c1 == cript_formated:
                        repeat = True
                    else:
                        pass
                if repeat:#If this crypt already exist 
                    pass
                else:#If all validation for this crypt successfully 
                    if not crypts == "":
                        crypts = crypts + "," + cript_formated
                    else: 
                        crypts = cript_formated
                    print(crypts)
            else:
                false_cripts.append(cript)
                success = False

        mycursor.execute("UPDATE main SET crypts = " + "'" + str(crypts) + "'" \
        + " WHERE id = " + str(message.chat.id))
        mydb.commit()
        '''Print result to user'''
        if success == True:#If all crypts added, successfilly
            if language == "eng":
                success_text = "New crypts saved successfully."
            elif language == "rus":
                success_text = "Новиє криптовалюти успешно сохранились."
            bot.send_message(message.chat.id, success_text)
        else:#If one or more crypts hasn't in bot base
            print(false_cripts)
            msg_result = ""
            for c in false_cripts:
                msg_result += c + ","
            if language == "eng":
                false_text = "Wrong writed this crypts \
(Or for this moment hasn't this crypts in base): "\
+ msg_result +".\n All other crypts were saved"
            elif language == "rus":
                false_text = "Неправильно написано такие криптовалюти \
(Либо их еще нет в базе криптовалют бота): "\
+ msg_result +".\n Все другие написани правильно"
            bot.send_message(message.chat.id, false_text)
        mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
        mydb.commit()#change function 

    elif current_func == 2:#If current func = choosing
        hide_markup = telebot.types.ReplyKeyboardRemove()
        if message.text == "Continue":
            mycursor.execute("UPDATE main SET cur_func = 1 WHERE id = " + user)
            mydb.commit()
            if language == "eng":
                continue_text = "Input new crypts for your list."
            elif language == "rus":
                continue_text = "Введите новие криптовалюти для вашева списка."
            bot.send_message(message.chat.id, continue_text,
            reply_markup = hide_markup)
        if message.text == "Cancel":
            mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
            mydb.commit()
            if language == "eng":
                cancel_text = "You canceled adding new crypts."
            elif language == "rus":
                cancel_text = "Ви отменили добавление нових криптовалют."
            bot.send_message(message.chat.id, cancel_text,
            reply_markup = hide_markup)

    elif current_func == 3:#Current func = Settings  
        hide_markup = telebot.types.ReplyKeyboardRemove()
        if message.text == "Language":
            lang_text = "Choose language for bot"
            langs_markup = telebot.types.ReplyKeyboardMarkup()
            langs_markup.row("English", "Руский")
            langs_markup.row("Cancel")
            bot.send_message(message.chat.id, lang_text,
             reply_markup = langs_markup)
        if message.text == "Cancel":
            hide_markup = telebot.types.ReplyKeyboardRemove()
            mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
            mydb.commit()
            cancel_text = "You canceled adding new crypts."
            bot.send_message(message.chat.id, cancel_text,
             reply_markup = hide_markup)
        if message.text == "Руский":
            mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
            mydb.commit()
            mycursor.execute("UPDATE main SET lang = 'rus' \
WHERE id =" +str(message.chat.id))
            mydb.commit()
            rus_text = "Язик успешно установлен."
            bot.send_message(message.chat.id, rus_text,
             reply_markup = hide_markup)
        if message.text == "English":
            mycursor.execute("UPDATE main SET cur_func = 0 WHERE id = " + user)
            mydb.commit()
            mycursor.execute("UPDATE main SET lang = 'eng' \
WHERE id =" + str(message.chat.id))
            mydb.commit()
            eng_text = "Language successfully changed"
            bot.send_message(message.chat.id, eng_text,
             reply_markup = hide_markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)

# start - Start using bot
# help - to see all commands
# add_list - You can reate and add your favorite cripts to list
# price_list - Check price of cripts from list
# clear_list - Delete your list
# settings - Set configuration of this bot
# subscribe - Buy subscription to have full list of function
