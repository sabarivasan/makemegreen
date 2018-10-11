import LexUtils
import AlexaUtils
import MiscUtils
import Constants as CC
import User


def handle_lex(event, content):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}

    set_user_response = MiscUtils.set_session_user_id_and_type(event, False)
    if set_user_response is not None:
        return set_user_response

    if LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
        message = "You must provide an email address or phone number to use this feature."
        return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)

    user = User.User(session_attrs[CC.SESS_ATTR_USER_ID], session_attrs[CC.SESS_ATTR_USER_ID_TYPE])

    points_period_days = 30
    if LexUtils.is_slot_present(slots, CC.SLOT_POINTS_TIME_PERIOD):
        points_time_period = slots[CC.SLOT_POINTS_TIME_PERIOD]
        if points_time_period == CC.WEEKLY:
            points_period_days = 7
        elif points_time_period == CC.YEARLY:
            points_period_days = 365

    # TODO get points from user opportunities + points per opportunity

    message = "The point period is {}.".format(points_period_days)
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)

def handle_alexa(event, content):
    intent_name = event['request']['intent']['name']
    slots = event['request']['intent']['slots']
    session_attrs = event['session'].get('attributes', {})

    set_user_response = MiscUtils.set_session_user_id_and_type(event, True)
    if set_user_response is not None:
        return set_user_response

    if LexUtils.is_yes(session_attrs[CC.SESS_ATTR_ANONYMOUS]):
        message = "You must provide an email address or phone number to use this feature."
        return AlexaUtils.build_response(session_attrs,
                                         AlexaUtils.build_speechlet_response("Sorry", message, None, False))

    user = User.User(session_attrs[CC.SESS_ATTR_USER_ID], session_attrs[CC.SESS_ATTR_USER_ID_TYPE])

    points_period_days = 30
    if AlexaUtils.is_slot_present(slots, CC.SLOT_POINTS_TIME_PERIOD):
        points_time_period = slots[CC.SLOT_POINTS_TIME_PERIOD]
        if points_time_period == CC.WEEKLY:
            points_period_days = 7
        elif points_time_period == CC.YEARLY:
            points_period_days = 365

    # TODO get points from user opportunities + points per opportunity

    message = "The point period is {}.".format(points_period_days)
    return AlexaUtils.build_response(session_attrs,
                                     AlexaUtils.build_speechlet_response("Point Period", message, None, False))


def get_points(user, points_period_days):
