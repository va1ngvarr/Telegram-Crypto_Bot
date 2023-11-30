# Token of telegram bot
TOKEN: int

# User that receives important data
ADMIN: int

CHECKED_CHAT_ID: int

# Token of oxapay merchants (take a look at https://oxapay.com/)
OXAPAY_MERCHANT_KEY = {
    # You can use different keys for "ru" and "en" audiences
    # Or you can use the same one for both
    "ru": "",
    "en": "",
}


# Enables debug mode with test payments
DEBUG = True

if DEBUG:
    OXAPAY_MERCHANT_KEY = {
        "ru": "oxapay",
        "en": "oxapay",
    }
