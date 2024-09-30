"""This module contains test suite for
the main() function only.
"""

import pytest
from unittest.mock import patch, MagicMock  # noqa
from src.main import main

mock_data = {
    'response': {
        'status': 'ok',
        'results': [
            {
                'id': 'article-1',
                'webTitle': 'Test Article 1',
                'webUrl': 'https://www.theguardian.com/article-1'
            },
            {
                'id': 'article-2',
                'webTitle': 'Test Article 2',
                'webUrl': 'https://www.theguardian.com/article-2'
            }
        ]
    }
}


def test_main_success(mocker):
    """
    Test that the main() function successfully processes
    articles and sends them to Kinesis when all steps
    work correctly.
    Each assert is done to ensure each part of the main()
    function is called successfully.
    """
    mock_interaction = mocker.patch(
        'src.main.api_interaction',
        return_value=mock_data)
    mock_format = mocker.patch(
        'src.main.format_article',
        side_effect=lambda article: article)
    mock_send = mocker.patch('src.main.send_to_kinesis')

    main('test', 'test-kinesis-stream', '2024-01-01')

    mock_interaction.assert_called_once_with('test', '2024-01-01')

    assert mock_format.call_count == 2

    mock_send.assert_called_once_with(
        mock_data['response']['results'],
        'test-kinesis-stream')


def test_main_no_articles_found(mocker):
    """
    Test that the main() function raises a
    ValueError when no articles are found.
    """
    empty_data = {'response': {'status': 'ok', 'results': []}}
    mocker.patch('src.main.api_interaction', return_value=empty_data)
    mocker.patch('src.main.send_to_kinesis')

    with pytest.raises(ValueError, match="No articles found for the given query and date!"):  # noqa
        main('test', 'test-kinesis-stream', '2024-01-01')


def test_main_api_exception(mocker):
    """
    Test that the main() function raises an Exception
    if api_interaction() throws an error.
    """
    mocker.patch('src.main.api_interaction',
                 side_effect=Exception("API interaction failed"))

    with pytest.raises(Exception, match="API interaction failed"):
        main('test', 'test-kinesis-stream')


def test_main_format_exception(mocker):
    """
    Test that the main() function raises an Exception
    if format_article() throws an error.
    """
    mocker.patch('src.main.api_interaction', return_value=mock_data)
    mocker.patch('src.main.format_article',
                 side_effect=Exception('Error with formatting'))

    with pytest.raises(Exception, match='Error with formatting'):
        main('test', 'test-kinesis-stream')


def test_main_kinesis_exception(mocker):
    """
    Test that the main() function raises an Exception
    if send_to_kinesis() throws an error.
    """
    mocker.patch('src.main.api_interaction', return_value=mock_data)
    mocker.patch(
        'src.main.format_article',
        side_effect=lambda article: article)
    mocker.patch('src.main.send_to_kinesis',
                 side_effect=Exception('Error with sending to Kinesis'))

    with pytest.raises(Exception, match='Error with sending to Kinesis'):
        main('test', 'test-kinesis-stream')
