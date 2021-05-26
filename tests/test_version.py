from urllib.request import urlopen
from urllib.error import HTTPError
from pkg_resources import parse_version
import json
from pathlib import Path


def test_local_against_pypi_version():
    d = Path(__file__).parent / ".." / "monolense" / "__init__.py"
    with open(d) as f:
        d = {}
        exec(f.read(), d)
        local_version = parse_version(d["__version__"])

    try:
        r = urlopen("https://pypi.org/pypi/monolense/json")
    except HTTPError:
        # not yet on PyPI
        return
    assert r.code == 200
    payload = r.read()
    releases = json.loads(payload)["releases"]

    latest_pypi_version = max(parse_version(v) for v in releases)
    assert (
        local_version > latest_pypi_version
    ), "PyPI release with same version number found, version needs to be incremented"


if __name__ == "__main__":
    test_local_against_pypi_version()
