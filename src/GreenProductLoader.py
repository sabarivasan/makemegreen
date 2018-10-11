import DynamoDB
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class GreenProductLoader:
    def __init__(self):
        self.dynamo_client = DynamoDB.create_client()


    def load_product_recommendations(self, product_category):
        product_rec_table = self.dynamo_client.Table(DynamoDB.PRODUCTS_TABLE)
        try:
            # Find products by type
            response = product_rec_table.query(
                IndexName='idx_category',
                KeyConditionExpression=Key('category').eq(product_category),
                ScanIndexForward=False
            )
            if response['Count'] > 0:
                products = response['Items']
            else:
                print("No products for type " + product_category)
                return None

            # Return names of first 5 products
            print(products)
            return map(lambda p: "Product: {}, Rating: {}".format(p['name'], p['rating']), products[:5])
        except ClientError as e:
            print("Error reading product recommendations " + e.response['Error']['Message'])
            return None

