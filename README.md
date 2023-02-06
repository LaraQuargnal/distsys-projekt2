# distsys-projekt2
Master - Worker architecture
constraints: asnycio, pandas, Python standard library

Client: 
- create list of 10 000 clients (for now only 100)
- load data.json
- read all lines (for now only 1000 lines)
- divide the content evenly among clients
- dict {clientID : content}
...

...

Workers:
- async
- simulate delay, random 0.1-0.3 sec
- count number of words in the received file
- simulate delay in sending the results
- send result back to Master



