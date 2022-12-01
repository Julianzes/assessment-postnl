import os
import boto3
import json
from botocore.errorfactory import ClientError

dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")


def get_item(table_name: str, isbn: str):
    """Updates an item in a DynamoDB table.

    Args:
        table_name (str): Name of the target DynamoDB table.
        isbn (str): Isbn number
    Returns:
        Values of the isbn record.
    """
    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                "isbn": {
                    "S": isbn
                }
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"])
        }

    except ClientError as err:
        return {
            "statusCode": 500,
            "body": f"ClientError: {str(err)}"
        }


def lambda_handler(event, context):
    """
    This lambda retrieves data based on a isbn number received in the API path parameter.

    Args:
        event (dict): Lambda event
        context (LambdaContext): 
    Returns:
        status: Status of the request
    """
    table_name = os.environ["TABLE_NAME"]
    try:
        isbn = event["pathParameters"]["isbn"]
    except KeyError:
        return {
            "statusCode": 404,
            "body": f"KeyError: no path parameter received"
        }
    response = get_item(isbn=isbn, table_name=table_name)

    return response
