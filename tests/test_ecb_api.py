import pandas as pd
from ecb_ts_lab.ecb_api import fetch_timeseries

def test_fetch_mir_pt_housing_loans():
    """
    Smoke test:
    Verify that the ECB API client returns a non-empty DataFrame
    with the expected columns for a known MIR series.
    """
    flow = "MIR"
    key = "M.PT.B.A2C.A.R.A.2250.EUR.N"

    df = fetch_timeseries(flow, key, start_period="2020-01")

    # Basic structural assertions
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "time" in df.columns
    assert "value" in df.columns

    # Sanity check on types
    assert pd.api.types.is_datetime64_any_dtype(df["time"])
    assert pd.api.types.is_numeric_dtype(df["value"])