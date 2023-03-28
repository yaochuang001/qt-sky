#QTableWidget 控件使用
from PyQt5.QtWidgets import  QComboBox,QTableView,QAbstractItemView,QHeaderView,QTableWidget, QTableWidgetItem, QMessageBox,QListWidget,QListWidgetItem, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QStandardItem,QStandardItemModel,QCursor,QFont,QBrush,QColor
from PyQt5.QtCore import QStringListModel,QAbstractListModel,QModelIndex,QSize,Qt

import sys


class WindowClass(QWidget):

    def __init__(self,parent=None):

        super(WindowClass, self).__init__(parent)
        self.layout=QHBoxLayout()
        self.resize(400,300)
        tableWidget=QTableWidget()
        tableWidget.setRowCount(4)#行数
        tableWidget.setColumnCount(4)#列数
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#所有列自动拉伸，充满界面
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        tableWidget.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置只有行选中, 整行选中
        tableWidget.resizeColumnsToContents()#设置列宽高按照内容自适应
        tableWidget.resizeRowsToContents()#设置行宽和高按照内容自适应
        #tableWidget.horizontalHeader().setVisible(False)#设置列标题隐藏（针对列标题横向排列）
        #tableWidget.verticalHeader().setVisible(False)#设置列标题隐藏（针对列标题纵向排列）
        self.layout.addWidget(tableWidget)
        tableWidget.setHorizontalHeaderLabels(['姓名','地址','年龄','操作']) #横向标题排列，如果使用setVerticalHeaderLabels则是纵向排列标题
        items=[['JONES','Beijing','23',''],['SMITH','SHAngHai','23',''],['ZY','Tianjin','23',''],['Smith','SJT','22','']]
        for i in range(len(items)):#注意上面列表中数字加单引号，否则下面不显示(或者下面str方法转化一下即可)
            item=items[i]

            for j in range(len(item)):
#-----------------------------修改后程序，最后一列添加按钮-------------------#
                 if  j!=3:
                     item = QTableWidgetItem(str(items[i][j]))
                     tableWidget.setItem(i, j, item)
                 else: #最后一列添加控件
                     btn = QPushButton("删除")
                     btn.setDown(True)
                     btn.setStyleSheet("QPushButton{margin:3px};")
                     tableWidget.setCellWidget(i, j, btn)
#--------------------------------------------------------------------------#

#------------------------------0,1位置添加下拉列表框----------------------#
        #某个单元格设置为控件
        comBox=QComboBox()
        comBox.addItem("北京")
        comBox.addItems(["上海","天津"])
        comBox.setStyleSheet("QComboBox{margin:3px};")
        tableWidget.setCellWidget(0,1,comBox)
#------------------------------------------------------------------------#
        #字体设置
        newItem=tableWidget.item(0,0)
        newItem.setFont(QFont("Times",12,QFont.Black))#字体样式加粗
        newItem.setForeground(QBrush(QColor(255,0,0)))#字体颜色
        #设置排序
        tableWidget.sortItems(1,Qt.AscendingOrder)#Qt.DescendingOrder 升序降序
        item_00=tableWidget.item(0,0)
        item_00.setTextAlignment(Qt.AlignRight)#Qt.AlignCenter ...
        #合并单元格
        tableWidget.setSpan(0,0,3,1)
        #单元格宽高设置
        tableWidget.setColumnWidth(0,150)#第一个参数为行下标
        tableWidget.setRowHeight(0,40)
        #设置不显示分割线
        tableWidget.setShowGrid(False)

        #单元格设置图片
        tableWidget.setItem(1,1,QTableWidgetItem(QIcon("./image/add.ico"),"百度"))

        tableWidget.setItem(0,0,newItem)

        self.setLayout(self.layout)

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())