from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, 
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton,
                            QGroupBox, QMessageBox,
                            QSizePolicy)
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QFile, QDataStream, QIODevice, QTextStream

# from recognition import test_one_image

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_path = r'C:\Users\qazwsx\Desktop\GUI\D2_M_570528_00030.jpg'
        self.img_dir = r''
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
        main_layout.addLayout(self.loglayout, 3, 0, 1, 7)

        mainwidget.setLayout(main_layout)
        self.setCentralWidget(mainwidget)


        self.setGeometry(300, 100, 700, 400)
        self.setWindowTitle('缺陷识别')



    # 图片显示区
    def creatImgLabel(self):
        self.imglabel = QLabel()
        self.imglabel.setAlignment(Qt.AlignHCenter)
        self.imgBox = QGroupBox("defect image")
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

        shibie_btn = QPushButton('识别')
        shibie_btn.clicked.connect(self.recognition)

        print('显示区就绪')

        self.result_layout.addWidget(nameLabel)
        self.result_layout.addWidget(self.bigEditor)
        self.result_layout.addWidget(shibie_btn)

    # 日志显示区
    def creatInfoBox(self):
        # self.logBox = QGroupBox("信息")
        # self.logBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.loglayout = QVBoxLayout()

        loglabel = QLabel('信息')
        self.logEdit = QTextEdit()
        self.logEdit.setReadOnly(True)
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
                        statusTip="Open a dir of images", triggered=self.open)
        self.saveAct = QAction( "&保存", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the recognition result to disk", triggered=self.save)
        self.saveAsAct = QAction("保存为...", self,
                                shortcut=QKeySequence.SaveAs,
                                statusTip="Save the defect info",
                                triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        
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
    # QFile file( fileName ); // 把文本写入到文件中
    # if ( file.open( IO_WriteOnly ) ) {
    #     QTextStream ts( &file );
    #     ts << textEdit->text();
    #     textEdit->setModified( FALSE );
    # }
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
                "折叠、压痕、划伤、结疤、氧化铁皮、黑斑6大钢板缺陷的分类")
    
    def abouthelp(self):
        pass

    def recognition(self):
        # pro, defect_name = test_one_image(self.img_path)
        pro, defect_name = 1, "haha"
        # self.bigEditor.setPlainText()
        self.bigEditor.append('%s,%s,%s' % (self.img_path.split('\\')[-1], pro, defect_name))

    def setCurrentFile(self, fileName):
        self.txt_path = fileName
        # self.bigEditor.document().setModified(False)
        # self.setWindowModified(False)

        # if self.curFile:
        #     shownName = self.strippedName(self.curFile)
        # else:
        #     shownName = 'untitled.txt'

        # self.setWindowTitle("%s[*] - Application" % shownName)
    



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

