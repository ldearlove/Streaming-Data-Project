"""This module contains the definition for the
send_to_kinesis() function."""

import logging
import boto3
import json
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(level=logging.INFO)


def send_to_kinesis(data, broker_id):
    """
        Sends a list of articles to an Amazon Kinesis stream
        as a single record.

    This function takes a list of dictionaries representing
    articles and sends the entire list as a single record
    to the specified Kinesis stream.
    The list of articles is serialized into JSON format
    and sent with a partition key of 'article_data'.

    Args:
        data (list): A list of dictionaries, where each dictionary contains
        the following keys:
            - 'webPublicationDate' (str): The publication date of the article.
            - 'webTitle' (str): The title of the article.
            - 'webUrl' (str): The URL of the article.
        broker_id (str): The name of the Kinesis stream to which the records
        will be sent.
    Raises:
        BotoCoreError: If there is an issue with the Kinesis client
        (e.g., AWS credentials or connection issues).
        ClientError: If Kinesis returns an error related to the stream
        or request parameters.
        JSONDecodeError: If there is an error in encoding the article
        data into JSON format.
    """
    if not data:
        logging.info("No data send to Kinesis")
        return

    kinesis = boto3.client('kinesis')

    try:

        serialized_data = json.dumps(data)

        kinesis.put_record(
            StreamName=broker_id,
            Data=serialized_data,
            PartitionKey='guardian_content'
        )
        logging.info("Data successfully sent to Kinesis!")
    except (BotoCoreError, ClientError) as boto_err:
        logging.error(f"Error sending data to Kinesis: {boto_err}")
        raise
    except json.JSONDecodeError as json_err:
        logging.error(f"Error with JSON encoding: {json_err}")
        raise
