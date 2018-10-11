import json

import Constants as CC
import FindGreenOpportunity
import GetPoints
import GetProductRecommendation
import AlexaUtils


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
                "emailAddress": "sabari2@cvent.com"
            }
        },
        "sessionAttributes": {}
    }

    event = {
        "version": "1.0",
        "session": {
            "new": None,
            "sessionId": "amzn1.echo-api.session.74f33d53-8b8e-4b2b-baf5-0414193c7a63",
            "application": {
                "applicationId": "amzn1.ask.skill.9f48eb3d-c3c2-436e-a679-87cf9d7bf18b"
            },
            "attributes": {
                "opportunityType": "plastic",
                "State": "AwaitingIdentifyingInfo"
            },
            "user": {
                "userId": "amzn1.ask.account.AHO7HTGN5XEXJPQBDP2FSUV45VXO33AI4PH3B6WR2FV33BMXQYDED5NXWFAG7IUOLHBVOL6XR2WCRHCDDYRWBDWBI7QC6B6VRDQ67ILAJRHA2AMHQ2A24GQ34VMKUIWQMQWKYBM4GYVMTONEC7NBKAGLSI4CPJOPPLLOYDIBIMBKZMTKIM5XYEA4UEDJNXFGVM4OBUUXUOWDEYI"
            }
        },
        "context": {
            "System": {
                "application": {
                    "applicationId": "amzn1.ask.skill.9f48eb3d-c3c2-436e-a679-87cf9d7bf18b"
                },
                "user": {
                    "userId": "amzn1.ask.account.AHO7HTGN5XEXJPQBDP2FSUV45VXO33AI4PH3B6WR2FV33BMXQYDED5NXWFAG7IUOLHBVOL6XR2WCRHCDDYRWBDWBI7QC6B6VRDQ67ILAJRHA2AMHQ2A24GQ34VMKUIWQMQWKYBM4GYVMTONEC7NBKAGLSI4CPJOPPLLOYDIBIMBKZMTKIM5XYEA4UEDJNXFGVM4OBUUXUOWDEYI"
                },
                "device": {
                    "deviceId": "amzn1.ask.device.AFFEYY7SICZP6WZYOKUAPUO5IOZOXLCD47SJY3DJIEPDVF6VTWAYJ5PWXMPKQHU5UEQ7SC3J7LQGHXIGTRZVWUQCOQVBPPOT5O7BXTO6KMXKTR3WCSZCVGPL7BVP3H73FFY7E2GH2HAMVD3ITYQNLPRHWWXRI7NUD5UP5RNEHLXLMI5SALDLQ",
                    "supportedInterfaces": {}
                },
                "apiEndpoint": "https://api.amazonalexa.com",
                "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjlmNDhlYjNkLWMzYzItNDM2ZS1hNjc5LTg3Y2Y5ZDdiZjE4YiIsImV4cCI6MTUzOTI3MDc5MCwiaWF0IjoxNTM5MjY3MTkwLCJuYmYiOjE1MzkyNjcxOTAsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUZGRVlZN1NJQ1pQNldaWU9LVUFQVU81SU9aT1hMQ0Q0N1NKWTNESklFUERWRjZWVFdBWUo1UFdYTVBLUUhVNVVFUTdTQzNKN0xRR0hYSUdUUlpWV1VRQ09RVkJQUE9UNU83QlhUTzZLTVhLVFIzV0NTWkNWR1BMN0JWUDNINzNGRlk3RTJHSDJIQU1WRDNJVFlRTkxQUkhXV1hSSTdOVUQ1VVA1Uk5FSExYTE1JNVNBTERMUSIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFITzdIVEdONVhFWEpQUUJEUDJGU1VWNDVWWE8zM0FJNFBIM0I2V1IyRlYzM0JNWFFZREVENU5YV0ZBRzdJVU9MSEJWT0w2WFIyV0NSSENERFlSV0JEV0JJN1FDNkI2VlJEUTY3SUxBSlJIQTJBTUhRMkEyNEdRMzRWTUtVSVdRTVFXS1lCTTRHWVZNVE9ORUM3TkJLQUdMU0k0Q1BKT1BQTExPWURJQklNQktaTVRLSU01WFlFQTRVRURKTlhGR1ZNNE9CVVVYVU9XREVZSSJ9fQ.U6HpfhdWrNaXdhZfctHKRstWHSn4ZpW3UXha7jcSBHkA_gvrGxrIa2__VKtrnGtTrM9_2uzFQAc_Sw8_di9nfxwlzcy9_0QCDDRw25laSN4Axj-jNgf_N9sZM8FUtYlG6LK-3q3v2vcD0vKwty4I5xhuWpILldTgkBvhmvR9c6CTsimqYmsRfNtCrTwtwCPluyOnkMXBf5KmDOrOrROvL8J3ackG7fiMUCxHCEGrMHvoGcI0Tkn0yCyuLltMc58Gc_pfWK0VCtStj8PuXJ_A4jqVwO5ybtWzV5r8MRsBBP8-CTm_mh2FQUT6fJJHDYjWUNDpO8KhFlBZe_XpwRc4Aw"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.f17816f4-8342-4544-afbe-47209aa5411f",
            "timestamp": "2018-10-11T14:13:10Z",
            "locale": "en-US",
            "intent": {
                "name": "FindGreenOpportunity",
                "confirmationStatus": "NONE",
                "slots": {
                    "opportunityType": {
                        "name": "opportunityType",
                        "value": "plastic",
                        "resolutions": {
                            "resolutionsPerAuthority": [
                                {
                                    "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.9f48eb3d-c3c2-436e-a679-87cf9d7bf18b.OpportunityType",
                                    "status": {
                                        "code": "ER_SUCCESS_MATCH"
                                    },
                                    "values": [
                                        {
                                            "value": {
                                                "name": "plastic",
                                                "id": "3f01a108d7ed607934a2aced227f1c77"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        "confirmationStatus": "NONE"
                    },
                    "emailOrPhone": {
                        "name": "emailOrPhone",
                        "confirmationStatus": "NONE"
                    },
                    "yesNoIdentifyingInfoWillingness": {
                        "name": "yesNoIdentifyingInfoWillingness",
                        "value": "yes",
                        "resolutions": {
                            "resolutionsPerAuthority": [
                                {
                                    "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.9f48eb3d-c3c2-436e-a679-87cf9d7bf18b.YesNo",
                                    "status": {
                                        "code": "ER_SUCCESS_MATCH"
                                    },
                                    "values": [
                                        {
                                            "value": {
                                                "name": "Yes",
                                                "id": "93cba07454f06a4a960172bbd6e2a435"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        "confirmationStatus": "NONE"
                    },
                    "phone": {
                        "name": "phone",
                        "value": "111111111",
                        "confirmationStatus": "NONE"
                    },
                    "yesNoGreenOpportunity": {
                        "name": "yesNoGreenOpportunity",
                        "confirmationStatus": "NONE"
                    }
                }
            },
            "dialogState": "IN_PROGRESS"
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
