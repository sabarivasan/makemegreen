"""
What is my green profile?
                                       VOICE : Please provide your phone number so I can look you up!
                                       TEXT: Please provide your phone number or email address so I can look you up!
1111111111
                                      You have 1,2323 points in total this year
                                      You have implemented XX opportunities!!


"""
import LexUtils
import Constants as CC
import User

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

    if CC.SESS_ATTR_STATE not in session_attrs:
        if is_slack:
            # Slack clients come with user id
            id_type = User.ID_TYPE_SLACK
            id = userId
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_IDENTIFYING_INFO_COMPLETE
            session_attrs[CC.SESS_ATTR_ANONYMOUS] = False
        else:
            info_msg = "phone number" if is_voice else "phone number or email address"
            slot = CC.SLOT_PHONE if is_voice else CC.SLOT_EMAIL_OR_PHONE
            message = "Please provide your {} so we can lookup your green history and provide personalized service".format(
                info_msg)
            session_attrs[CC.SESS_ATTR_STATE] = CC.SESS_STATE_AWAITING_IDENTIFY_INFO
            return LexUtils.elicit_slot(session_attrs, intent_name, slots, slot, message, None)

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
            message = "We cannot lookup your green profile without identifying info"
            return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)

        user = User.User(id, id_type)
        session_attrs[CC.SESS_ATTR_USER_ID] = id
        session_attrs[CC.SESS_ATTR_USER_ID_TYPE] = id_type