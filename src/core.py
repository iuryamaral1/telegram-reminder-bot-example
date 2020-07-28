import telebot
from conf.settings import TELEGRAM_TOKEN

tasks = []
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    firstName = message.from_user.first_name
    lastName  = message.from_user.last_name
    msg = bot.reply_to(message, "Olá " + firstName + " " + lastName + ", tudo bem? Qual lembrete quer gravar hoje?")
    bot.register_next_step_handler(msg, addReminder)

def addReminder(message):
    text = message.text
    chat_id = message.chat.id
    tasks.append(text)
    bot.send_message(chat_id, 'Lembrete salvo com sucesso!')

@bot.message_handler(commands=['adicionar'])
def addTask(message):
    msg = bot.reply_to(message, "Qual o título do lembrete?")
    bot.register_next_step_handler(msg, addReminder)

@bot.message_handler(commands=['apagarTudo'])
def deleteTasks(message):
    tasks = []
    bot.send_message(message.chat.id, "Todos os lembretes foram apagados!")

@bot.message_handler(commands=['apagar'])
def deleteOneTask(message):
    for i in range(len(tasks)):
        bot.send_message(message.chat.id, "{}: {}".format(i + 1, tasks[i]))
    msg = bot.reply_to(message, "Digite o numero do lembrete que deseja remover")
    bot.register_next_step_handler(msg, processDelete)

def processDelete(message):
    index = message.text
    if not index.isdigit():
        bot.reply_to(message, "Por favor, digite um numero valido")
    del tasks[int(index)]
    bot.reply_to(message, "Tarefa excluída com sucesso!")

@bot.message_handler(commands=['agenda'])
def agenda(message):
    for task in tasks:
        bot.send_message(message.chat.id, task)

bot.polling()