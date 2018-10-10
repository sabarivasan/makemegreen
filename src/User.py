import decimal

import boto3
from botocore.exceptions import ClientError

import LambdaEnviron
import DBSchema
import json

# COLUMNS
EMAIL_ADDRESS = 'email_address'

region = LambdaEnviron.get_aws_region()
dynamodb = boto3.client('dynamodb', region_name=region, endpoint_url=DBSchema.get_endpoint_url(region))

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class User:

    def __init__(self, email_address):
        self.email_address = email_address
        self.user_table = dynamodb.Table(DBSchema.USERS_TABLE)
        self.user = None


    def load_from_db(self):
        try:
            response = self.user_table.get_item(Key={
                EMAIL_ADDRESS: self.email_address
            })
        except ClientError as e:
            print("Error reading user" + e.response['Error']['Message'])
            self.user = None
        else:
            self.user = response['Item']
            print("User read succeeded:")
            print(json.dumps(self.user, indent=4, cls=DecimalEncoder))
        return self.user

    def upsert_user(self):
        if not self.load_from_db():
            dynamodb.put_item(Item={
                EMAIL_ADDRESS: self.email_address
            })
