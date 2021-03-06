import time

import DynamoDB

import GreenOpportunity
import User

DAYS_PER_WEEK = 7
SECONDS_PER_DAY = 24 * 60 * 60

class GreenPointsCalculator:
    def __init__(self, user):
        self.user = user
        self.dynamo_client = DynamoDB.create_client()


    # TODO: implement filtering for only points from start
    def calculate_points(self, start):
        implemented = self.user.get_implemented_opportunities()
        now = int(time.time())
        num_implemented = 0
        tot_points = 0
        for io in implemented:
            num_implemented += 1
            oppty = GreenOpportunity.Opportunity(io[GreenOpportunity.COL_ID])
            if io[User.COL_FROM] < start:
                num_seconds = (now - start)
            else:
                num_seconds = now - io[User.COL_FROM]
            tot_points += float(oppty.get_person_points_per_week() * num_seconds / SECONDS_PER_DAY / DAYS_PER_WEEK)

        return (num_implemented, int(tot_points))