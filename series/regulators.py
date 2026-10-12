"""
Parsers for regulator statistics collected by hand (files saved under data/public/raw/central_banks/<ISO3>/).

    python -m series.regulators
"""
import re

import numpy as np
import pandas as pd

from .config import PROC, RAW

def _to_bn(v):
    """OJK's 2019–2020 files report rupiah, except some that already report billions; normalise to IDR billion."""
    v = float(v)
    return v / 1e9 if v > 1e7 else v


MONTHS_ID = {"januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7, "agustus": 8,
             "september": 9, "oktober": 10, "november": 11, "desember": 12}


def _id_month(label):
    """'Desember 2019' / 'Oktober2019' -> Timestamp, else None."""
    m = re.match(r"\s*([A-Za-z]+)\s*(\d{4})", str(label))
    if m and m.group(1).lower() in MONTHS_ID:
        return pd.Timestamp(int(m.group(2)), MONTHS_ID[m.group(1).lower()], 1)
    return None


# ------------------------------------------------------------------ Indonesia: OJK P2P lending (outstanding loans)
def ojk_outstanding():
    """Monthly outstanding P2P (fintech lending) loans, Indonesia, IDR billion.

    Three file layouts:
      * 2019 December file, sheet 'Statistik': row 'Outstanding Pinjaman', months in row 3, values in Rp.
      * 2020 monthly files, sheet 'Outstanding': row '    c. Agregat', months in row 3, values in Rp.
      * 2021+ December files, sheet '9': row 'JUMLAH', dates in row 1, 'Outstanding Pinjaman' column per date,
        values in Rp billion.
    Where two files report the same month, the later file wins (revisions); differences are returned for checking.
    """
    folder = RAW / "central_banks" / "IDN" / "ojk"
    obs = []                                                         # (month, value_bn, file)
    for f in sorted(folder.glob("statistik_*.xlsx")):
        book = pd.read_excel(f, sheet_name=None, header=None, engine="calamine")
        if "Statistik" in book:                                      # 2019 layout
            x = book["Statistik"]
            hdr = x.iloc[3].tolist()
            # the label sits in column 1; the section heading has the same text but no values
            row = next(i for i in range(x.shape[0]) if str(x.iloc[i, 1]).strip().startswith("Outstanding Pinjaman")
                       and pd.notna(pd.to_numeric(x.iloc[i, 2], errors="coerce")))
            for j, h in enumerate(hdr):
                t = _id_month(h)
                if t is not None:
                    obs.append((t, _to_bn(x.iloc[row, j]), f.name))
        elif "Outstanding" in book:                                  # 2020 monthly layout
            x = book["Outstanding"]
            hdr = x.iloc[3].tolist()
            row = next(i for i in range(x.shape[0]) if "Agregat" in str(x.iloc[i, 0]))
            for j, h in enumerate(hdr):
                t = _id_month(h)
                if t is not None:
                    obs.append((t, _to_bn(x.iloc[row, j]), f.name))
        else:                                                        # 2021+ layout
            x = book["9"]
            row = next(i for i in range(x.shape[0]) if str(x.iloc[i, 1]).strip().upper() == "JUMLAH")
            # dates are datetimes, except a few text headers such as '*Jan-22' (asterisk = revised)
            dates = x.iloc[1].map(lambda v: v if hasattr(v, "year") else
                                  pd.to_datetime(str(v).strip("* "), format="%b-%y", errors="coerce")
                                  if pd.notna(v) else pd.NaT).ffill()
            for j in range(x.shape[1]):
                if "Outstanding" in str(x.iloc[2, j]) and pd.notna(dates[j]):
                    t = pd.Timestamp(dates[j].year, dates[j].month, 1)
                    obs.append((t, float(x.iloc[row, j]), f.name))
    # December 2020 is published only in OJK's year-end PDF ("Statistik Fintech Lending Desember 2020", p. 9:
    # outstanding loans Rp 15,319.09 billion), so it is entered by hand
    obs.append((pd.Timestamp(2020, 12, 1), 15319.09, "statistik_2020_12.pdf (manual, p. 9)"))
    d = pd.DataFrame(obs, columns=["month", "outstanding_idr_bn", "file"]).sort_values(["month", "file"])
    # revisions: same month reported in more than one file
    dup = d[d.duplicated("month", keep=False)].groupby("month").outstanding_idr_bn.agg(["min", "max"])
    dup["pct_diff"] = (dup["max"] / dup["min"] - 1) * 100
    s = d.drop_duplicates("month", keep="last").set_index("month").outstanding_idr_bn
    full = pd.date_range(s.index.min(), s.index.max(), freq="MS")
    missing = full.difference(s.index)
    s = s.reindex(full)
    out = pd.DataFrame({"outstanding_idr_bn": s, "interpolated": s.isna()})
    # single missing months are filled by log-linear interpolation and flagged
    out["outstanding_idr_bn"] = np.exp(np.log(out.outstanding_idr_bn).interpolate(limit=1))
    out.index.name = "month"
    return out, dup, list(missing), d


if __name__ == "__main__":
    out, dup, missing, _ = ojk_outstanding()
    out.to_csv(PROC / "idn_ojk_p2p_outstanding_monthly.csv")
    print(f"{len(out)} months {out.index.min():%Y-%m}–{out.index.max():%Y-%m}; interpolated: {[f'{m:%Y-%m}' for m in missing]}")
    print("months reported twice (max % difference):", round(dup.pct_diff.abs().max(), 3) if len(dup) else "none")
