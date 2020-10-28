import sys
from PyQt4 import QtGui

app=QtGui.QApplication(sys.argv)
window=QtGui.QWidget()
# setGeometry(x coord, y coord, width, height)
window.setGeometry(10,100,500,300)
window.setWindowTitle("abc")
window.show()
# app.exec_() helps us to retain window.
sys.exit(app.exec_())


