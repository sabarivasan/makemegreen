from __future__ import print_function # Python 2/3 compatibility
import boto3
session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='green_users',
    KeySchema=[
        {
            'AttributeName': 'id_type',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'id',
            'KeyType': 'RANGE' # range key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id_type',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)