import LexUtils
import Constants as CC
import User


def handle(event, content):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}

    if not LexUtils.is_slot_present(slots, CC.SLOT_EMAIL_ADDRESS):
        message = "Can you provide your email address so we can lookup your green history?"
        return LexUtils.elicit_slot(session_attrs, intent_name, slots, CC.SLOT_EMAIL_ADDRESS, message, None)
    email_address = slots[CC.SLOT_EMAIL_ADDRESS]
    session_attrs[CC.SLOT_EMAIL_ADDRESS] = email_address

    user = User.User(email_address)

    points_period_days = 30
    if LexUtils.is_slot_present(slots, CC.SLOT_POINTS_TIME_PERIOD):
        points_time_period = slots[CC.SLOT_POINTS_TIME_PERIOD]
        if points_time_period == CC.WEEKLY:
            points_time_period = 7
        elif points_time_period == CC.YEARLY:
            points_time_period = 365

    # TODO get points from user opportunities + points per opportunity

    message = "This has not been implemented yet."
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)
