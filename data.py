import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["NPS_API_KEY"]
BASE_URL = "https://developer.nps.gov/api/v1/parks"

def fetch_parks(limit=50):
    all_parks = []
    start = 0

    while True:
        params = {
            "api_key": API_KEY,
            "limit": limit,
            "start": start
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        parks = data.get("data", [])
        if not parks:
            break

        all_parks.extend(parks)

        if len(parks) < limit:
            break

        start += limit

    return all_parks

def transform_parks(parks):
    return [
        {
            "id": p.get("id"),
            "name": p.get("fullName"),
            "states": p.get("states"),
            "designation": p.get("designation"),
            "activities": [a.get("name", "") for a in p.get("activities", [])],
            "latitude": p.get("latitude"),
            "longitude": p.get("longitude")
        }
        for p in parks
    ]

@st.cache_data(ttl=3600)
def build_dataset():
    parks = fetch_parks()
    df = pd.DataFrame(transform_parks(parks))

    ## Base dataframe (clean source of truth)
    df["activity_count"] = df["activities"].apply(len)

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df = df.dropna(subset=["latitude", "longitude"])
    df = df.reset_index(drop=True)

    ## States dataframe (for filtering)
    states_df = df[["id", "states"]].copy()
    states_df["states_list"] = states_df["states"].str.split(",")
    states_df = states_df.explode("states_list")
    states_df["states_list"] = states_df["states_list"].str.strip()

    ## Activities dataframe (for charts)
    activities_df = df[["id", "name", "activities"]].copy()
    activities_df = activities_df.explode("activities")
    activities_df = activities_df.rename(columns={"activities": "activity"})

    activities_df = activities_df[
        activities_df["activity"].notna() &
        (activities_df["activity"] != "")
    ]

    activity_counts = (
        activities_df["activity"]
        .value_counts()
        .reset_index()
    )
    activity_counts.columns = ["activity", "count"]

    return df, states_df, activities_df, activity_counts