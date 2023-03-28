import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

class exp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(200, 300, 400, 400)
        self.setWindowTitle('Quit')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'You sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('我关闭了')
        else:
            event.ignore()
            print('wobuguanbi')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = exp()
    sys.exit(app.exec_())