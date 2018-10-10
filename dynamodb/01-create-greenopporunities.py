from __future__ import print_function # Python 2/3 compatibility
import boto3
session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='green_opportunities',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'KeyType': 'RANGE',
            'AttributeName': 'person_points_per_day'
        }
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'idx_type',
            'KeySchema': [
                {
                    'KeyType': 'HASH',
                    'AttributeName': 'type'
                },
                {
                    'KeyType': 'RANGE',
                    'AttributeName': 'person_points_per_day'
                }
            ],
            # Note: since we are projecting all the attributes of the table
            # into the LSI, we could have set ProjectionType=ALL and
            # skipped specifying the NonKeyAttributes
            'Projection': {
                'ProjectionType': 'ALL',
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'type',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'person_points_per_day',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)