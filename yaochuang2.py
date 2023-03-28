import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMdiArea, QMdiSubWindow, QAction, \
    QTextEdit, QToolBar, QDesktopWidget
class SubWin(QMainWindow):
    count = 0
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.toolBar.addAction("新建")
        self.toolBar.addAction("级联")
        self.toolBar.addAction("平铺")
        self.toolBar.addAction("关闭全部")
        self.toolBar.addAction("关闭活动窗口")
        self.toolBar.addAction("测试")
        self.toolBar.addAction("nidaye")
        self.toolBar.actionTriggered[QAction].connect(self.windowaction)
        bar = self.menuBar()
        file = bar.addMenu("File")
        # 添加子菜单
        file.addAction("新建")
        file.addAction("级联")
        file.addAction("平铺")
        file.triggered[QAction].connect(self.windowaction)
        self.setWindowTitle("MDI Demo")
        #self.showFullScreen() #全屏显示
        self.showMaximized() #窗口最大化
        #self.showNormal() #正常显示
        # self.setGeometry(QDesktopWidget().screenGeometry())
    def windowaction(self, q):
        type = q.text()
        print("Triggered : %s" % type)
        if type == "新建":
            # 子窗口增加一个
            self.count = self.count + 1
            # 实例化多文档界面对象
            sub = QMdiSubWindow()
            # 向sub内部添加控件
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subWindow %d" % self.count)
            self.mdi.addSubWindow(sub)
            sub.show()
        elif type == "级联":
            self.mdi.cascadeSubWindows()
        elif type == "平铺":
            self.mdi.tileSubWindows()
        elif type == "关闭全部":
            self.mdi.closeAllSubWindows()
        elif type == "关闭活动窗口":
            self.mdi.closeActiveSubWindow()
        elif type == "测试":
            lst = self.mdi.subWindowList()
            print(lst)
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SubWin()
    win.show()
    sys.exit(app.exec_())