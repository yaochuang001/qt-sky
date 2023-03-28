import sys
import os
import time
import cgitb
import datetime
#导入界面文件
from MainWindow import *
from ui_setting import *
#导入qt相关包
from PyQt5.QtWidgets import QMainWindow, QApplication,QMdiArea, QMdiSubWindow, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtGui import QPixmap
#导入mysql包
import pymysql
# modbus连接plc
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
# 定时任务
from apscheduler.schedulers.background import BackgroundScheduler

#获取表格数据函数
cgitb.enable(format='text')
class MyMainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("系统设置软件")

        #初始化参数
        self.flag_mysql = False
        self.flag_modbus = False
        self.flag_r_connect = 0
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.baiban_data, 'cron', hour=21, minute=0,second=0)
        self.scheduler.add_job(self.yeban_data, 'cron', hour=7, minute=44,second=0)
        self.scheduler.add_job(self.test, 'cron', second=0);
        #self.scheduler.add_job(self.test2, 'cron', minute=50,second=30)
        #self.scheduler.add_job(self.test3, 'cron', second = 40);
        self.scheduler.start()
        pixmap = QPixmap(".\qifeida.png")
        self.label_3.setPixmap(pixmap)  # 在label上显示图片
        #self.label_3.resize(60, 60)  # 重设Label大小
        self.label_3.setScaledContents(True)
        #self.setCentralWidget(self.mdiArea)
        # 设置堆叠布局给farme
        self.qsl = QStackedLayout(self.frame)
        # 获取表格界面1和2
        self.one = Biao1()
        self.two = Biao2()
        self.set_jiemian = Set_canshu()
        #建立堆叠窗口
        self.qsl.addWidget(self.one)
        self.qsl.addWidget(self.two)
        #创建按钮事件
        self.pushButton.clicked.connect(self.btnPress1_Clicked)
        self.pushButton_2.clicked.connect(self.btnPress2_Clicked)
        #创建工具栏事件
        #self.action_3.triggered.connect(self.qifeida_data)
        self.actionset_mysql.triggered.connect(self.qifeida_mysql)
        self.action_set.triggered.connect(self.qifeida_jiemian_set)
        self.actionstart.triggered.connect(self.qifeida_ym_data_start)
        self.actionstop.triggered.connect(self.qifeida_ym_data_stop)
        self.actionre_connect.triggered.connect(self.init_get_biaoge)
        #创建表格按钮事件
        self.one.hj_btn1.clicked.connect(lambda: self.btn_Clicked('机型1'))
        self.one.hj_btn2.clicked.connect(lambda: self.btn_Clicked('机型2'))
        self.one.hj_btn3.clicked.connect(lambda: self.btn_Clicked('机型3'))
        self.one.hj_btn4.clicked.connect(lambda: self.btn_Clicked('机型4'))
        self.one.hj_btn5.clicked.connect(lambda: self.btn_Clicked('机型5'))
        self.one.hj_btn6.clicked.connect(lambda: self.btn_Clicked('机型6'))
        self.one.hj_btn7.clicked.connect(lambda: self.btn_Clicked('机型7'))
        self.one.hj_btn8.clicked.connect(lambda: self.btn_Clicked('机型8'))
        self.one.hj_btn9.clicked.connect(lambda: self.btn_Clicked('机型9'))
        self.one.hj_btn10.clicked.connect(lambda: self.btn_Clicked('机型10'))
        self.two.hj_btn1.clicked.connect(lambda: self.btn_Clicked('机型11'))
        self.two.hj_btn2.clicked.connect(lambda: self.btn_Clicked('机型12'))
        self.two.hj_btn3.clicked.connect(lambda: self.btn_Clicked('机型13'))
        self.two.hj_btn4.clicked.connect(lambda: self.btn_Clicked('机型14'))
        self.two.hj_btn5.clicked.connect(lambda: self.btn_Clicked('机型15'))
        self.two.hj_btn6.clicked.connect(lambda: self.btn_Clicked('机型16'))
        self.two.hj_btn7.clicked.connect(lambda: self.btn_Clicked('机型17'))
        self.two.hj_btn8.clicked.connect(lambda: self.btn_Clicked('机型18'))
        self.two.hj_btn9.clicked.connect(lambda: self.btn_Clicked('机型19'))
        self.two.hj_btn10.clicked.connect(lambda: self.btn_Clicked('机型20'))
        #创建设置按钮事件
        self.set_jiemian.pushButton.clicked.connect(self.canshuset_save)
        #***********************************初始化用于连续采集的定时器****************************
        self.time_qifeida_ym = QTimer(self)#定时获取界面参数
        self.time_qifeida_ym.timeout.connect(self.qifeida_ym_data)
        self.tiem_xs = QTimer(self)
        self.tiem_xs.timeout.connect(self.qifeida_time)
        self.tiem_xs.start()
        self.time_modbus = QTimer(self)
        self.time_modbus.timeout.connect(self.test)
        #********************************************启动初始化***************************************
        self.qifeida_mysql()
        self.init_get_biaoge()

    def qifeida_time(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd\n hh:mm:ss\n  dddd")
        self.label_4.setText(timeDisplay)
# 测试用
    def test(self):
        try:
            data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=300,
                                         quantity_of_x=20)
            self.flag_r_connect = 0
            print(time.localtime(time.time()))
            print(data_dt_cl)
        except:
            self.flag_r_connect +=1
            if self.flag_r_connect>20:
                self.master = mt.TcpMaster('192.168.1.10', 502)
                self.master.set_timeout(2)
                print('PLC重连完成')

    def test2(self):
        print('50分0秒任务触发')
    def test3(self):
        print('45秒任务触发')
# 从数据库获取所有页面参数
    def init_get_biaoge(self):
        if self.flag_mysql==True:
            try:
                # 检测连接是否断开，如果断开重连
                self.conn.ping(reconnect=True)
                sql = "select jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry,bz from jt_cs;"
                self.cursor.execute(sql)
                a = self.cursor.fetchall()
                for i in range(0,20):
                    if i <10 :
                        for j in range(0,7):
                            item = QTableWidgetItem(str(a[i][j]))
                            self.one.tableWidget.setItem(i, j, item)
                    else:
                        for j in range(0,7):
                            item = QTableWidgetItem(str(a[i][j]))
                            self.two.tableWidget.setItem((i-10), j, item)
            except Exception as e:
                print(e)
        else:
            print('请先连接数据库')

# 白班数据刷新
    def baiban_data(self):
        try:
            data_biaoge = self.get_biaoge()
            # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
            data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=300,
                                    quantity_of_x=20)
            for i in range(0,20):
                self.write_ls_jxcs_data(data_biaoge[i],data_dt_cl[i],num=i+1)
            for j in range(3000,3020):
                b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, j, output_value=100)
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('获取白班数据完成，并置位PLC中各个机型当前型号产量')
        except Exception as e:
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('白班数据自动存储错误：'+str(e))


# 夜班数据刷新
    def yeban_data(self):
        try:
            data_biaoge = self.get_biaoge()
            # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
            data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=300,
                                    quantity_of_x=20)
            for i in range(0,20):
                self.write_ls_jxcs_data(data_biaoge[i],data_dt_cl[i],num=i+1)
            for j in range(3000,3020):
                b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, j, output_value=100)
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('获取夜班数据完成，并置位PLC中各个机型当前型号产量')
        except Exception as e:
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('夜班数据自动存储错误：'+str(e))

# 获取所有表格数据
    def get_biaoge(self):
        a = []
        for i in range(0, 10):
            b = []
            for j in range(0, 7):
                try:
                    b.append(self.one.tableWidget.item(i, j).text())
                except:
                    b.append('')
            a.append(b)
        for i in range(0, 10):
            b = []
            for j in range(0, 7):
                try:
                    b.append(self.two.tableWidget.item(i, j).text())
                except:
                    b.append('')
            a.append(b)
        return a
# 获取单行表格数据
    def get_single_biaoge(self,h_data):
        b = []
        if h_data<10:
            for j in range(0, 7):
                try:
                    b.append(self.one.tableWidget.item(h_data, j).text())
                except:
                    b.append('')
        else:
            h_data = h_data-10
            for j in range(0, 7):
                try:
                    b.append(self.two.tableWidget.item(h_data, j).text())
                except:
                    b.append('')
        return b
# 获取数据库中单行数据
    def get_single_mysql(self,id):
        # 检测连接是否断开，如果断开重连
        self.conn.ping(reconnect=True)
        sql = "select jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry,bz from jt_cs where id=%d;" %(id)
        self.cursor.execute(sql)
        a = self.cursor.fetchall()
        return a

# 写入当前机型数据参数到数据库
    def write_ls_jxcs_data(self,data_biao,data_plc,num):
        try:
            xh_num = int(data_biao[3][:1])
        except Exception as e:
            xh_num = 0
            print(e)
        try:
            # 检测连接是否断开，如果断开重连
            self.conn.ping(reconnect=True)
            sql_search = "select max(time_ls) from jt_ls_jx where jt_num_ls='%d';"%(num)
            self.cursor.execute(sql_search)
            a = self.cursor.fetchall()
            time = a[0][0]
            time = str(time.time())
        except Exception as e:
            time = '07:45:00'
            print(e)
        # 检测连接是否断开，如果断开重连
        self.conn.ping(reconnect=True)
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into jt_ls_jx(time_ls,jt_num_ls,kh_xh_ls,cp_gg_ls,jg_gx_ls,fz_ry_ls,zj_ry_ls," \
              "bz_ls,xh_cl_ls,xh_num,time_qieji) values('%s','%d','%s','%s','%s','%s','%s'," \
              "'%s','%d','%d','%s');" % (
                  dt, int(data_biao[0]), data_biao[1], data_biao[2], data_biao[3], data_biao[4], data_biao[5], data_biao[6],data_plc,xh_num,time)
        # 执行SQL语句
        self.cursor.execute(sql)
        # 提交事务
        self.conn.commit()


# 更新所有表格数据
    def qifeida_ym_data(self):
        if self.flag_mysql==True:
            a = self.get_biaoge()
            try:
                # 插入数据的SQL语句
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for i in range(0,20):
                    try:
                        # 检测连接是否断开，如果断开重连
                        self.conn.ping(reconnect=True)
                        sql = "replace into jt_cs(id,time,jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry," \
                            "bz) values(%d,'%s','%d','%s','%s','%s','%s','%s'," \
                            "'%s');" % ((i+1),dt,int(a[i][0]), a[i][1],a[i][2],a[i][3],a[i][4],a[i][5],a[i][6])
                        # 执行SQL语句
                        self.cursor.execute(sql)
                        # 提交事务
                        self.conn.commit()
                    except:
                        # 检测连接是否断开，如果断开重连
                        self.conn.ping(reconnect=True)
                        sql = "insert into jt_cs(id,time,jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry," \
                              "bz) values(%d,'%s','%d','%s','%s','%s','%s','%s'," \
                              "'%s');" % (
                              (i + 1), dt, int(a[i][0]), a[i][1], a[i][2], a[i][3], a[i][4], a[i][5], a[i][6])
                        # 执行SQL语句
                        self.cursor.execute(sql)
                        # 提交事务
                        self.conn.commit()
            except Exception as e:
                print(e)
            print(a)
        else:
            print('请创建mysql数据连接')

# 更新单行表格数据
    def qifeida_ym_single_data(self,h_data):
        a = self.get_single_biaoge(h_data)
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # 检测连接是否断开，如果断开重连
            self.conn.ping(reconnect=True)
            sql = "replace into jt_cs(id,time,jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry, \
                  bz) values(%d,'%s','%d','%s','%s','%s','%s','%s', \
                  '%s');" % ((h_data + 1), dt, int(a[0]), a[1], a[2], a[3], a[4], a[5], a[6])
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()
        except:
            # 检测连接是否断开，如果断开重连
            self.conn.ping(reconnect=True)
            sql = "insert into jt_cs(id,time,jt_num,kh_xh,cp_gg,jg_gx,fz_ry,zj_ry," \
                  "bz) values(%d,'%s','%d','%s','%s','%s','%s','%s'," \
                  "'%s');" % (
                      (h_data + 1), dt, int(a[0]), a[1], a[2], a[3], a[4], a[5], a[6])
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()

    def qifeida_ym_data_start(self):
        self.time_qifeida_ym.start(2000)
        print('kaishicaiji')
    def qifeida_ym_data_stop(self):
        self.time_qifeida_ym.stop()
        print('guanicaiji')


    def canshuset_save(self):
        try:
            self.set_jiemian.canshu_get()
            # 参数存储
            strFilePath = os.getcwd()
            os.chdir(strFilePath)
            cf = configparser.ConfigParser()
            cf.read("./canshu.conf")
            cf.set("Database", "host", self.set_jiemian.canshu_data['Database']['host'])
            cf.set("Database", "user", self.set_jiemian.canshu_data['Database']['user'])
            cf.set("Database", "password", self.set_jiemian.canshu_data['Database']['password'])
            cf.set("Database", "database", self.set_jiemian.canshu_data['Database']['database'])
            cf.set("Database", "charset", self.set_jiemian.canshu_data['Database']['charset'])
            self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser.append('参数保存成功:'+str(self.set_jiemian.canshu_data))
            with open("./canshu.conf", "w+") as f:
                cf.write(f)
        except Exception as e:
            print('参数保存失败:'+str(e))


    def btn_Clicked(self,a):
        if self.flag_modbus == True:
            reply = QMessageBox.question(self, 'Message', '请问是否转机',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                if a == '机型1':
                    try:
                        self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                        # 从数据库中获取当前行的参数
                        aa = self.get_single_mysql(1)
                        data_biao = aa[0]
                        print(data_biao)
                        # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                        data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=300,
                                                quantity_of_x=1)
                        data_plc = data_dt_cl[0]
                        self.write_ls_jxcs_data(data_biao,data_plc,num=1)
                        self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                        # 清零当前型号产量数据
                        b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3000, output_value=100)
                        # 将当前页面参数刷新到数据库
                        self.qifeida_ym_single_data(0)
                        self.textBrowser_2.append('数据刷新:刷新机台1参数并清除PLC中机台1当前机型产量数据')
                    except Exception as e:
                        self.textBrowser_2.append('错误信息：'+str(e))
                if a == '机型2':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(2)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=301,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=2)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3001, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(1)
                    self.textBrowser_2.append('数据刷新:刷新机台2参数并清除PLC中机台2当前机型产量数据')
                if a == '机型3':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(3)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=302,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=3)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3002, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(2)
                    self.textBrowser_2.append('数据刷新:刷新机台3参数并清除PLC中机台3当前机型产量数据')
                if a == '机型4':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(4)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=303,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=4)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3003, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(3)
                    self.textBrowser_2.append('数据刷新:刷新机台4参数并清除PLC中机台4当前机型产量数据')
                if a == '机型5':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(5)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=304,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=5)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b =self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3004, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(4)
                    self.textBrowser_2.append('数据刷新:刷新机台5参数并清除PLC中机台5当前机型产量数据')
                if a == '机型6':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(6)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=305,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=6)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3005, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(5)
                    self.textBrowser_2.append('数据刷新:刷新机台6参数并清除PLC中机台6当前机型产量数据')
                if a == '机型7':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(7)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=306,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=7)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3006, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(6)
                    self.textBrowser_2.append('数据刷新:刷新机台7参数并清除PLC中机台7当前机型产量数据')
                if a == '机型8':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(8)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=307,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=8)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3007, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(7)
                    self.textBrowser_2.append('数据刷新:刷新机台8参数并清除PLC中机台8当前机型产量数据')
                if a == '机型9':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(9)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=308,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=9)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3008, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(8)
                    self.textBrowser_2.append('数据刷新:刷新机台9参数并清除PLC中机台9当前机型产量数据')
                if a == '机型10':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(10)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=309,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=10)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3009, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(9)
                    self.textBrowser_2.append('数据刷新:刷新机台10参数并清除PLC中机台10当前机型产量数据')
                if a == '机型11':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(11)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=310,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=11)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3010, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(10)
                    self.textBrowser_2.append('数据刷新:刷新机台11参数并清除PLC中机台11当前机型产量数据')
                if a == '机型12':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(12)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=311,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=12)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3011, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(11)
                    self.textBrowser_2.append('数据刷新:刷新机台12参数并清除PLC中机台12当前机型产量数据')
                if a == '机型13':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(13)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=312,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=13)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3012, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(12)
                    self.textBrowser_2.append('数据刷新:刷新机台13参数并清除PLC中机台13当前机型产量数据')
                if a == '机型14':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(14)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=313,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=14)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3013, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(13)
                    self.textBrowser_2.append('数据刷新:刷新机台14参数并清除PLC中机台14当前机型产量数据')
                if a == '机型15':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(15)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=314,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=15)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3014, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(14)
                    self.textBrowser_2.append('数据刷新:刷新机台15参数并清除PLC中机台15当前机型产量数据')
                if a == '机型16':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(16)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=315,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=16)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3015, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(15)
                    self.textBrowser_2.append('数据刷新:刷新机台16参数并清除PLC中机台16当前机型产量数据')
                if a == '机型17':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(17)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=316,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=17)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3016, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(16)
                    self.textBrowser_2.append('数据刷新:刷新机台17参数并清除PLC中机台17当前机型产量数据')
                if a == '机型18':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(18)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=317,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=18)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3017, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(17)
                    self.textBrowser_2.append('数据刷新:刷新机台18参数并清除PLC中机台18当前机型产量数据')
                if a == '机型19':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(19)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=318,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=19)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3018, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(18)
                    self.textBrowser_2.append('数据刷新:刷新机台19参数并清除PLC中机台19当前机型产量数据')
                if a == '机型20':
                    self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                    # 从数据库中获取当前行的参数
                    aa = self.get_single_mysql(20)
                    data_biao = aa[0]
                    # PLC侧从数据寄存器300-399表示机型1-100对应设备当前型号产量
                    data_dt_cl = self.master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=319,
                                                quantity_of_x=1)
                    data_plc = data_dt_cl[0]
                    self.write_ls_jxcs_data(data_biao, data_plc, num=20)
                    self.textBrowser_2.append('数据写入:' + str(data_biao) + str(data_plc))
                    # 清零当前型号产量数据
                    b = self.master.execute(1, md.WRITE_SINGLE_REGISTER, 3019, output_value=100)
                    # 将当前页面参数刷新到数据库
                    self.qifeida_ym_single_data(19)
                    self.textBrowser_2.append('数据刷新:刷新机台20参数并清除PLC中机台20当前机型产量数据')
        else:
            self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser.append(a+'请先创建MODBUS连接...')

    def btn_Set(self):
        self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
        self.textBrowser.append('mysql数据参数保存成功')


    #def qifeida_data(self):
        #self.mdiArea.addSubWindow(self.qifeida_table)
        #self.qifeida_table.show()

    def btnPress1_Clicked(self):

        self.qsl.setCurrentIndex(0)
        #self.one.show()


    def btnPress2_Clicked(self):
        self.qsl.setCurrentIndex(1)
        #self.tow.show()


    def qifeida_mysql(self):
        if self.flag_mysql == False:
            try:
                self.set_jiemian.canshu_get()
                # 连接数据
                self.conn = pymysql.connect(host=self.set_jiemian.canshu_data['Database']['host'], user=self.set_jiemian.canshu_data['Database']['user'],
                                            password=self.set_jiemian.canshu_data['Database']['password'], database=self.set_jiemian.canshu_data['Database']['database'],
                                            charset=self.set_jiemian.canshu_data['Database']['charset'])
                # 得到一个可以执行SQL语句的光标对象
                self.cursor = self.conn.cursor()
                self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                self.textBrowser.append('创建mysql连接完成,置位mysql连接标志位')
                self.flag_mysql = True
            except Exception as e:
                self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                self.textBrowser.append('创建mysql连接失败'+str(e))
        else:
            self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser.append('mysql已经连接成功...')
        if self.flag_modbus == False:
            try:
                self.master = mt.TcpMaster('192.168.1.10', 502)
                self.master.set_timeout(2)
                self.time_modbus.start(4000)
                self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                self.textBrowser.append('创建PLC_MODBUS连接完成,置位MODBUS连接标志位')
                self.flag_modbus = True
            except Exception as e:
                self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
                self.textBrowser.append('创建PLC_MODBUS连接失败'+str(e))
        else:
            self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser.append('PLC_MODBUS已经创建连接...')



    def qifeida_jiemian_set(self):
        self.set_jiemian.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyMainWindow()
    w.show()
    sys.exit(app.exec_())