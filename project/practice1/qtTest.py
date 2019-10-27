from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication

import sys

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        btn = QPushButton('Quit', self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        self.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
