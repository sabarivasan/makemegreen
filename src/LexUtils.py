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

def cleanse_email(email_address):
    email_address = email_address.strip(">")
    email_address = email_address.strip("<")
    if email_address.find("|") != -1:
        email_address = email_address.split("|")[1]
    if email_address.find("mailto:") != -1:
        email_address = email_address.split(":")[1]

    return email_address

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
