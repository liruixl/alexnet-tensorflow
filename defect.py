from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QLineEdit,
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton,
                            QGroupBox, QMessageBox,
                            QSizePolicy,
                            QSlider)
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QFile, QDataStream, QIODevice, QTextStream

# from recognition import test_one_image, test_one_dir
from recognition import RecThread

from d_setting_win import SettingWindow
from train_win import StockWin

import threading
import numpy as np
import matplotlib.pyplot as plt
import re
import configparser
import os

# from recognition import test_one_image

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_path = ''
        self.img_dir = ''

        self.is_dir = False

        self.txt_path = ''  # 文件保存路径
        self.isModified = False

        self.model_path = ''

        self.initUI()

    def initUI(self):
        self.createActions()
        self.createMenus()
        self.createStatusBar()

        mainwidget = QWidget()
        self.creatImgLabel()
        self.creatResultBox()
        self.creatInfoBox()
        # vlayout = QVBoxLayout()  # 主布局也可采用网格布局
        main_layout = QGridLayout()
        # hlayout = QHBoxLayout()

        # hlayout.addWidget(self.imgBox)
        # hlayout.addLayout(self.result_layout)
        
        main_layout.addWidget(self.imgBox, 0, 0, 3, 3)
        main_layout.addLayout(self.result_layout, 0, 3, 3, 4)
        main_layout.addLayout(self.loglayout, 3, 0, 2, 7)

        mainwidget.setLayout(main_layout)
        self.setCentralWidget(mainwidget)

        self.setGeometry(300, 100, 700, 500)
        self.setWindowTitle('缺陷识别')



    # 图片显示区
    def creatImgLabel(self):
        self.imglabel = QLabel()
        self.imglabel.setAlignment(Qt.AlignCenter)
        self.imgBox = QGroupBox("defect image")
        self.imgBox.setAlignment(Qt.AlignHCenter)
        # self.imglabel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        layout = QVBoxLayout()

        # pixMap = QPixmap("icon.jpg")
        # imgeLabel.setPixmap(pixMap)
        layout.addWidget(self.imglabel)
        self.imgBox.setLayout(layout)

    # 结果显示区
    def creatResultBox(self):
        self.result_layout = QVBoxLayout() 
        nameLabel = QLabel("识别结果：")
        self.bigEditor = QTextEdit()
        self.bigEditor.setReadOnly(True)
        # bigEditor.setPlainText("黑斑黑斑.")

        btn_layout = QHBoxLayout()
        
        clear_btn = QPushButton('清除')
        clear_btn.clicked.connect(self.clear_result)
        shibie_btn = QPushButton('识别')
        shibie_btn.clicked.connect(self.recognition)
        tongji_btn = QPushButton('统计图')
        tongji_btn.clicked.connect(self.tongji)
        btn_layout.addStretch(1)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(shibie_btn)
        btn_layout.addStretch(2)
        btn_layout.addWidget(tongji_btn)
        btn_layout.addStretch(1)

        self.result_layout.addWidget(nameLabel)
        self.result_layout.addWidget(self.bigEditor)
        self.result_layout.addLayout(btn_layout)

    # 日志显示区
    def creatInfoBox(self):
        # self.logBox = QGroupBox("信息")
        # self.logBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.loglayout = QVBoxLayout()

        loglabel = QLabel('信息')
        self.logEdit = QTextEdit()
        self.logEdit.setReadOnly(True)
        # self.logEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # size = self.logEdit.sizeHint()
        # print(size)
        # size.setHeight(size.height() - 100)
        # self.logEdit.setBaseSize(size)
        
        self.loglayout.addWidget(loglabel)
        self.loglayout.addWidget(self.logEdit)

        

    def createActions(self):
        self.openAct = QAction("&打开图片", self, shortcut=QKeySequence.Open, 
                        statusTip="Open an img", triggered=self.open)
        self.openDirAct = QAction("&打开文件夹", self, 
                        statusTip="Open a dir of images", triggered=self.open_dir)
        self.saveAct = QAction( "&保存", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the recognition result to disk", triggered=self.save)
        self.saveAsAct = QAction("保存为...", self,
                                shortcut=QKeySequence.SaveAs,
                                statusTip="Save the defect info",
                                triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        
        self.settingAct = QAction("模型设置", self,
                statusTip="设置模型参数")

        self.trainAct = QAction("训练", self,
                                  statusTip="与训练功能有关")


        
        self.aboutAct = QAction("关于", self,
                statusTip="Show the application's About box",
                triggered=self.about)
        self.helpAct = QAction("帮助", self,
                statusTip="Show the application's help info",
                triggered=self.abouthelp)

    
    def createMenus(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.openDirAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        setMenu = menubar.addMenu('功能')
        setMenu.addAction(self.settingAct)
        setMenu.addAction(self.trainAct)


        helpMenu = menubar.addMenu('帮助')
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.helpAct)
    
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        
    def open(self):
        # 里面的参数具体是 题目 初始路径 后缀过滤
        # fname = QFileDialog.getOpenFileName(self, '选取钢板图片', 'C:\\',
        #                                     "Image File(*.jpg *.png *.tif)")
        fname = QFileDialog.getOpenFileName(self, '选取钢板图片', '/home/hexiang/data/set',
                                            "Image File(*.jpg *.png *.tif)")

        if fname[0]:
            self.img_path = fname[0]
            pixMap = QPixmap(self.img_path)
            self.imglabel.setPixmap(pixMap)
        self.is_dir = False
        self.logEdit.append('已打开图片 %s, 请点击识别<b>按钮</b>开始识别' % str(fname))
    
    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选取文件夹', '/home')
        self.img_dir = dir_name
        self.is_dir = True
        self.logEdit.append('已选取文件夹 %s, 请点击识别<b>按钮</b>开始识别' % str(dir_name))



    def save(self):
        if self.txt_path:
            return self.saveFile(self.txt_path)
        return self.saveAs()

    def saveAs(self):
        fname, _ = QFileDialog.getSaveFileName(self)
        if fname:
            return self.saveFile(fname)

        return False
    
    # 保存为.txt或者.csv
    def saveFile(self, file_name):
        print(self.bigEditor.toPlainText())
        qfile = QFile(file_name)
        if not qfile.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % re.split('\\ | /', file_name)[-1], qfile.errorString())
            return False

        outf = QTextStream(qfile)
        
        outf << self.bigEditor.toPlainText()
        self.setCurrentFile(file_name)

        self.statusBar().showMessage("File %s saved" % file_name)
        
        # 用python也可以
        # f = open(file_name, 'a')
        # f.write('\n')
        # f.write(self.bigEditor.toPlainText())
        # f.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '确定退出?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def about(self):
        QMessageBox.about(self, "About Applocation",
                "此<b>钢板缺陷识别系统</b>是基于深度学习搭建而成，目前适用于"
                "折叠、压痕、划伤、结疤、氧化铁皮、黑斑6大钢板缺陷的分类识别")
    
    def abouthelp(self):
        pass

    def recognition(self):
        # 有线程问题 识别完成后模型的初始化还在,下一次识别报错
        if self.is_dir:
            t1 = RecThread(True, self.img_dir)
            t1.start()
            t1.join()
            result = t1.get_result()
            for k, v in result.items():
                self.bigEditor.append('%s,%s,%s' % (re.split('/', k)[-1], v[0], v[1]))
        else:
            print(self.img_path)
            t2 = RecThread(False, self.img_path)
            t2.start()
            t2.join()

            pro, defect_name = t2.get_result()
            # pro, defect_name = t2.
            # self.bigEditor.setPlainText()
            self.bigEditor.append('%s,%s,%s' % (re.split('/', self.img_path)[-1], pro+1, defect_name))


    def tongji(self):
        ind = np.arange(5)
        width = 0.35

        a = [1, 2, 3, 4, 5]
        b = [5, 3, 3, 2, 1]

        plt.xlabel('defect class')
        plt.ylabel('Number')

        plt.bar(ind, a, width, color='r', label='man')
        plt.bar(ind + width, b, width, color='y', label='woman')

        plt.title('defect')

        plt.show()

    def clear_result(self):
        self.bigEditor.clear()

    def setCurrentFile(self, fileName):
        self.txt_path = fileName
        # self.bigEditor.document().setModified(False)
        # self.setWindowModified(False)

        # if self.curFile:
        #     shownName = self.strippedName(self.curFile)
        # else:
        #     shownName = 'untitled.txt'
        # self.setWindowTitle("%s[*] - Application" % shownName)
    
    def setting_change(self):
        pass

    def openSetting(self):
        setting_win = SettingWindow()
        setting_win.handle_click()  # 显示设置窗口
        print("设置窗口来了")

    def openTrain(self):
        pass




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    setting_win = SettingWindow()
    mainWin.settingAct.triggered.connect(setting_win.handle_click)  # 显示设置窗口

    train_win = StockWin()
    mainWin.trainAct.triggered.connect(train_win.handle_click)  # 显示训练窗口

    mainWin.show()
    sys.exit(app.exec_())

