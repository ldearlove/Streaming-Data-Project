"""This module contains the test suite
for the api_interaction() function only."""

import pytest
import requests
from src.api_interaction import api_interaction
from dotenv import load_dotenv

load_dotenv()

mock_data = {
    'response': {
        'status': 'ok',
        'results': [
            {
                'id': 'article-1',
                'webTitle': 'Test Article 1',
                'webUrl': 'https://www.theguardian.com/article-1',
                'fields': {
                    'trailText': 'This is a brief preview of article 1.',
                    'body': '<p>This is the full content of article 1...</p>'
                }
            },
            {
                'id': 'article-2',
                'webTitle': 'Test Article 2',
                'webUrl': 'https://www.theguardian.com/article-2',
                'fields': {
                    'trailText': 'This is a brief preview of article 2.',
                    'body': '<p>This is the full content of article 2...</p>'
                }
            }
        ]
    }
}


def test_api_interaction_success(mocker):
    """
    Test that the api_interaction function successfully fetches articles when
    the API call returns a 200 status.
    """
    mocker.patch('os.getenv', return_value='test-api-key')
    mock_get = mocker.patch('requests.get')

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_data

    result = api_interaction('machine learning')

    mock_get.assert_called_once_with(
        'https://content.guardianapis.com/search',
        params={
            'q': 'machine learning',
            'api-key': 'test-api-key',
            'show-fields': 'trailText, body'
        }
    )

    assert result == mock_data


def test_api_interaction_success_with_date(mocker):
    """
    Test that the api_interaction function correctly handles the date filter.
    """
    mocker.patch('os.getenv', return_value='test-api-key')
    mock_get = mocker.patch('requests.get')

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_data

    result = api_interaction('machine learning', date_from='2023-01-01')

    mock_get.assert_called_once_with(
        'https://content.guardianapis.com/search',
        params={
            'q': 'machine learning',
            'api-key': 'test-api-key',
            'show-fields': 'trailText, body',
            'from-date': '2023-01-01'
        }
    )

    assert result == mock_data


def test_missing_api_key(mocker):
    """
    Test that the api_interaction function returns a ValueError when the
    API key is missing.
    """
    mocker.patch('os.getenv', return_value=None)

    with pytest.raises(ValueError, match='API key is missing. Please set the "Guardian_API_Key" environment variable'):  # noqa
        api_interaction('machine learning')


def test_api_interaction_http_error(mocker):
    """
    Test that the api_interaction function raises an HTTPError when
    the API call results in an HTTP error.
    """
    mocker.patch('os.getenv', return_value='test-api-key')
    mock_get = mocker.patch('requests.get')

    mock_get.side_effect = requests.exceptions.HTTPError(
        "404 Client Error: Not Found for url")

    with pytest.raises(requests.exceptions.HTTPError, match="404 Client Error"):  # noqa
        api_interaction('machine learning')


def test_api_interaction_request_exception(mocker):
    """
    Test that the api_interaction function raises a RequestException when
    a network-related error or timeout occurs.
    """
    mocker.patch('os.getenv', return_value='test-api-key')
    mock_get = mocker.patch('requests.get')

    mock_get.side_effect = requests.exceptions.RequestException(
        "A network-related error occurred")

    with pytest.raises(requests.exceptions.RequestException, match="A network-related error occurred"):  # noqa
        api_interaction('machine learning')


def test_api_interaction_generic_exception(mocker):
    """
    Test that the api_interaction function raises a generic Exception when
    an unexpected error occurs.
    """
    mocker.patch('os.getenv', return_value='test-api-key')
    mock_get = mocker.patch('requests.get')

    mock_get.side_effect = Exception("Unexpected error")

    with pytest.raises(Exception, match="Unexpected error"):
        api_interaction('machine learning')
