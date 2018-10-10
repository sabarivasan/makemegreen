"""
This is the single central place to get environmental vars for lambda

"""

import os

# List of env vars
AWS_REGION = "AWS_REGION"

"""
Returns the lambda environment value for a name, defaulting to None
"""


def get_aws_region():
    return get_required_env(AWS_REGION)


def get_optional_env(name, default=None):
    return os.environ.get(name, default)

def get_required_env(name):
    v = os.environ.get(name)
    if not v:
        raise NameError("undefined env var {}".format(name))
    return v

