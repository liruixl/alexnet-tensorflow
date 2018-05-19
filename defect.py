from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QLineEdit,
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton,
                            QGroupBox, QMessageBox,
                            QSizePolicy,
                            QSlider)
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QFile, QDataStream, QIODevice, QTextStream
import os

# from recognition import test_one_image

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_path = r'C:\Users\qazwsx\Desktop\GUI\D2_M_570528_00030.jpg'
        self.img_dir = r''
        self.is_dir = False
        self.txt_path = ''
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
        self.imglabel.setAlignment(Qt.AlignHCenter)
        self.imgBox = QGroupBox("defect image")
        self.imglabel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

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
        btn_layout.addStretch(1)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(shibie_btn)
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
        
        self.settingAct = QAction("设置", self, 
                statusTip="设置模型参数")
        
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

        setMenu = menubar.addMenu('设置')
        setMenu.addAction(self.settingAct)


        helpMenu = menubar.addMenu('帮助')
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.helpAct)
    
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        
    def open(self):
        # 里面的参数具体是 题目 初始路径 后缀过滤
        fname = QFileDialog.getOpenFileName(self, '选取钢板图片', 'C:\\', 
                                            "Image File(*.jpg *.png *.tif)") 

        if fname[0]:
            self.img_path = fname[0]
            pixMap = QPixmap(self.img_path)
            self.imglabel.setPixmap(pixMap)
        self.is_dir = False
        self.logEdit.append('已打开图片 %s, 请点击识别<b>按钮</b>开始识别' % fname)
    
    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选取文件夹', 'C:/')
        self.img_dir = dir_name
        self.is_dir = True
        self.logEdit.append('已选取文件夹 %s, 请点击识别<b>按钮</b>开始识别' % dir_name)



    def save(self):
        if self.txt_path:
            return self.saveFile(self.curFile)
        return self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False
    
    # 保存为.txt或者.csv
    def saveFile(self, file_name):
        print(self.bigEditor.toPlainText())
        qfile = QFile(file_name)
        if not qfile.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (file_name.split('\\')[-1], qfile.errorString()))
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
        event.accept()
    
    def about(self):
        QMessageBox.about(self, "About Applocation",
                "此<b>钢板缺陷识别系统</b>是基于深度学习搭建而成，目前适用于"
                "折叠、压痕、划伤、结疤、氧化铁皮、黑斑6大钢板缺陷的分类识别")
    
    def abouthelp(self):
        pass

    def recognition(self):
        if self.is_dir:
            img_list = os.listdir(self.img_dir)
            for i in img_list:
                p = os.path.join(img_list, i)
                # pro, defect_name = test_one_image(p)
                pro, defect_name = 2, "文件夹"
                self.bigEditor.append('%s,%s,%s' % (p.split('\\')[-1], pro, defect_name))
        else:
            # pro, defect_name = test_one_image(self.img_path)
            pro, defect_name = 1, "haha"
            # self.bigEditor.setPlainText()
            self.bigEditor.append('%s,%s,%s' % (self.img_path.split('\\')[-1], pro, defect_name))

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

# 设置窗口
class SettingWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle('设置')
        self.setStyleSheet("background: gray")

        self.initUI()

    def initUI(self):
        glayout = QGridLayout()

        para_label = QLabel('ModlePara:')
        dropout_label =QLabel('Dropout:')

        para_text = QLineEdit()
        dropout_text = QLineEdit('1.0')
        dropout_text.setReadOnly(True)

        sld = QSlider(Qt.Horizontal)

        btn = QPushButton('选择')

        glayout.setVerticalSpacing(10)

        glayout.addWidget(para_label, 1,1,1,2)
        glayout.addWidget(para_text, 1,3,1,2)
        glayout.addWidget(btn, 1,5,1,1)
        glayout.addWidget(dropout_label,2,1,1,2)
        glayout.addWidget(dropout_text, 2,3,1,1)
        glayout.addWidget(sld, 2,4,1,2)

        self.setLayout(glayout)

    def handle_click(self):
        if not self.isVisible():
            self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    settingWin = SettingWindow()
    mainWin.settingAct.triggered.connect(settingWin.handle_click)  # 显示设置窗口
    mainWin.show()
    sys.exit(app.exec_())

