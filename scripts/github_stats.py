"""Generate assets/stats-{dark,light}.svg (contribution numbers and streaks) from live GitHub data.

Run by .github/workflows/stats.yml on a schedule, which publishes to the `output` branch. Locally:  python3 scripts/github_stats.py
Needs a token in GH_TOKEN or GITHUB_TOKEN (falls back to `gh auth token`).
"""

import json
import os
import subprocess
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from build_assets import MONO, OUT, SANS, THEMES, svg

USER = "mali-anjum"

YEAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    createdAt
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

def token():
    t = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if t:
        return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def gql(query, tok, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]["user"]


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch():
    tok = token()
    now = datetime.now(timezone.utc)
    recent = gql(YEAR_QUERY, tok, login=USER, **{"from": iso(now - timedelta(days=365)), "to": iso(now)})
    created = datetime.fromisoformat(recent["createdAt"].replace("Z", "+00:00"))

    # All-time: one collection per calendar year (the API caps a range at one year).
    days = {}
    for year in range(created.year, now.year + 1):
        start = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        end = min(now, datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        cal = gql(YEAR_QUERY, tok, login=USER, **{"from": iso(start), "to": iso(end)})
        for w in cal["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    cc = recent["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    return dict(
        created=created.date(),
        year_total=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"],
        active=sum(1 for w in weeks for d in w["contributionDays"] if d["contributionCount"]),
        all_total=sum(days.values()),
        **streaks(days),
    )


def streaks(days):
    ordered = sorted(days)
    longest = (0, None, None)
    run, run_start = 0, None
    for ds in ordered:
        if days[ds]:
            run_start = run_start if run else ds
            run += 1
            if run > longest[0]:
                longest = (run, run_start, ds)
        else:
            run = 0
    # Current streak: ends today, or yesterday if nothing has landed yet today.
    i = len(ordered) - 1
    if i >= 0 and not days[ordered[i]]:
        i -= 1
    cur_end, cur = (ordered[i] if i >= 0 else None), 0
    while i >= 0 and days[ordered[i]]:
        cur, i = cur + 1, i - 1
    cur_start = ordered[i + 1] if cur else None
    return dict(cur=cur, cur_range=(cur_start, cur_end if cur else None),
                longest=longest[0], longest_range=(longest[1], longest[2]))


def fmt_day(ds, with_year=False):
    d = date.fromisoformat(ds) if isinstance(ds, str) else ds
    return d.strftime("%b %-d, %Y" if with_year else "%b %-d")


def rng(r):
    return f"{fmt_day(r[0])} – {fmt_day(r[1])}" if r[0] else "–"


FLAME = ("M12 2c1 3 4 4.5 4 8.5A4 4 0 0 1 8 10.5c0-1.6.8-2.8 1.6-3.6.2 1.4 1 2.1 1.8 2.3C11 7 11 4.5 12 2z")


def render(c, s):
    W, H = 1200, 280
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{c["panel"]}" stroke="{c["border"]}"/>']

    # left: last-12-months numbers
    b.append(f'<rect x="24" y="24" width="560" height="232" rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    b.append(f'<text x="52" y="65" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="2" fill="{c["amber"]}">GITHUB · LAST 12 MONTHS</text>')
    b.append(f'<rect x="52" y="75" width="36" height="3" rx="1.5" fill="{c["amber"]}"/>')
    cells = [(s["year_total"], "CONTRIBUTIONS"), (s["commits"], "COMMITS"),
             (s["prs"], "PULL REQUESTS"), (s["active"], "ACTIVE DAYS")]
    for i, (v, lbl) in enumerate(cells):
        x, y = 52 + (i % 2) * 270, 129 + (i // 2) * 74
        b.append(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="36" font-weight="700" fill="{c["text"]}">{v:,}</text>')
        b.append(f'<text x="{x}" y="{y+22}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{c["muted"]}">{lbl}</text>')

    # right: streaks
    b.append(f'<rect x="604" y="24" width="572" height="232" rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    cols = [(700, f'{s["all_total"]:,}', "Total contributions", f'{fmt_day(s["created"], True)} – Present'),
            (1080, f'{s["longest"]}', "Longest streak", rng(s["longest_range"]))]
    for x, v, lbl, sub in cols:
        b.append(f'<text x="{x}" y="132" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="700" fill="{c["text"]}">{v}</text>')
        b.append(f'<text x="{x}" y="168" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{c["text"]}">{lbl}</text>')
        b.append(f'<text x="{x}" y="194" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{c["muted"]}">{sub}</text>')
    for x in (795, 985):
        b.append(f'<line x1="{x}" y1="68" x2="{x}" y2="212" stroke="{c["border"]}"/>')
    cx, cy, r = 890, 116, 46
    circ = 2 * 3.14159 * r
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["teal"]}" stroke-width="6" '
             f'stroke-dasharray="{circ-34:.1f} 34" transform="rotate({-90+ (34/circ)*180:.2f} {cx} {cy})" stroke-linecap="round"/>')
    b.append(f'<path transform="translate({cx-11} {cy-r-13}) scale(0.92)" d="{FLAME}" fill="{c["amber"]}"/>')
    b.append(f'<text x="{cx}" y="{cy+12}" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="700" fill="{c["text"]}">{s["cur"]}</text>')
    b.append(f'<text x="{cx}" y="{cy+76}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{c["teal"]}">Current streak</text>')
    b.append(f'<text x="{cx}" y="{cy+100}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{c["muted"]}">{rng(s["cur_range"])}</text>')

    title = (f'{s["year_total"]:,} contributions in the last year, {s["all_total"]:,} total, '
             f'current streak {s["cur"]} days, longest {s["longest"]} days')
    return svg(W, H, "".join(b), title)


def main():
    stats = fetch()
    out = Path(os.environ.get("STATS_OUT", OUT))  # CI writes to dist/ for the output branch
    out.mkdir(parents=True, exist_ok=True)
    for theme, c in THEMES.items():
        (out / f"stats-{theme}.svg").write_text(render(c, stats), encoding="utf-8")
    print(stats)


if __name__ == "__main__":
    main()
