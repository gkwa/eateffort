import datetime
import logging
import pathlib

import peewee
import platformdirs

appname = "eateffort"
appauthor = "monacelli"

db_path = pathlib.Path(platformdirs.user_data_dir(appname, appauthor)) / f"{appname}.db"

db_path.parent.mkdir(exist_ok=True, parents=True)

_logger = logging.getLogger(__name__)

_logger.debug(db_path)


db = peewee.SqliteDatabase(db_path)


class Repository(peewee.Model):
    repository = peewee.CharField()
    github_json = peewee.CharField()
    secrets = peewee.CharField()
    dt_checked = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db
