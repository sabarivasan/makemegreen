import DynamoDB
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class GreenOpportunityLoader:
    def __init__(self, opportunityType, user):
        self.opportunityType = opportunityType.lower()
        self.user = user
        self.dynamo_client = DynamoDB.create_client()


    # Takes a user and opportunity type and returns the next opportunity type the user has not implemented
    # with the max number of green points
    def load_next_opportunity_for_user(self):
        green_opty = self.dynamo_client.Table(DynamoDB.OPPORTUNITIES_TABLE)
        try:
            # 1) find all the green opportunities available
            response = green_opty.query(
                IndexName='idx_type',
                KeyConditionExpression=Key('type').eq(self.opportunityType),
                ScanIndexForward=False
            )
            if response['Count'] > 0:
                available_opportunities = response['Items']
            else:
                print("No green opportunities found for type " + self.opportunityType)
                return None
            available_opportunities.sort(key=lambda o: o['person_points_per_day'], reverse=True)

            # 2) Filter opportunities refused by the user in the past
            refused_ids = list(map(lambda o: str(o['id']), self.user.get_refused_opportunities()))
            available_opportunities = list(filter(lambda ao: str(ao['id']) not in refused_ids, available_opportunities))

            # 3) Find which opportunities the user has already implemented
            for ao in available_opportunities:
                implemented = False
                for io in self.user.get_implemented_opportunities():
                    if str(io['id']) == str(ao['id']):
                        implemented = True
                        break
                if not implemented:
                    return ao
            return None

        except ClientError as e:
            print("Error reading green opportunities " + e.response['Error']['Message'])
            return None




