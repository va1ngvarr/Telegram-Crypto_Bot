import logging
import json

import requests

from config import OXAPAY_MERCHANT_KEY


url = "https://api.oxapay.com/merchants/request"


def payment_request(amount: float, lang: str):
    data = {
        "merchant": OXAPAY_MERCHANT_KEY[lang],
        "amount": amount,
        "underPaidCover": 15,
    }

    response = requests.post(url=url, data=json.dumps(data))

    res = response.json()

    if res["result"] == 100:
        logging.info("Oxapay responsed succesfully.")
        return res
        # store res['trackId'] and redirect to res['payLink'] urlth
    logging.error(f"Oxapay says that result is {res['result']}")
    return None
