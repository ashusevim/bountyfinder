import json, subprocess, sys
from pathlib import Path


def test_json_valid():
    data = json.loads(Path("platforms.json").read_text())
    assert len(data) >= 20, "need curated set"
    for p in data:
        for k in (
            "name",
            "url",
            "programs_url",
            "region",
            "focus",
            "access",
            "payout_range",
        ):
            assert k in p, f"{p.get('name')} missing {k}"


def test_finder_filters():
    r = subprocess.run(
        [sys.executable, "finder.py", "--focus", "web3", "--public-only"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "Immunefi" in r.stdout
    r2 = subprocess.run(
        [sys.executable, "finder.py", "--beginner", "--public-only"],
        capture_output=True,
        text=True,
    )
    assert "Intigriti" in r2.stdout or "Bugcrowd" in r2.stdout
