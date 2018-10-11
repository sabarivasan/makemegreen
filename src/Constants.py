
EMPTY_OBJ = {}

# Intents
INTENT_FIND_GREEN_OPPORTUNITY = "FindGreenOpportunity"
INTENT_GET_POINTS = "GetPoints"
INTENT_GET_PRODUCT_RECOMMENDATION = "GetProductRecommendation"
INTENT_GET_POSSIBLE_ACTIONS = "GetPossibleActions"
INTENT_GREEN_CHALLENGE = "GreenChallenge"
INTENT_GREEN_PROFILE = "GreenProfile"

# Slots

# FindGreenOpportunity
SLOT_OPPORTUNITY_TYPE = "opportunityType"
SLOT_POINTS_TIME_PERIOD = "pointsTimePeriod"
SLOT_HOME_OR_WORK = "homeOrWork"
SLOT_PHONE = "phone"
SLOT_EMAIL_ADDRESS = "emailAddress"
SLOT_EMAIL_OR_PHONE = "emailOrPhone"
SLOT_PRODUCT_TYPE = "productType"
SLOT_YES_NO_GREEN_OPPORTUNITY = "yesNoGreenOpportunity"
SLOT_YES_NO_IDENTIFYING_INFO_WILLINGNESS = "yesNoIdentifyingInfoWillingness"

# Green challenge
SLOT_USER_GROUP = "group"
SLOT_LOCATIONS = "locations"
SLOT_OPPORTUNITY_TYPE_OR_ALL = "opportunityTypeOrAll"
SLOT_START = "start"
SLOT_END = "end"
SLOT_CHALLENGE_NAME = "challengeName"

# Point time periods
DAILY = "daily"
WEEKLY = "weekly"
YEARLY = "yearly"


SESSION_ATTRS = "sessionAttributes"
REQUEST_ATTRS = "requestAttributes"


# Session Attributes
# State of the conversation

SESS_ATTR_USER_ID = 'userId'
SESS_ATTR_USER_ID_TYPE = 'userIdType'
SESS_ATTR_ANONYMOUS = 'anonymous'
SESS_ATTR_CURRENT_OPPORTUNITY_ID = 'CurrentOpptyId'
SESS_ATTR_CURRENT_OPPORTUNITY_NAME = 'CurrentOpptyName'
SESS_ATTR_OPPORTUNITY_TAG = "opportunityTag"

# State of a conversation
SESS_ATTR_STATE = 'State'
# Asked user if they are willing to provide identifying info. Awaiting yes/no
SESS_STATE_AWAITING_IDENTIFY_INFO_WILLINGNESS = 'AwaitingIdentifyingInfoWillingness'

# Asked user to provide identifying info. Awaiting info
SESS_STATE_AWAITING_IDENTIFY_INFO = 'AwaitingIdentifyingInfo'

# Opportunity offered to the user. Awaiting yes/no
SESS_STATE_AWAITING_OPPORTUNITY_CONF = 'AwaitingOpportunityConfirmation'

# We either didn't need identifying info or we asked the user to provide identifying info and they either accepted or refused
SESS_STATE_IDENTIFYING_INFO_COMPLETE = 'IdentifyingInfoComplete'


# User attributes
USER_ATTR_CHANNEL_TYPE = "x-amz-lex:channel-type"

# Attribute that comes with event
EVENT_INPUT_USER_ID = 'userId'
EVENT_INPUT_OUTPUT_DIALOG_MODE = 'outputDialogMode'
EVENT_INPUT_TRANSCRIPT = 'inputTranscript'
