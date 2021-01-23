
import uuid, atexit

from tree import Signal
from PySide2 import QtWidgets, QtCore

from idem.ui.window import IdemWindow
from idem.lib import osutils
from idem.lib.connection import Connection, ConnectionState

class IdemSession(object):
	""" core 'model' for running an idem session
	Idem is largely a functional program (in contrast to Tesserae) -
	only connect and fire different processes, do not store any state
	"""

	def __init__(self, *args, **kwargs):
		self.mainWindow = None

		self.connections = {}
		self.connectionsChanged = Signal()
		self.update = Signal()
		self.update.connect(self.connectionsChanged)
		self.qObj = QtCore.QObject()

		# common shared data from processes
		self.sharedData = {}

		# bridge files and directories to watch for updates
		# could make this a map of
		# {file : every callback that depends on it?}
		self._bridgeFilePaths = []

		# watch them
		# test to make file paths update live
		self.watcher = QtCore.QFileSystemWatcher(
			parent=self.qObj)
		# actually this is probably extremely unsafe

		# map of fileName : pid? or process object?
		self.processes = {}
		# timer to poll them so we know if a program is shut down
		self.timer = QtCore.QTimer(parent=self.qObj)
		self.timer.setTimerType(QtCore.Qt.VeryCoarseTimer)

		# separate high-frequency timer to do nothing but query sockets



	@property
	def bridgeFilePaths(self):
		"""return files currently being watched """
		return self._bridgeFilePaths

	def addConnection(self, targetApp=None):
		""" creates and adds new connection to targetApp"""
		uid = uuid.uuid4()
		con = Connection(targetApp, uid)
		self.connections[uid] = con
		self.timer.timeout.connect(con.sync)

		self.connectionsChanged()


	def buildUI(self):
		print("build UI")
		#window = IdemWindow(parent=None, session=self)
		window = QtWidgets.QMainWindow()
		widget = IdemWindow(parent=window, session=self)
		window.setCentralWidget(widget)
		self.mainWindow = window

	def onClose(self):
		""" called when ui is closed down - shut down all
		connected processes """
		for name, con in self.connections.items():
			con.breakConnection()


	@staticmethod
	def newSession(*args, **kwargs):
		""" initialises new session with new window """
		s = IdemSession(*args, **kwargs)
		s.buildUI()
		s.addConnection(None)
		s.timer.start(5000)

		# register close function for exit
		# not sure if there is a cleaner way
		atexit.register(s.onClose)


		# show the main window
		s.mainWindow.show()
		s.update()








