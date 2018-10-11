
EMPTY_OBJ = {}

# Intents
INTENT_FIND_GREEN_OPPORTUNITY = "FindGreenOpportunity"
INTENT_GET_POINTS = "GetPoints"
INTENT_GET_PRODUCT_RECOMMENDATION = "GetProductRecommendation"

# Slots
SLOT_OPPORTUNITY_TYPE = "opportunityType"
SLOT_POINTS_TIME_PERIOD = "pointsTimePeriod"
SLOT_PHONE = "phone"
SLOT_EMAIL_ADDRESS = "emailAddress"
SLOT_EMAIL_OR_PHONE = "emailOrPhone"
SLOT_PRODUCT_TYPE = "productType"
SLOT_YES_NO = "yesNo"

# Point time periods
DAILY = "daily"
WEEKLY = "weekly"
YEARLY = "yearly"


SESSION_ATTRS = "sessionAttributes"
REQUEST_ATTRS = "requestAttributes"


# Session Attributes
# State of the conversation
SESS_ATTR_STATE = 'State'
SESS_ATTR_USER_ID = 'UserId'

# Opportunity offered to the user. Awaiting yes/no
SESS_ATTR_AWAITING_OPPORTUNITY_CONF = 'AwaitingOpportunityConfirmation'
SESS_ATTR_CURRENT_OPPORTUNITY_ID = 'CurrentOpptyId'
SESS_ATTR_CURRENT_OPPORTUNITY_NAME = 'CurrentOpptyName'

# S