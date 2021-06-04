from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 0, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 0, 1, 1, 1)
        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setObjectName("toolButton_5")
        self.gridLayout.addWidget(self.toolButton_4, 0, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 3, 1, 1)
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 0, 4, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("border: 1px solid black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionOpen_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_file.setObjectName("actionOpen_file")
        self.actionSave_file = QtWidgets.QAction(MainWindow)
        self.actionSave_file.setObjectName("actionSave_file")
        self.actionOpen_folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_folder.setObjectName("actionOpen_folder")
        self.actionOpen_files = QtWidgets.QAction(MainWindow)
        self.actionOpen_files.setObjectName("actionOpen_files")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "МоиДеньги browser"))
        self.toolButton.setText(_translate("MainWindow", "Назад"))
        self.toolButton_2.setText(_translate("MainWindow", "Обновить"))
        self.toolButton_4.setText(_translate("MainWindow", "Домой"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "https://"))
        self.toolButton_3.setText(_translate("MainWindow", "Поиск"))
        self.actionOpen_file.setText(_translate("MainWindow", "Open file"))
        self.actionSave_file.setText(_translate("MainWindow", "Save file"))
        self.actionOpen_folder.setText(_translate("MainWindow", "Open folder"))
        self.actionOpen_files.setText(_translate("MainWindow", "Open files"))
        self.toolButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(118, 192, 141);\n"
                                        "font: 14pt \"Times New Roman\";\n"
                                        "")
        self.toolButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(118, 192, 141);\n"
                                        "font: 14pt \"Times New Roman\";\n"
                                        "")
        self.toolButton_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(118, 192, 141);\n"
                                        "font: 14pt \"Times New Roman\";\n"
                                        "")
        self.toolButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(118, 192, 141);\n"
                                        "font: 14pt \"Times New Roman\";\n"
                                        "")