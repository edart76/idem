
""" houdini-facing lib to set up server listener thread
copied from hdaemon, by Coen Klosters """
from __future__ import print_function


import threading
import socket
import uuid
import time

from tree import Signal

try:
	import hou, toolutils
except ImportError:
	print("idem houdini failed to import hou module")
	hou = None
	toolutils = None

from idem.lib import osutils
from idem.lib.server import IdemDCCServer


hServer = None # module-level var for server
# probably fine?


# map from idem camera keys to houdini camera param names
iToHCameraMap = {
	"aspectRatio" : "aspect",
	"focalLength" : "focal",
}
# cameraDataKeys = (
# 	"matrix", # tuple of floats
# 	"shutter", "aspectRatio", "fstop", "focalLength", "focus",
# 	"aperture"
# )




print("h client imported")


class IdemHoudiniServer(IdemDCCServer):
	""" server for receiving and sending data in houdini """


	def execute(self, data):
		""" run any commands that come in """
		#print("hserver execute {}".format(data))

	def sendDCCData(self, data):
		""" emit camera position """
		print("hserver send {}".format(data))
		self.emit(data)




# function to create camera and attach callback to it
def createCallbackCamera(name="idemCam", sendFn=None):
	""" create camera node emitting its position on change """

	camParms = (
		"shutter", "focal", ""
	)

	obj = hou.node("/obj")
	cam = obj.createNode("cam", name)

	def _emitCameraData(event_type, **kwargs):
		""" callback function on camera,
		passes camera's data to sendFn """
		#print("callbackKwargs {}".format(kwargs))
		# format all parametres
		nodeObj = kwargs["node"]
		parmData = {i.name() : i.eval() for i in nodeObj.parms()}

		cameraData = {k : parmData.get(
			iToHCameraMap.get(k, k)) for k in osutils.cameraDataKeys}

		mat = nodeObj.worldTransform().asTuple()
		cameraData["matrix"] = mat

		# emit data
		sendFn(cameraData) # works

	cam.addEventCallback(
		[hou.nodeEventType.ParmTupleChanged],
		_emitCameraData)

	return cam


def blockingFunction():
	""" test for checking which structures block the main thread """
	while True:
		print("blocking fn called")
		time.sleep(3)

# execute with command line startup
if __name__ == '__main__':
	print( "h main run" )
	# serverThread = startHPythonServer(
	# 	osutils.programData["houdini"]["threadName"])
	hData = osutils.programData["houdini"]

	serverThread = IdemHoudiniServer(
		name=hData["threadName"],
		clientIdentifier=hData["portName"],
		portNumber=hData["portNumber"]
	)


	# set up callback camera
	cam = createCallbackCamera(
		# name="idemCam",sendFn=print)
		name="idemCam",sendFn=serverThread.sendDCCData)

	serverThread.run()
	print("serverThread activated from main")
	testThread = threading.Thread(target=blockingFunction, name="testBlockThread")
	#testThread.run()
	#testThread.start()

	#serverThread.listenThread.run()

