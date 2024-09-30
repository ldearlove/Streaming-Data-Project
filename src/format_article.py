"""This module contains the definition for the for_article() function."""

import logging

logging.basicConfig(level=logging.INFO)


def format_article(article):
    """
    Formats a Guardian article into a standardized JSON format.

    This function takes a dictionary representing a Guardian article
    and returns a new dictionary with specific fields formatted for output.
    It ensures that the input is a dictionary and retrieves the fields:
    'webPublicationDate', 'webTitle', 'webUrl', and generates a
    'content_preview'.

    Args:
        article (dict): A dictionary containing article data with
        the following keys:
            - 'webPublicationDate' (str): The publication date of the article.
            - 'webTitle' (str): The title of the article.
            - 'webUrl' (str): The URL of the article.
            - 'fields' (dict): Contains additional fields like
            'trailText' or 'body'.

    Returns:
        dict: A dictionary with the following keys:
            - 'webPublicationDate' (str): The publication date of the article.
            - 'webTitle' (str): The title of the article.
            - 'webUrl' (str): The URL of the article.
            - 'content_preview' (str): The first 1000 characters
            of the article content.

    Raises:
        TypeError: If the input is not a dictionary.
        Exception: If an unexpected error occurs.
    """
    try:
        if not isinstance(article, dict):
            raise TypeError("Expected a dictionary representing an article!")

        content = article.get('fields', {}).get('body', '')

        content_preview = content[:1000] if content else article.get('webTitle', '')[:1000]  # noqa

        return {
            "webPublicationDate": article.get("webPublicationDate"),
            "webTitle": article.get("webTitle"),
            "webUrl": article.get("webUrl"),
            "content_preview": content_preview
        }

    except Exception as err:
        logging.error(f'Unexpected Error has occurred: {err}')
        raise
