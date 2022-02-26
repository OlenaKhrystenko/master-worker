import xmlrpc.client
import datetime
import sys

try:
    master_port = int(sys.argv[1])
except ValueError:
    print("Port value must be of a type int.")
    sys.exit(0)

proxy = xmlrpc.client.ServerProxy(f"http://localhost:{master_port}/")

try:
    name = 'xander'
    print(f'Client => Asking for person with {name}')
    result = proxy.getbyname(name)
    print(result)
    print('------------------------------------------------------')

    location = 'Kansas City'
    print(f'Client => Asking for person lived at {location}')
    result = proxy.getbylocation(location)
    print(result)
    print('------------------------------------------------------')

    location = 'New York City'
    year = 2002
    print(f'Client => Asking for person lived in {location} in {year}')
    result = proxy.getbyyear(location, year)
    print(result)
    print('------------------------------------------------------')

    name = 'fannie'
    print(f'Client => Asking for person with {name}')
    result = proxy.getbyname(name)
    print(result)
    print('------------------------------------------------------')

    location = 'Newport Beach'
    print(f'Client => Asking for person lived at {location}')
    result = proxy.getbylocation(location)
    print(result)
    print('------------------------------------------------------')

    location = 'Saint Louis'
    year = 2012
    print(f'Client => Asking for person lived in {location} in {year}')
    result = proxy.getbyyear(location, year)
    print(result)
    print('------------------------------------------------------')
except ConnectionRefusedError:
    print("Connection failed. Check the value of the port.")
