import json

import Constants as CC
import FindGreenOpportunity
import GetPoints
import GetProductRecommendation
import AlexaUtils
import GreenChallenge
import GreenProfile


def lambda_handler(event, context):
    # Check if Alexa request
    if 'request' in event:
        is_alexa = True
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event, context)
        elif event['request']['type'] == "SessionEndedRequest":
            return #on_session_ended(event, context)
        elif event['request']['type'] == "IntentRequest":
            intent = event['request']['intent']
    else:
        is_alexa = False
        intent = event['currentIntent']

    intent_name = intent['name']
    print("input event = " + json.dumps(event))

    if CC.INTENT_FIND_GREEN_OPPORTUNITY == intent_name:
        return FindGreenOpportunity.handle_alexa(event, context) if is_alexa else FindGreenOpportunity.handle_lex(event, context)
    if CC.INTENT_GET_POINTS == intent_name:
        return GetPoints.handle_alexa(event, context) if is_alexa else GetPoints.handle_lex(event, context)
    if CC.INTENT_GET_PRODUCT_RECOMMENDATION == intent_name:
        return GetProductRecommendation.handle_alexa(event, context) if is_alexa else GetProductRecommendation.handle_lex(event, context)
    if CC.INTENT_GET_POSSIBLE_ACTIONS == intent_name and is_alexa:
        output = "You can ask for a way to reduce your environmental footprint, ask for a green product " \
                 "recommendation, start a green challenge, or ask for your green profile. "
        return AlexaUtils.build_response(event['session'].get('attributes', {}),
                                         AlexaUtils.build_speechlet_response("Help", output, None, False))
    if CC.INTENT_GREEN_CHALLENGE == intent_name:
        return GreenChallenge.handle_alexa(event, context) if is_alexa else GreenChallenge.handle_lex(event, context)
    if CC.INTENT_GREEN_PROFILE == intent_name:
        return GreenProfile.handle_alexa(event, context) if is_alexa else GreenProfile.handle_lex(event, context)
    else:
        raise ValueError("Invalid intent")


def on_launch(event, context):
    # Called when the user launches the skill without specifying what they want

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Make Me Green. Try asking how you can reduce your envionmental footprint" \
                    "or say help to hear about all available actions"
    reprompt_text = "Try asking how you can reduce your envionmental footprint" \
                    "or say help to hear about all available actions"
    should_end_session = False
    return AlexaUtils.build_response(session_attributes, AlexaUtils.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


if "__main__" == __name__:
    # FIND_GREEN_OPPORTUNITY
    event = {
        "outputDialogMode": "Text",
        "userId": "72njs51uuv71jj9hggb9mvzvwpzn21ng",
        "currentIntent": {
            "name": CC.INTENT_FIND_GREEN_OPPORTUNITY,
            "slots": {
                "opportunityType": "water",
                "emailAddress": "sabari2@cvent.com",
                "homeOrWork": "work"
            }
        },
        "sessionAttributes": {}
    }

    event = {
    "messageVersion": "1.0",
    "invocationSource": "DialogCodeHook",
    "userId": "f7tcrbfwiqt4muhzfrg8w8cz2dhj73wp",
    "sessionAttributes": {
        "State": "AwaitingIdentifyingInfo"
    },
    "requestAttributes": None,
    "bot": {
        "name": "MakeMeGreen",
        "alias": "$LATEST",
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "GreenProfile",
        "slots": {
            "phone": None,
            "emailOrPhone": None,
            "start": None
        },
        "slotDetails": {
            "phone": {
                "resolutions": [],
                "originalValue": None
            },
            "emailOrPhone": {
                "resolutions": [],
                "originalValue": None
            },
            "start": {
                "resolutions": [],
                "originalValue": None
            }
        },
        "confirmationStatus": "None"
    },
    "inputTranscript": "sabari@g.com"
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
