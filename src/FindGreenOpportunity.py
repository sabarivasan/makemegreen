import LexUtils
import AlexaUtils
import Constants as CC
import User
from GreenOpportunityLoader import GreenOpportunityLoader


def handle_lex(event, context):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}

    if not LexUtils.is_slot_present(slots, CC.SLOT_OPPORTUNITY_TYPE):
        message = "Would you like to learn about paper, plastic or water consumption today?"
        response_card = LexUtils.build_response_card(
            'Consumption Type', 'What type of consumption would you like to learn about?',
            [
                {'text': 'Paper', 'value': 'paper'},
                {'text': 'Plastic', 'value': 'plastic'},
                {'text': 'Water', 'value': 'water'}
            ]
        )
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_OPPORTUNITY_TYPE, message, response_card)

    opportunity_type = slots[CC.SLOT_OPPORTUNITY_TYPE]
    session_attrs[CC.SLOT_OPPORTUNITY_TYPE] = opportunity_type

    if not LexUtils.is_slot_present(slots, CC.SLOT_EMAIL_ADDRESS):
        message = "Can you provide your email address so we can lookup your green history?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_EMAIL_ADDRESS, message, None)
    email_address = slots[CC.SLOT_EMAIL_ADDRESS]
    session_attrs[CC.SLOT_EMAIL_ADDRESS] = email_address

    user = User.User(email_address)
    if CC.SESS_ATTR_STATE not in session_attrs or session_attrs[
        CC.SESS_ATTR_STATE] != CC.SESS_ATTR_AWAITING_OPPORTUNITY_CONF:
        session_attrs[CC.SESS_ATTR_USER_ID] = email_address
        oppty_loader = GreenOpportunityLoader(opportunity_type, user)
        oppty = oppty_loader.load_next_opportunity_for_user()

        if oppty:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_ATTR_AWAITING_OPPORTUNITY_CONF
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID] = str(oppty['id'])
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME] = oppty['name']
            message = "{}. Would you like to give that a try?".format(oppty['user_text'])
            return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO, message, None)
        else:
            message = "Sorry, we don't have any green tips for you at the moment!"
    else:
        if LexUtils.is_slot_present(slots, CC.SLOT_YES_NO):
            if LexUtils.is_yes(slots[CC.SLOT_YES_NO]):
                user.add_implemented_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                           session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "That's great! Thanks for doing your part!"
            else:
                user.add_refused_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                       session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "No worries! See you next time!"
        else:
            message = "No worries! See you next time!"

    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)

def handle_alexa(event, context):
    intent_name = event['request']['intent']['name']
    slots = event['request']['intent']['slots']
    session_attrs = event['session'].get('attributes', {})

    if not AlexaUtils.is_slot_present(slots, CC.SLOT_OPPORTUNITY_TYPE):
        message = "Would you like to learn about paper, plastic or water consumption today?"
        return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_OPPORTUNITY_TYPE, "Consumption Type",
                                      message)

    opportunity_type = slots[CC.SLOT_OPPORTUNITY_TYPE]['value']
    session_attrs[CC.SLOT_OPPORTUNITY_TYPE] = opportunity_type

    if not AlexaUtils.is_slot_present(slots, CC.SLOT_EMAIL_ADDRESS):
        message = "Can you provide your email address so we can lookup your green history?"
        return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_EMAIL_ADDRESS, "Email Address",
                                      message)

    email_address = slots[CC.SLOT_EMAIL_ADDRESS]['value']
    session_attrs[CC.SLOT_EMAIL_ADDRESS] = email_address

    user = User.User(email_address)
    if CC.SESS_ATTR_STATE not in session_attrs or session_attrs[
        CC.SESS_ATTR_STATE] != CC.SESS_ATTR_AWAITING_OPPORTUNITY_CONF:
        session_attrs[CC.SESS_ATTR_USER_ID] = email_address
        oppty_loader = GreenOpportunityLoader(opportunity_type, user)
        oppty = oppty_loader.load_next_opportunity_for_user()

        if oppty:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_ATTR_AWAITING_OPPORTUNITY_CONF
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID] = str(oppty['id'])
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME] = oppty['name']
            message = "{}. Would you like to give that a try?".format(oppty['user_text'])
            return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO, "Accept Opportunity?",
                                          message)
        else:
            message = "Sorry, we don't have any green tips for you at the moment!"
    else:
        if AlexaUtils.is_slot_present(slots, CC.SLOT_YES_NO):
            if LexUtils.is_yes(slots[CC.SLOT_YES_NO]['value']):
                user.add_implemented_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                           session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "That's great! Thanks for doing your part!"
            else:
                user.add_refused_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                       session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "No worries! See you next time!"
        else:
            message = "No worries! See you next time!"

    return AlexaUtils.build_response(session_attrs,
                                     AlexaUtils.build_speechlet_response("Thank you", message, None, True))
