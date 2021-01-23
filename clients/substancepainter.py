
""" for the hell of it,
example code needed for formatting commands as json
"""


import base64
import json
import sys
if sys.version_info >= (3, 0):
    import http.client as http
else:
    import httplib as http

###############################################################################################
# Const data
###############################################################################################

# Json server connection
_PAINTER_ROUTE = '/run.json'
_HEADERS = {'Content-type': 'text/plain', 'Accept': 'application/json'}


###############################################################################################
# Exceptions
###############################################################################################

# Generic exception on the Painter class
class PainterError(Exception):
    def __init__(self, message):
        super(PainterError, self).__init__(message)


class ExecuteScriptError(PainterError):
    def __init__(self, data):
        super(PainterError, self).__init__('An error occured when executing script: {0}'.format(data))


###############################################################################################
# Remote Substance Painter control
###############################################################################################

class Painter:
    def __init__(self, port=60041, host='localhost'):
        self._host = host
        self._port = port

    # Execute a HTTP POST request to the Substance Painter server and send/receive JSON data
    def _jsonPostRequest(self, route, body):
        connection = http.HTTPConnection(self._host, self._port, timeout=3600)
        connection.request('POST', route, body, _HEADERS)
        response = connection.getresponse()

        data = json.loads(response.read().decode('utf-8'))
        connection.close()

        if 'error' in data:
            raise ExecuteScriptError(data['error'])
        return data

    def checkConnection(self):
        connection = http.HTTPConnection(self._host, self._port)
        connection.connect()

    # Execute a JavaScript script
    def execScript(self, script):
        main = base64.b64encode(script.encode('utf-8'))
        return self._jsonPostRequest(_PAINTER_ROUTE, ('{"js":"' + main.decode('utf-8') + '"}').encode('utf-8'))