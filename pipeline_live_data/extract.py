"""Extracting plant data from the API."""

import csv
import asyncio
from datetime import datetime, timezone

import aiohttp

BASE_URL = 'https://sigma-labs-bot.herokuapp.com/api/plants/'
CSV_NAME = 'raw_plants.csv'


async def extract_plant_data() -> list[dict]:
    """Extract all plant data."""

    async with aiohttp.ClientSession() as session:  # Running all the time

        plants = [extract_single_plant_data(i, session) for i in range(51)]

        plant_data = await asyncio.gather(*plants)

    print("Finished all plants")
    return plant_data


async def extract_single_plant_data(plant_id: int, session: aiohttp.ClientSession) -> dict:
    """Extracts plant data for a given id. """

    print(f"Started plant {plant_id}.")
    response = await session.get(f'{BASE_URL}{plant_id}')

    html = await response.json()

    if response.status != 200:
        html['received_at'] = datetime.now(
            timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    print("Status:", response.status)
    print(f"Finished plant {plant_id}.")

    return html


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
