import decimal

import boto3
from botocore.exceptions import ClientError

import LambdaEnviron
import json
import DynamoDB

# COLUMNS
EMAIL_ADDRESS = 'email_address'

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
        self.dynamo_client = DynamoDB.create_client()
        self.user_table = self.dynamo_client.Table(DynamoDB.USERS_TABLE)
        self.upsert_user()

    def load_from_db(self):
        try:
            response = self.user_table.get_item(Key={
                EMAIL_ADDRESS: self.email_address
            })
        except ClientError as e:
            print("Error reading user" + e.response['Error']['Message'])
            return False
        else:
            if 'Item' in response:
                self.user = response['Item']
                print("User read succeeded:")
                print(json.dumps(self.user, indent=4, cls=DecimalEncoder))
                return True
            else:
                print("No user with email address " + self.email_address)
                return False


    def upsert_user(self):
        if not self.load_from_db():
            self.user = {EMAIL_ADDRESS: self.email_address}
            self.user_table.put_item(Item=self.user)

    def persist(self):
        self.dynamo_client.put_item(Item=self.user)

    def get_user_obj(self):
        return self.user