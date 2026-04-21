import streamlit as st
import plotly.express as px
from data import build_dataset

##Header
st.set_page_config(page_title="US National Parks Dashboard", layout="wide")

st.title("US National Parks Data")

with st.spinner("Loading data..."):
    df, states_df, exploded, activity_counts = build_dataset()

## Sidebar Section
st.sidebar.header("Filters")

# states filter (only for UI selection)
state_filter = st.sidebar.multiselect(
    "Select State(s)",
    sorted(states_df["states_list"].dropna().unique())
)

# apply filter using stable id
if state_filter:
    filtered_ids = states_df[states_df["states_list"].isin(state_filter)]["id"].unique()
    df = df[df["id"].isin(filtered_ids)]
    exploded = exploded[exploded["id"].isin(filtered_ids)]

activity_counts = (
    exploded["activity"]
    .value_counts()
    .reset_index()
)

activity_counts.columns = ["activity", "count"]

## KPI Section
col1, col2 = st.columns(2)

col1.metric("Total Parks", len(df))
col2.metric("Unique Activities", exploded["activity"].nunique())

## Main Body
st.markdown("""<style>
button[data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
    padding: 12px 24px;
    flex-grow: 1;
    text-align: center;
}
</style>""", unsafe_allow_html=True)

mapTab, activityTab, dataTab = st.tabs(["Map", "Activities", "Data"])


with mapTab:
    st.subheader("National Parks Map")

    info_box = st.container(height=325)

    fig_map = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        color="activity_count",
        color_continuous_scale="bluered",
        scope="usa",
        title="US National Parks by State",
        labels={
            "activity_count": "Activity Count",
            "longitude": "Longitude",
            "latitude": "Latitude"
        }
    )

    fig_map.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        uirevision="keep",
        coloraxis_colorbar=dict(title="Activity Count")
    )

    fig_map.update_traces(marker=dict(size=10))

    event = st.plotly_chart(
        fig_map,
        width="stretch",
        config={"displayModeBar": True},
        on_select="rerun"
    )

    with info_box:
        if event and event.selection and len(event.selection["points"]) > 0:
            selected_index = event.selection["points"][0]["point_index"]
            selected_park = df.iloc[selected_index]
            st.subheader(selected_park["name"])
            st.write("States:", selected_park["states"])
            st.write("Type:", selected_park["designation"])
            st.write("**Activities:**", ", ".join(selected_park["activities"]))
            st.write("Activity Count:", selected_park["activity_count"])
            
        else:
            st.info("Click on a park to see details")


with activityTab:
    
    top_10 = activity_counts.sort_values("count", ascending=False).head(10)

    fig = px.bar(
        top_10,
        x="count",
        y="activity",
        orientation="h",
        color="count",
        color_continuous_scale="bluered",
        title="Top Activities"
    )

    fig.update_yaxes(autorange="reversed", title="Activity")
    fig.update_xaxes(title="Parks offering this activity")

    st.plotly_chart(fig, width="stretch")


with dataTab:
    st.subheader("Park Data")

    display_df = df[["name", "states", "designation", "activities"]].copy()
    display_df["activities"] = display_df["activities"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn("Park Name"),
            "states": st.column_config.TextColumn("States"),
            "designation": st.column_config.TextColumn("Type"),
            "activities": st.column_config.TextColumn("Activities")
        }
    )