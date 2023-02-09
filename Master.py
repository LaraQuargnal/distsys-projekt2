import aiohttp
from aiohttp import web
import random

routes = web.RouteTableDef()


@routes.post("/send_data")
async def receive_data(request):
    # Receive incoming request data from client
    data = await request.json()

    # Extract all the lines of data from Json
    lines_of_data = list(data.values())

    # List of worker ports
    worker_ports = [8083, 8084, 8085, 8086, 8087]

    # Listen for signals from the worker nodes if they are ready
    workers = {}
    async with aiohttp.ClientSession() as session:
        for port in worker_ports:
            async with session.get(f"http://localhost:{port}/worker_ready") as resp:
                if resp.status == 200:
                    # If a worker is ready, add it to the list of workers
                    worker_id = f"server{port}"
                    workers[worker_id] = port
        print(f"Received worker ready signals from: {list(workers.keys())}")

        # Select 3 to 5 workers randomly
        selected_worker_ids = random.sample(list(workers.keys()), random.randint(3, 5))
        print(f"Selected workers: {selected_worker_ids}")

        # Send data to selected workers
        if workers:
            while lines_of_data:
                async with aiohttp.ClientSession() as session:
                    for worker_id in selected_worker_ids:
                        port = workers[worker_id]
                        index = worker_ports.index(port)
                        data_to_send = lines_of_data[index * 3: index * 3 + 3]
                        if data_to_send: # Check if data_to_send is not empty
                            await session.post(f"http://localhost:{port}/receive_data", json={"data": data_to_send, "worker_id": worker_id})
                        lines_of_data = lines_of_data[3:]
        else:
            print("No workers are ready")

        # If all data has been sent, print a message
        if not lines_of_data:
            print("No more data to send")

    # Return a response to the client indicating that the data has been received
    return web.Response(text="Data received")

# Define a dictionary to store the word counts received from the worker nodes
word_counts = {}


@routes.post("/receive_worker_word_count")
async def receive_word_count(request):
    # Receive the word count data from the worker node
    data = await request.json()
    print(f"Received word count from {data['worker_port']}: {data['word_count']}")
    return web.Response(status=200)

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8081)
