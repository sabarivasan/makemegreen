import DynamoDB
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class GreenOpportunityLoader:
    def __init__(self, opportunityType, user):
        self.opportunityType = opportunityType
        self.user = user
        self.dynamo_client = DynamoDB.create_client()


    def load_next_opportunity_for_user(self):
        user_obj = self.user.get_user_obj()
        green_opty = self.dynamo_client.Table(DynamoDB.OPPORTUNITIES_TABLE)
        try:
            # Firstly, find all the green opportunities available
            response = green_opty.query(
                KeyConditionExpression=Key('type').eq(self.opportunityType)
            )
            if response['Count'] > 0:
                available_opportunities = response['items']
            else:
                print("No green opportunities for type " + self.opportunityType)
                return None

            # Secondly, find which opportunities the user has already implemented
            # TODO
            return available_opportunities[0]['Name']
        except ClientError as e:
            print("Error reading green opportunities " + e.response['Error']['Message'])
            return None




