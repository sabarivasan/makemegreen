import LexUtils
import Constants as CC
import GreenProductLoader


def handle(event, content):
    slots = event['currentIntent']['slots']
    product_type = slots[CC.SLOT_PRODUCT_TYPE]

    loader = GreenProductLoader.GreenProductLoader()
    products = loader.load_product_recommendations(product_type)

    message = "The following products are recommended: " + ''.join(map(lambda p: "\n {}".format(p), products))
    return LexUtils.close(CC.EMPTY_OBJ, True, message, CC.EMPTY_OBJ)
