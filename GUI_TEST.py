from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

app = QApplication([])
app.setStyle('Fusion')

label = QLabel('Hello World')
label.show()

button = QPushButton('DO NOT CLICK')
button.show()

palette = QPalette()
app.setStyleSheet("QPushButton { margin: 10ex; }")
palette.setColor(QPalette.ButtonText, Qt.red)
app.setPalette(palette)

width = 50
height = 50
#app.setFixedWidth(width)
#app.setFixedHeight(height)

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()


button.clicked.connect(on_button_clicked)


app.exec_()
