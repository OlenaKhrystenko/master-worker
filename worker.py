from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys
import json

# Registered JSON files
files = [
    'data-am.json',
    'data-nz.json'
]

# Storage of JSON data
data_table = {}

# Counter for balancing work load
load_counter = 0        # increments on each call from master


def load_file(index):
    search_marker = index[0].lower()
    if search_marker >= 'a' and search_marker <= 'm':
        return load_data(files[0])
    elif search_marker >= 'n' and search_marker <= 'z':
        return load_data(files[1])


def load_data(file):
    try:
        with open(file) as json_file:
            data_table = json.load(json_file)
            return data_table
    except:
        print("ERROR: Failed to load JSON data file.")
        sys.exit(0)


def getbyname(name):
    global load_counter
    load_counter += 1
    # print("Worker: getbyname")  # TEST
    data_table = load_file(name)

    if name in data_table:
        return {
            'error': False,
            'load': load_counter,
            'result': data_table[name]
        }
    else:
        return {
            'error': True,
            'error_message': "Failed to search by name.",
        }


def getbylocation(location):
    global load_counter
    load_counter += 1

    # print("Worker: getbylocation", location, "   ", type(location))   # TEST
    locList = []

    # Search by location through each listed file
    for file in files:
        data_table = load_data(file)
        dict_value = data_table.values()

        for i in range(len(dict_value)):
            if location == (list(dict_value))[i].get("location"):
                locList.append((list(dict_value))[i])

    if len(locList) > 0:
        return {
            'error': False,
            'load': load_counter,
            'result': locList
        }
    else:
        return {
            'error': True,
            'error_message': "Failed to search by location.",
        }


def getbyyear(location, year):
    # print("Worker: getbyyear")    # TEST
    global load_counter
    load_counter += 1
    locYearList = []

    # Search by year through each listed file
    for file in files:
        data_table = load_data(file)

        elements = data_table.values()
        for index in range(len(elements)):
            if location == (list(elements))[index].get("location") and year == (list(elements))[index].get("year"):
                locYearList.append((list(elements))[index])

    if len(locYearList) > 0:
        return {
            'error': False,
            'load': load_counter,
            'result': locYearList
        }
    else:
        return {
            'error': True,
            'error_message': "Failed to search by year and location.",
        }


def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <master port>')
        sys.exit(0)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port value must be of a type int.")
        sys.exit(0)

    # Connect Worker to user-specified port
    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    print(f"WORKER: Listening on port {port}...")

    # Register Worker with Master
    with xmlrpc.client.ServerProxy(f'http://localhost:{sys.argv[2]}/') as register:
        if register.registerWorker(port):
            print('Registered with the master.  Ready to take on workload.')
        else:
            print("Failed to register worker with the master.")

    # Register RPC functions
    server.register_function(getbyname, "getbyname")
    server.register_function(getbylocation, "getbylocation")
    server.register_function(getbyyear, "getbyyear")

    try:
        print('\tProcess running.  Ctrl+C to exit.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')


main()
