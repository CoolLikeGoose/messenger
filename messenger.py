import sys
from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook



class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.sendMessage)
        self.last_message_time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)

    def sendMessage(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        if not username:
            self.addText('ERROR: username is empty!')
            self.addText('')
        if not password:
            self.addText('ERROR: password is empty!')
            self.addText('')
        if not text:
            self.addText('ERROR: text is empty!')
            self.addText('')

        response = requests.post('http://127.0.0.1:5000/send',
                                 json={'username': username, 'password': password, 'text': text})
        if not response.json()['ok']:
            self.addText("ERROR: Access denied")
            self.addText('')

        self.textEdit.clear()
        self.textEdit.repaint()

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

    def getUpdates(self):
        response = requests.get('http://127.0.0.1:5000/history',
                                params={'after': self.last_message_time})
        data = response.json()
        for message in data['messages']:
            time = datetime.fromtimestamp(message['time'])
            time = time.strftime('%Y/%m/%d - %H:%M:%S')
            self.addText(time + ' ' + message['username'])
            self.addText(message['text'])
            self.addText('')
            self.last_message_time = message['time']


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")