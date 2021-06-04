import sys
import sqlite3
from random import randint
from datetime import datetime
import os
import hashlib
import base64

import login_window as first_window
import main_window as second_window
import reg_window as third_window
import pay_window
import transfer_window
from browser_window import *
from card_number_generator import process_data
import card_creat
import card_window
import progress_bar

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox


class ProgressBarWindow(QtWidgets.QMainWindow, progress_bar.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progress_value = 0
        self.progressBar.setValue(self.progress_value)
        self.n = 0

        # Обработчики кнопок
        self.pushButton.clicked.connect(self.time)
        self.pushButton_2.clicked.connect(self.buy)

    # Фунция выполняет проверку возможности покупки баллов и их покупку
    def buy(self):
        count = self.lineEdit.text()
        if not count.isdigit() or int(count) <= 0 or '.' in count or ',' in count:
            QMessageBox.critical(self, 'Ошибка', 'Не верно ввели кол-во баллов!', QMessageBox.Ok)
        else:
            con = sqlite3.connect('DB_test.db')
            cur = con.cursor()
            que = """SELECT money, points FROM Users WHERE login='{0}'""".format(login)
            money = cur.execute(que).fetchall()[0][0]
            points = cur.execute(que).fetchall()[0][1]
            if int(money) <= int(count):
                QMessageBox.critical(self, 'Ошибка', 'Слишком много баллов Вы хотите!', QMessageBox.Ok)
            else:
                que2 = """UPDATE Users SET points = {0},
                 money = {1}
                  WHERE login = '{2}'""".format(int(points) + int(count), float(money) - float(count), login)
                cur.execute(que2)
                con.commit()
                QMessageBox.information(self, 'Успех', 'Баллы успешно преобретены!', QMessageBox.Ok)
                con.close()
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()

    # Функция выполняет проверку возможности выиграть баллы и начисляет выигрыш
    def time(self):
        if self.n == 0:
            con = sqlite3.connect('DB_test.db')
            cur = con.cursor()
            que = """SELECT points FROM Users WHERE login='{0}'""".format(login)
            points = cur.execute(que).fetchall()[0][0]
            if points <= 60:
                QMessageBox.warning(self, 'Ошибка', 'У вас слишком мало баллов', QMessageBox.Ok)
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()
                return False
            for _ in range(4):
                for _ in range(80000000):
                    pass
                self.progress_value += 25
                self.progressBar.setValue(self.progress_value)
            self.n += 1
            present = randint(1, 100)
            que2 = """UPDATE Users SET points = {0}
             WHERE login = '{1}'""".format(int(points) - 60 + present, login)
            cur.execute(que2)
            con.commit()
            if present >= 20:
                QMessageBox.information(self, 'Удача!', 'Ваш выигрыш'
                                                        ' {0}!'.format(present), QMessageBox.Ok)
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()
            else:
                QMessageBox.information(self, ':(',
                                        'Ваш выигрыш {0},'
                                        ' в следующий раз больше повезет.'.format(present), QMessageBox.Ok)
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()
        else:
            pass

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()


class CardCreate(QtWidgets.QMainWindow, card_creat.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        que = """SELECT card_number FROM Users WHERE login='{0}'""".format(login)
        self.card_num = cur.execute(que).fetchall()[0][0]
        self.all_card_num = cur.execute("""SELECT card_number FROM Users""").fetchall()
        # print(self.all_card_num)
        con.close()

        self.pushButton.clicked.connect(self.create_card)

    # Ф-ция создает карту(номер, срок действия и CVC)
    def create_card(self):
        while True:
            card_number = randint(3333000000000000, 7777000000000000)
            card_numbr = (card_number,)
            if process_data(card_number) == 1 and card_numbr not in self.all_card_num:
                self.card_num = card_number
                break
        cvc = randint(100, 999)
        card_date = str(datetime.now().month) + '/' + str(datetime.now().year + 2)[-2:]
        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        que2 = """UPDATE Users SET card_number = {0},
         card_date = '{1}', cvc = {2} WHERE login == '{3}'""".format(self.card_num, card_date, cvc, str(login))
        cur.execute(que2)
        con.commit()

        con.close()
        QMessageBox.information(self, "Успех!", "Виртуальная карта успешно создана!", QMessageBox.Ok)
        self.close()

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()


class CardWindow(QtWidgets.QMainWindow, card_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        que = """SELECT card_number, card_date, cvc FROM Users WHERE login='{0}'""".format(login)
        res = cur.execute(que).fetchall()
        card_num = res[0][0]
        # print(card_num)
        card_date = res[0][1]
        cvc = res[0][2]
        con.close()

        # print('Номер карты: {0}'.format(card_num), '\n', 'Срок действия: {0}'.format(card_date))
        self.label_2.setText('Номер карты: {0}'.format(card_num))
        self.label_2.resize(self.label_2.sizeHint())
        self.label_3.setText('Срок действия: {0}'.format(card_date))
        self.label_3.resize(self.label_3.sizeHint())
        self.label_4.setText('CVC: {0}'.format(cvc))
        self.label_4.resize(self.label_4.sizeHint())

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()


class Browser(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Инициализация WebView
        self.web = QtWebEngineWidgets.QWebEngineView()
        self.ui.gridLayout.addWidget(self.web, 1, 0, 1, 7)

        # Обработчики кнопок
        self.ui.toolButton.clicked.connect(self.back)
        self.ui.toolButton_2.clicked.connect(self.update)
        self.ui.toolButton_3.clicked.connect(self.search)
        self.ui.toolButton_4.clicked.connect(self.home)

        # Подсказки
        self.ui.toolButton.setToolTip('Назад')
        self.ui.toolButton_2.setToolTip('Обновить')
        self.ui.toolButton_3.setToolTip('Поиск')
        self.ui.toolButton_4.setToolTip('Главная')

    # Поиск информации
    def search(self):
        text = self.ui.lineEdit.text()

        if len(text) > 0:
            # Проверка ввода
            if not text.startswith('http'):
                text = QtCore.QUrl('https://duckduckgo.com/?q={0}'.format(text))
                # print(text)
            else:
                text = QtCore.QUrl(text)
            self.web.load(text)

    # Домашняя страница
    def home(self):
        home_page = QtCore.QUrl('https://duckduckgo.com')
        self.web.load(home_page)

    # Обновить страницу
    def update(self):
        self.web.reload()

    # Вернуться на предыдущую страницу
    def back(self):
        self.web.back()

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()


class TransferWindow(QtWidgets.QMainWindow, transfer_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Обработчики кнопок
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.quit)

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()

    # Выход в главное окно
    def quit(self):
        self.close()

    # Ф-ция осуществляющая перевод пользователю
    def trans(self):
        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        all_logins = cur.execute("""SELECT login FROM Users""").fetchall()
        other_login = (self.loginData.text(),)
        if (other_login in all_logins) and self.loginData.text() != login:
            con = sqlite3.connect('DB_test.db')
            cur = con.cursor()
            que = """SELECT money FROM Users WHERE login='{0}'""".format(self.loginData.text())
            money = cur.execute(que).fetchall()
            que2 = """SELECT money FROM Users WHERE login='{0}'""".format(login)
            money2 = cur.execute(que2).fetchall()

            m = self.amountData.text().replace(',', '.')

            if float(m) >= float(money2[0][0]):
                QMessageBox.warning(self, 'Ошибка', "Слишком большая сумма", QMessageBox.Ok)
                return False
            new_money = float(money[0][0]) + float(m)

            new_que = """UPDATE Users SET money = {0}
                         WHERE login = '{1}'""".format(new_money, self.loginData.text())
            cur.execute(new_que)
            con.commit()

            m2 = self.amountData.text().replace(',', '.')
            new_money2 = float(money2[0][0]) - float(m2)

            new_que2 = """UPDATE Users SET money = {0}
                                         WHERE login = '{1}'""".format(new_money2, login)
            cur.execute(new_que2)
            con.commit()

            con.close()
            return True
        else:
            QMessageBox.warning(self, 'Ошибка', "Неверный логин", QMessageBox.Ok)
            return False

    # Выполняем проверку для отправки денег
    def check(self):
        if self.loginData.text() == '' and self.amountData.text() == '':
            QMessageBox.critical(self, 'Ошибка', "Вы не ввели никаких значений", QMessageBox.Ok)
            self.close()
            self.secondWindow = TwoWindow()
            self.secondWindow.show()
        elif self.loginData.text() == '' and self.amountData.text() != '':
            QMessageBox.critical(self, 'Ошибка', "Вы не ввели кому отправлять деньги", QMessageBox.Ok)
            self.close()
            self.secondWindow = TwoWindow()
            self.secondWindow.show()
        elif self.loginData.text() != '' and self.amountData.text() == '':
            QMessageBox.critical(self, 'Ошибка', "Вы не ввели сколько переводить", QMessageBox.Ok)
            self.close()
            self.secondWindow = TwoWindow()
            self.secondWindow.show()
        elif not self.amountData.text().isdigit():
            QMessageBox.critical(self, 'Ошибка', "Вы неправильно указали сумму", QMessageBox.Ok)
            self.close()
            self.secondWindow = TwoWindow()
            self.secondWindow.show()
        else:
            if self.trans():
                QMessageBox.information(self, "Перевод ", "Перевод успешно выполнен!", QMessageBox.Ok)
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()
            else:
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()

        # new_money = float(money[0][0]) - float(m)


class PayWindow(QtWidgets.QMainWindow, pay_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.secondWindow = TwoWindow()
        self.secondWindow.show()

        # Обработчики кнопок
        self.payButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.quit)

    def closeEvent(self, value):
        self.secondWindow = TwoWindow()
        self.secondWindow.show()

    # Возвращаемся в предыдущее окно
    def quit(self):
        self.close()

    # Выполняем пополнение счета
    def fill_up(self):
        try:
            if float(self.amountData.text()) < 0:
                return False
            con = sqlite3.connect('DB_test.db')
            cur = con.cursor()
            que = """SELECT money FROM Users WHERE login='{0}'""".format(login)
            money = cur.execute(que).fetchall()
            m = self.amountData.text().replace(',', '.')
            new_money = float(money[0][0]) + float(m)

            new_que = """UPDATE Users SET money = {0} WHERE login = '{1}'""".format(new_money, login)
            cur.execute(new_que)
            con.commit()

            con.close()
            return True
        except:
            return False

    # Осуществляем проверку номера карты и суммы пополнения
    def check(self):
        if self.cardData.text() == '' and self.amountData.text() != '':
            QMessageBox.warning(self, 'Ошибка карты', "Вы не ввели номер карты", QMessageBox.Ok)
        elif self.cardData.text() != '' and self.amountData.text() == '':
            QMessageBox.warning(self, 'Ошибка суммы', "Вы не ввели сумму пополнения", QMessageBox.Ok)
        elif self.cardData.text() == '' and self.amountData.text() == '':
            QMessageBox.warning(self, 'Ошибка', "Вы не ввели никаких значений", QMessageBox.Ok)
        elif self.cardData.text() != '' and self.amountData.text() == str(0):
            QMessageBox.warning(self, 'Ошибка', "Неверное значение суммы пополнения", QMessageBox.Ok)
        else:
            if self.process_data() == 0:
                if self.fill_up():
                    QMessageBox.information(self, 'Успешно!', "Пополнение выполнено успешно!", QMessageBox.Ok)
                    self.close()
                    self.secondWindow = TwoWindow()
                    self.secondWindow.show()
                else:
                    QMessageBox.critical(self, 'Ошибка', "Вы ввели некорректные значения", QMessageBox.Ok)
            elif self.process_data() == 1:
                self.errorCard()
            elif self.process_data() == -1:
                self.errorNumber()

    def errorCard(self):
        QMessageBox.warning(self, 'Ошибка', "Введите только 16 цифр. Допускаются пробелы", QMessageBox.Ok)

    def errorNumber(self):
        QMessageBox.warning(self, 'Ошибка', "Номер недействителен. Попробуйте снова.", QMessageBox.Ok)

    # Функция делает проверку, чтобы введенный номер карты - цифры, произвольно разделенные пробелами
    # Позволяет в ответ на некорректный запрос программе не умирать,
    # а требовать ввести 16 цифр, разделенные пробелами или не разделенные.
    def get_card_number(self):
        card_num = self.cardData.text()
        if card_num.isdigit() and len(card_num) == 16:
            return card_num
        else:
            return 404

    # Дальше идет алгоритм Луна
    def double(self, x):
        res = x * 2
        if res > 9:
            res = res - 9
        return res

    def luhn_algorithm(self, card):
        odd = map(lambda x: self.double(int(x)), card[::2])
        even = map(int, card[1::2])
        return (sum(odd) + sum(even)) % 10 == 0

    def process_data(self):
        number = self.get_card_number()
        if number == 404:
            return 1
        elif self.luhn_algorithm(number):
            return 0
        else:
            return -1


class TwoWindow(QtWidgets.QMainWindow, second_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Обработчики кнопок
        self.pushButton.clicked.connect(self.quit)
        self.pushButton_3.clicked.connect(self.repl)
        self.pushButton_2.clicked.connect(self.transfer)
        self.pushButton_4.clicked.connect(self.browserWindow)
        self.pushButton_6.clicked.connect(self.card)
        self.pushButton_5.clicked.connect(self.point)

        # Получаем значения денег и баллов пользователя, затем выводим эти данные на окно
        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        que = """SELECT money, points, card_number FROM Users WHERE login='{0}'""".format(login)
        self.money = cur.execute(que).fetchall()[0][0]
        points = cur.execute(que).fetchall()[0][1]

        self.card_num = cur.execute(que).fetchall()[0][2]
        self.label_3.setText('{0} ₽'.format(round(float(self.money), 2)))
        self.label_3.resize(self.label_3.sizeHint())
        self.label_4.setText('Баллы: {0}'.format(points))
        self.label_4.resize(self.label_4.sizeHint())

        con.close()

    # Запускаются ф-ции кнопок
    def transfer(self):
        self.close()
        self.transferWindow = TransferWindow()
        self.transferWindow.show()

    def quit(self):
        self.close()
        self.firstWindow = OneWindow()
        self.firstWindow.show()

    def repl(self):
        self.close()
        self.payWindow = PayWindow()
        self.payWindow.show()

    def browserWindow(self):
        self.close()
        self.browserWindow = Browser()
        self.browserWindow.show()

    def card(self):
        if str(self.card_num) == '0':
            self.close()
            self.cardcreatWindow = CardCreate()
            self.cardcreatWindow.show()
        else:
            self.close()
            self.cardWindow = CardWindow()
            self.cardWindow.show()

    def point(self):
        self.close()
        self.pointsWindow = ProgressBarWindow()
        self.pointsWindow.show()


class ThreeWindow(QtWidgets.QMainWindow, third_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Текст становится таким, каким должен быть
        self.label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.label.setGeometry(QtCore.QRect(175, 10, 331, 100))
        self.label.adjustSize()
        self.label_2.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.label_2.adjustSize()
        self.label_3.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.label_3.adjustSize()

        # Для удобства понимания
        self.reg_login = self.lineEdit
        self.reg_password = self.lineEdit_2

        self.f = True

        # Обработчики кнопок
        self.pushButton.clicked.connect(self.registration)
        self.pushButton_2.clicked.connect(self.back)

    def back(self):
        self.close()
        self.firstWindow = OneWindow()
        self.firstWindow.show()

    # Ф-ции запускающие окна с сообщениями, если ошибок несколько(в случае с паролем), то они показываются все
    def reg_successful(self):
        QMessageBox.information(self, "Успешная регистрация ", "Вы успешно зарегистрированы!", QMessageBox.Ok)
        self.close()
        self.firstWindow = OneWindow()
        self.firstWindow.show()

    def LoginError(self):
        QMessageBox.critical(self, "Ошибка ", "Пользователь с таким логином уже существует"
                                              " или вы не заполнили поля", QMessageBox.Ok)
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()

    def LengthError(self):
        QMessageBox.warning(self, "Ошибка пароля ",
                            "Длина пароля меньше 9 символов", QMessageBox.Ok)
        self.f = False
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()

    def LetterError(self):
        QMessageBox.warning(self, "Ошибка пароля ",
                            "В пароле все символы одного регистра", QMessageBox.Ok)
        self.f = False
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()

    def DigitError(self):
        QMessageBox.warning(self, "Ошибка пароля ",
                            "В пароле нет ни одной цифры", QMessageBox.Ok)
        self.f = False
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()

    def SequenceError(self):
        QMessageBox.warning(self, "Ошибка пароля ", "В пароле не должно быть "
                                                    "ни одной комбинации из 3 буквенных символов,"
                                                    " стоящих рядом в строке клавиатуры независимо от того,"
                                                    " русская раскладка выбрана или английская.", QMessageBox.Ok)
        self.f = False
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()

    # Фунция выполняющая проверку пароля на сложность
    def check_password(self, password):
        s = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ',
             'фывапролджэё', 'ячсмитьбю']
        f = False
        if len(password) < 9:
            self.LengthError()
        if password.lower() == password or password.upper() == password:
            self.LetterError()
        password = password.lower()
        for n in password:
            if n.isdigit():
                f = True
                break
        if f:
            pass
        else:
            self.DigitError()
        for i in s:
            for j in range(len(i) - 2):
                if i[j: j + 3] in password:
                    self.SequenceError()
                    break

    # Функция регистрации пользователя
    def registration(self):
        con = sqlite3.connect('DB_test.db')
        reg_login = self.reg_login.text()
        reg_password = self.reg_password.text()
        cur = con.cursor()
        # Получаем все логины
        res = cur.execute("""SELECT login FROM Users""").fetchall()
        res = [a[0] for a in res]
        if reg_login in res or reg_password == '' or reg_login == '':
            self.LoginError()
        elif reg_password != '':
            self.check_password(reg_password)
            if self.f:
                salt = os.urandom(32)
                password = hashlib.pbkdf2_hmac('sha256', reg_password.encode('utf-8'), salt, 100000)

                def Base_64(s):
                    b = s
                    # Кодируем байты в Base64
                    e = base64.b64encode(b)
                    # Декодируем байты Base64 в строку
                    return e.decode("UTF-8")

                key = Base_64(salt)
                password = Base_64(password)
                que = """INSERT INTO Users
                    (login, password, points, money, card_number, card_date, cvc, key)
                    VALUES('{0}', '{1}', {2}, {3}, {4}, {5},
                     {6}, '{7}')""".format(reg_login, password, 0, 0, 0, 0, 0, key)
                # print(que)
                cur.execute(que)
                con.commit()

                con.close()

                # print(self.reg_login.text(), self.reg_password.text())
                self.reg_successful()


class OneWindow(QtWidgets.QMainWindow, first_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.secondWindow = None
        self.thirdWindow = None
        self.label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.label.setGeometry(QtCore.QRect(122, 10, 331, 100))
        self.label.adjustSize()
        self.label_2.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.label_2.adjustSize()
        self.label_3.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        self.label_3.adjustSize()

        # Для удобства понимания
        self.login = self.lineEdit
        self.password = self.lineEdit_2

        # Обработчики кнопок
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.reg)

    # Ф-ции запускающие окна с сообщениями
    def User_identError(self):
        QMessageBox.warning(self, "Ошибка ", "Неправильно введен логин или пароль", QMessageBox.Ok)
        self.close()
        self.firstWindow = OneWindow()
        self.firstWindow.show()

    def BlankLine(self):
        QMessageBox.warning(self, "Ошибка ", "Вы не ввели логин или пароль", QMessageBox.Ok)
        self.close()
        self.firstWindow = OneWindow()
        self.firstWindow.show()

    # Выполняет проверку введенных данных
    def check(self):
        global login
        login = self.login.text()
        password = self.password.text()

        con = sqlite3.connect('DB_test.db')
        cur = con.cursor()
        # Получаем все данные для идентификации пользователя
        users_ident = cur.execute("""SELECT login FROM Users""").fetchall()
        all_logins = [i[0] for i in users_ident]
        # print(log_passw, users_ident)
        if password == '' or login == '':
            self.BlankLine()
        elif login in all_logins:
            storage = cur.execute("""SELECT password, key FROM Users WHERE login = '{0}'""".format(login)).fetchall()
            storage_password = storage[0][0]
            key = storage[0][1]
            # Превращаем строку обратно в байты
            b1 = key.encode("UTF-8")
            # Расшифровка байтов Base64
            d = base64.b64decode(b1)
            salt = d
            password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            b = password
            # Кодируем байты в Base64
            e = base64.b64encode(b)
            # Декодируем байты Base64 в строку
            password = e.decode("UTF-8")
            # Сравниваем полученный пароль с паролем из бд
            if password == storage_password:
                self.close()
                self.secondWindow = TwoWindow()
                self.secondWindow.show()
            else:
                self.User_identError()
        else:
            self.User_identError()
        con.close()

    def reg(self):
        self.close()
        self.thirdWindow = ThreeWindow()
        self.thirdWindow.show()


# sys._excepthook = sys.excepthook
#
#
# def my_exception_hook(exctype, value, traceback):
#     print(exctype, value, traceback)
#     sys._excepthook(exctype, value, traceback)
#     sys.exit(1)
#
#
# sys.excepthook = my_exception_hook


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = OneWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
