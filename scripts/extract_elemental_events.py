#!/usr/bin/env python
import click
import json
import sys
from pathlib import Path

from wcl.magesim.query import extract

@click.command()
@click.option('--json-dir', default=sys.maxsize, help='Directory to read from.')
def read_extract(json_dir):
    """Extract relevant water elemental events."""
    # For output
    data_dir = Path(Path(__file__).parent.parent, "data")
    pass

if __name__ == "__main__":
    read_extract()