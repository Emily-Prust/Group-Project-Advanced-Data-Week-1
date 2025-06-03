"""Extracting plant data from the API."""

import csv
import asyncio

import aiohttp

BASE_URL = 'https://sigma-labs-bot.herokuapp.com/api/plants/'
CSV_NAME = 'raw_plants.csv'


async def extract_plant_data():
    """Extract plant information by id."""

    async with aiohttp.ClientSession() as session:

        plants = []
        for i in range(51):
            async with session.get(f'{BASE_URL}{i}') as response:

                print("Status:", response.status)
                html = await response.json()

                # if response.status == 200:
                plants.append(html)

    return plants


def create_plants_csv(plants: list[dict]) -> None:
    """Create a csv from the extracted plants data."""

    fieldnames = set()
    for entry in plants:
        fieldnames.update(entry.keys())
    fieldnames = list(fieldnames)

    with open(CSV_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(plants)


if __name__ == "__main__":
    plants_data = asyncio.run(extract_plant_data())

    create_plants_csv(plants_data)
