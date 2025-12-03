import io
from typing import Dict, Optional
import pandas as pd
import requests

BASE_URL = "https://data-api.ecb.europa.eu/service/data"

class ECBApiError(Exception):
    """Custom exception for ECB API errors."""
    pass

def fetch_timeseries(
    flow_ref: str,
    key: str,
    start_period: str = "2003-01",
    extra_params: Optional[Dict[str, str]] = None,
) -> pd.DataFrame:
    """
    Fetch a time series from the ECB Data Portal (SDMX CSV) and return a tidy DataFrame
    with columns ['time', 'value'].

    Parameters
    ----------
    flow_ref : str
        Dataset identifier, e.g. 'MIR'.
    key : str
        Full series key inside the dataset.
    start_period : str
        First period to request (e.g. '2003-01').
    extra_params : dict, optional
        Additional query parameters for the API.

    Returns
    -------
    DataFrame
        Columns: 'time' (datetime64[ns]) and 'value' (float).
    """
    url = f"{BASE_URL}/{flow_ref}/{key}"
    headers = {"Accept": "text/csv"}
    params = {
        "startPeriod": start_period,
        "detail": "dataonly",
        "includeHistory": "false",
    }
    if extra_params:
        params.update(extra_params)

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        raise ECBApiError(
            f"ECB API error {resp.status_code} for {url} with params={params}: "
            f"{resp.text[:300]}"
        )

    df = pd.read_csv(io.StringIO(resp.text))

    # Normalise standard SDMX column names
    if "TIME_PERIOD" in df.columns:
        df = df.rename(columns={"TIME_PERIOD": "time"})
    if "OBS_VALUE" in df.columns:
        df = df.rename(columns={"OBS_VALUE": "value"})

    df["time"] = pd.to_datetime(df["time"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.sort_values("time").reset_index(drop=True)
    return df