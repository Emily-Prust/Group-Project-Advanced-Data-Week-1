"""Extracting plant data from the API."""

import aiohttp
import asyncio

BASE_URL = 'https://sigma-labs-bot.herokuapp.com/api/plants/'


async def extract_plant_data():

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}50') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.json()
            print(html)


if __name__ == "__main__":
    asyncio.run(extract_plant_data())
