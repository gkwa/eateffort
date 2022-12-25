import argparse
import json
import logging
import os
import sys

import requests

from eateffort import __version__

from . import storage

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

access_token_env_var = "GITHUB_TOKEN"
personal_access_token = os.environ.get(access_token_env_var)
api_base_url = "https://api.github.com"

headers = {
    "Authorization": f"Token {personal_access_token}",
    "Accept": "application/vnd.github+json",
}


def doit(url: str):
    response = requests.get(url, headers=headers)

    _logger.info(f"Status code: {response.status_code}")
    _logger.info("Repositories:")

    if not response.json():
        return None

    for repository in response.json():
        _logger.info(repository["name"])

    repo_names = [repo.repository for repo in storage.Repository.select()]

    for repository in response.json():

        name = repository["name"]
        _logger.debug(name)

        if name in repo_names:
            _logger.debug(f"skipping {name} because its already been seen")
            continue

        url = f"{api_base_url}/repos/{repository['full_name']}/actions/secrets"

        response = requests.get(url, headers=headers)
        secrets = response.json()["secrets"]
        js = json.dumps(secrets)
        github_json = json.dumps(repository)

        repo = storage.Repository(repository=name, secrets=js, github_json=github_json)
        repo.save()

    return True


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--version",
        action="version",
        version="eateffort {ver}".format(ver=__version__),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")

    storage.Repository.create_table()

    page_count = 1
    while True:
        _logger.info(f"page {page_count}")
        url = f"{api_base_url}/user/repos?per_page=100&page={page_count}"
        if not doit(url):
            break
        page_count += 1

    # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m eateffort.skeleton 42
    #
    run()
