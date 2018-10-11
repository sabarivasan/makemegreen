import Constants as CC
import User
import LexUtils
import AlexaUtils


def set_session_user_id_and_type(event, is_alexa):
    if is_alexa:
        intent_name = event['request']['intent']['name']
        slots = event['request']['intent']['slots']
        session_attrs = event['session'].get('attributes', {})
        is_voice = True
        is_text = False
        is_slack = False
        user_id = event['session']['user']['userId']
    else:
        intent_name = event['currentIntent']['name']
        slots = event['currentIntent']['slots']
        session_attrs = event['sessionAttributes'] if 'sessionAttributes' in event and event[
            'sessionAttributes'] is not None else {}
        request_attrs = event['requestAttributes'] if 'requestAttributes' in event and event[
            'requestAttributes'] is not None else {}
        output_dialog_mode = event[CC.EVENT_INPUT_OUTPUT_DIALOG_MODE]
        is_voice = "Voice" == output_dialog_mode
        is_text = "Text" == output_dialog_mode
        is_slack = CC.USER_ATTR_CHANNEL_TYPE in request_attrs and "Slack" == request_attrs[CC.USER_ATTR_CHANNEL_TYPE]
        user_id = event[CC.EVENT_INPUT_USER_ID]

    if CC.SESS_ATTR_STATE not in session_attrs:

        if is_slack:
            # Slack clients come with user id
            session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = User.ID_TYPE_SLACK
            session_attrs[CC.SESS_ATTR_USER_ID] = user_id
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            # Voice clients mean we ask for phone number alone, not email address which is unreliable over voice
            info_msg = "phone number" if is_voice else "phone number or email address"
            message = "Would you be willing to provide your {} so we can lookup your green history and provide personalized service?".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS
            if is_alexa:
                return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS,
                                     "Phone Number", message)
            else:
                return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS,
                                        message, None)

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS:

        if is_yes(slots[CC.SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS], is_alexa):
            info_msg = "phone number" if is_voice else "phone number or email address"
            slot = CC.SLOT_PHONE if is_voice else CC.SLOT_EMAIL_OR_PHONE
            message = "Please provide your {} so we can lookup your green history and provide personalized service".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO
            if is_alexa:
                return AlexaUtils.elicit_slot(session_attrs, intent_name, slots, slot, "Phone Number", message)
            else:
                return LexUtils.elicit_slot(session_attrs, intent_name, slots, slot, message, None)
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    elif session_attrs[CC.SESS_ATTR_STATE] == CC.SESS_STATE_AWAITING_IDENTIFY_INFO:
        session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
        slot = CC.SLOT_PHONE if is_voice else CC.SLOT_EMAIL_OR_PHONE
        session_attrs[CC.SESS_ATTR_USER_ID] = slots[slot] if is_slot_present(slots, slot, is_alexa) else event[CC.EVENT_INPUT_TRANSCRIPT]
        if is_alexa:
            session_attrs[CC.SESS_ATTR_USER_ID] = slots[slot]['value']
        if len(session_attrs[CC.SESS_ATTR_USER_ID]) > 0:
            if is_voice:
                session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = User.ID_TYPE_PHONE
            elif LexUtils.looks_like_phone_number(session_attrs[CC.SESS_ATTR_USER_ID]):
                session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = User.ID_TYPE_PHONE
            else:
                session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = User.ID_TYPE_EMAIL
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = True

    return None


def is_slot_present(slots, slot, is_alexa):
    return AlexaUtils.is_slot_present(slots, slot) if is_alexa else LexUtils.is_slot_present(slots, slot)


def is_yes(val, is_alexa):
    return AlexaUtils.is_yes(val) if is_alexa else LexUtils.is_yes(val)