
# import tkinter as tk
#
# root= tk.Tk()
#
# canvas1 = tk.Canvas(root, width = 300, height = 300)
# canvas1.pack()
#
# button1 = tk.Button (root, text='Exit Application', command=root.destroy)
# canvas1.create_window(150, 150, window=button1)
#
# root.mainloop()



import sys

from PySide2 import QtWidgets, QtCore

from tree import Tree
# from idem.ui.window import IdemWindow
from idem.session import IdemSession

app = QtWidgets.QApplication(sys.argv)
session = IdemSession.newSession(sys.argv)
sys.exit(app.exec_())

#
# if __name__ == "__main__":
#
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = QtWidgets.QMainWindow()
# 	s = window.show()
# 	sys.exit(app.exec_())
