from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(725, 562)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setEnabled(True)
        self.Title.setGeometry(QtCore.QRect(30, 30, 661, 91))
        font = QtGui.QFont()
        font.setPointSize(34)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.downloadbutton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadbutton.setGeometry(QtCore.QRect(270, 370, 161, 31))
        self.downloadbutton.setObjectName("downloadbutton")
        self.EnterS = QtWidgets.QLabel(self.centralwidget)
        self.EnterS.setGeometry(QtCore.QRect(30, 150, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterS.setFont(font)
        self.EnterS.setObjectName("EnterS")
        self.EnterE = QtWidgets.QLabel(self.centralwidget)
        self.EnterE.setGeometry(QtCore.QRect(30, 220, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterE.setFont(font)
        self.EnterE.setObjectName("EnterE")
        self.StartingEnumBox = QtWidgets.QLineEdit(self.centralwidget)
        self.StartingEnumBox.setGeometry(QtCore.QRect(460, 160, 171, 41))
        self.StartingEnumBox.setObjectName("StartingEnumBox")
        self.EndingEnumBox = QtWidgets.QLineEdit(self.centralwidget)
        self.EndingEnumBox.setGeometry(QtCore.QRect(460, 230, 171, 41))
        self.EndingEnumBox.setObjectName("EndingEnumBox")
        self.locationinput = QtWidgets.QLineEdit(self.centralwidget)
        self.locationinput.setGeometry(QtCore.QRect(460, 290, 171, 41))
        self.locationinput.setObjectName("locationinput")
        self.EnterL = QtWidgets.QLabel(self.centralwidget)
        self.EnterL.setGeometry(QtCore.QRect(30, 280, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.EnterL.setFont(font)
        self.EnterL.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.EnterL.setMouseTracking(False)
        self.EnterL.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnterL.setAutoFillBackground(False)
        self.EnterL.setWordWrap(True)
        self.EnterL.setObjectName("EnterL")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "MSBTE Result Downloader"))
        self.downloadbutton.setText(_translate("MainWindow", "Download Result"))
        self.EnterS.setText(_translate("MainWindow", "Enter Starting Enrollment Num:"))
        self.EnterE.setText(_translate("MainWindow", "Enter Ending Enrollment Num:"))
        self.EnterL.setText(_translate("MainWindow", "Enter Location Where You want to Save The Results:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
