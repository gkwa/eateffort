import json

from . import storage

for repo in storage.Repository.select():
    _lst = json.loads(repo.secrets)
    for secret in _lst:
        print(repo.repository, secret["name"])
