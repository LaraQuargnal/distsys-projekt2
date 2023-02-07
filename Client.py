import aiohttp
import asyncio
import json

# Create list of 10 client IDs
client_ids = [f"client{i}" for i in range(10)]

# Read json from 'data.json' file
with open("data.json", "r") as file:
    # Read the first 20 from file
    content = [json.loads(line)['content'] for line in file.readlines()[:20]]

# Divide the content evenly among the 10 clients
num_lines = len(content)
lines_per_client = num_lines // len(client_ids)

# Create a dictionary of client IDs and the lines assigned to each
clients_data = {}
for i, client_id in enumerate(client_ids):
    start = i * lines_per_client
    end = start + lines_per_client
    clients_data[client_id] = content[start:end]

# Testing for client n.38
# print(f"client38: {clients_data['client38']}")

# For each client, count the average number of letters in python code and print
for client_id, client_content in clients_data.items():
    total_letters = sum(len(line) for line in client_content)
    average_letters = total_letters / len(client_content)
    print(f"{client_id}: Average number of letters in python code: {average_letters}")


async def send_data():
    # Send database to Master
    database = clients_data

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8081/send_data", json=database) as resp:
            print(resp.status)

asyncio.run(send_data())

