import os
import boto3
import json
from botocore.errorfactory import ClientError

dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")


def update_item(table_name: str, payload: dict):
    """Updates an item in a DynamoDB table.

    Args:
        table_name (str): Name of the target DynamoDB table.
        payload (dict): Payload containing record information
    Returns:
        Status of the updated item.
    """
    isbn = payload.get("isbn")
    try:
        response = dynamodb_client.update_item(
            TableName=table_name,
            Key={
                "isbn": {
                    "S": isbn
                }
            },
            ExpressionAttributeValues={
                ":nm": {"S": payload.get("name")},
                ":athrs": {"S": payload.get("authors")},
                ":lnggs": {"S": payload.get("languages")},
                ":cntrs": {"S": payload.get("countries")},
                ":nrpgs": {"S": payload.get("numberOfPages")},
                ":rlsdt": {"S": payload.get("releaseDate")}
            },
            ExpressionAttributeNames={"#nm": "name"},
            UpdateExpression="set #nm = :nm, \
                authors = :athrs, \
                languages = :lnggs, \
                countries = :cntrs, \
                numberOfPages = :nrpgs, \
                releaseDate = :rlsdt"
        )
        return {
            "statusCode": 200,
            "body": f"Updating isbn {isbn} succesfull. Record:{payload} "
        }

    except ClientError as err:
        return {
            "statusCode": 500,
            "body": f"ClientError: {str(err)}"
        }


def lambda_handler(event: dict, context):
    """
    This lambda updates an item in a DynamoDB Table.

    Example payload retrieved from the event:
        {
        "payload": {
            "name": "Test BookUPDATED",
            "isbn": "123-4-56-789098-7",
            "authors": "Test, Writer",
            "languages": "English",
            "countries": "Netherlands",
            "numberOfPages": "490",
            "releaseDate": "11-11-2011"
        }
    }
    Args:
        event (dict): Lambda event
        context (LambdaContext): 
    Returns:
        status: Status of the request
    """
    table_name = os.environ["TABLE_NAME"]
    try:
        payload = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 404,
            "body": f"KeyError: no body received in this request"
        }
    status = update_item(payload=payload["payload"], table_name=table_name)

    return status
