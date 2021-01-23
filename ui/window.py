


from PySide2 import QtWidgets
from ..lib import osutils
from .connectionwidget import ConnectionWidget
from tree import Signal

#class IdemWindow(QtWidgets.QMainWindow):
class IdemWindow(QtWidgets.QWidget):
	""" super basic for testing functions """

	def __init__(self, parent=None, session=None):
		""":type parent : QtWidgets.QWidget, None
		:type session : idem.session.IdemSession"""
		super(IdemWindow, self).__init__(parent)
		self.session = session

		self.connectionLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.connectionLayout)

		self.sync = Signal()
		self.session.update.connect(self.sync)

		self.sync.connect(self.onSync)



		# houdiniButton = QtWidgets.QPushButton("houdini", self)
		# houdiniButton.clicked.connect(osutils.createHoudiniSession)
		# self.setCentralWidget(houdiniButton)

	def onSync(self):
		""" for each existing connection,
		create and add a connection widget """
		while self.layout().takeAt(0):
			print("taking widget")
			continue

		for uid, connection in self.session.connections.items():
			widget = ConnectionWidget(parent=self,
			                          connectionObj=connection)
			self.layout().addWidget(widget)


