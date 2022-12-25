import json

from . import storage

for repo in storage.Repository.select():
    _lst = json.loads(repo.secrets)
    js = repo.github_json
    dct = json.loads(js)
    for secret in _lst:
        out = (
            f'gh secret set {secret["name"]} --repo '
            '{dct["full_name"]} --body "${secret["name"]}"'
        )
        print(out)
