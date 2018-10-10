import LexUtils
import Constants as CC
import User


def handle(event, content):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}

    if not LexUtils.is_slot_present(slots, CC.OPPORTUNITY_TYPE):
        message = "Would you like to learn about paper, plastic or water consumption today?"
        response_card = LexUtils.build_response_card(
                    'Consumption Type', 'What type of consumption would you like to learn about?',
                    [
                        {'text': 'Paper', 'value': 'Paper'},
                        {'text': 'Plastic', 'value': 'Plastic'},
                        {'text': 'Water', 'value': 'Water'}
                    ]
                )
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.OPPORTUNITY_TYPE, message, response_card)
    opportunity_type = slots[CC.OPPORTUNITY_TYPE]
    session_attrs[CC.OPPORTUNITY_TYPE] = opportunity_type

    if not LexUtils.is_slot_present(slots, CC.EMAIL_ADDRESS):
        message = "Can you provide your email address so we can lookup your green history?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.EMAIL_ADDRESS, message, None)
    email_address = slots[CC.EMAIL_ADDRESS]
    session_attrs[CC.EMAIL_ADDRESS] = email_address

    user = User.User(email_address)

    message = "You can reduce the {} consumption by consuming less".format(opportunity_type)
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)
