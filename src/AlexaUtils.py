def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_speechlet_response(title, output, reprompt_text, should_end_session, directives=None):
    if directives is None:
        directives = []
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session,
        'directives': directives
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, title, message):
    directives = [
            {
                "type": "Dialog.ElicitSlot",
                "slotToElicit": slot_to_elicit,
                "updatedIntent": {
                    "name": intent_name,
                    "confirmationStatus": "NONE",
                    "slots": slots
                }
            }
        ]

    return build_response(session_attributes, build_speechlet_response(title, message, message, False, directives))


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
    return slot in slots and 'value' in slots[slot]