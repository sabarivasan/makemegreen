import LexUtils
import Constants as CC
import User

def handle(event, content):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attrs = event['sessionAttributes']

    if not LexUtils.is_slot_present(slots, CC.OPPORTUNITY_TYPE):
        message = "Would you like to learn about paper, plastic or water consumption today?"
        return LexUtils.elicit_slot(CC.EMPTY_OBJ, intent_name, slots, CC.OPPORTUNITY_TYPE, message, None)
    opportunityType = slots[CC.OPPORTUNITY_TYPE]
    session_attrs[CC.OPPORTUNITY_TYPE] = opportunityType

    if not LexUtils.is_slot_present(slots, CC.EMAIL_ADDRESS):
        message = "Can you provide your email address so we can lookup your green history?"
        return LexUtils.elicit_slot(CC.EMPTY_OBJ, intent_name, slots, CC.EMAIL_ADDRESS, message, None)
    emailAddress = slots[CC.EMAIL_ADDRESS]
    session_attrs[CC.EMAIL_ADDRESS] = emailAddress

    user = User.User(emailAddress)

    message = "You can reduce the {} consumption by consuming less".format(opportunityType)
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)
