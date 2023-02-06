import json
import pandas as pd
import re
import string
import asyncio
import random
from aiohttp import web

# async function to simulate delay
async def random_delay(delay: float):
    await asyncio.sleep(delay)

# async function to count the words
async def count_words(text: str) -> int:
    await asyncio.sleep(0)  # Simulate an async operation
    words = re.sub("[" + string.punctuation + "]", "", text).split()
    return len(words)

routes = web.RouteTableDef()


@routes.post("/")
async def worker(req):
    try:
        # simulate delay in receiving the file
        delay = random.uniform(0.1, 0.3)
        print(f"Waiting for {delay} seconds")
        await random_delay(delay)

        # count the number of words in the received file
        data = await req.json()
        text = data.get("data")
        word_count = await count_words(text)
        print(f"Word count: {word_count}")

        # simulate delay in sending the result
        delay = random.uniform(0.1, 0.3)
        print(f"Waiting for {delay} seconds")
        await random_delay(delay)

        # send the result back to the master
        print("Sending result")
        return web.json_response({
            "name": "worker",
            "status": "OK",
            "word_count": word_count
        }, status=200)
    except Exception as e:
        return web.json_response({
            "name": "worker",
            "error": str(e)
        }, status=500)


app = web.Application()
app.router.add_routes(routes)

web.run_app(app, port=8082)
