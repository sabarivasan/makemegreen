import json

import Constants as CC
import FindGreenOpportunity
import GetPoints
import GetProductRecommendation


def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']

    print("input event = " + json.dumps(event))

    if CC.FIND_GREEN_OPPORTUNITY == intent_name:
        return FindGreenOpportunity.handle(event, context)
    if CC.GET_POINTS == intent_name:
        return GetPoints.handle(event, context)
    if CC.GET_PRODUCT_RECOMMENDATION == intent_name:
        return GetProductRecommendation.handle(event, context)



if "__main__" == __name__:

    # FIND_GREEN_OPPORTUNITY
    event = {
        "currentIntent": {
            "name": CC.FIND_GREEN_OPPORTUNITY,
            "slots": {
                "opportunityType": "water",
                "emailAddress": "sabari2@cvent.com"
            }
        },
        "sessionAttributes": {}
    }

#     event = {
#     "messageVersion": "1.0",
#     "invocationSource": "DialogCodeHook",
#     "userId": "72njs51uuv71jj9hggb9mvzvwpzn21ng",
#     "sessionAttributes": {
#         "CurrentOpptyId": "8",
#         "opportunityType": "Water",
#         "emailAddress": "abc@def.com",
#         "State": "AwaitingOpportunityConfirmation",
#         "UserId": "abc@def.com"
#     },
#     "bot": {
#         "name": "MakeMeGreen",
#         "alias": "$LATEST",
#         "version": "$LATEST"
#     },
#     "outputDialogMode": "Text",
#     "currentIntent": {
#         "name": "FindGreenOpportunity",
#         "slots": {
#             "opportunityType": "Water",
#             "yesNo": "no",
#             "emailAddress": "abc@def.com",
#             "phoneNumber": None,
#             "opportunityTask": None,
#             "lookupType": None
#         },
#         "confirmationStatus": "None"
#     },
#     "inputTranscript": "yes"
# }

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
