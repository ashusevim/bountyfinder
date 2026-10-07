# Bounty Platforms Finder

Find bug bounty *platforms* where you can hunt programs. Not programs themselves — the directories that host them.

Data: 29 curated platforms from disclose.io (122 total) + 2026 payout/beginner research.

## Use

CLI:
```
python3 finder.py --focus web3 --public-only
python3 finder.py --beginner --public-only
python3 finder.py --search japan
python3 finder.py --focus ai
```

Web:
```
python3 -m http.server 8000
# open index.html -> filter by focus/beginner/search
```

Full list source: https://disclose.io/platforms/
