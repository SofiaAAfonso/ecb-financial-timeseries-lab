from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import STL
from .ecb_api import fetch_timeseries

# Dataset: MIR (MFI Interest Rates)
# Series: Portugal, new loans to households for house purchase, AAR, monthly
FLOW = "MIR"
KEY = "M.PT.B.A2C.A.R.A.2250.EUR.N"

def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic quality checks for a monthly time series.
    """
    full_range = pd.date_range(df["time"].min(), df["time"].max(), freq="MS")
    missing_months = sorted(set(full_range) - set(df["time"]))

    return pd.DataFrame(
        [
            {
                "check": "missing_values",
                "value": int(df["value"].isna().sum()),
            },
            {
                "check": "duplicate_timestamps",
                "value": int(df["time"].duplicated().sum()),
            },
            {
                "check": "missing_months",
                "value": len(missing_months),
            },
        ]
    )


def main() -> None:
    # 1) Fetch data from ECB API
    print("Fetching MIR Portugal time series from ECB API…")
    df = fetch_timeseries(FLOW, KEY, start_period="2003-01")

    # 2) Save cleaned series
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    out_path = Path("data/processed/mir_pt_housing_loans.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved processed series to: {out_path}")

    # 3) Generate quality report
    qr = quality_report(df)
    Path("reports/quality").mkdir(parents=True, exist_ok=True)
    qr_path = Path("reports/quality/mir_pt_housing_loans_quality.csv")
    qr.to_csv(qr_path, index=False)
    print(f"Saved quality report to: {qr_path}")

    # 4) Plot raw series
    Path("reports/figures").mkdir(parents=True, exist_ok=True)
    fig_path = Path("reports/figures/mir_pt_housing_loans.png")

    plt.figure(figsize=(8, 4))
    plt.plot(df["time"], df["value"])
    plt.title("Portugal – Housing loan interest rates (MIR)")
    plt.xlabel("Time")
    plt.ylabel("Annualised agreed rate (%)")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Saved time series plot to: {fig_path}")

    # 5) Add year-on-year change
    df = df.copy()
    df["pct_change_12m"] = df["value"].pct_change(12) * 100

    out_growth_path = Path("data/processed/mir_pt_housing_loans_with_growth.csv")
    df.to_csv(out_growth_path, index=False)
    print(f"Saved series with YoY change to: {out_growth_path}")

    # 6) STL decomposition
    y = df["value"].dropna().values

    if len(y) > 24:
        stl = STL(y, period=12, robust=True)
        _ = stl.fit()
        print("STL decomposition completed.")

        # 7) ARIMA example model
        model = ARIMA(y, order=(1, 1, 1))
        fit = model.fit()
        print("\n=== ARIMA(1,1,1) summary ===")
        print(fit.summary())
    else:
        print("Not enough data for STL/ARIMA analysis.")


if __name__ == "__main__":
    main()