"""
Cached fetchers for the public sources.

Each fetcher writes under data/public/raw/<source>/ and reuses the file if it exists, so re-running a notebook never
re-downloads. Delete a file to force a refresh.

    python -m series.fetch imf_fas
"""
import io
import sys
import time

import pandas as pd
import requests

from .config import COUNTRIES, FINDEX_INDICATORS, IMF_FAS_INDICATORS, RAW, USER_AGENT, WB_INDICATORS

S = requests.Session()
S.headers["User-Agent"] = USER_AGENT


def _path(source, name):
    d = RAW / source
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def _get(url, params=None, tries=5, timeout=120, **kw):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=timeout, **kw)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(10 * 2 ** i)
                continue
            return r
        except requests.RequestException:
            time.sleep(5 * 2 ** i)
    raise RuntimeError(f"failed after {tries} tries: {url}")


# ------------------------------------------------------------------ IMF Financial Access Survey
def fetch_imf_fas(countries=tuple(COUNTRIES)):
    """Digital-finance outcomes (mobile money, mobile/internet banking) from the IMF FAS, 2004 onward."""
    f = _path("imf_fas", "fas.parquet")
    if f.exists():
        return pd.read_parquet(f)
    key = "+".join(countries) + ".*.*.*"
    r = _get(f"https://api.imf.org/external/sdmx/2.1/data/IMF.STA,FAS,5.0.0/{key}",
             params={"startPeriod": 2004},
             headers={"Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=300)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.text), low_memory=False)
    d = d[d.INDICATOR.isin(IMF_FAS_INDICATORS)]
    # some codes are published twice (domestic currency AND % of GDP / per adult); keep the scaled version only
    d = d[~d.SERIES_NAME.str.contains("Domestic currency", na=False)]
    assert not d.duplicated(["COUNTRY", "INDICATOR", "TIME_PERIOD"]).any(), "duplicate FAS rows after filtering"
    df = pd.DataFrame(dict(iso3=d.COUNTRY, year=d.TIME_PERIOD.astype(int),
                           indicator=d.INDICATOR.map(IMF_FAS_INDICATORS), value=d.OBS_VALUE.astype(float)))
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ World Bank (WDI + Findex)
def _wb(indicators, source=None, years="2000:2025"):
    codes = ";".join(COUNTRIES)
    rows = []
    for code, name in indicators.items():
        params = {"format": "json", "date": years, "per_page": 2000}
        if source:
            params["source"] = source
        r = _get(f"https://api.worldbank.org/v2/country/{codes}/indicator/{code}", params=params)
        js = r.json()
        for row in (js[1] if len(js) > 1 and js[1] else []):
            if row["value"] is not None:
                rows.append(dict(iso3=row["countryiso3code"] or row["country"]["id"], year=int(row["date"]),
                                 indicator=name, value=float(row["value"])))
    return pd.DataFrame(rows)


def fetch_worldbank():
    """WDI denominators and context for the 11 SEA countries."""
    f = _path("worldbank", "wdi.parquet")
    if f.exists():
        return pd.read_parquet(f)
    df = _wb(WB_INDICATORS)
    df.to_parquet(f)
    return df


def fetch_findex():
    """Global Findex survey indicators (World Bank source 28). Only survey years have values."""
    f = _path("worldbank", "findex.parquet")
    if f.exists():
        return pd.read_parquet(f)
    df = _wb(FINDEX_INDICATORS, source=28, years="2011:2025")
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ IMF World Economic Outlook
def fetch_imf_weo_gdp():
    """Nominal GDP in current US$ billions (IMF WEO, NGDPD). Denominator for GMV as % of GDP."""
    f = _path("imf_weo", "ngdpd.parquet")
    if f.exists():
        return pd.read_parquet(f)
    # this endpoint rejects custom user-agents and ignores country filters, so fetch all and filter
    r = requests.get("https://www.imf.org/external/datamapper/api/v1/NGDPD", timeout=120)
    vals = r.json()["values"]["NGDPD"]
    df = pd.DataFrame([dict(iso3=c, year=int(y), gdp_usd_b=float(v))
                       for c, ys in vals.items() if c in COUNTRIES for y, v in ys.items()])
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ Reachability check
def http_status(url):
    """Status code and content type of a landing page, for sources that need manual collection."""
    try:
        r = S.get(url, timeout=45, allow_redirects=True, stream=True)
        r.close()
        return r.status_code, r.headers.get("Content-Type", "").split(";")[0]
    except requests.RequestException as e:
        return None, type(e).__name__


FETCHERS = {"imf_fas": fetch_imf_fas, "worldbank": fetch_worldbank, "findex": fetch_findex,
            "imf_weo": fetch_imf_weo_gdp}

if __name__ == "__main__":
    FETCHERS[sys.argv[1]]()
    print(f"[{sys.argv[1]}] done", flush=True)
