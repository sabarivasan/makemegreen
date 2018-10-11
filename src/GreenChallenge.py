"""
Conduct a green challenge at Cvent.
                                       Which locations would you like to participate?
All
                                       Would you like to target plastic, paper or water or all green opportunities?
All
                                       When would like this the challenge to start?
Next Monday
                                       When would you like the challenge to end?
End of next month
                                       What would you like the challenge to be called?
blah
                                       Your green challenge has been setup!


"""
import LexUtils
import Constants as CC


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

    if not LexUtils.is_slot_present(slots, CC.SLOT_USER_GROUP):
        message = "Please specify the group name like Cvent to trigger challenge. Example: I would like to start a green challenge at Cvent"
        return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)
    user_group = slots[CC.SLOT_USER_GROUP]

    if not LexUtils.is_slot_present(slots, CC.SLOT_LOCATIONS):
        message = "Which {} locations would you like to participate or say all?".format(user_group)
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_LOCATIONS, message, None)
    locations = slots[CC.SLOT_LOCATIONS]

    if not LexUtils.is_slot_present(slots, CC.SLOT_START):
        message = "When would like this the challenge to start?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_START, message, None)
    start = slots[CC.SLOT_START]

    if not LexUtils.is_slot_present(slots, CC.SLOT_END):
        message = "When would like this the challenge to end?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_END, message, None)
    end = slots[CC.SLOT_END]

    if not LexUtils.is_slot_present(slots, CC.SLOT_CHALLENGE_NAME):
        message = "What would you like the challenge to be called?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_CHALLENGE_NAME, message, None)
    challenge_name = slots[CC.SLOT_CHALLENGE_NAME]


    message = "Green challenge {} has been setup! I am keeping track of points for all participating locations!".format(challenge_name)
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)

