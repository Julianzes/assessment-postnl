import os
import boto3
import json
from botocore.errorfactory import ClientError

dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")


def delete_item(table_name: str, isbn: str):
    """
    Deletes an item from a DynamoDB table.

    Args:
        table_name (str): Name of the target DynamoDB table.
        isbn (str): isbn value.
    Returns:
        Status of the deleted item.
    """
    try:
        response = dynamodb_client.delete_item(
            TableName=table_name,
            Key={
                "isbn": {"S": isbn}
            },
            ExpressionAttributeValues={":isbn": {"S": isbn}},
            ConditionExpression="contains(isbn, :isbn)"
        )
        return {
            "statusCode": 200,
            "body": f"Deletion of isbn {isbn} succesfull"
        }

    except dynamodb_client.exceptions.ConditionalCheckFailedException:
        return {
            "statusCode": 404,
            "body": f"Error: isbn: {isbn} does not exist or is already deleted."
        }
    except ClientError as err:
        return {
            "statusCode": 500,
            "body": f"ClientError: {str(err)}"
        }


def lambda_handler(event, context):
    """
    This lambda deletes a record from the DynamoDB table,
    based on a isbn number received in the API path parameter.

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
    response = delete_item(isbn=isbn, table_name=table_name)

    return response
