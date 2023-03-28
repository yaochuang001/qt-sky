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
        tableWidget.setRowCount(10)#行数
        tableWidget.setColumnCount(10)#列数
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#所有列自动拉伸，充满界面
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        tableWidget.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems);  # 设置只能选中单元格
        tableWidget.resizeColumnsToContents()#设置列宽高按照内容自适应
        tableWidget.resizeRowsToContents()#设置行宽和高按照内容自适应
        #tableWidget.setHorizontalHeaderLabels(['','','','','','','','','',''])

        for i in range(10):
            tableWidget.setColumnWidth(i,20)
        for i in range(10):
            tableWidget.setRowHeight(i,20)
            tableWidget.item(0,0).te
        for k in range(10):
            for m in range(10):
                item=QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)#点击图片选中单元格
                icon=QIcon('./image/7.ico')
                item.setIcon(icon)

                tableWidget.setItem(k,m,item)
        tableWidget.itemClicked.connect(self.getItemsText)
        self.layout.addWidget(tableWidget)
        self.setLayout(self.layout)
    def getItemsText(self,item):
        print("获取内容：",item)#item.icon())

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())