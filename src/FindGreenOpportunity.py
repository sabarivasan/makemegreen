"""
Levels of personalization in conversations:
For slack clients, we get detailed user information that helps us reliably identify an entity
For voice, text-based and other clients, we don't get user information.

We aim for the following levels of personalization:
- Completely anonymous: User does not wish to provide a unique identifying information (phone number or email address).
    We will still provide as much info as we can: green opportunities, product ratings, etc. We just won't be able
    to store their green history
- Anonmymous personalized experience whenever we can (Currently Slack): In this case, we can still identify the user
    uniquely. We can't initiate or send info to the user since we don't have contact info.
    TODO: Can we parse the slack user id and post messages to them if necessary like for weekly green tips, etc
- Personalized: Phone or email provided by user in 1 prompt. We detect it and act accordingly.


- Slack
	- use request attribute "x-amz-lex:channel-type": "Slack" to detect Slack
	- use "userId": "ea4b1552-45f0-4fe1-ab45-b3a9b0e46485:TDAGGP9DH:UDAE42BA4" to identify user
	- Can we post to invidual user? This is only for weekly green notifications

"""

import LexUtils
import AlexaUtils
import Constants as CC
import User
from GreenOpportunityLoader import GreenOpportunityFinder


def handle_lex(event, context):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes'] if 'sessionAttributes' in event and event['sessionAttributes'] is not None else {}
    request_attrs = event['requestAttributes'] if 'requestAttributes' in event and event['requestAttributes'] is not None else {}
    userId = event[CC.EVENT_INPUT_USER_ID]
    outputDialogMode = event[CC.EVENT_INPUT_OUTPUT_DIALOG_MODE]
    is_voice = "Voice" == outputDialogMode
    is_text = "Text" == outputDialogMode
    is_slack = CC.USER_ATTR_CHANNEL_TYPE in request_attrs and "Slack" == request_attrs[CC.USER_ATTR_CHANNEL_TYPE]
    user = None

    # First, find out what opportunity type they are interested in hearing about
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

    # Next, lets find out if we need identifying info and if user is willing to provide identifying info
    if CC.SESS_ATTR_STATE not in session_attrs:

        if is_slack:
            # Slack clients come with user id
            id_type = User.ID_TYPE_SLACK
            id = userId
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            # Voice clients mean we ask for phone number alone, not email address which is unreliable over voice
            info_msg = "phone number" if is_voice else "phone number or email address"
            message = "Would you be willing to provide your {} so we can lookup your green history and provide personalized service?".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS
            return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS,
                                        message, None)

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS:

        if LexUtils.is_yes(slots[CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS]):
            info_msg = "phone number" if is_voice else "phone number or email address"
            slot = CC.SLOT_PHONE if is_voice else CC.SLOT_EMAIL_OR_PHONE
            message = "Please provide your {} so we can lookup your green history and provide personalized service".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO
            return LexUtils.elicit_slot(session_attrs, intent_name, slots, slot, message, None)
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO:
        session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
        slot = CC.SLOT_PHONE if is_voice else CC.SLOT_EMAIL_OR_PHONE
        id = slots[slot] if LexUtils.is_slot_present(slots, slot) else event[CC.EVENT_INPUT_TRANSCRIPT]
        if len(id.strip()) > 0:
            if is_voice:
                id_type = User.ID_TYPE_PHONE
            elif LexUtils.looks_like_phone_number(id):
                id_type = User.ID_TYPE_PHONE
            else:
                id_type = User.ID_TYPE_EMAIL
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    # TODO: It would be natural if this if clause were part of the previous if clauses
    if session_attrs[CC.SESS_ATTR_STATE] != CC.SESS_STATE_AWAITING_OPPORTUNITY_CONF:
        # Store/load the user
        if not LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
            user = User.User(id, id_type)
            session_attrs[CC.SESS_ATTR_USER_ID] = id
            session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = id_type

        # Tag: home or work
        tag = slots[CC.SLOT_HOME_OR_WORK] if LexUtils.is_slot_present(slots, CC.SLOT_HOME_OR_WORK) else None

        oppty_loader = GreenOpportunityFinder(opportunity_type, user, tag)
        oppty = oppty_loader.find_opportunity()

        if oppty:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_OPPORTUNITY_CONF
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID] = str(oppty['id'])
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME] = oppty['name']
            message = "{}. Would you like to give that a try?".format(oppty['user_text'])
            return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_GREEN_OPPORTUNITY, message,
                                        None)
        else:
            message = "Sorry, we don't have any green tips for you at the moment!"

    else:
        if LexUtils.is_slot_present(slots, CC.SLOT_YES_NO_GREEN_OPPORTUNITY):
            if not LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
                user = User.User(session_attrs[CC.SESS_ATTR_USER_ID], session_attrs[CC.SESS_ATTR_USER_ID_TYPE])
            if LexUtils.is_yes(slots[CC.SLOT_YES_NO_GREEN_OPPORTUNITY]):
                if user:
                    user.add_implemented_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                               session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "That's great! Thanks for doing your part!"
            else:
                if user:
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
    userId = event['session']['user']['userId']
    is_voice = True
    is_text = False
    is_slack = False
    user = None

    # First, find out what opportunity type they are interested in hearing about
    if not AlexaUtils.is_slot_present(slots, CC.SLOT_OPPORTUNITY_TYPE):
        message = "Would you like to learn about paper, plastic or water consumption today?"
        return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_OPPORTUNITY_TYPE, "Consumption Type",
                                      message)

    opportunity_type = slots[CC.SLOT_OPPORTUNITY_TYPE]['value']
    session_attrs[CC.SLOT_OPPORTUNITY_TYPE] = opportunity_type

    # Next, lets find out if we need identifying info and if user is willing to provide identifying info
    if CC.SESS_ATTR_STATE not in session_attrs:
        # Voice clients mean we ask for phone number alone, not email address which is unreliable over voice
        info_msg = "phone number"
        message = "Would you be willing to provide your {} so we can lookup your green history and provide personalized service?".format(
            info_msg)
        session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS
        return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS,
                                    "Personalized Service", message)

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS:

        if AlexaUtils.is_yes(slots[CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS]):
            info_msg = "phone number"
            slot = CC.SLOT_PHONE
            message = "Please provide your {} so we can lookup your green history and provide personalized service".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO
            return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, slot, "Phone Number", message)
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO:
        session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
        slot = CC.SLOT_PHONE
        id = slots[slot]['value'] if AlexaUtils.is_slot_present(slots, slot) else event[CC.EVENT_INPUT_TRANSCRIPT]
        if len(id.strip()) > 0:
            id_type = User.ID_TYPE_PHONE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    # TODO: It would be natural if this if clause were part of the previous if clauses
    if session_attrs[CC.SESS_ATTR_STATE] != CC.SESS_STATE_AWAITING_OPPORTUNITY_CONF:
        # Store/load the user
        if not LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
            user = User.User(id, id_type)
            session_attrs[CC.SESS_ATTR_USER_ID] = id
            session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = id_type
        oppty_loader = GreenOpportunityFinder(opportunity_type, user)
        oppty = oppty_loader.find_opportunity()

        if oppty:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_OPPORTUNITY_CONF
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID] = str(oppty['id'])
            session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME] = oppty['name']
            message = "{}. Would you like to give that a try?".format(oppty['user_text'])
            return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_GREEN_OPPORTUNITY,
                                          "Accept Opportunity", message)
        else:
            message = "Sorry, we don't have any green tips for you at the moment!"

    else:
        if AlexaUtils.is_slot_present(slots, CC.SLOT_YES_NO_GREEN_OPPORTUNITY):
            if not LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
                user = User.User(session_attrs[CC.SESS_ATTR_USER_ID], session_attrs[CC.SESS_ATTR_USER_ID_TYPE])
            if AlexaUtils.is_yes(slots[CC.SLOT_YES_NO_GREEN_OPPORTUNITY]):
                if user:
                    user.add_implemented_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                               session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "That's great! Thanks for doing your part!"
            else:
                if user:
                    user.add_refused_oppty(session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_ID],
                                       session_attrs[CC.SESS_ATTR_CURRENT_OPPORTUNITY_NAME])
                message = "No worries! See you next time!"
        else:
            message = "No worries! See you next time!"

    return AlexaUtils.build_response(session_attrs,
                                     AlexaUtils.build_speechlet_response("Thank you", message, None, True))
