"""This module contains the definition for api_interaction() function. """

import requests
import os
import logging
from dotenv import load_dotenv

url = 'https://content.guardianapis.com/search'

load_dotenv()

logging.basicConfig(level=logging.INFO)


def api_interaction(query, date_from=None):
    """
    Fetches articles from The Guardian API based on a search query
    and optional date filter. Includes trailText for a content
    preview of each article.

    This function interacts with The Guardian's content search API,
    sending a GET request to retrieve articles that match the given query.
    Optionally, a starting date (`date_from`) can be provided
    to filter articles published after that date.

    Args:
        query (str): The search query string to filter articles by.
        date_from (str, optional): A string representing the earliest
        publication date to filter articles, formatted as 'YYYY-MM-DD'.
        Defaults to None.

    Returns:
        dict: A JSON response containing the search results from
        The Guardian API, including metadata like article titles,
        URLs, and other relevant details.

    Raises:
        ValueError: If the API key is not found in the environment variables.
        requests.exceptions.HTTPError:
        If the HTTP request returned an unsuccessful status code.
        requests.exceptions.RequestException:
        For network-related errors during the request.
        Exception:
        For any other unexpected errors.

    Notes:
        - Ensure that the Guardian API key is stored as an
        environment variable with the name 'Guardian_API_Key'.
        You can load it via a `.env` file using `python-dotenv`.
    """
    key = os.getenv('Guardian_API_Key')
    if not key:
        raise ValueError(
            'API key is missing. Please set the "Guardian_API_Key" environment variable')  # noqa

    params = {
        'q': query,
        'api-key': key,
        'show-fields': 'trailText, body'
    }
    if date_from:
        params['from-date'] = date_from

    try:
        response = requests.get(url, params=params)
        response.raise_for_status
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP Error has occurred: {http_err}!')
        raise
    except requests.exceptions.RequestException as request_err:
        logging.error(f'Error during request: {request_err}!')
        raise
    except Exception as err:
        logging.error(f'Unexpected Error has occurred: {err}')
        raise
