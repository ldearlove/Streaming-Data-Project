"""This module contains the test suite for
for the format_article() function only.
"""

import pytest
from unittest.mock import Mock  # noqa
from src.format_article import format_article


def test_format_article_valid():
    """
    Test that the format_article function
    correctly formats a valid article with fields.
    """
    mock_data = {
        "id": "info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes",  # noqa
        "type": "article",
        "sectionId": "info",
        "sectionName": "Info",
        "webPublicationDate": "2023-11-21T11:11:31Z",
        "webTitle": "Who said what: using machine learning to correctly attribute quotes",  # noqa
        "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes",  # noqa
        "fields": {
            "trailText": "This is a preview of the article content.",
            "body": "<p>This is the full content of the article.</p>"
        }
    }

    expected = {
        "webPublicationDate": "2023-11-21T11:11:31Z",
        "webTitle": "Who said what: using machine learning to correctly attribute quotes",  # noqa
        "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes",  # noqa
        "content_preview": "<p>This is the full content of the article.</p>"
    }

    result = format_article(mock_data)
    assert result == expected


def test_format_article_type_error():
    """
    Test that format_article raises
    a TypeError when the input is not a dictionary.
    """
    article = ["Not", "a", "dict"]

    with pytest.raises(TypeError, match="Expected a dictionary representing an article."):  # noqa
        format_article(article)


def test_format_article_missing_fields():
    """
    Test that the format_article function handles missing fields
    in the article dictionary and returns reasonable defaults.
    """
    mock_data = {
        "id": "info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes",  # noqa
        "type": "article",
        "sectionId": "info",
        "sectionName": "Info",
        "webTitle": "Who said what: using machine learning to correctly attribute quotes",  # noqa
        "apiUrl": "https://content.guardianapis.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes",  # noqa
        "isHosted": False,
        "pillarId": "pillar/news",
        "pillarName": "News"
    }

    expected = {
        "webPublicationDate": None,
        "webTitle": "Who said what: using machine learning to correctly attribute quotes",  # noqa
        "webUrl": None,
        "content_preview": "Who said what: using machine learning to correctly attribute quotes"  # noqa
    }

    result = format_article(mock_data)
    assert result == expected


def test_format_article_empty_dict():
    """
    Test that the format_article function returns
    None for all fields and an empty content preview when
    the article is an empty dictionary.
    """
    article = {}

    expected_output = {
        "webPublicationDate": None,
        "webTitle": None,
        "webUrl": None,
        "content_preview": ""
    }

    result = format_article(article)
    assert result == expected_output
