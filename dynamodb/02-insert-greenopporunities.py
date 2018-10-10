from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

session = boto3.session.Session(profile_name='cvent-sandbox')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('green_opportunities')

with open("green_opportunities.json") as json_file:
    opportunities = json.load(json_file)
    for op in opportunities:
        opid = int(op['id'])
        optype = op['type']
        points = int(op['person_points_per_day'])
        name = op['name']
        print("Adding opportunities:", opid, name,optype,points)

        table.put_item(
           Item={
               'id': opid,
              'person_points_per_day': points,
               'type': optype,
               'name': name
            }
        )