#!/usr/bin/env python
# coding: utf-8

import click

import pandas as pd
from pathlib import Path


@click.command()
@click.argument('log')
def main(log: str):
    """Print timestamp deltas between Waterbolts per summon."""
    p = Path(log)
    lines = p.read_text().split('\n')

    summon_sessions = []
    for line in lines:
        if "SPELL_SUMMON" in line and "Water Elemental" in line:
            summon_sessions.append([])
        if "SPELL_CAST_SUCCESS" in line and "Waterbolt" in line:
            summon_sessions[-1].append(line)

    for sess in summon_sessions:
        print(pd.Series([line.split(" ")[1] for line in sess], dtype='m8[ns]').diff())


if __name__ == "__main__":
    main()