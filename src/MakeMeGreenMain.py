import json
import Constants as CC
import User
import sys

def close(session_attributes, fullfilled, message, responseCard):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled' if fullfilled else 'Failed',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message,
            'responseCard': response_card
        }
    }


def is_slot_present(slots, slot):
    return slot in slots


def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']

    if CC.FIND_GREEN_OPPORTUNITY == intent_name:
        if not is_slot_present(slots, CC.OPPORTUNITY_TYPE):
            return elicit_slot(CC.EMPTY_OBJ, intent_name, slots, CC.OPPORTUNITY_TYPE, None, CC.EMPTY_OBJ)
        opportunityType = slots[CC.OPPORTUNITY_TYPE]

    message = "You can reduce the {} consumption by consuming less".format(opportunityType)
    return close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)


if "__main__" == __name__:

    # FIND_GREEN_OPPORTUNITY
    event = {
        "currentIntent": {
            "name": CC.FIND_GREEN_OPPORTUNITY,
            "slots": {}
        }
    }
    print(json.dumps(lambda_handler(event, None)))

# Response
# return {
#     "sessionAttributes": {
#          "key1": "value1",
#          "key2": "value2"
#     },
#     "dialogAction": {
#         "type": "ConfirmIntent",
#         "message": {
#             "contentType": "PlainText or SSML or CustomPayload",
#             "content": "Message to convey to the user. For example, Are you sure you want a large pizza?"
#         },
#         "intentName": "intent-name",
#         "slots": {
#             "slot-name": "value",
#             "slot-name": "value",
#             "slot-name": "value"
#         }
#     }
# }
#

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
