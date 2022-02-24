from xmlrpc.server import SimpleXMLRPCServer
import sys
import json

# Storage of data
data_table = {}


def load_data(group):
    # TODO load data based which portion it handles (am or nz)
    file_name = "data-" + group + ".json"
    print("filename = ", file_name)
    try:
        with open(file_name) as json_file:
          data_table = json.load(json_file)
          return data_table
    except:
        print("Something went wrong when working with the file.")
        print("Check the name of the file or its content.")
        sys.exit(0)
          

def getbyname(name):
    # TODO
    print("Worker: getbyname")
    if name in data_table:
        print(data_table[name])
        return data_table[name]
    else:
        return {
            'error': False,
            'result': []
        }
 

def getbylocation(location):
    # TODO
    print("Worker: getbylocation", location, "   ", type(location))
    locList = []
    dict_value = data_table.values()
    for i in range(len(dict_value)):
        if location == (list(dict_value))[i].get("location"):
            locList.append((list(dict_value))[i])
    if len(locList) > 0:
        return locList
    else:
        return {
            'error': False,
            'result': []
        }

def getbyyear(location, year):
    # TODO
    print("Worker: getbyyear")
    locYearList = []
    elements = data_table.values()
    for index in range(len(elements)):
        if location == (list(elements))[index].get("location"):
            if year == (list(elements))[index].get("year"):
                locYearList.append((list(elements))[index])
    if len(locYearList) > 0:
        return locYearList
    else:
        return {
            'error': False,
            'result': []
        }

if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)
try:
    port = int(sys.argv[1])
except ValueError:
    print("Port value must be of a type int.")
    sys.exit(0)
    
group = sys.argv[2]
print("group: ", group)
server = SimpleXMLRPCServer(("localhost", port), allow_none = True)
print(f"WORKER: Listening on port {port}...")
data_table = load_data(group)
print(data_table)

# TODO register RPC functions

server.register_function(getbyname, "getbyname")
server.register_function(getbylocation, "getbylocation")
server.register_function(getbyyear, "getbyyear")

try:
    print('Press Ctrl+C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting...')

#server.serve_forever()
