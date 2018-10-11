import LexUtils
import AlexaUtils
import Constants as CC
import GreenProductLoader


def handle_lex(event, content):
    slots = event['currentIntent']['slots']
    product_type = slots[CC.SLOT_PRODUCT_TYPE]

    loader = GreenProductLoader.GreenProductLoader()
    products = loader.load_product_recommendations(product_type)

    message = "The following products are recommended: " + ''.join(map(lambda p: "\n {}".format(p), products))
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)


def handle_alexa(event, content):
    intent_name = event['request']['intent']['name']
    slots = event['request']['intent']['slots']
    session_attrs = event['session'].get('attributes', {})

    if event['request']['dialogState'] == 'STARTED':
        return AlexaUtils.delegate(session_attrs, intent_name, slots)

    product_type = slots[CC.SLOT_PRODUCT_TYPE]['value']

    loader = GreenProductLoader.GreenProductLoader()
    products = loader.load_product_recommendations(product_type)

    message = "The following products are recommended: " + ''.join(map(lambda p: "\n {}".format(p), products))
    return AlexaUtils.build_response({}, AlexaUtils.build_speechlet_response("Product Recommendations", message,
                                                                             message, True))
