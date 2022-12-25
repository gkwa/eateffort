import datetime
import json
import logging
import os
import pathlib
import sys

import peewee
import requests

access_token_env_var = "GITHUB_TOKEN"
personal_access_token = os.environ.get(access_token_env_var)
api_base_url = "https://api.github.com"

headers = {
    "Authorization": f"Token {personal_access_token}",
    "Accept": "application/vnd.github+json",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(f"{pathlib.Path(__file__)}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def doit(url: str):
    response = requests.get(url, headers=headers)

    logging.info(f"Status code: {response.status_code}")
    logging.info("Repositories:")

    if not response.json():
        return None

    for repository in response.json():
        logging.info(repository["name"])

    repo_names = [repo.repository for repo in Repository.select()]

    for repository in response.json():

        name = repository["name"]
        logging.debug(name)

        if name in repo_names:
            logging.debug(f"skipping {name} because its already been seen")
            continue

        url = f"{api_base_url}/repos/{repository['full_name']}/actions/secrets"

        response = requests.get(url, headers=headers)
        secrets = response.json()["secrets"]
        github_json = json.dumps(repository)

        repo = Repository(repository=name, secrets=secrets, github_json=github_json)
        repo.save()

    return True


db = peewee.SqliteDatabase("stuff.db")


class Repository(peewee.Model):
    repository = peewee.CharField()
    github_json = peewee.CharField()
    secrets = peewee.CharField()
    dt_checked = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db  # This model uses the "stuff.db" database.


Repository.create_table()

page_count = 1
while True:
    logging.info(f"page {page_count}")
    url = f"{api_base_url}/user/repos?per_page=100&page={page_count}"
    if not doit(url):
        break
    page_count += 1
