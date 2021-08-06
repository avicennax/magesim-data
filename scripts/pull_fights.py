#!/usr/bin/env python
import asyncio
import click
import json
import os
import sys
from pathlib import Path

from wcl.auth import get_oauth_token
from wcl.query import WCLClient
from wcl.magesim.query import extract

LOG_DIR = Path(Path(__file__).parent.parent, "logs")

MASTER_QUERY = """
    query ($zoneID: Int!, $encounterID: Int!, $startTime: Float!, $limit: Int!, $page: Int!) {
      reportData {
        reports(zoneID: $zoneID, guildServerRegion: "US", startTime: $startTime, limit: $limit, page: $page) {
          last_page
          has_more_pages
          data {
            code
            events(encounterID: $encounterID, startTime: 0, endTime: 999999999, limit: 20000) {
               data
            }
          }
        }
      }
    }
"""

# All Kara encounters
ENCOUNTERS = list(range(652, 663))
ENCOUNTERS.remove(660)


@click.command()
@click.option('--max-pages', default=sys.maxsize, help='Max number of pages to pull.')
@click.option('--start-page', default=1)
@click.option('--run', help="Run name - should be unique.")
@click.option(
    '--encounter-id',
    type=click.IntRange(652, 663), # Don't be an ass and pass 660.
    default=-1,
    help="Encounter ID - all Kara fights pulled if unspecified"
)
def pull_extract(max_pages, start_page, encounter_id):
    """Query WCL GQL API, extract relevant water elemental events."""
    c = WCLClient(get_oauth_token())

    # Some hard-coded + configurable params
    start_time = 0
    limit = 10
    page = start_page
    if encounter_id == -1:
        encounters = ENCOUNTERS
    else:
        encounters = [encounter_id]

    # For output
    data_dir = Path(Path(__file__).parent.parent, "data")

    for enc_id in encounters:
        extract_subdir = Path(data_dir, "extracts", "v1", str(enc_id))
        print(f"Writing data to: {extract_subdir.as_posix()}")
        os.makedirs(extract_subdir.as_posix(), exist_ok=True)

        more_pages = True
        while more_pages or page > max_pages:
            qparams = {
                "zoneID": 1007, # kara
                "encounterID": enc_id,
                "startTime": start_time,
                "limit": limit,
                "page": page,
            }
            res = asyncio.run(c.query(MASTER_QUERY, qparams))
            print("Results fetched!")

            data = res["reportData"]["reports"]["data"]
            more_pages = res["reportData"]["reports"]["has_more_pages"]
            reports, dlq = extract(data)
            print(f"DLQ: {dlq}")

            for num, report in reports.items():
                if report:
                    fp = os.path.join(extract_subdir.as_posix(), f"report_{page}-{num}.json")
                    with open(fp, "w") as fobj:
                        json.dump(report, fobj)
                    
            page += 1

if __name__ == "__main__":
    pull_extract()