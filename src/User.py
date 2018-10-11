"""
See FindGreenOpportunity for documentation on levels of personalization we provide in conversations
"""
import time

from botocore.exceptions import ClientError

import json
import DynamoDB
import LexUtils
from DynamoDB import DecimalEncoder

# ID_TYPES
ID_TYPE_SLACK = 'Slack'
ID_TYPE_PHONE = 'Phone'
ID_TYPE_EMAIL = 'Email'

# COLUMNS
COL_ID='id'
COL_ID_TYPE='id_type'   #Slack|Phone|Email
COL_IMPLEMENTED_OPPORTUNITIES = 'implemented_opportunities'
COL_REFUSED_OPPORTUNITIES = 'refused_opportunities'
COL_FROM = 'from'

class User:

    def __init__(self, id, id_type):
        if ID_TYPE_EMAIL == id_type:
            id = LexUtils.cleanse_email(id)
        self.id = id
        self.id_type = id_type
        self.dynamo_client = DynamoDB.create_client()
        self.user_table = self.dynamo_client.Table(DynamoDB.USERS_TABLE)
        self.upsert_user()

    def load_from_db(self):
        try:
            response = self.user_table.get_item(Key=self.primary_key())
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
                print("No user with (id, id_type) = ({}, {})".format(self.id, self.id_type))
                return False

    def primary_key(self):
        return {
            COL_ID: self.id,
            COL_ID_TYPE: self.id_type
        }

    def upsert_user(self):
        if not self.load_from_db():
            self.user = {COL_ID: self.id, COL_ID_TYPE: self.id_type,
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
        implemented_oppty = {'id': oppty_id, 'name': oppty_name, COL_FROM: int(time.time())}
        self.add_field_to_arr(implemented_oppty, COL_IMPLEMENTED_OPPORTUNITIES)

    def add_refused_oppty(self, oppty_id, oppty_name):
        refused_oppty = {'id': oppty_id, 'name': oppty_name, 'on': int(time.time())}
        self.add_field_to_arr(refused_oppty, COL_REFUSED_OPPORTUNITIES)

    def add_field_to_arr(self, oppty, field_name):
        response = self.user_table.update_item(Key=self.primary_key(),
            UpdateExpression="SET {0} = list_append({0}, :o)".format(field_name),
            ExpressionAttributeValues={
                ':o': [oppty],
            },
            ReturnValues="UPDATED_NEW")
        print("add_implemented_oppty succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))



# Helper class to convert a DynamoDB item to JSON.
