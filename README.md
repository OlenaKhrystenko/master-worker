# Programming Assignment #1

## Team Members

Olena Khrystenko :: ovkncp@umsystem.edu<br>
Joe Moon :: jmn5y@umsystem.edu<br>
Jack Zhang :: zz9g4@umsystem.edu<br>

## Instructions

This RPC program requires a client, a master server, and at least one worker server. In order to function, the master server must be brought online first as worker servers will register with the master server as they come online.

Inititate the servers in the following order with the following commands where ##### is a port number:

<ol>
    <li>python3 master.py [master port number] &</li>
    <li>python3 worker.py ##### [master port number] &</li>
    <li>python3 worker.py ##### [master port number] &</li>
    <li>python3 worker.py ##### [master port number] &</li>
    <li>python3 client.py [master port number]</li>
</ol>

Note: you can add as many worker servers as you'd like. <br>

### Testing Script

Alternatively, a bash script has been included that will kill any existing python3 processes and initiate the above list with three worker servers. To run the bash script, execute the following command from the program directory: <br>
<ul>
    <li>From a Linux/UNIX terminal, type: <b>./pa1</b></li>
    <li>From a Windows terminal, type: <b>bash pa1</li>
 </ul>

### ADDITIONAL FEATURE 1: Registering a Worker

Worker servers are no longer hard coded into the program and will be dynamically added. Simply use the command <b>python3 worker.py ##### [master port number] &</b> where ##### is a free port number. The second parameter MUST be the same as the master server's port number or the worker will not register.

### ADDITIONAL FEATURE 2: Load Balancing

The master server will assign a worker to execute a function based on its load factor (lower loads will go next). As such, workers are no longer assigned a JSON file to search upon creation. Instead, they are assigned a JSON file based on the input and that assignment may change with each function call.
