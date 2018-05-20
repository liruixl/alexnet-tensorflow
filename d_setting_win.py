from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QLineEdit,
                            QFileDialog, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton,
                            QGroupBox, QMessageBox,
                            QSizePolicy,
                            QSlider)
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QFile, QDataStream, QIODevice, QTextStream

# 设置功能窗口


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
