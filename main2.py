import datetime

import peewee

db = peewee.SqliteDatabase("stuff.db")


class Repository(peewee.Model):
    repository = peewee.CharField()
    secrets = peewee.CharField()
    dt_checked = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db  # This model uses the "stuff.db" database.


repo_names = [repo.repository for repo in Repository.select()]

print(repo_names)
