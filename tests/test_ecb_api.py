import pandas as pd
from ecb_ts_lab.ecb_api import fetch_timeseries


def test_fetch_mir_pt_housing_loans_structure_and_sanity():
    """
    Smoke + sanity test for the ECB API client.

    We verify that:
    - the call succeeds and returns a non-empty DataFrame,
    - the expected columns are present,
    - types are as expected (datetime for time, numeric for value),
    - the sample has a reasonable length,
    - the values are within an economically plausible range.
    """
    # MIR dataset: MFI interest rate statistics
    # Series: Portugal, new loans to households for house purchase, AAR, monthly
    flow = "MIR"
    key = "M.PT.B.A2C.A.R.A.2250.EUR.N"

    df = fetch_timeseries(flow, key, start_period="2020-01")

    # Basic structural assertions
    assert isinstance(df, pd.DataFrame), "fetch_timeseries should return a DataFrame"
    assert not df.empty, "MIR PT housing loans series should not be empty"

    # Required columns
    assert "time" in df.columns, "time column missing from ECB time series"
    assert "value" in df.columns, "value column missing from ECB time series"

    # Type checks
    assert pd.api.types.is_datetime64_any_dtype(
        df["time"]
    ), "time column should be datetime-like"
    assert pd.api.types.is_numeric_dtype(
        df["value"]
    ), "value column should be numeric"

    # Expect at least 12 months of data since 2020
    assert len(df) >= 12, "Too few observations returned for MIR series since 2020"

    # Economic sanity: MIR housing loan rates in recent years should be between 0 and 20%
    v_min = df["value"].min()
    v_max = df["value"].max()

    assert v_min > -1.0, f"Unrealistic negative interest rate detected: {v_min}"
    assert v_max < 20.0, f"Unrealistically high interest rate detected: {v_max}"