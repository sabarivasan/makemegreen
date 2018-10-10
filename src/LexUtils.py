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


def is_slot_present(slots, slot):
    return slot in slots and slots[slot]

