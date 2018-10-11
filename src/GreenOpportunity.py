import DynamoDB
from botocore.exceptions import ClientError
from DynamoDB import DecimalEncoder
import json
from boto3.dynamodb.conditions import Key

# COLUMNS
COL_ID='id'
COL_PERSON_POINTS_PER_WEEK = 'person_points_per_week'

class Opportunity:

    def __init__(self, id):
        self.id = id
        self.dynamo_client = DynamoDB.create_client()
        self.table = self.dynamo_client.Table(DynamoDB.OPPORTUNITIES_TABLE)
        self.oppty = None
        self.load_from_db()

    def load_from_db(self):
        try:
            # response = self.table.get_item(Key=self.primary_key())

            response = self.table.query(
                KeyConditionExpression=Key(COL_ID).eq(int(self.id))
            )
        except ClientError as e:
            print("Error reading opportunity " + e.response['Error']['Message'])
            return False
        else:
            if 'Items' in response:
                self.oppty = response['Items'][0]
                print("Opportunity read succeeded:")
                print(json.dumps(self.oppty, indent=4, cls=DecimalEncoder))
                return True
            else:
                print("No opportunity with id = {}".format(self.id))
                return False

    def primary_key(self):
        return {
            COL_ID: int(self.id)
        }

    def get_person_points_per_week(self):
        return int(self.get_attr(COL_PERSON_POINTS_PER_WEEK, 0))


    def get_attr(self, attr_name, default_val):
        return self.oppty[attr_name] if attr_name in self.oppty else default_val

