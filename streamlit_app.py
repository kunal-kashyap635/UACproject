import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.data_loader import load_clean_data
from src.metrics import compute_system_metrics
from src.trends import compute_rolling_metrics, detect_stress_window


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="UAC Capacity Analytics", layout="wide")
st.title("System Capacity & Care Load Analytics")
st.markdown("Interactive Monitoring Dashboard for UAC Care System")


# =====================================================
# LOAD DATA
# =====================================================
DATA_PATH = "data/processed/clean_children_data.csv"
df = load_clean_data(DATA_PATH)
df = compute_system_metrics(df)


# =====================================================
# SIDEBAR CONTROLS
# =====================================================
st.sidebar.header("Dashboard Controls")

start_date = st.sidebar.date_input("Start Date", value=df["date"].min())
end_date = st.sidebar.date_input("End Date", value=df["date"].max())

short_window = st.sidebar.slider("Rolling Window (Short)", 3, 14, 7)
long_window = st.sidebar.slider("Rolling Window (Long)", 7, 30, 14)

granularity = st.sidebar.selectbox("Time Granularity", ["Daily", "Weekly", "Monthly"])


# =====================================================
# FILTER DATA
# =====================================================
mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))

filtered_df = df.loc[mask].copy()
filtered_df = compute_rolling_metrics(filtered_df, short_window, long_window)
filtered_df = detect_stress_window(filtered_df)

# Time aggregation
if granularity == "Weekly":
    filtered_df = (
        filtered_df.resample("W", on="date").mean(numeric_only=True).reset_index()
    )
elif granularity == "Monthly":
    filtered_df = (
        filtered_df.resample("ME", on="date").mean(numeric_only=True).reset_index()
    )

# Update the stress detection logic for weekly and Monthly
filtered_df["stress_window"] = (filtered_df["net_daily_intake"] > 0) & (
    filtered_df["total_system_load"] > filtered_df["total_system_load"].median()
)


# =====================================================
# KPI SECTION
# =====================================================
st.subheader("KPI Summary Cards")

latest_total_load = int(filtered_df["total_system_load"].iloc[-1])
avg_net_intake = filtered_df["net_daily_intake"].mean()
volatility_index = filtered_df["load_volatility"].mean()
backlog_rate = ((filtered_df["net_daily_intake"] > 0).sum() / len(filtered_df)) * 100
avg_discharge_offset = filtered_df["discharge_offset_ratio"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Children Under Care", latest_total_load)
col2.metric("Net Intake Pressure (Avg)", f"{avg_net_intake:.0f}")
col3.metric("Care Load Volatility Index", f"{volatility_index:.2f}")
col4.metric("Backlog Accumulation Rate", f"{backlog_rate:.1f}%")
col5.metric("Discharge Offset Ratio", f"{avg_discharge_offset:.2f}")


# =====================================================
# CHART PANEL — Tab switcher
# =====================================================
tab_load, tab_comp, tab_net, tab_stress = st.tabs(
    [
        "📈 Total Load",
        "⚖️ CBP vs HHS Comparison",
        "📊 Net Intake & Backlog",
        "🚨 Stress Detection",
    ]
)


# --- Tab 1: System Load Overview ---
with tab_load:
    st.subheader("System Load Overview")

    fig_load = go.Figure()

    fig_load.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["total_system_load"],
            mode="lines",
            name="Daily Load",
            line=dict(color="lightgray"),
        )
    )

    if granularity == "Daily":
        fig_load.add_trace(
            go.Scatter(
                x=filtered_df["date"],
                y=filtered_df[f"total_load_{short_window}d_avg"],
                mode="lines",
                name=f"{short_window}-Day Avg",
                line=dict(color="blue", width=3),
            )
        )

    fig_load.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_load, width="stretch")


# --- Tab 2: CBP vs HHS Load Comparison ---
with tab_comp:
    st.subheader("CBP vs HHS Load Comparison")

    fig_comp = go.Figure()

    fig_comp.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["cbp_custody"],
            mode="lines",
            name="CBP Custody",
        )
    )

    fig_comp.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["hhs_care"],
            mode="lines",
            name="HHS Care",
        )
    )

    fig_comp.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_comp, width="stretch")


# --- Tab 3: Net Intake & Backlog Trends ---
with tab_net:
    st.subheader("Net Intake & Backlog Trends")

    fig_net = go.Figure()

    fig_net.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["net_daily_intake"],
            mode="lines",
            name="Net Intake",
        )
    )

    fig_net.add_hline(y=0, line_dash="dash")

    fig_net.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_net, width="stretch")


# --- Tab 4: Capacity Stress Detection ---
with tab_stress:
    st.subheader("Capacity Stress Detection")

    fig_stress = go.Figure()

    fig_stress.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["total_system_load"],
            mode="lines",
            name="Total Load",
        )
    )

    fig_stress.add_trace(
        go.Scatter(
            x=filtered_df[filtered_df["stress_window"]]["date"],
            y=filtered_df[filtered_df["stress_window"]]["total_system_load"],
            mode="markers",
            marker=dict(color="red", size=6),
            name="Stress Period",
        )
    )

    fig_stress.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_stress, width="stretch")
