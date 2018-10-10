from __future__ import print_function # Python 2/3 compatibility
import boto3
session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='green_products',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'idx_category',
            'KeySchema': [
                {
                    'KeyType': 'HASH',
                    'AttributeName': 'category'
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
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)