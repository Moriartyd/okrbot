import sqlite3
from sqlite3.dbapi2 import IntegrityError

from aiogram.dispatcher.storage import RESULT

class BotDB:

    nameArray = ['Дмитрий Галеев',
    'Евгений Васильев',
    'Сергей Славский',
    'Андрей Беседа',
    'Александр Другов',
    'Андрей Лепухов',
    'Алексей Разумов',
    'Ксения Ивахнина',
    'Виолетта Хомкалова',
    'Алексей Прохоров',
    'Кристина Чумак',
    'Бутко Антон']

    def __init__(self, db_file):
        """Инициализация содинения с бд"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def insertName(self, name):
        self.cursor.execute("INSERT INTO 'Names' ('name', 'used') VALUES (?, ?)", (name, 0))
        # return self.conn.commit()

    def getUserIDByChatID(self, chat_id):
        """Поиск id пользователя по ChatID"""
        result = self.cursor.execute("SELECT id FROM 'chats' where chat_id = ?", (chat_id,))
        return result.fetchone()

    def isUserExist(self, chat_id):
        result = self.cursor.execute("SELECT id FROM 'chats' where chat_id = ?", (chat_id,))
        return result.fetchall()

    def getUserNameByChatID(self, chat_id):
        result = self.cursor.execute("SELECT name FROM 'chats' where chat_id = ?", (chat_id,))
        return result.fetchone()[0]
    
    def getUserIDByName(self, name):
        """Поиск id пользователя по Имени"""
        result = self.cursor.execute("SELECT id FROM 'chats' where name = ?", (name,))
        return result.fetchone()

    def addNewChat(self, chat_id, name):
        """Добавление нового пользователя"""
        try:
            self.cursor.execute("INSERT INTO 'chats' ('name', 'chat_id') VALUES (?, ?)", (name, chat_id))
            return self.conn.commit()
        except IntegrityError:
            print("User registered")

    def isAllUsersRegistered(self):
        """Проверка регистрации всех пользователей"""
        result = self.cursor.execute("SELECT * FROM 'chats'")
        return result.fetchall()

    def getUnusedNames(self):
        result = self.cursor.execute("SELECT name from 'Names' where used = 0")
        return result.fetchall()

    def setSanta(self, santaID, userID, usedName):
        self.cursor.execute("UPDATE 'Names' SET 'used' = 1 WHERE name = ?", (usedName,))
        self.cursor.execute("INSERT INTO 'santas' ('santa', 'person') VALUES (?, ?)", (santaID, userID))
        self.conn.commit()

    def getAllChatIDs(self):
        result = self.cursor.execute("SELECT chat_id FROM 'chats'")
        return result.fetchall()
    
    def getRegisteredUsersName(self):
        result = self.cursor.execute("SELECT name FROM 'chats'")
        return result.fetchall()

    def isSantaAlreadyRegistered(self, userID):
        result = self.cursor.execute("SELECT * FROM 'santas' where santa = ?", (userID,))
        return bool(len(result.fetchall()) == 1)

    def getGiftedUserIDBySanta(self, santa):
        result = self.cursor.execute("SELECT person FROM 'santas' where santa = ?", (santa,))
        return result.fetchone()

    def getSantaByGiftedUser(self, user):
        result = self.cursor.execute("SELECT santa FROM 'santas' where person = ?", (user,))
        return result.fetchone()[0]

    def getUserNameByUserID(self, userID):
        result = self.cursor.execute("SELECT name FROM 'chats' where id = ?", (userID,))
        return result.fetchone()[0]
    
    def clearNames(self):
        result = self.cursor.execute("DELETE FROM 'Names'")
        self.conn.commit()
    
    def clearChats(self):
        result = self.cursor.execute("DELETE FROM 'chats'")
        self.conn.commit()

    def clearSantas(self):
        result = self.cursor.execute("DELETE FROM 'santas'")
        self.conn.commit()
    
    def clearAllDB(self):
        self.cursor.execute("DELETE FROM 'santas'")
        self.cursor.execute("DELETE FROM 'chats'")
        self.cursor.execute("DELETE FROM 'Names'")
        self.conn.commit()

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
