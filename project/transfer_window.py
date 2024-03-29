# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transfer_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(195, 470)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(63, 63, 63);")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 201, 211))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("transfer.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 240, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.loginData = QtWidgets.QLineEdit(self.centralwidget)
        self.loginData.setGeometry(QtCore.QRect(7, 270, 181, 20))
        self.loginData.setStyleSheet("color: rgb(118, 192, 144);")
        self.loginData.setObjectName("loginData")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 310, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.amountData = QtWidgets.QLineEdit(self.centralwidget)
        self.amountData.setGeometry(QtCore.QRect(7, 330, 181, 20))
        self.amountData.setStyleSheet("color: rgb(118, 192, 144);")
        self.amountData.setObjectName("amountData")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 360, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(118, 192, 144);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 420, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Окно перевода"))
        self.label_2.setText(_translate("MainWindow", "Кому (логин):"))
        self.label_2.resize(self.label_2.sizeHint())
        self.label_3.setText(_translate("MainWindow", "Сумма перевода (только целое):"))
        self.label_3.resize(self.label_3.sizeHint())
        self.pushButton.setText(_translate("MainWindow", "Перевести"))
        self.pushButton.resize(self.pushButton.sizeHint())
        self.pushButton_2.setText(_translate("MainWindow", "<--\n"
"Назад"))
