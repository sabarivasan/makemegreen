import boto3
import LambdaEnviron

USERS_TABLE = "green_users"
OPPORTUNITIES_TABLE = "green_opportunities"
PRODUCTS_TABLE = "green_products"
OPPORTUNITY_TYPES_TABLE = "green_opp_types"


def get_endpoint_url(aws_region):
    return "https://dynamodb.{}.amazonaws.com".format(aws_region)


def create_client():
    region = LambdaEnviron.get_aws_region()
    return boto3.resource('dynamodb', region_name=region, endpoint_url=get_endpoint_url(region))
