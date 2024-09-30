"""This module contains the test suite for
for the send_to_kinesis() function only.
"""

import pytest
from src.send_to_kinesis import send_to_kinesis
from unittest.mock import patch
from botocore.exceptions import BotoCoreError, ClientError
import json


data = [{"webPublicationDate": "2023-11-21T11:11:31Z",
         "webTitle": "Who said what: using machine learning to correctly attribute quotes",  # noqa
         "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes"},  # noqa
        {"webPublicationDate": "2023-11-22T12:30:00Z",
         "webTitle": "AI advancements in speech recognition",
         "webUrl": "https://www.theguardian.com/info/2023/nov/22/ai-advancements-in-speech-recognition"}]  # noqa

broker_id = "test_broker_id"


@patch('boto3.client')
def test_send_to_kinesis_success(mock_boto_client):
    """
    Test that the send_to_kinesis function successfully
    sends all articles as a single record to the Kinesis stream.
    """
    mock_kinesis = mock_boto_client.return_value
    mock_kinesis.put_record.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200}}

    send_to_kinesis(data, broker_id)
    mock_kinesis.put_record.assert_called_once()
    mock_kinesis.put_record.assert_called_with(
        StreamName=broker_id,
        Data=json.dumps(data),
        PartitionKey='guardian_content'
    )


@patch('boto3.client')
def test_send_to_kinesis_empty_data(mock_boto_client):
    """
    Test that the send_to_kinesis function handles
    an empty data list without calling put_record.
    """
    result = send_to_kinesis([], broker_id)
    assert mock_boto_client.return_value.put_record.call_count == 0
    assert result is None


@patch('boto3.client')
def test_send_to_kinesis_client_error(mock_boto_client):
    """
    Test that the send_to_kinesis function raises a ClientError
    when there is an issue with the Kinesis client.
    """
    mock_kinesis = mock_boto_client.return_value
    mock_kinesis.put_record.side_effect = ClientError(
        {"Error": {"Code": "500", "Message": "Internal Server Error"}}, "put_record"  # noqa
    )

    with pytest.raises(ClientError):
        send_to_kinesis(data, broker_id)


@patch('boto3.client')
def test_send_to_kinesis_botocore_error(mock_boto_client):
    """
    Test that the send_to_kinesis function raises a BotoCoreError
    when the boto3 client encounters a core error.
    """
    mock_kinesis = mock_boto_client.return_value
    mock_kinesis.put_record.side_effect = BotoCoreError()

    with pytest.raises(BotoCoreError):
        send_to_kinesis(data, broker_id)


@patch('boto3.client')
def test_send_to_kinesis_json_error(mock_boto_client):
    """
    Test that the send_to_kinesis function raises a TypeError
    when it encounters a non-serializable JSON object.
    """
    malformed_data = [{"webTitle": set()}]

    with pytest.raises(TypeError):
        send_to_kinesis(malformed_data, broker_id)
