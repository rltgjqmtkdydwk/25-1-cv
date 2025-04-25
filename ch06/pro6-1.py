# PyQt로 간단한 GUI 만들기(버튼을 클릭하면 삑 소리 들려주기)
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QpushButton
import sys
import winsound

class BeepSound(QMainWindow):
    def __init__(self):
        super().init()
        self.setWindowTitle('삑 소리')
        self.setGeometry(200, 200, 500, 100)

        shortBeepButton = QpushButton('짧게 삑', self)
        longBeepButton = QpushButton('길게 삑', self)
        quitBeepButton = QpushButton('나가기', self)
        self.label = QLabel('환영합닏다.', self)

        shortBeepButton.setGeometry(10, 10, 100, 30)
        longBeepButton.setGeometry(110, 10, 100, 30)
        quitBeepButton.setGeometry(210, 10, 100, 30)
        self.label.setGeometry('환영합닏다.', self)

        shortBeepButton.clicked.connect(self.shortBeepFunction)
        longBeepButton.clicked.connect(self.longBeepFunction)
        quitBeepButton.clicked.connect(self.quitFunction)

    def shortBeepFunction(self):
        self.label.setText('주파수 1000으로 0.5초 동안')
        winsound.Beep(1000, 500)
    
    def longBeepFunction(self):
        self.label.setText('주파수 1000으로 3초 동안')
        winsound.Beep(1000, 3000)

    def quitFunction(self):
        self.close()

app = QApplication(sys.argv)
win = BeepSound()
win.show()
app.exec_()
