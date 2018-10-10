"""
This is the single central place to get environmental vars for lambda

"""

import os

# List of env vars
DYNAMO_DB_ENDPOINT = "DYNAMO_DB_ENDPOINT"
AWS_REGION = "AWS_REGION"

"""
Returns the lambda environment value for a name, defaulting to None
"""

def get_dynamo_db_endpoint():
    return get_required_env(DYNAMO_DB_ENDPOINT)

def get_aws_region():
    return get_required_env(AWS_REGION)


def get_optional_env(self, name, default=None):
    return os.environ.get(name, default)

def get_required_env(self, name):
    v = os.environ.get(name)
    if not v:
        raise NameError("undefined env var {}".format(name))

