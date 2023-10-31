import telebot
import sqlite3

bot = telebot.TeleBot('6495076091:AAGsI0zf-c4peNeTjLjEGyW-8dJJHnNbxJE')

@bot.message_handler(commands=['start'])
def start(mesage):
    markup = telebot.types.ReplyKeyboardMarkup()
    r_btn = telebot.types.KeyboardButton('/register')
    c_btn = telebot.types.KeyboardButton('/code')
    markup.row(r_btn, c_btn)
    bot.send_message(mesage.chat.id, 'Приветствуем в нашем Телеграм боте для отметки посещения! Зарегестрируйтесь если вы еще не зарегестрированы', reply_markup=markup)


s_name = None
@bot.message_handler(commands=['register'])
def check_user(message):
    login = message.from_user.username

    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, s_name varchar(50), name varchar(50), login varchar(50))')

    data = cur.execute('SELECT login FROM users WHERE login = ?', (login,)).fetchall()
    conn.commit()
    cur.close() 
    conn.close()

    if len(data) > 0:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    else:
        bot.register_next_step_handler(message, register)

def register(message):
    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Cейчас тебя зарегистрируем! Введите фамилию')
    bot.register_next_step_handler(message, user_s_name)

def user_s_name(message):
    global s_name
    s_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()
    login = message.from_user.username

    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('INSERT INTO users (s_name, name, login) VALUES (?,?,?)', (s_name, name, login))
    conn.commit()
    cur.close() 
    conn.close()

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован')

s_name = None

@bot.message_handler(commands=['code'])
def check(message):
    login = message.from_user.username

    conn = sqlite3.connect('enactus.sql')
    cur = conn.cursor()

    cur.execute('SELECT COUNT(login) FROM users WHERE login = ?', (login,))
    user = cur.fetchall()
    check = '[(0,)]'
    user=str(user)

    if check == user:
       bot.send_message(message.chat.id, 'Пожалуйста зарегистрируйтесь')
    else:
        bot.register_next_step_handler(message, code) 

def code(message):
    bot.send_message(message.chat.id, 'Введите код')
    bot.register_next_step_handler(message, user_code)

def user_code(message):

    from datetime import date

    current_date = date.today()

    login = message.from_user.username

    conn = sqlite3.connect('enactus.sql')
    cur = conn.cursor()

    cur.execute('SELECT code FROM code')
    code = cur.fetchall()

    cur.execute('SELECT COUNT(*) FROM code')
    check = cur.fetchall()

    cur.execute('SELECT COUNT(login)+COUNT(code)+COUNT(date) FROM attendance WHERE login = ? AND code = ? AND date = ?', (login, str(code), current_date))
    data = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    t_code = message.text.strip()
    compare= ("[('"+t_code+"',)]")
    # compare_w= ("[('"+data+"',)]")
    code = str((code),)
    data = str((data),)     
    check1='[(0,)]'

    print(data)
    # print(compare_w)
     
    if check[0] == check1:
        bot.send_message(message.chat.id, 'Собрание не проводится') 
    elif data != check1:
        bot.send_message(message.chat.id, 'Вы уже отметились') 
    elif compare == code:
        conn = sqlite3.connect('enactus.sql')
        cur =   conn.cursor()

        cur.execute("SELECT s_name FROM users WHERE login = ?;", (login,))
        s_name = cur.fetchall()

        cur.execute("SELECT name FROM users WHERE login = ?;", (login,))
        name = cur.fetchall()
        

        symbol_to_remove = "[(',)]"

        for symbol in symbol_to_remove:
            s_name = str(s_name).replace(symbol, '')
            name = str(name).replace(symbol, '')

        cur.execute('INSERT INTO attendance (s_name, name, login, code, date) VALUES(?,?,?,?,?)', (str(s_name), str(name), login, code, current_date))

        bot.send_message(message.chat.id, 'Спасибо за отметку!')

        conn.commit()
        cur.close()
        conn.close()
    elif compare != code:
        bot.send_message(message.chat.id, 'Неверный код') 


bot.polling(none_stop=True)
