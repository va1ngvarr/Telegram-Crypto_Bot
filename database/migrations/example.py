from playhouse.migrate import *


db = SqliteDatabase("userdata.db")
migrator = SqliteMigrator(db)

with db.atomic():
    migrate(
        migrator.add_column("User", "language", CharField(default="en", max_length=2))
    )
