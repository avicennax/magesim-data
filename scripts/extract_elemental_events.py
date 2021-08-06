#!/usr/bin/env python
import click
import json
import time
import os
from pathlib import Path

from wcl.magesim.query import extract

LOG_DIR = Path(Path(__file__).parent.parent, "logs")

# All Kara encounters
ENCOUNTERS = list(range(652, 663))
ENCOUNTERS.remove(660)


@click.command()
@click.option('--run', required=True, help='Pull run to extract from.')
@click.option(
    '--encounter-id',
    type=click.IntRange(652, 663), # Don't be an ass and pass 660.
    default=-1,
    help="Encounter ID - all Kara fights pulled if unspecified"
)
def read_extract(run, encounter_id):
    """Extract relevant water elemental events."""
    # Log "bad" reports
    now = time.time()
    log_file = Path(LOG_DIR, f"{now}_{run}_extract.log")

    # For output
    data_dir = Path(Path(__file__).parent.parent, "data")
    if encounter_id == -1:
        encounters = ENCOUNTERS
    else:
        encounters = [encounter_id]

    for enc_id in encounters:
        pull_subdir = Path(data_dir, "raw_reports", run, str(enc_id))
        extract_subdir = Path(data_dir, "extracts", run, str(enc_id))
        os.makedirs(extract_subdir.as_posix(), exist_ok=True)

        for report_path in pull_subdir.glob("report*"):
            report_data = json.loads(report_path.read_text())
            code = report_data["code"]

            # Pull out the events we care about
            try:
                events = extract(report_data)
            except Exception as err:
                import sys
                err_type, msg, tb = sys.exc_info()
                err = f"Extract failed: {code} -- {err_type}\n"
                log_file.open("a").write(err)
            else:
                if events:
                    extract_path = Path(extract_subdir, f"report_{code}.json")
                    extract_path.write_text(json.dumps(events))
                else:
                    log_file.open("a").write(f"No data for report: {code}\n")


if __name__ == "__main__":
    read_extract()