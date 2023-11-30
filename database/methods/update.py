import logging

from peewee import OperationalError, decimal

from database.models import User
from utils.make_migrations import make_migrations


def update_user_data(
    user_id: int, balance: float = None, subscription: int = None, language: str = None
):
    try:
        user = User.get_by_id(user_id)

        if subscription:
            user.subscription = subscription
        if language:
            user.language = language

        if balance == 0.0:
            user.balance = decimal.Decimal(balance)
        elif balance:
            user.balance += decimal.Decimal(balance)

        user.save()
        logging.info(
            f"Successfully updated {user_id} ID user's data with new balance {balance} or subscription {subscription}"
        )
    except Exception as e:
        logging.error(
            f"Unable to update {user_id} ID user's data with new balance {balance} or subscription {subscription}"
        )
        raise e
    except OperationalError:
        make_migrations()
