# Programming Assignment #1

## Team Members

Olena Khrystenko :: ovkncp@umsystem.edu<br>
Joe Moon :: jmn5y@umsystem.edu<br>
Jack Zhang :: zz9g4@umsystem.edu<br>

## Instructions

This RPC program requires a client, a master server, and at least one worker server. In order to function, <b><u>the master server must be brought online first</u></b> as worker servers will register with the master server when they come online.

Inititate the servers in the following order with the following commands:

<ol>
    <li>python3 master.py [master port] &</li>
    <li>python3 worker.py [worker-1 port] [master port] &</li>
    <li>python3 worker.py [worker-2 port] [master port] &</li>
    <li>python3 worker.py [worker-3 port] [master port] &</li>
    <li>python3 client.py [master port]</li>
</ol>

Note: you can add as many worker servers as you'd like. <br>

### Testing Script

Alternatively, a bash script has been included that will kill any existing python3 processes and initiate the above list with three worker servers. To run the bash script, execute the following command from the program directory: <br>

<ul>
    <li>From a Linux/UNIX terminal, type: <b>./pa1</b></li>
    <li>From a Windows terminal, type: <b>bash pa1</li>
 </ul>

### Failure Handling

The program has been coded to handle failures of registered workers (see <i>Additional Feature 1</i>). If a connection cannot be established to a particular worker, it is deregistered from the master's worker list and the task is forwarded to the next available worker with the lowest load.<br>
This can be tested by running the Testing Script and then manually killing a worker process.

### ADDITIONAL FEATURE 1: Registering a Worker

Worker servers are no longer hard coded into the program and will be dynamically added. Simply use the command <b>python3 worker.py ##### [master port number] &</b> where ##### is a free port number. The second parameter MUST be the same as the master server's port number or the worker will not register.

### ADDITIONAL FEATURE 2: Load Balancing

The master server will assign a worker to execute a function based on its load factor (lower loads will go next). As such, workers are no longer assigned a JSON file to search upon creation. Instead, they are assigned a JSON file based on the input and that assignment may change with each function call.

### ADDITIONAL FEATURE 3: Rerouting Failed Workers

When a worker fails after registering with the master, the connection error resulting from a function call will be captured and initiate the "removeWorker" functio that will remove that worker from the master's worker list (that worker's load data will be removed as well).<br>
If that worker comes back online, it will be reregistered with a load count of zero.<br>
A worker failure was simulated by killing that process.
