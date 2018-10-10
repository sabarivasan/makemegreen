from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('green_products')

with open("green_products.json") as json_file:
    products = json.load(json_file)
    for prod in products:

        print("Adding product:", str(prod))

        table.put_item(
           Item=prod
        )