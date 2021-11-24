from os import name
from aiogram.types.callback_query import CallbackQuery
from attr import s
import telebot
import config
import random

from bot import BotDB
from dispatcher import dp
from aiogram import types

bot = telebot.TeleBot(config.TOKEN)

@dp.message_handler(commands='init_db')
async def initDataBase(message: types.Message):
    items = []
    for name in BotDB.nameArray:
        BotDB.insertName(name)
    BotDB.conn.commit()
    await message.bot.send_message(message.chat.id, 'Все имена занесены в таблицу')

@dp.message_handler(commands='send_all')
async def sendOneDayReminder(message: types.Message):
    m = message.text
    ids = BotDB.getAllChatIDs()
    for id in ids:
        await message.bot.send_message(id[0], m[m.find(' ') + 1:])

@dp.message_handler(commands='del_names')
async def initDataBase(message: types.Message):
    BotDB.clearNames()
    await message.bot.send_message(message.chat.id, 'Все имена удалены')

@dp.message_handler(commands='rules')
async def showHelp(message: types.Message):
    rules = "\t1. Каждому участнику генерируется случайное имя\n\t2. Ты должен подарить 1 подарок ценой от 500р до 1000р\n\t3. Взамен ты получишь 1 подарок\n\t4. В конце игры тайный санта становится явным\n\t5. Игра закончится 23.12 в 10:00\nЕще нельзя дарить: алкоголь, все, что связано с религией, деньги и любой другой обидный подарок (вспомни про 4-ый пункт)"
    await message.bot.send_message(message.chat.id, rules)

@dp.message_handler(commands='del_chats')
async def initDataBase(message: types.Message):
    BotDB.clearChats()
    await message.bot.send_message(message.chat.id, 'Все чаты удалены')

@dp.message_handler(commands='del_santas')
async def initDataBase(message: types.Message):
    BotDB.clearSantas()
    await message.bot.send_message(message.chat.id, 'Все связи сант удалены')

@dp.message_handler(commands='del_all')
async def initDataBase(message: types.Message):
    BotDB.clearAllDB()
    await message.bot.send_message(message.chat.id, 'Минус БД')

def isIn(name, names):
    for n in names:
        if n[0] == name:
            return True
    return False

@dp.message_handler(commands='start')
async def welcomeMessage(message: types.Message):

    welcome_message = "Привет, если ты попал сюда, значит ты хочешь поиграть в тайного санту.\nПравила очень просты:\n\t1. Каждому участнику генерируется случайное имя\n\t2. Ты должен подарить 1 подарок ценой от 500р до 1000р\n\t3. Взамен ты получишь 1 подарок\n\t4. В конце игры тайный санта становится явным\n\t7. Игра закончится 23.12 в 10:00\n\t6. Хорошей игры :)\nЕсли ты что-то забудешь, то пропиши команду /rules"
    badSurprise = "Еще нельзя дарить: алкоголь, все, что связано с религией, деньги и любой другой обидный подарок (вспомни про 4-ый пункт)"
    
    if BotDB.isUserExist(message.chat.id) == []:
        markup = types.InlineKeyboardMarkup()
        # welcomeMarkup = types.InlineKeyboardMarkup()
        items = []
        # welcomeItems = []

        # welcomeItems.append(types.InlineKeyboardButton('B', callback_data='B'))
        # welcomeItems.append(types.InlineKeyboardButton('A', callback_data='A'))
        # welcomeItems.append(types.InlineKeyboardButton('F', callback_data='F'))
        # welcomeItems.append(types.InlineKeyboardButton('G', callback_data='G'))

        names = BotDB.getRegisteredUsersName()
        for name in BotDB.nameArray:
            if isIn(name, names) != True:
                items.append(types.InlineKeyboardButton(name, callback_data=name))
        for item in items:
            markup.add(item)
        await message.bot.send_message(message.chat.id, welcome_message)
        await message.bot.send_message(message.chat.id, badSurprise)
        await message.bot.send_message(message.chat.id, 'Нужно определиться со своим именем', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Стать тайным Сантой"))
        await message.bot.send_message(message.chat.id, 'Зачем еще раз тыкать /start? Это ничего не изменит', reply_markup=markup)

@dp.callback_query_handler(lambda call: True)
async def callback_inline(call: CallbackQuery):
    try:
        BotDB.addNewChat(call.message.chat.id, call.data)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Стать тайным Сантой"))

        await call.bot.send_message(call.message.chat.id, 'Привет, ' + call.data + '!', reply_markup=markup)
 
        # remove inline buttons
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы успешно зарегистрировались!",
                reply_markup=None)
 
    except Exception as e:
        print(repr(e))


def getUserSantaName(message):
    santaChatID = message.chat.id
    santaID = BotDB.getUserIDByChatID(santaChatID)[0]
    santaName = BotDB.getUserNameByChatID(santaChatID)
    names = BotDB.getUnusedNames()
    while True:
        i = random.randint(1, 1000) % len(names)
        userName = names[i][0]
        print("Пользователь " + santaName + "получил имя")
        if userName != santaName:
            if (BotDB.getGiftedUserIDBySanta(userName) == [] & len(names) > 1) | (BotDB.getGiftedUserIDBySanta(userName) != [] & len(names) == 1):
                userID = BotDB.getUserIDByName(userName)[0]
                print(userID)
                BotDB.setSanta(santaID, userID, userName)
                return userName


@dp.message_handler(content_types='text')
async def lalala(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Стать тайным Сантой"))
    userID = BotDB.getUserIDByChatID(message.chat.id)[0]
    if message.text == "Стать тайным Сантой":
        if BotDB.isSantaAlreadyRegistered(userID) != True:
            if len(BotDB.isAllUsersRegistered()) == len(BotDB.nameArray):
                # Проверка на последнего зарегистрироваашегося пользователя
                if len(BotDB.getUnusedNames()) == len(BotDB.nameArray):
                    # Отсылаем всем пользователям, что можно стать сантой
                    ids = BotDB.getAllChatIDs()
                    for id in ids:
                        if message.chat.id != id[0]:
                            await message.bot.send_message(id[0], "Наконец-то можно стать Cантой!", reply_markup=markup)
                text = "Вы должны подарить подарок " + getUserSantaName(message)
                await message.bot.send_message(message.chat.id, text)
            else:
                text = "Еще не все пользователи зарегистрировались, придется подождать"
                await message.bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            giftedUserID = BotDB.getGiftedUserIDBySanta(userID)[0]
            giftedUserName = BotDB.getUserNameByUserID(giftedUserID)
            text = "Санта, ты что, забыл кому даришь подарок?\nЧеловек, которого ты осчастливишь " + giftedUserName
            await message.bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        text = "Чтооооо? Мы тут собрались в санту играть, а не болтать"
        await message.bot.send_message(message.chat.id, text, reply_markup=markup)

#RUN
bot.polling(none_stop=True)