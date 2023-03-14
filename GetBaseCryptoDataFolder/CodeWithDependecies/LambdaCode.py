import boto3
import requests
import json




def handler(event, context):
    # API call
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    data = json.loads(response.text)

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cryptoTable')

    # Save data to DynamoDB
    table.put_item(
        Item={
            'Id': data['id'],
            'userId': data['userId'],
            'title': data['title'],
            'completed': data['completed']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Data saved to DynamoDB')
    }
