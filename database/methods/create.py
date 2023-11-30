from database.models import User


def add_new_user(user_id: int, referrer_id: int = None) -> None:
    User.get_or_create(user_id=user_id, referrer_id=referrer_id)
