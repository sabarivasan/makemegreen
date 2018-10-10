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
            'message': {
                'contentType': 'PlainText',
                'content': message
            },
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
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


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }


def is_slot_present(slots, slot):
    return slot in slots and slots[slot]


def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']

    print("input event = " + json.dumps(event))

    if CC.FIND_GREEN_OPPORTUNITY == intent_name:
        find_green_opportunity(event)

    message = "Intent {} not implemented".format(intent_name)
    return close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)


def find_green_opportunity(event):
    source = event['invocationSource']
    slots = event['currentIntent']['slots']
    opportunity_type = slots[CC.OPPORTUNITY_TYPE]
    output_session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        if not opportunity_type:
            return elicit_slot(
                output_session_attributes,
                event['currentIntent']['name'],
                event['currentIntent']['slots'],
                'OpportunityType',
                {'contentType': 'PlainText', 'content': 'Would you like to learn about paper, plastic or water '
                                                        'consumption today?'},
                build_response_card(
                    'Consumption Type', 'What type of consumption would you like to learn about?',
                    [
                        {'text': 'Paper', 'value': 'Paper'},
                        {'text': 'Plastic', 'value': 'Plastic'},
                        {'text': 'Water', 'value': 'Water'}
                    ]
                ))
    message = "You can reduce {} consumption by consuming less".format(opportunity_type)
    return close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)


if "__main__" == __name__:

    # FIND_GREEN_OPPORTUNITY
    event = {
        "currentIntent": {
            "name": CC.FIND_GREEN_OPPORTUNITY,
            "slots": {
                "opportunityType": None
            }
        }
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
