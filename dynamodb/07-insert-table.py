from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table_name = str(sys.argv[1])

if table_name.startswith('green'):
	table = dynamodb.Table(table_name)
	file_name = '{}.json'.format(table_name)
	with open(file_name) as json_file:
	    items = json.load(json_file)
	    for item in items:

	        print("Adding item:", str(item))

	        table.put_item(
	           Item=item
	        )
else:
	print("Only insert tables start with green")

