"""
Gold / FTSE 100 — Liquidity Rotation Signal
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# ── CONFIG ────────────────────────────────────────────────────────────────────
WINDOW       = 30    # rolling correlation window (trading days)
LOOKBACK     = 2     # years of history
EXPORT_CSV   = True  # set False to skip CSV export

# Thresholds
STRONG_NEG  = -0.50   # below this   → Strong Negative
WEAKENING   = -0.25   # below this   → Weakening
NEUTRAL     =  0.00   # below this   → Neutral
POSITIVE    =  0.25   # below this   → Positive
                      # above 0.25   → Strong Positive
# ─────────────────────────────────────────────────────────────────────────────

def fetch_data():
    start = datetime.today() - timedelta(days=LOOKBACK * 365 + 30)

    raw_gold = yf.download("GC=F",  start=start, progress=False)
    raw_ftse = yf.download("^FTSE", start=start, progress=False)

    # Flatten multi-level columns if present (yfinance >= 0.2.x)
    if isinstance(raw_gold.columns, pd.MultiIndex):
        raw_gold.columns = raw_gold.columns.get_level_values(0)
    if isinstance(raw_ftse.columns, pd.MultiIndex):
        raw_ftse.columns = raw_ftse.columns.get_level_values(0)

    gold = raw_gold["Close"].squeeze()
    ftse = raw_ftse["Close"].squeeze()

    gold.index = pd.to_datetime(gold.index).tz_localize(None)
    ftse.index = pd.to_datetime(ftse.index).tz_localize(None)

    df = pd.DataFrame({"Gold": gold, "FTSE": ftse}).dropna()
    return df

def compute(df):
    df["Gold_ret"] = df["Gold"].pct_change()
    df["FTSE_ret"] = df["FTSE"].pct_change()
    df["Corr"]     = df["Gold_ret"].rolling(WINDOW).corr(df["FTSE_ret"])
    return df.dropna(subset=["Corr"])

def signal(corr):
    if corr < STRONG_NEG:
        return (
            "⚫  STRONG NEGATIVE",
            "Strong negative correlation. Stay on safety. Flight-to-gold active."
        )
    elif corr < WEAKENING:
        return (
            "🔴  WEAKENING",
            "Weakening negative correlation. Approaching zone of interest."
        )
    elif corr < NEUTRAL:
        return (
            "🟡  NEUTRAL",
            "Neutral correlation. Ready for potential rotation signal."
        )
    elif corr < POSITIVE:
        return (
            "🟠  POSITIVE",
            "Positive correlation. Liquidity returning to the system."
        )
    else:
        return (
            "🟢  STRONG POSITIVE",
            "Strong positive correlation. Confirmed rotation signal — Gold → Equities."
        )

def main():
    print("Fetching data...")
    df   = compute(fetch_data())
    last = df.iloc[-1]
    corr = float(last["Corr"])
    label, description = signal(corr)

    print("\n" + "="*55)
    print(f"  GOLD / FTSE LIQUIDITY SIGNAL  —  {df.index[-1].date()}")
    print("="*55)
    print(f"  Gold (GC=F)  : ${float(last['Gold']):,.2f}")
    print(f"  FTSE 100     : {float(last['FTSE']):,.2f}")
    print(f"\n  {WINDOW}-day Correlation : {corr:+.4f}")
    print(f"\n  {label}")
    print(f"  {description}")

    prev_vals = {
        "Yesterday" : df.iloc[-2]["Corr"],
        "1 week ago": df.iloc[-6]["Corr"]  if len(df) >= 6  else None,
        "1 month ago":df.iloc[-22]["Corr"] if len(df) >= 22 else None,
    }
    print("\n  History:")
    for lbl, val in prev_vals.items():
        if val is not None:
            v = float(val)
            l, _ = signal(v)
            print(f"    {lbl:<12}: {v:+.4f}  {l}")

    print(f"\n  Scale:")
    print(f"    ⚫ Strong Negative  corr < {STRONG_NEG}")
    print(f"    🔴 Weakening        corr < {WEAKENING}")
    print(f"    🟡 Neutral          corr < {NEUTRAL}")
    print(f"    🟠 Positive         corr < {POSITIVE}")
    print(f"    🟢 Strong Positive  corr >= {POSITIVE}")
    print("="*55 + "\n")

    if EXPORT_CSV:
        out = "../data/output/gold_ftse_signal.csv"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        df[["Gold", "FTSE", "Corr"]].to_csv(out)
        print(f"[CSV] Exported → {out}\n")

if __name__ == "__main__":
    main()
