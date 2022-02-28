from re import A
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys

# DIAGNOSTIC FEATURE (True = on / False = off)
# Displays data on selected worker and load
show_details = True

# Available Workers
# Key:Value => #####: xmlrpc.client.ServerProxy("http://localhost:#####/")
# ##### = port number of registered worker
workers = {}

# Tracking for balancing load among workers
# Key:Value => port_number : load
load_tracker = {}


# Diagnostic method displaying various states of the program
def details(active_worker):
    print(f'\t****************** DETAILS ***********************')
    print(f'\t* Worker on port {active_worker} selected for task')
    print(
        f'\t* Load Count for Worker on port {active_worker}: {load_tracker[active_worker]}')
    print(f'\t* LOAD TRACKER => {load_tracker}')
    print(f'\t**************************************************')


# Adds a worker to a list of available workers able to receive tasks
def registerWorker(worker_port):
    try:
        int(worker_port)    # integer check, otherwise raise exception
        if worker_port in workers:
            return False    # Port number already in use
        else:
            workers.update(
                {worker_port: xmlrpc.client.ServerProxy(f"http://localhost:{worker_port}")})
            load_tracker.update({worker_port: 0})
            print(f'\tRegistering worker on port {worker_port} with MASTER...')
            return True
    except ValueError:
        print(f'Failed to recognize {worker_port} as a valid port number')


# Removes a worker upon a lost connection
def removeWorker(worker_port):
    print(f"{worker_port} failed to connect.")
    removed_worker = workers.pop(worker_port)
    load_tracker.pop(worker_port)
    print(f'Removed {removed_worker} from workers list.')


def getbyname(name):
    nameList = []       # array of returned results

    # Send query to Worker and record reply
    try:
        active_worker = lowestLoad()
        s = workers.get(active_worker)
        result = s.getbyname(name)
        nameList.append(result.get('result'))

        # Update tracker data
        load_tracker[active_worker] = result['load']

        if show_details:
            details(active_worker)

        return {
            'error': False,
            'result': nameList
        }
    except TypeError:
        return {
            'error': True,
            'error_message': f'ERROR: Incorrect argument: {name}.  Must be a string.'
        }
    except ConnectionRefusedError:
        removeWorker(active_worker)
        return getbyname(name)


def getbylocation(location):
    locationList = []   # array of returned results

    try:
        if len(location) > 0:
            active_worker = lowestLoad()

            s = workers.get(active_worker)
            result = s.getbylocation(location)
            locationList.append(result.get('result'))

            # Update tracker data
            load_tracker[active_worker] = result['load']

            if show_details:
                details(active_worker)

            return {
                'error': False,
                'result': locationList
            }
    except TypeError:
        return {
            'error': True,
            'error_message': 'The argument must be of a type string.'
        }
    except ConnectionRefusedError:
        removeWorker(active_worker)
        return getbylocation(location)


def getbyyear(location, year):
    lyList = []
    try:
        if len(location) > 0:
            active_worker = lowestLoad()

            s = workers.get(active_worker)
            result = s.getbyyear(location, year)
            lyList.append(result.get('result'))

        # Update tracker data
        load_tracker[active_worker] = result['load']

        if show_details:
            details(active_worker)

        return {
            'error': False,
            'result': lyList
        }
    except TypeError:
        return {
            'error': True,
            'error_message': 'The arguments must be a string and int respectively.'
        }
    except ConnectionRefusedError:
        removeWorker(active_worker)
        return getbyyear(location, year)


# Searches the 'workers' dictionary for the worker with the lowest load
def lowestLoad():
    return min(load_tracker, key=load_tracker.get)


def main():
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port value must be of a type int.")
        sys.exit(0)

    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    print(f"MASTER: Listening on port {port}...")

    server.register_function(registerWorker, "registerWorker")
    server.register_function(getbyname, "getbyname")
    server.register_function(getbylocation, "getbylocation")
    server.register_function(getbyyear, "getbyyear")

    try:
        print('\tProcess running.  Ctrl+C to exit.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')


main()
