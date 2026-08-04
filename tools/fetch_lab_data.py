"""Download the public datasets the labs run on, into labs/data/.

Why datasets are downloaded ahead of the class, not fetched live:

  * catalog.data.gov retired its CKAN Action API in 2026 and the rebuilt catalog
    exposes **no JSON API at all** — every /api/* path returns 404 (verified
    2026-08-01). Search is HTML-only. So "query data.gov live" is no longer a
    thing a lab can rely on.
  * Agency portals (Socrata) *do* still serve JSON/CSV, but classroom networks
    are unreliable and several agencies rate-limit.

Every file here is public-domain US government data, which satisfies the course's
public-or-synthetic-data-only rule by construction.

Run:  python tools/fetch_lab_data.py [--force]
"""
import csv
import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "labs" / "data"
UA = {"User-Agent": "LearningTree-1258-courseware/1.0"}

# name -> (url, kind, row cap, description used in the manifest)
SOURCES = {
    "federal_ai_use_cases.csv": (
        "https://raw.githubusercontent.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/"
        "main/Data/2025_individually_reported_AI_use_cases.csv",
        "csv", 1200,
        "OMB 2025 Federal Agency AI Use Case Inventory — individually reported use cases "
        "(3,611 across 56 agencies; capped here). The course's own subject matter, as data.",
    ),
    "federal_ai_cots.csv": (
        "https://raw.githubusercontent.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/"
        "main/Data/2025_consolidated_COTS_AI_use_cases.csv",
        "csv", 0,
        "OMB 2025 inventory — consolidated commercial off-the-shelf AI use cases.",
    ),
    "chicago_311.csv": (
        "https://data.cityofchicago.org/resource/v6vf-nfxy.csv?$limit=4000"
        "&$order=created_date%20DESC",
        "csv", 0,
        "City of Chicago 311 service requests (Socrata). Deliberately messy real data: "
        "blank fields, inconsistent casing, duplicate rows — the data-quality lab.",
    ),
    "cdc_flu_wastewater.csv": (
        "https://data.cdc.gov/resource/ymmh-divb.csv?$limit=3000",
        "csv", 0,
        "CDC wastewater surveillance for Influenza A — time series by site. The real "
        "version of the early-warning story told in Chapter 2.",
    ),
    "epa_aqi_by_county.csv": (
        "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2024.zip",
        "zip", 0,
        "EPA Annual Air Quality Index by county, 2024 — clean, small, national. Good "
        "for grouping, ranking and charting.",
    ),
    "nyc_air_quality.csv": (
        "https://data.cityofnewyork.us/resource/c3uy-2p5r.csv?$limit=3000",
        "csv", 0,
        "NYC air quality surveillance (PM2.5 and related indicators) by neighbourhood "
        "and time period — a tidy long-format table for pivots and trend questions.",
    ),
}

# NOTE on text corpora: CFPB's complaint API and bulk download both return 403 to
# automated clients (verified 2026-08-01), so the free-text corpus for the NLP,
# classification and RAG labs comes from two shipped sources instead:
#   * federal_ai_use_cases.csv — the 'Purpose'/'Outputs' columns are rich free text
#   * labs/data/corpus/*.md    — four synthetic agency policy documents


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cap_csv(raw, max_rows):
    """Keep the header plus max_rows data rows (0 = keep everything)."""
    if not max_rows:
        return raw
    text = raw.decode("utf-8", "replace")
    rdr = csv.reader(io.StringIO(text))
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    for i, row in enumerate(rdr):
        if i > max_rows:
            break
        w.writerow(row)
    return out.getvalue().encode("utf-8")


def main(force=False):
    DATA.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, (url, kind, cap, desc) in SOURCES.items():
        dest = DATA / name
        if dest.exists() and not force:
            print(f"  = {name} (exists, {dest.stat().st_size:,} b) — use --force to refresh")
            manifest.append({"file": name, "url": url, "description": desc,
                             "bytes": dest.stat().st_size})
            continue
        try:
            raw = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  ! {name}: FETCH FAILED ({e}) — lab must use its shipped fallback")
            continue
        if kind == "zip":
            import zipfile
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                inner = next(n for n in z.namelist() if n.lower().endswith(".csv"))
                raw = cap_csv(z.read(inner), cap)
            rows = raw.count(b"\n") - 1
        elif kind == "csv":
            raw = cap_csv(raw, cap)
            rows = raw.count(b"\n") - 1
        else:
            try:
                obj = json.loads(raw)
                hits = obj.get("hits", {}).get("hits", obj) if isinstance(obj, dict) else obj
                raw = json.dumps(hits, indent=1).encode()
                rows = len(hits)
            except json.JSONDecodeError:
                rows = 0
        dest.write_bytes(raw)
        print(f"  + {name}: {len(raw):,} bytes, ~{rows} records")
        manifest.append({"file": name, "url": url, "description": desc, "bytes": len(raw)})

    (DATA / "MANIFEST.json").write_text(json.dumps(
        {"note": "Public US government data, downloaded for offline classroom use. "
                 "catalog.data.gov has no JSON API as of 2026-08-01; these come from "
                 "agency portals and the OMB GitHub mirror.",
         "retrieved": "2026-08-01",
         "datasets": manifest}, indent=2))
    print(f"\n  manifest: {DATA/'MANIFEST.json'} ({len(manifest)} datasets)")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
