import json

# Create list of 100 client IDs
client_ids = [f"client{i}" for i in range(100)]

# Read json  
with open("data.json", "r") as file:
    # Read the first 1000 lines from the file
    content = [json.loads(line) for line in file.readlines()[:1000]]

# Divide the content evenly among the clients
num_lines = len(content)
lines_per_client = num_lines // len(client_ids)

# Create a dictionary of client IDs and the lines assigned to each
clients_data = {}
for i, client_id in enumerate(client_ids):
    start = i * lines_per_client
    end = start + lines_per_client
    clients_data[client_id] = content[start:end]

# Testing for client n.38
print(f"client38: {clients_data['client38']}")
 
