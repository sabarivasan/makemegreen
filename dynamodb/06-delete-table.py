from __future__ import print_function # Python 2/3 compatibility
import boto3
import sys

session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table_name = str(sys.argv[1])

if table_name.startswith('green'):
	print("The table to be deleted ", table_name)
	table = dynamodb.Table(table_name)
	table.delete()
	print('delete')
else:
	print("Only delete tables start with green")
