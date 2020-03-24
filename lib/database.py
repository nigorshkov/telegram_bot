# -*- coding: utf-8 -*-
import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_all(self, name_table):
        """ Считаем все строки из таблицы"""
        with self.connection:
            result = self.cursor.execute('select * from {}'.format(name_table)).fetchall()
            return len(result)

    def count_rows(self, user_id):
        """ Считаем количество строк в таблице"""
        with self.connection:
            result = self.cursor.execute('select * from logpass where user_id={} and actual=1'.format(user_id)).fetchall()
            return len(result)


    def check_create_user(self, user_id):
        """Проверка что такой юзер есть в бд"""
        with self.connection:
            result = self.cursor.execute('''select count(*) from users
                                           where user_id = ?''', [user_id]).fetchall()
            return result[0][0]

    def insert_user(self, user_id, username, first_name, last_name):
        """ Добавляем нового юзера"""
        self.cursor.execute(
            "Insert into users values (?, ?, ?, ?)",
            [user_id, username, first_name, last_name])
        self.commit()

    def show_all(self, user_id):
        """ Получаем информацию о логинах и паролях по user_id """
        with self.connection:
            logpass = ''
            for i in self.cursor.execute('select l.* from users u '
                                         'join logpass l on u.user_id=l.user_id '
                                         'where u.user_id = ? and l.actual=1', [user_id]).fetchall():
                logpass += 'Name: {}, Login: {}, Password: {} \n'\
                    .format(i[2].encode('utf-8'), i[3].encode('utf-8'), i[4].encode('utf-8'))
        return logpass

    def show_one(self, user_id, name):
        """Ищем нужный логин/пароль"""
        with self.connection:
            logpass = ''
            for i in self.cursor.execute('select l.* from users u '
                                         'join logpass l on u.user_id=l.user_id '
                                         'where u.user_id = ? and name = ? and actual=1', (user_id, name)).fetchall():
                logpass += 'Name: {}, Login: {}, Password: {} \n'.\
                    format(i[2].encode('utf-8'), i[3].encode('utf-8'), i[4].encode('utf-8'))
        return logpass

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

    def insert(self, user_id, name, login, password):
        """ Добавляем строку """
        self.cursor.execute(
            "Insert into logpass values (?, ?, ?, ?, ?, ?)", [self.select_all('logpass') + 1, user_id, name, login, password, 1])
        self.commit()

    def remove(self, user_id, name):
        """Удаление записи"""
        with self.connection:
            self.cursor.execute('update logpass set actual=0 where user_id = ? and name = ?', (user_id, name))

    def check_uniq_name(self, user_id, name):
        with self.connection:
            count = self.cursor.execute('select count(*) from users u '
                                        'join logpass l on u.user_id=l.user_id '
                                        'where u.user_id = ? and name = ? and actual=1', (user_id, name)).fetchall()
        return count[0][0]

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
