"""Interactive bike shop sales dashboard.

Run:  streamlit run dashboard/app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data" / "orders.csv"

st.set_page_config(page_title="Bike Shop Sales Dashboard", layout="wide")
st.title("🚲 Bike Shop Sales Dashboard")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["order_date"])
    df["net_revenue"] = df["revenue"] * (1 - df["returned"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


df = load_data()

# ---- sidebar filters ----
st.sidebar.header("Filters")
cats = sorted(df["category"].unique())
sel_cats = st.sidebar.multiselect("Category", cats, default=cats)
channels = sorted(df["channel"].unique())
sel_channels = st.sidebar.multiselect("Channel", channels, default=channels)

fdf = df[df["category"].isin(sel_cats) & df["channel"].isin(sel_channels)]
kept = fdf[fdf["returned"] == 0]

# ---- KPIs ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Net revenue", f"${fdf['net_revenue'].sum():,.0f}")
c2.metric("Orders", f"{len(fdf):,}")
c3.metric("Avg order value", f"${kept['revenue'].mean():,.0f}" if len(kept) else "—")
c4.metric("Return rate", f"{fdf['returned'].mean():.1%}")

# ---- monthly trend ----
monthly = fdf.groupby("month", as_index=False)["net_revenue"].sum()
fig_trend = px.line(monthly, x="month", y="net_revenue",
                    title="Net revenue by month",
                    labels={"month": "Month", "net_revenue": "Net revenue ($)"})
fig_trend.update_xaxes(tickangle=45)
st.plotly_chart(fig_trend, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    by_cat = fdf.groupby("category", as_index=False)["net_revenue"].sum() \
                .sort_values("net_revenue", ascending=False)
    st.plotly_chart(
        px.bar(by_cat, x="category", y="net_revenue",
               title="Net revenue by category",
               labels={"category": "Category", "net_revenue": "Net revenue ($)"}),
        use_container_width=True)

    by_brand = fdf.groupby("brand", as_index=False)["net_revenue"].sum() \
                  .sort_values("net_revenue", ascending=False).head(10)
    st.plotly_chart(
        px.bar(by_brand, x="net_revenue", y="brand", orientation="h",
               title="Top 10 brands by net revenue",
               labels={"brand": "Brand", "net_revenue": "Net revenue ($)"}),
        use_container_width=True)

with col_b:
    ret_cat = fdf.groupby("category", as_index=False)["returned"].mean() \
                 .sort_values("returned", ascending=False)
    st.plotly_chart(
        px.bar(ret_cat, x="category", y="returned",
               title="Return rate by category",
               labels={"category": "Category", "returned": "Return rate"}),
        use_container_width=True)

    by_channel = fdf.groupby("channel", as_index=False)["net_revenue"].sum()
    st.plotly_chart(
        px.pie(by_channel, names="channel", values="net_revenue",
               title="Net revenue by channel"),
        use_container_width=True)

st.caption("Synthetic demo data — replace data/orders.csv with a real export to use live.")
