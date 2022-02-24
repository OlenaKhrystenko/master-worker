import datetime
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys

w1 = "abcdefghijklm"
w2 = "nopqrstuvwxyz"

workers = {
    'worker-1': xmlrpc.client.ServerProxy("http://localhost:23001/"),
    'worker-2': xmlrpc.client.ServerProxy("http://localhost:23002/")
}


def getbyname(name):
    # TODO
    nameList = []
    print("MASTER: name", name)
    try:
      if name[0] in w1:
        s = workers['worker-1']
        nameList.append(s.getbyname(name))
        return {
          'error':True,
          'result': nameList
        }
      elif name[0] in w2:
        s = workers['worker-2']
        nameList.append(s.getbyname(name))
        return {
          'error':True,
          'result': nameList
        }
      else:
        return {
          'error': False,
          'result': []
        }
    except TypeError:
      print(f"Incorrect argument: {name}. Must be string.")


def getbylocation(location):
    # TODO
    print("MASTER: location", location)
    locationList = []
    try:
      if len(location) > 0:
        s1 = workers['worker-1']
        locationList.append(s1.getbylocation(location))
        s2 = workers['worker-2']
        locationList.append(s2.getbylocation(location))
        return {
          'error': True,
          'result': locationList
        }
      else:
        return {
          'error': False,
          'result': []
        }
    except TypeError:
      print(f"The argument must be of a type string.")


def getbyyear(location, year):
    # TODO
    print("MASTER: year")
    lyList = []
    try:
      if len(location) > 0:
        s1 = workers['worker-1']
        lyList.append(s1.getbyyear(location, year))
        s2 = workers['worker-2']
        lyList.append(s2.getbyyear(location, year))
        return {
          'error': True,
          'result': lyList
        }
      else:
        return {
            'error': False,
            'result': []
        }
    except TypeError:
      print(f"Check types of the arguments.")
      print(f"They must be string and int respectively.")

try:
  port = int(sys.argv[1])
except ValueError:
  print("Port value must be of a type int.")
  sys.exit(0)

server = SimpleXMLRPCServer(("localhost", port), allow_none = True)
print(f" MASTER: Listening on port {port}...")

server.register_function(getbyname, "getbyname")
server.register_function(getbylocation, "getbylocation")
server.register_function(getbyyear, "getbyyear")

#server.serve_forever()
try:
    print('Press Ctrl+C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting...')
