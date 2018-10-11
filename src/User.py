import decimal
import time

import boto3
from botocore.exceptions import ClientError

import LambdaEnviron
import json
import DynamoDB
import LexUtils

# COLUMNS
COL_EMAIL_ADDRESS = 'email_address'
COL_IMPLEMENTED_OPPORTUNITIES = 'implemented_opportunities'
COL_REFUSED_OPPORTUNITIES = 'refused_opportunities'

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
        email_address = LexUtils.cleanse_email(email_address)
        self.email_address = email_address
        self.dynamo_client = DynamoDB.create_client()
        self.user_table = self.dynamo_client.Table(DynamoDB.USERS_TABLE)
        self.upsert_user()

    def load_from_db(self):
        try:
            response = self.user_table.get_item(Key={
                COL_EMAIL_ADDRESS: self.email_address
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
            self.user = {COL_EMAIL_ADDRESS: self.email_address,
                         COL_IMPLEMENTED_OPPORTUNITIES: [],
                         COL_REFUSED_OPPORTUNITIES: []}
            self.user_table.put_item(Item=self.user)

    def persist(self):
        self.dynamo_client.put_item(Item=self.user)

    def get_implemented_opportunities(self):
        return self.get_attr(COL_IMPLEMENTED_OPPORTUNITIES, [])

    def get_refused_opportunities(self):
        return self.get_attr(COL_REFUSED_OPPORTUNITIES, [])

    def get_attr(self, attr_name, default_val):
        return self.user[attr_name] if attr_name in self.user else default_val

    def add_implemented_oppty(self, oppty_id, oppty_name):
        implemented_oppty = {'id': oppty_id, 'name': oppty_name, 'from': int(time.time())}
        self.add_field_to_arr(implemented_oppty, COL_IMPLEMENTED_OPPORTUNITIES)

    def add_refused_oppty(self, oppty_id, oppty_name):
        refused_oppty = {'id': oppty_id, 'name': oppty_name, 'on': int(time.time())}
        self.add_field_to_arr(refused_oppty, COL_REFUSED_OPPORTUNITIES)

    def add_field_to_arr(self, oppty, field_name):
        response = self.user_table.update_item(Key={
                COL_EMAIL_ADDRESS: self.email_address
            },
            UpdateExpression="SET {0} = list_append({0}, :o)".format(field_name),
            ExpressionAttributeValues={
                ':o': [oppty],
            },
            ReturnValues="UPDATED_NEW")
        print("add_implemented_oppty succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))



