# distsys-projekt2
Master - Worker architecture

constraints: asnycio, aiohttp, pandas, Python standard library

Client: 
- create list of 10 000 clients (for now only 10)
- load data.json
- take all python code (for now only 20 )
- divide the content evenly among clients
- create a dictionary of client IDs and the lines assigned to each
- for each client, count the average number of letters in python code and print
- send database to Master


Master (async):
- Receive incoming request data from client
- Extract the first 1000 lines of data (3 for now)
- Listen for workers to say HELLO!
- Select 3 to 5 workers randomly

... to do ...

- Send 1000 (3 for now) lines at a time to workers
- Receives back from workers "word count"

... to do ....



Workers:
- async
- simulate delay, random 0.1-0.3 sec
- count number of words in the received file
- simulate delay in sending the results
- send result back to Master



