"""Load script."""
# pylint: disable=unused-argument

from os import environ as ENV
import logging
import boto3
from dotenv import load_dotenv

from transform import create_csv

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def handler(event=None, context=None):
    """Uploads the csv to the bucket."""

    info = create_csv()
    logging.info("CSV created.")

    s3_client = boto3.client(
        's3', aws_access_key_id=ENV["AWS_ACCESS_KEY"], aws_secret_access_key=ENV["AWS_SECRET_KEY"])

    s3_client.upload_file(
        info["file_name"], ENV["BUCKET_NAME"], info["bucket_key"])
    logging.info("CSV successfully uploaded to bucket %s, at path: %s. ",
                 ENV["BUCKET_NAME"], info["bucket_key"])


if __name__ == "__main__":

    load_dotenv()
