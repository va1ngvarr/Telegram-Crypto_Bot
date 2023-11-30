from peewee import DoesNotExist, OperationalError

from database.models import User
from utils.make_migrations import make_migrations


def get_user_with_id(user_id: int) -> User:
    try:
        user = User.get_by_id(user_id)
        return user
    except DoesNotExist:
        return None
    except OperationalError:
        make_migrations()


def get_users_with_referrer(referrer_id: int) -> list[User]:
    users = []

    for user in User.select():
        if user.referrer_id == referrer_id:
            users.append(user)

    return users
