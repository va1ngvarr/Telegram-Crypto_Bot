from peewee import (
    Model,
    IntegerField,
    DecimalField,
    CharField,
    SqliteDatabase,
)


conn = SqliteDatabase("userdata.db")


class BaseModel(Model):
    class Meta:
        database = conn


class User(BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)
    referrer_id = IntegerField(null=True)
    subscription = IntegerField(null=True)
    balance = DecimalField(default=0.0)
    language = CharField(default="en", max_length=2)
