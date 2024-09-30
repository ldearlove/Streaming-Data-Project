"""This module contains the definition
for the main() function.
"""
from src.api_interaction import api_interaction
from src.format_article import format_article
from src.send_to_kinesis import send_to_kinesis
import logging

logging.basicConfig(level=logging.INFO)


def main(query, broker_id, date_from=None):
    try:
        raw_data = api_interaction(query, date_from)

        if not raw_data or 'response' not in raw_data or not raw_data['response'].get(   # noqa
                'results'):
            raise ValueError("No articles found for the given query and date!")

        formatted_data = [format_article(
            article) for article in raw_data['response']['results'][:10]]

        send_to_kinesis(formatted_data, broker_id)

        logging.info("Articles sent to Kinesis successfully!")
    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error has occurred: {e}")
        raise
