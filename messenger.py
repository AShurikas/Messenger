from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore
import clientui


class ExampleApp(clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # to run on button click
        self.pushButton.pressed.connect(self.send_message)
        # to run on timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)
        self.after = 0

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            response = requests.post('http://127.0.0.1:5000/send', json={
                'name': name,
                'text': text})
        except:
            self.textBrowser.append('No connection with server....')
            self.textBrowser.append('')
            return
        if response.status_code != 200:
            self.textBrowser.append('Message not sent')
            self.textBrowser.append('Check name and text')
            self.textBrowser.append('')
            return
        self.textEdit.clear()


    def show_messages(self, messages):
        for message in messages:
            dt = datetime.fromtimestamp(message['time'])
            dt = dt.strftime('%H:%M')
            self.textBrowser.append(dt + ' ' + message['name'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get('http://127.0.0.1:5000/messages',
                                    params={'after': self.after}
                                    )
        except:
            return
        messages = response.json()['messages']
        if len(messages) > 0:
            self.show_messages(messages)
            self.after = messages[-1]['time']






app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()
