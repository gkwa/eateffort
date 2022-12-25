import argparse
import datetime
import json
import logging
import sys

import dateparser
import humanize

from . import storage

parser = argparse.ArgumentParser()

levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
parser.add_argument("--log-level", default="INFO", choices=levels)

args = parser.parse_args()

logging.basicConfig(
    level=args.log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #        logging.FileHandler(f"{pathlib.Path(__file__)}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

_lst = []
for repo in storage.Repository.select():
    dct = json.loads(repo.github_json)
    logging.debug(json.dumps(dct, indent=2))
    _lst.append(dct)

_lst.sort(key=lambda d: d["pushed_at"])

# now = datetime.datetime.now(pytz.timezone("UTC"))
now = datetime.datetime.now(datetime.timezone.utc)

for dct in _lst:
    dt = dateparser.parse(dct["pushed_at"])
    delta = now - dt
    relative = humanize.naturaldelta(delta)
    print(f"{relative:>20} {dct['visibility']:>10} {dct['html_url']}")
