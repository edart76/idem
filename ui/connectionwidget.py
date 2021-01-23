
""" widget class showing state of live connection """

from idem.lib.connection import Connection, ConnectionState

from PySide2 import QtWidgets, QtCore, QtGui


class ConnectionWidget(QtWidgets.QFrame):
	""" shows state of connection object
	we use basic widget, then paint stuff within it

	to differentiate instances of the same program,
	consider also writing out the currently loaded file name
	"""

	noneColour = (0, 0, 255)
	vacantColour = (50, 50, 50)
	readyColour = (0, 255, 0)
	busyColour = (255, 0, 0)
	stateColourMap = {ConnectionState.VACANT : vacantColour,
	                  ConnectionState.READY : readyColour,
	                  ConnectionState.BUSY : busyColour}

	def __init__(self, parent=None, connectionObj=None):
		""":type parent: QtWidgets.QWidget, None
		:type connectionObj : Connection"""
		super(ConnectionWidget, self).__init__(parent)
		print("init connection widget")
		self._connection = connectionObj
		self._connection.changed.connect(self.sync)
		self.sync()

	@property
	def connection(self):
		return self._connection

	def sync(self):
		self.update()

	def contextMenuEvent(self, event):
		"""display available programs"""
		menu = QtWidgets.QMenu(parent=self)

		# check if connection is empty
		if not self.connection.targetApp:
			availableMenu = menu.addMenu("choose app")

			# add option for each available exe
			for key in self.connection.availableExes().keys():
				action = availableMenu.addAction(
					key	)
				action.triggered.connect(
					lambda : self.connection.setTargetApp(key))
			return menu.exec_(event.globalPos())

		if not self.connection.process:
			# add connection options
			textFnMap = {"create new process" :
			             self.connection.createNewProcess}
			for text, fn in textFnMap.items():
				action = menu.addAction(text)
				action.triggered.connect(
					lambda : fn()
				)
		else:
			closeAction = menu.addAction("close program")
			closeAction.triggered.connect(
				lambda : self.connection.breakConnection(
					closeProgram=True
				))

		return menu.exec_(event.globalPos())


	def paintEvent(self, event):
		""" update colour and text """
		super(ConnectionWidget, self).paintEvent(event)
		painter = QtGui.QPainter(self)


		# check for empty connection

		if not self.connection.targetApp:
			pen = QtGui.QPen(QtGui.QColor(*self.noneColour))
			pen.setStyle(QtCore.Qt.SolidLine)
			painter.setPen(pen)
			painter.drawText(self.rect(), "no connection")
			return

		# set colour
		pen = QtGui.QPen(QtGui.QColor(
			*self.stateColourMap[self.connection.state]) )
		pen.setStyle(QtCore.Qt.SolidLine)
		painter.setPen(pen)

		painter.drawText(self.rect(), self.connection.targetApp)








