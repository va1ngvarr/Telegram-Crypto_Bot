from .models import User


def register_all_models():
    models = [User]

    for model in models:
        model.create_table()
