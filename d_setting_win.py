from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QLineEdit,
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton,
                            QGroupBox, QMessageBox,
                            QSizePolicy,
                            QSlider)
from PyQt5.QtGui import QFont, QPixmap, QPalette
from PyQt5.QtCore import Qt, QFile, QDataStream, QIODevice, QTextStream


# 堆栈对话框 https://www.linuxidc.com/Linux/2012-06/63652p16.htm
# 调色板 https://blog.csdn.net/rl529014/article/details/51589096
# 配置读取 configparser

# 设置功能窗口 设置模型参数.


class SettingWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.model_path = ''
        self.dropout = 1.0
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle('设置')
        # self.setStyleSheet("background: gray")



        glayout = QGridLayout()

        para_label = QLabel('ModlePara:')
        dropout_label =QLabel('Dropout:')

        # para_label.setStyleSheet("color:white")
        # dropout_label.setPalette(palette)

        self.para_text = QLineEdit()
        self.dropout_text = QLineEdit('1.0')
        bound_label = QLabel("范围(0,1]")
        bound_label.setFont(QFont("Roman times", 12, QFont.Bold))
        bound_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # dropout_text.setReadOnly(True)

        # sld = QSlider(Qt.Horizontal)

        btn = QPushButton('...')
        btn_cancel = QPushButton('Cancel')
        btn_ok = QPushButton('OK')

        btn.clicked.connect(self.choose)
        btn_cancel.clicked.connect(self.canncel)
        btn_ok.clicked.connect(self.ok)




        f = QFont("Roman times", 10, QFont.Bold)
        self.setFont(f)

        #  与 self.setStyleSheet()不能同时用???
        palette = self.palette()
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Background, Qt.gray)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        glayout.setVerticalSpacing(10)

        glayout.addWidget(para_label, 1,1,1,2)
        glayout.addWidget(self.para_text, 1,3,1,2)
        glayout.addWidget(btn, 1,5,1,1)
        glayout.addWidget(dropout_label,2,1,1,2)
        glayout.addWidget(self.dropout_text, 2,3,1,1)
        glayout.addWidget(bound_label, 2,4,1,1)

        glayout.addWidget(btn_cancel, 3,4,1,1)
        glayout.addWidget(btn_ok, 3,5,1,1)

        # glayout.addWidget(sld, 2,4,1,2)

        self.setLayout(glayout)

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def choose(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择参数', '/home')
        if fname:
            print(fname)

            self.para_text.setText(fname.split('.')[0])

            print(fname.split('.'))

        return False

    def canncel(self):

        self.close()

    def ok(self):
        self.model_path = self.para_text.text()
        self.dropout = float(self.dropout_text.text())
        self.close()
        print(self.model_path)
        print(self.dropout)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    settingWin = SettingWindow()
    settingWin.show()
    sys.exit(app.exec_())