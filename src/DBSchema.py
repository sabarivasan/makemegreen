
USERS_TABLE = "green_users"
OPPORTUNITIES_TABLE = "green_opportunities"
PRODUCTS_TABLE = "green_products"


def get_endpoint_url(aws_region):
    return "https://dynamodb.{}.amazonaws.com".format(aws_region)