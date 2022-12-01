import os
import boto3
import json
from botocore.errorfactory import ClientError

dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")


def put_item(table_name: str, payload: dict):
    """_summary_

    Args:
        table_name (str): Name of the target DynamoDB table.
        payload (dict): Payload containing record information

    Returns:
      Status of the added item.
    """
    isbn = payload.get("isbn")
    try:
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item={
                "isbn": {"S": isbn},
                "name": {"S": payload.get("name")},
                "authors": {"S": payload.get("authors")},
                "languages": {"S": payload.get("languages")},
                "countries": {"S": payload.get("countries")},
                "numberOfPages": {"S": payload.get("numberOfPages")},
                "releaseDate": {"S": payload.get("releaseDate")}
            },
            ConditionExpression="attribute_not_exists(isbn)"
        )
    except dynamodb_client.exceptions.ConditionalCheckFailedException:
        return {
            "statusCode": 409,
            "body": f"Could not create record. Record with isbn: {isbn} already exists"
        }

    except ClientError as err:
        return {
            "statusCode": 500,
            "body": f"ClientError: {str(err)}"
        }
    return response


def lambda_handler(event, context):
    """
    This lambda adds one or more items to a DynamoDB Table.

    Example payload retrieved from the event:
    {
        "payload": [
            {
                "name": "Test Book1",
                "isbn": "111-1-11-111111-1",
                "authors": "Test, Writer",
                "languages": "Dutch",
                "countries": "Netherlands",
                "numberOfPages": "460",
                "releaseDate": "11-11-2011"
            },
            {
                "name": "Test Book2",
                "isbn": "123-4-56-789098-7",
                "authors": "Test, Writer",
                "languages": "Dutch",
                "countries": "Netherlands",
                "numberOfPages": "490",
                "releaseDate": "11-11-2011"
            }
        ]
    }
    Args:
        event (dict): Lambda event
        context (LambdaContext)
    Returns:
        status: Status of the request
    """
    table_name = os.environ["TABLE_NAME"]
    try:
        body = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 404,
            "body": f"KeyError: no body received in this request"
        }

    for payload in body["payload"]:
        status = put_item(table_name=table_name, payload=payload)

    if "ResponseMetadata" in status:
        return {
            "statusCode": 201,
            "body": json.dumps(body["payload"])
        }
    return status
