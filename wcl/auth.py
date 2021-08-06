from pathlib import Path
import requests
from typing import Tuple


def _get_secrets() -> Tuple[str, str]:
    oauth_file = Path(Path(__file__).parent.parent, ".oauth")
    with open(oauth_file, "r") as fobj:
        cid, secret = [s.rstrip('\n') for s in fobj.readlines()]
    return cid, secret


def get_oauth_token() -> str:
    cid, secret = _get_secrets()
    url = "https://classic.warcraftlogs.com/oauth/token"
    r = requests.post(
        url,
        auth = (cid, secret),
        data = {"grant_type": "client_credentials"}
    )

    if r.ok:
        return r.json()["access_token"]
    else:
        r.raise_for_status()
