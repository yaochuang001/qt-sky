from BiaoGe1 import *
from Biao1 import *
from Biao2 import *
from set_canshu import *
import configparser
from PyQt5.QtWidgets import QWidget, QStackedLayout,QMdiSubWindow,QPushButton,QMessageBox


class Biaoge1(QWidget, Ui_Form_biaoge1):

    def __init__(self):
        super(Biaoge1, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("biaoge1")
        # 设置堆叠布局给farme
        self.qsl = QStackedLayout(self.frame)
        # 获取表格界面1和2
        one = Biao1()
        two = Biao2()
        self.qsl.addWidget(one)
        self.qsl.addWidget(two)
        self.pushButton.clicked.connect(self.btnPress1_Clicked)
        self.pushButton_2.clicked.connect(self.btnPress2_Clicked)

    def btnPress1_Clicked(self):

        self.qsl.setCurrentIndex(0)
        #self.one.show()


    def btnPress2_Clicked(self):
        self.qsl.setCurrentIndex(1)
        #self.tow.show()


class Biao1(QWidget, Ui_biao1):

    def __init__(self):
        super(Biao1, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("biao1")
        self.tableWidget.verticalHeader().setVisible(False)
        self.hj_btn1 = QPushButton("换机")
        #self.hj_btn1.setDown(True)
        self.hj_btn1.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(0,7,self.hj_btn1)
        self.hj_btn2 = QPushButton("换机")
        #self.hj_btn2.setDown(True)
        self.hj_btn2.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(1,7,self.hj_btn2)
        self.hj_btn3 = QPushButton("换机")
        #self.hj_btn3.setDown(True)
        self.hj_btn3.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(2,7,self.hj_btn3)
        self.hj_btn4 = QPushButton("换机")
        #self.hj_btn4.setDown(True)
        self.hj_btn4.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(3,7,self.hj_btn4)
        self.hj_btn5 = QPushButton("换机")
        #self.hj_btn5.setDown(True)
        self.hj_btn5.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(4,7,self.hj_btn5)
        self.hj_btn6 = QPushButton("换机")
        #self.hj_btn6.setDown(True)
        self.hj_btn6.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(5,7,self.hj_btn6)
        self.hj_btn7 = QPushButton("换机")
        #self.hj_btn7.setDown(True)
        self.hj_btn7.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(6,7,self.hj_btn7)
        self.hj_btn8 = QPushButton("换机")
        #self.hj_btn8.setDown(True)
        self.hj_btn8.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(7,7,self.hj_btn8)
        self.hj_btn9 = QPushButton("换机")
        #self.hj_btn9.setDown(True)
        self.hj_btn9.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(8,7,self.hj_btn9)
        self.hj_btn10 = QPushButton("换机")
        #self.hj_btn10.setDown(True)
        self.hj_btn10.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(9,7,self.hj_btn10)


class Biao2(QWidget, Ui_biao2):

    def __init__(self):
        super(Biao2, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("biao2")
        self.tableWidget.verticalHeader().setVisible(False)
        self.hj_btn1 = QPushButton("换机")
        # self.hj_btn1.setDown(False)
        self.hj_btn1.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(0,7,self.hj_btn1)
        self.hj_btn2 = QPushButton("换机")
        #self.hj_btn2.setDown(True)
        self.hj_btn2.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(1,7,self.hj_btn2)
        self.hj_btn3 = QPushButton("换机")
        #self.hj_btn3.setDown(True)
        self.hj_btn3.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(2,7,self.hj_btn3)
        self.hj_btn4 = QPushButton("换机")
        #self.hj_btn4.setDown(True)
        self.hj_btn4.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(3,7,self.hj_btn4)
        self.hj_btn5 = QPushButton("换机")
        #self.hj_btn5.setDown(True)
        self.hj_btn5.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(4,7,self.hj_btn5)
        self.hj_btn6 = QPushButton("换机")
        #self.hj_btn6.setDown(True)
        self.hj_btn6.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(5,7,self.hj_btn6)
        self.hj_btn7 = QPushButton("换机")
        #self.hj_btn7.setDown(True)
        self.hj_btn7.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(6,7,self.hj_btn7)
        self.hj_btn8 = QPushButton("换机")
        #self.hj_btn8.setDown(True)
        self.hj_btn8.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(7,7,self.hj_btn8)
        self.hj_btn9 = QPushButton("换机")
        #self.hj_btn9.setDown(True)
        self.hj_btn9.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(8,7,self.hj_btn9)
        self.hj_btn10 = QPushButton("换机")
        #self.hj_btn10.setDown(True)
        self.hj_btn10.setStyleSheet("QPushButton(margin:3px);")
        self.tableWidget.setCellWidget(9,7,self.hj_btn10)


class Set_canshu(QWidget,Ui_canshu):

    def __init__(self):
        super(Set_canshu, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("参数设置")

        #获取初始参数
        cf = configparser.ConfigParser()
        cf.read("./canshu.conf")
        self.lineEdit.setText(cf.get("Database", 'host'))
        self.lineEdit_2.setText(cf.get("Database", 'user'))
        self.lineEdit_3.setText(cf.get("Database", 'password'))
        self.lineEdit_4.setText(cf.get("Database", 'database'))
        self.lineEdit_5.setText(cf.get("Database", 'charset'))


    def canshu_get(self):
        #获取设置参数
        host = self.lineEdit.text()
        user = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        database = self.lineEdit_4.text()
        charset = self.lineEdit_5.text()

        self.canshu_data = {'Database':{'host':host,'user':user,'password':password,'database':database,'charset':charset},}
        return self.canshu_data


