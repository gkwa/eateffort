import datetime

import peewee

db = peewee.SqliteDatabase("stuff.db")


class Repository(peewee.Model):
    repository = peewee.CharField()
    github_json = peewee.CharField()
    secrets = peewee.CharField()
    dt_checked = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
