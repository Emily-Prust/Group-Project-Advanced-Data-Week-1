"""Load script."""

from os import environ as ENV
import boto3
from dotenv import load_dotenv

from transform import get_file_data

if __name__ == "__main__":

    load_dotenv()

    info = get_file_data()

    s3_client = boto3.client(
        's3', aws_access_key_id=ENV["AWS_ACCESS_KEY"], aws_secret_access_key=ENV["AWS_SECRET_KEY"])
    s3_client.upload_file(
        info["file_name"], ENV["BUCKET_NAME"], info["bucket_key"])
