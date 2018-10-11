import DynamoDB
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


# COLUMNS
COL_ID = 'id'
COL_TAGS = 'tags'
COL_PERSON_POINTS_PER_WEEK = 'person_points_per_week'


class GreenOpportunityFinder:
    def __init__(self, oppty_type, user, oppty_tag):
        self.oppty_type = oppty_type.lower()
        self.user = user
        self.oppty_tag = oppty_tag
        self.dynamo_client = DynamoDB.create_client()


    # Takes a user and opportunity type and returns the next opportunity type the user has not implemented
    # with the max number of green points
    def find_opportunity(self):
        green_oppty = self.dynamo_client.Table(DynamoDB.OPPORTUNITIES_TABLE)
        try:
            # 1) find all the green opportunities available
            response = green_oppty.query(
                IndexName='idx_type',
                KeyConditionExpression=Key('type').eq(self.oppty_type),
                ScanIndexForward=False
            )
            if response['Count'] > 0:
                available_opportunities = response['Items']
            else:
                print("No green opportunities found for type " + self.oppty_type)
                return None

            # Filter by opportunity tag (if present)
            if self.oppty_tag:
                available_opportunities = list(filter(lambda ao: self.oppty_tag in ao[COL_TAGS], available_opportunities))

            # TODO: Randomize green opportunities so they don't keep getting the same opportunities
            available_opportunities.sort(key=lambda o: o[COL_PERSON_POINTS_PER_WEEK], reverse=True)

            if self.user is not None:
                # 2) Filter opportunities refused by the user in the past
                refused_ids = list(map(lambda o: str(o['id']), self.user.get_refused_opportunities()))
                available_opportunities = list(filter(lambda ao: str(ao[COL_ID]) not in refused_ids, available_opportunities))

                # 3) Find which opportunities the user has already implemented

                for ao in available_opportunities:
                    implemented = False
                    for io in self.user.get_implemented_opportunities():
                        if str(io[COL_ID]) == str(ao[COL_ID]):
                            implemented = True
                            break
                    if not implemented:
                        return ao
                return None
            else:
                return available_opportunities[0]

        except ClientError as e:
            print("Error reading green opportunities " + e.response['Error']['Message'])
            return None




