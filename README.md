# distsys-projekt2
Master - Worker architecture
[pokretanje svakog servisa u zasebnom terminalu: worker(run workers on separate terminals specifying different ports) -> master -> client]

constraints: asnycio, aiohttp, pandas, Python standard library

Client: 
- create list of 10 000 clients (1000)
- load data.json
- take all python code (10.000 )
- divide the content evenly among clients
- create a dictionary of client IDs and the lines assigned to each
- for each client, count the average number of letters in python code and print
- send database to Master


Master (async):
- Receive incoming request data from client
- Listen for workers if they are ready
- If a worker is ready, add it to the list of workers, assign ID based on port number
- Select 3 to 5 workers randomly
- send data to selected worker
- start a timer for each task
- Send 1000 (400) lines at a time to workers
- Receives back from workers "word count"
- calculate the elapsed time between sent and received data from worker
- print total number of completed task from each worker


5 Workers:
- async
- simulate delay, random 0.1-0.3 sec
- count number of words in the received file from master
- simulate delay in sending the results
- send result back to Master



