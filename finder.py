#!/usr/bin/env python3
"""bounty-platform finder: search/filter platforms where you can hunt programs."""

import argparse
import json
import sys
from pathlib import Path

DATA = Path(__file__).with_name("platforms.json")


def load():
    return json.loads(DATA.read_text())


def match(p, focus=None, region=None, beginner=False, public_only=False, query=None):
    if focus and focus.lower() not in [f.lower() for f in p.get("focus", [])]:
        return False
    if region and region.lower() not in p.get("region", "").lower():
        return False
    if beginner and not p.get("beginner_friendly"):
        return False
    if public_only and "public" not in p.get("access", ""):
        return False
    if query:
        q = query.lower()
        hay = " ".join(
            [
                p.get("name", ""),
                p.get("best_for", ""),
                p.get("notes", ""),
                " ".join(p.get("focus", [])),
                p.get("region", ""),
            ]
        ).lower()
        if q not in hay:
            return False
    return True


def payout_tier(s):
    s = (s or "").lower()
    if "10m" in s or "2m" in s:
        return 3
    if "100k" in s or "50k" in s or "500k" in s:
        return 2
    if "$" in s:
        return 1
    return 0


def score(p, level="", interest="", goal=""):
    sc, why = 0, []
    focus = [f.lower() for f in p.get("focus", [])]
    if interest and interest.lower() in focus:
        sc += 5
        why.append(f"matches {interest}")
    if level == "beginner" and p.get("beginner_friendly"):
        sc += 3
        why.append("beginner-friendly")
    if level == "beginner" and "invite" in p.get("access", ""):
        sc -= 2
        why.append("invite-only")
    if level == "advanced" and not p.get("beginner_friendly"):
        sc += 2
        why.append("pro crowd")
    if level == "advanced" and payout_tier(p.get("payout_range")) >= 2:
        sc += 2
        why.append("high ceiling")
    if goal == "money" and payout_tier(p.get("payout_range")) >= 2:
        sc += 2
        why.append("top payouts")
    if goal == "learning" and p.get("beginner_friendly"):
        sc += 2
        why.append("fast feedback")
    if goal == "portfolio" and "public" in p.get("access", ""):
        sc += 2
        why.append("public entry")
    if "public" in p.get("access", ""):
        sc += 1
    return sc, why


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find bug bounty platforms")
    ap.add_argument(
        "--focus", help="web2, web3, ai, gov, mobile, wordpress, pentest, etc"
    )
    ap.add_argument("--region", help="filter by region, e.g. EU, USA, Japan")
    ap.add_argument("--beginner", action="store_true", help="only beginner-friendly")
    ap.add_argument(
        "--public-only", action="store_true", help="only platforms with public programs"
    )
    ap.add_argument("--search", help="free-text search")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--level", help="beginner|intermediate|advanced (AI rank)")
    ap.add_argument("--interest", help="web2|web3|ai|gov|mobile|wordpress|pentest")
    ap.add_argument("--goal", help="money|learning|portfolio (AI rank)")
    args = ap.parse_args(argv)

    plats = load()
    out = [
        p
        for p in plats
        if match(
            p, args.focus, args.region, args.beginner, args.public_only, args.search
        )
    ]
    ranked = bool(args.level or args.interest or args.goal)
    scored = [
        (p, *score(p, args.level or "", args.interest or "", args.goal or ""))
        for p in out
    ]
    if ranked:
        scored.sort(key=lambda x: x[1], reverse=True)

    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    if not out:
        print("No platforms match. Try --focus web2 / web3 / ai, or drop filters.")
        return 1

    for p, sc, why in scored:
        star = "★" if p.get("beginner_friendly") else " "
        extra = f" score={sc} ({', '.join(why)})" if ranked else ""
        print(f"[{star}] {p['name']} ({p['region']}) [{p['access']}]{extra}")
        print(f"    focus: {', '.join(p['focus'])} | payout: {p['payout_range']}")
        print(f"    best: {p['best_for']}")
        print(f"    programs: {p['programs_url']}")
    print(
        f"\n{len(out)}/{len(plats)} platforms shown. Source: disclose.io + 2026 research."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
