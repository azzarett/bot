import telebot
import sqlite3

bot = telebot.TeleBot('6841370063:AAGLzc9Sp7far3uusn-DMZtxdHLRM7z9xjY')

@bot.message_handler(commands=['start', 'back'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    u_btn = telebot.types.KeyboardButton('/view_users')
    markup.row(u_btn)
    a_btn = telebot.types.KeyboardButton('/attendance')     
    markup.row(a_btn)
    bot.send_message(message.chat.id, 'Начало работы', reply_markup=markup)


@bot.message_handler(commands=['attendance'])
def attendance(message):
    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS attendance (id int auto_increment primary key, s_name varchar(50), name varchar(50), login varchar(50), code varchar(50), date DATE)')

    markup = telebot.types.ReplyKeyboardMarkup()
    u_btn = telebot.types.KeyboardButton('/code')
    a_btn = telebot.types.KeyboardButton('/delete')
    v_btn = telebot.types.KeyboardButton('/view_attendance')
    markup.row(u_btn, a_btn)
    markup.row(v_btn)
    b_btn = telebot.types.KeyboardButton('/back')
    markup.row(b_btn)
    bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=markup)


@bot.message_handler(commands=['code'])
def code(message):
    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS code (code varchar(100))')

    cur.execute('SELECT COUNT(*) FROM code')
    data=cur.fetchall()
    conn.commit()
    cur.close() 
    conn.close()

    print(data)

    comapare = (0,)
    

    if data[0] == comapare:
        bot.send_message(message.chat.id, 'Введите код')
        bot.register_next_step_handler(message, add_code)
    else:
        bot.send_message(message.chat.id, 'Код уже существует! Удалите предыдущий код')



def add_code(message):
    code = message.text.strip()

    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('INSERT INTO code (code) VALUES (?)', (code,))
    conn.commit()
    cur.close() 
    conn.close()

    bot.send_message(message.chat.id, 'Код добавлен')

@bot.message_handler(commands=['view_users'])
def view_users(message):
    conn = sqlite3.connect('enactus.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users=cur.fetchall()

    info = ''
    for el in users:
        info += f'Фамилия: {el[1]}, Имя: {el[2]}, Логин: {el[3]}\n'
    cur.close() 
    conn.close()

    bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['delete'])
def delete(message):
    conn = sqlite3.connect('enactus.sql')
    cur =   conn.cursor()

    cur.execute('DELETE FROM code')
    conn.commit()
    cur.close() 
    conn.close()

    bot.send_message(message.chat.id, 'Код удален')


@bot.message_handler(commands=['view_attendance'])
def select_date(message):
    bot.send_message(message.chat.id, 'Введите дату')
    bot.register_next_step_handler(message, view_attendanced)

def view_attendanced(message):
    date = message.text.strip()

    conn = sqlite3.connect('enactus.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM attendance WHERE date = ?;', (date,))
    data = cur.fetchall()

    info = ''
    for i in data:
        info += f'Фамилия: {i[1]}, Имя: {i[2]}, Логин: {i[3]}\n'
    cur.close() 
    conn.close()

    bot.send_message(message.chat.id, info)
    


bot.polling(none_stop=True)