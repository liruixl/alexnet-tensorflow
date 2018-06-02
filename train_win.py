from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QLineEdit,
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton, QListWidget, QStackedWidget,
                            QGroupBox, QMessageBox,
                            QSizePolicy,
                            QSlider)
from tfrecord_generator import creat_tfrecords
import sys



class StockWin(QWidget):
    def __init__(self, parent=None):
        super(StockWin, self).__init__(parent)
        self.setWindowTitle(self.tr("辅助功能"))

        listWidget = QListWidget()
        listWidget.insertItem(0, self.tr("训练"))
        listWidget.insertItem(1, self.tr("数据集"))
        # listWidget.insertItem(2, self.tr("数据集管理"))

        #  训练窗体
        train_widget = QWidget()
        glayout = QGridLayout()

        label1 = QLabel('batchszie:')
        self.text1 = QLineEdit()
        label2 = QLabel('step:')
        self.text2 = QLineEdit()
        label3 = QLabel('学习速率:')
        self.text3 = QLineEdit()
        label4 = QLabel('训练集:')
        self.text4 = QLineEdit()
        label5 = QLabel('测试集:')
        self.text5 = QLineEdit()
        label6 = QLabel('参数保存:')
        self.text6 = QLineEdit()

        self.btn1 = QPushButton('...')
        self.btn1.setFixedSize(35, 25)
        self.btn1.clicked.connect(self.choose_set)
        self.btn2 = QPushButton('...')
        self.btn2.setFixedSize(35, 25)
        self.btn2.clicked.connect(self.choose_set)


        btn_model = QPushButton('...')
        btn_model.setFixedSize(35,25)
        btn_ok = QPushButton('开始')

        btn_model.clicked.connect(self.choose)
        btn_ok.clicked.connect(self.ok)

        glayout.addWidget(label1,0,0,1,1)
        glayout.addWidget(label2,1,0,1,1)
        glayout.addWidget(label3,2,0,1,1)
        glayout.addWidget(label4,3,0,1,1)
        glayout.addWidget(label5,4,0,1,1)
        glayout.addWidget(label6,5,0,1,1)
        glayout.addWidget(self.btn1, 3, 3, 1, 1)
        glayout.addWidget(self.btn2, 4, 3, 1, 1)
        glayout.addWidget(btn_model,5,3,1,1)

        glayout.addWidget(self.text1, 0, 1, 1, 2)
        glayout.addWidget(self.text2, 1, 1, 1, 2)
        glayout.addWidget(self.text3, 2, 1, 1, 2)
        glayout.addWidget(self.text4, 3, 1, 1, 2)
        glayout.addWidget(self.text5, 4, 1, 1, 2)
        glayout.addWidget(self.text6, 5, 1, 1, 2)
        glayout.addWidget(btn_ok, 6, 3, 1, 1)

        train_widget.setLayout(glayout)
        #  训练窗体结束

        #  数据集管理窗体

        set_widget = QWidget()
        glayout2 = QGridLayout()

        label_data = QLabel('选择数据集')
        self.text_data_dir = QLineEdit()
        label_none = QLabel()
        btn_make = QPushButton("生成数据")
        btn_make.clicked.connect(self.generate)

        btn3 = QPushButton('...')
        btn3.setFixedSize(35, 25)
        btn3.clicked.connect(self.choose_data_dir)

        glayout2.addWidget(label_data,0,0,1,1)
        glayout2.addWidget(self.text_data_dir,0,1,1,3)
        glayout2.addWidget(btn3,0,4,1,1)

        glayout2.addWidget(label_none,1,4,1,1)
        glayout2.addWidget(btn_make,2,4,1,1)


        set_widget.setLayout(glayout2)






        stack = QStackedWidget()
        stack.addWidget(train_widget)
        stack.addWidget(set_widget)

        mainLayout = QHBoxLayout(self)
        mainLayout.addWidget(listWidget)
        mainLayout.addWidget(stack, 0)
        mainLayout.setStretchFactor(listWidget, 1)
        mainLayout.setStretchFactor(stack, 3)



        # self.connect(listWidget, SIGNAL("currentRowChanged(int)"), stack, SLOT("setCurrentIndex(int)"))
        listWidget.currentRowChanged.connect(stack.setCurrentIndex)


    def handle_click(self):
        if not self.isVisible():
            self.show()

    def choose(self):

        dir_name = QFileDialog.getExistingDirectory(self, '保存模型', '/home')
        if dir_name:
            print(dir_name)
            self.text6.setText(dir_name)

        return False

    def choose_set(self):
        # 里面的参数具体是 题目 初始路径 后缀过滤
        # print(self.sender())
        fname = QFileDialog.getOpenFileName(self, '选取数据集', '/home/hexiang/data/set')
        print(fname)
        if self.sender() is self.btn1:
            self.text4.setText(fname[0])
        if self.sender() is self.btn2:
            self.text5.setText(fname[0])


    def canncel(self):

        self.close()

    def ok(self):
        self.model_path = self.para_text.text()
        self.dropout = float(self.dropout_text.text())
        self.close()
        print(self.model_path)
        print(self.dropout)

    # 第二个数据集窗口
    def choose_data_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选取文件夹', '/home')
        self.text_data_dir.setText(dir_name)

        # 主页面提示
        # self.logEdit.append('已选取文件夹 %s, 请点击识别<b>按钮</b>开始识别' % str(dir_name))

    def generate(self):
        fname, _ = QFileDialog.getSaveFileName(self,'保存为','/home','TFrecords File(*.tfrecords)')
        if fname:
            save_path = fname+'.tfrecords'
            creat_tfrecords(self.text_data_dir.text(), save_path)
            return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = StockWin()
    main.show()
    # app.exec_()
    sys.exit(app.exec_())