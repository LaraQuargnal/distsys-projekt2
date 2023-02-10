import aiohttp
import asyncio
import random
import time
from aiohttp import web


MAX_WORKERS = 5
start_time = time.monotonic_ns()

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
        worker_ready_responses = [session.get(f"http://localhost:{port}/worker_ready") for port in worker_ports]
        worker_ready_responses = await asyncio.gather(*worker_ready_responses)
        for port, resp in zip(worker_ports, worker_ready_responses):
            if resp.status == 200:
                # If a worker is ready, add it to the list of workers, assign ID based on port number
                worker_id = f"server{port}"
                workers[worker_id] = port
        print(f"Received worker ready signals from: {list(workers.keys())}")

        # Select 3 to 5 workers randomly
        selected_worker_ids = random.sample(list(workers.keys()), random.randint(3, 5))
        print(f"Selected workers: {selected_worker_ids}")

        # Send data to selected workers
        if workers:
            task_count = {}  # Dict to keep track of the number of sent tasks for each worker
            while lines_of_data:
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for worker_id in selected_worker_ids:
                        port = workers[worker_id]
                        index = worker_ports.index(port)
                        data_to_send = lines_of_data[index * 400: index * 400 + 400]  # select 400 lines of data
                        if data_to_send:  # Check if data_to_send is not empty
                            start_time = time.monotonic_ns()  # start a timer for each task
                            task = asyncio.create_task(session.post(
                                f"http://localhost:{port}/receive_data",
                                json={"data": data_to_send, "worker_id": worker_id}))  # create task to send data
                            tasks.append(task)
                    await asyncio.gather(*tasks)
                    for port in task_count:
                        print(f"Total tasks sent to worker{port}: {task_count[port]}")
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
    # Receive the word count data from the worker
    data = await request.json()
    # Extract the worker port and word count from the received data
    worker_port = data["worker_port"]
    word_count = data["word_count"]

    # Log the current time when receiving the word count from the worker
    current_time = time.monotonic_ns()  # Timer ends here
    print(f"Received word count from {worker_port} : {word_count} words counted.")
    elapsed_time = current_time - start_time  # Calculate the elapsed time
    # print(f"Elapsed time between sending and receiving data: {elapsed_time} ns")
    print(f"Elapsed time between sending and receiving data: {elapsed_time} ns ({elapsed_time / 1000000:.2f} ms)")

    # Increment the count of completed tasks from the worker
    if worker_port in word_counts:
        word_counts[worker_port] += 1
    else:
        word_counts[worker_port] = 1

    # Print the total number of completed tasks from the worker
    print(f"Total tasks returned {worker_port}: {word_counts[worker_port]}")

    return web.Response(status=200)


app = web.Application(client_max_size=1024 * 1024 * 200)
app.add_routes(routes)
web.run_app(app, port=8081)
