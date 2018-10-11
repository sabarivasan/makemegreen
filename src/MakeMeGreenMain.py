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
    "userId": "w6oya0njyqxijub0gnf0xi3w5o1yiyv1",
    "sessionAttributes": {
        "CurrentOpptyId": "8",
        "opportunityType": "water",
        "State": "AwaitingOpportunityConfirmation",
        "userIdType": "Phone",
        "CurrentOpptyName": "garden",
        "anonymous": "false",
        "userId": "5555555555"
    },
    "requestAttributes": None,
    "bot": {
        "name": "MakeMeGreen",
        "alias": "$LATEST",
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "FindGreenOpportunity",
        "slots": {
            "opportunityType": "water",
            "phone": None,
            "yesNoGreenOpportunity": "yes",
            "emailOrPhone": None,
            "yesNoIdentifyingInfoWillingness": "yes"
        },
        "slotDetails": {
            "opportunityType": {
                "resolutions": [
                    {
                        "value": "water"
                    }
                ],
                "originalValue": "water"
            },
            "phone": {
                "resolutions": [],
                "originalValue": None
            },
            "yesNoGreenOpportunity": {
                "resolutions": [
                    {
                        "value": "Yes"
                    }
                ],
                "originalValue": "yes"
            },
            "emailOrPhone": {
                "resolutions": [],
                "originalValue": None
            },
            "yesNoIdentifyingInfoWillingness": {
                "resolutions": [
                    {
                        "value": "Yes"
                    }
                ],
                "originalValue": "yes"
            }
        },
        "confirmationStatus": "None"
    },
    "inputTranscript": "yes"
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
