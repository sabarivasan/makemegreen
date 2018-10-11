import json

import Constants as CC
import FindGreenOpportunity
import GetPoints
import GetProductRecommendation


def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']

    print("input event = " + json.dumps(event))

    if CC.INTENT_FIND_GREEN_OPPORTUNITY == intent_name:
        return FindGreenOpportunity.handle(event, context)
    if CC.INTENT_GET_POINTS == intent_name:
        return GetPoints.handle(event, context)
    if CC.INTENT_GET_PRODUCT_RECOMMENDATION == intent_name:
        return GetProductRecommendation.handle(event, context)



if "__main__" == __name__:

    # FIND_GREEN_OPPORTUNITY
    event = {
        "outputDialogMode": "Text",
        "userId": "72njs51uuv71jj9hggb9mvzvwpzn21ng",
        "currentIntent": {
            "name": CC.INTENT_FIND_GREEN_OPPORTUNITY,
            "slots": {
                "opportunityType": "water",
                "emailAddress": "sabari2@cvent.com"
            }
        },
        "sessionAttributes": {}
    }
    
    
    event = {
    "messageVersion": "1.0",
    "invocationSource": "DialogCodeHook",
    "userId": "ea4b1552-45f0-4fe1-ab45-b3a9b0e46485:TDAGGP9DH:UDAE42BA4",
    "sessionAttributes": {},
    "requestAttributes": {
        "x-amz-lex:channel-id": "ea4b1552-45f0-4fe1-ab45-b3a9b0e46485",
        "x-amz-lex:webhook-endpoint-url": "https://channels.lex.us-east-1.amazonaws.com/slack/webhook/ea4b1552-45f0-4fe1-ab45-b3a9b0e46485",
        "x-amz-lex:accept-content-types": "PlainText",
        "x-amz-lex:user-id": "452560791459.454526013046",
        "x-amz-lex:slack-team-id": "TDAGGP9DH",
        "x-amz-lex:slack-bot-token": "xoxb-452560791459-453003707012-7AZT1oG1DlRqmIhaPIlR2L8Y",
        "x-amz-lex:channel-name": "BotSlackIntegration",
        "x-amz-lex:channel-type": "Slack"
    },
    "bot": {
        "name": "MakeMeGreen",
        "alias": "verA",
        "version": "9"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "FindGreenOpportunity",
        "slots": {
            "opportunityType": "plastic",
            "phone": None,
            "yesNoGreenOpportunity": None,
            "emailOrPhone": None,
            "yesNoIdentifyingInfoWillingness": None
        },
        "slotDetails": {
            "opportunityType": {
                "resolutions": [
                    {
                        "value": "plastic"
                    }
                ],
                "originalValue": "plastic"
            },
            "phone": {
                "resolutions": [],
                "originalValue": None
            },
            "yesNoGreenOpportunity": {
                "resolutions": [],
                "originalValue": None
            },
            "emailOrPhone": {
                "resolutions": [],
                "originalValue": None
            },
            "yesNoIdentifyingInfoWillingness": {
                "resolutions": [],
                "originalValue": None
            }
        },
        "confirmationStatus": "None"
    },
    "inputTranscript": "plastic"
}
 
    print(json.dumps(lambda_handler(event, None)))

# Response
#   "dialogAction": {
#     "type": "ElicitSlot",
#     "message": {
#       "contentType": "PlainText or SSML or CustomPayload",
#       "content": "Message to convey to the user. For example, What size pizza would you like?"
#     },
#    "intentName": "intent-name",
#    "slots": {
#       "slot-name": "value",
#       "slot-name": "value",
#       "slot-name": "value"
#    },
#    "slotToElicit" : "slot-name"
#   }#

# Input
# {
#   "currentIntent": {
#     "name": "intent-name",
#     "slots": {
#       "slot name": "value",
#       "slot name": "value"
#     },
#     "slotDetails": {
#       "slot name": {
#         "resolutions" : [
#           { "value": "resolved value" },
#           { "value": "resolved value" }
#         ],
#         "originalValue": "original text"
#       },
#       "slot name": {
#         "resolutions" : [
#           { "value": "resolved value" },
#           { "value": "resolved value" }
#         ],
#         "originalValue": "original text"
#       }
#     },
#     "confirmationStatus": "None, Confirmed, or Denied (intent confirmation, if configured)"
#   },
#   "bot": {
#     "name": "bot name",
#     "alias": "bot alias",
#     "version": "bot version"
#   },
#   "userId": "User ID specified in the POST request to Amazon Lex.",
#   "inputTranscript": "Text used to process the request",
#   "invocationSource": "FulfillmentCodeHook or DialogCodeHook",
#   "outputDialogMode": "Text or Voice, based on ContentType request header in runtime API request",
#   "messageVersion": "1.0",
#   "sessionAttributes": {
#      "key": "value",
#      "key": "value"
#   },
#   "requestAttributes": {
#      "key": "value",
#      "key": "value"
#   }
# }
