from pathlib import Path
import pandas as pd
from .ecb_api import fetch_timeseries

FLOW = "MIR"
KEY = "M.PT.B.A2C.A.R.A.2250.EUR.N"

def main() -> None:
    df = fetch_timeseries(FLOW, KEY, start_period="2003-01")

    # Basic info
    print("=== MIR PT – Housing loans (new business, AAR) ===")
    print(f"Number of observations: {len(df)}")
    print(f"Time range: {df['time'].min().date()} → {df['time'].max().date()}")
    print()

    # Descriptive stats
    print("=== Descriptive statistics on interest rate (%) ===")
    print(df["value"].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]))
    print()

    # Last few points
    print("=== Last 6 observations ===")
    print(df.tail(6).to_string(index=False))

    # Save a copy for inspection if needed
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/processed/mir_pt_full_describe.csv", index=False)
    print("\nSaved full series to data/processed/mir_pt_full_describe.csv")


if __name__ == "__main__":
    main()