"""Extracting plant data from the API."""

import os
import csv
import asyncio
import logging
from datetime import datetime, timezone

import aiohttp


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG", 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


BASE_URL = 'https://sigma-labs-bot.herokuapp.com/api/plants/'
CSV_NAME = 'raw_plants.csv'
FIELD_NAMES = ['plant_id', 'name', 'error', 'temperature', 'soil_moisture', 'last_watered',
               'recording_taken', 'received_at', 'scientific_name', 'botanist',
               'origin_location', 'images']


async def extract_plant_data(plant_id_start: int = 1,
                             plant_id_end: int = 50,
                             ) -> list[dict]:
    """Extract all plant data."""

    # Current plant IDs range from 1 to 50, this may need to be updated in the future.

    async with aiohttp.ClientSession() as session:  # Running all the time.

        plants = [extract_single_plant_data(
            i, session) for i in range(plant_id_start, plant_id_end+1)]
        plant_data = await asyncio.gather(*plants)

    logger.info(
        f"Completed API calls for plants with plant_id in the range {plant_id_start} - {plant_id_end}."
        )

    return plant_data


async def extract_single_plant_data(plant_id: int, session: aiohttp.ClientSession) -> dict:
    """Extracts plant data for a given id. """

    logger.debug(
        f"Started function extract_single_plant() for plant_id {plant_id}."
        )

    response = await session.get(f'{BASE_URL}{plant_id}')

    html = await response.json()

    if response.status != 200:
        html['received_at'] = datetime.now(
            timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    logger.info(f"Made API call for plant_id: {plant_id}. Status code: {response.status}.")

    if not html["plant_id"]:
        logger.warning(
            f"Received unexpected result. Request to {BASE_URL}{plant_id} missing plant_id key.")

    logger.debug(
        f"Finished function extract_single_plant() for plant_id {plant_id}."
    )

    return html


def create_plants_csv(plants: list[dict]) -> None:
    """Create a csv from the extracted plants data."""

    with open(CSV_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)

        if not os.path.exists(CSV_NAME) or os.path.getsize(CSV_NAME) == 0:
            writer.writeheader()

        writer.writerows(plants)


if __name__ == "__main__":

    plants_data = asyncio.run(extract_plant_data())
    create_plants_csv(plants_data)
