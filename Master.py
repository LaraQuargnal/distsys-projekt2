import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/send_data")
async def receive_data(request):
    # Receive incoming request data from client
    data = await request.json()

    # Print the data
    print(data)

    # Extract the first 3 lines of data
    data_to_send = list(data.values())[:3]

    #    return web.Response(status=200)

    # Listen for workers (server 3, server 4, server 5)
    workers = []
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8083/worker_ready") as resp:
            if resp.status == 200:
                workers.append("server3")
        async with session.get("http://localhost:8084/worker_ready") as resp:
            if resp.status == 200:
                workers.append("server4")
        # async with session.get("http://localhost:8085/worker_ready") as resp:
        #     if resp.status == 200:
        #         workers.append("server5")

    print(f"Received worker ready signals from: {workers}")
    # return web.Response(text="Data received")

    if "server3" in workers:
        # Send the first 3 lines to server 3
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8083/receive_data", json=data_to_send) as resp:
                if resp.status == 200:
                    print("Sent data to server 3")

    # Extract the next 3 lines of data
    data_to_send = list(data.values())[3:6]

    if "server4" in workers:
        # Send the next 3 lines to server 4
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8084/receive_data", json=data_to_send) as resp:
                if resp.status == 200:
                    print("Sent data to server 4")

    return web.Response(text="Data received")

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8081)
