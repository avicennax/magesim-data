from pathlib import Path
from setuptools import setup


def get_requirements():
    wcl_reqs = []
    with open(Path(Path(__file__).parent, "requirements.txt")) as f:
        reqs = f.readlines()

    for r in reqs:
        if r == "\n":
            return wcl_reqs
        wcl_reqs.append(r.rstrip("\n"))


setup(
    name='wcl',
    version='0.0.1',
    packages=['wcl'],
    install_requires=get_requirements()
)