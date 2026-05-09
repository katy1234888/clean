import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import plotly.express as px

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# -------------------------------
# STATE MANAGEMENT
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0

def next_page():
    st.session_state.page += 1

# -------------------------------
# PAGE 0: STORY INTRO
# -------------------------------
if st.session_state.page == 0:

    st.title("📦 Seashells Logistics - Case Story")

    st.markdown("""
    ## 📖 Background & Business Context

    Festive surge caused operational stress leading to:
    - Declining NPS
    - Increased complaints
    - Higher RTO
    - Drop in repeat users
    """)

    if st.button("➡️ Start Analysis"):
        next_page()

# -------------------------------
# PAGE 1: DATA ENGINE
# -------------------------------
elif st.session_state.page == 1:

    st.title("📊 Data Upload & Exploration")

    st.sidebar.header("Upload Datasets")

    orders_file = st.sidebar.file_uploader("Orders", type=["csv"])
    customers_file = st.sidebar.file_uploader("Customers", type=["csv"])
    nps_file = st.sidebar.file_uploader("NPS", type=["csv"])
    complaints_file = st.sidebar.file_uploader("Complaints", type=["csv"])
    hub_file = st.sidebar.file_uploader("Hub", type=["csv"])
    courier_file = st.sidebar.file_uploader("Courier", type=["csv"])

    def load_data(file):
        return pd.read_csv(file)

    def clean_data(df):
        df = df.copy()
        num = df.select_dtypes(include=np.number).columns
        cat = df.select_dtypes(exclude=np.number).columns

        if len(num):
            df[num] = IterativeImputer().fit_transform(df[num])
        if len(cat):
            df[cat] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat])

        return df

    datasets = {}

    if orders_file: datasets["Orders"] = load_data(orders_file)
    if customers_file: datasets["Customers"] = load_data(customers_file)
    if nps_file: datasets["NPS"] = load_data(nps_file)
    if complaints_file: datasets["Complaints"] = load_data(complaints_file)
    if hub_file: datasets["Hub"] = load_data(hub_file)
    if courier_file: datasets["Courier"] = load_data(courier_file)

    # ✅ SESSION FIX
    st.session_state.datasets = datasets

    if datasets:
        st.success("Datasets Loaded")

    if st.toggle("Enable Cleaning"):
        for k in datasets:
            datasets[k] = clean_data(datasets[k])
        st.success("Data Cleaned")

    if st.button("➡️ Basic Insights"):
        next_page()

# -------------------------------
# PAGE 2: BASIC Q&A
# -------------------------------
elif st.session_state.page == 2:

    st.title("📊 Basic Insights")

    data = st.session_state.get("datasets", {})

    if "Orders" in data:
        df = data["Orders"]

        st.subheader("Order Status Distribution")
        st.plotly_chart(px.pie(df, names="order_status"))

        st.subheader("Orders by City")
        st.plotly_chart(px.bar(df["city"].value_counts().reset_index(),
                               x="index", y="city"))

    if st.button("➡️ Advanced Analysis Story"):
        next_page()

# -------------------------------
# PAGE 3: FULL CASE STUDY ANSWERS
# -------------------------------
elif st.session_state.page == 3:

    st.title("📈 Advanced Insights Story (Case Study Answers)")

    data = st.session_state.get("datasets", {})

    if not all(k in data for k in ["Orders","Customers","NPS","Complaints","Hub","Courier"]):
        st.warning("Upload all datasets first")
    else:

        orders = data["Orders"]
        nps = data["NPS"]
        cust = data["Customers"]
        comp = data["Complaints"]
        hub = data["Hub"]
        courier = data["Courier"]

        # -------------------------------
        # NPS
        # -------------------------------
        st.header("📊 NPS Analysis")

        promoters = nps[nps.score >= 9].shape[0]
        detractors = nps[nps.score <= 6].shape[0]
        total = len(nps)

        overall_nps = ((promoters - detractors) / total) * 100

        st.metric("Overall NPS", round(overall_nps,2))

        nps["date"] = pd.to_datetime(nps["response_date"])
        nps["month"] = nps["date"].dt.to_period("M")

        trend = nps.groupby("month").size().reset_index(name="count")
        st.plotly_chart(px.line(trend, x="month", y="count", title="NPS Trend"))

        merged = nps.merge(cust, on="customer_id")
        seg = merged.groupby("segment").size().reset_index(name="count")
        st.plotly_chart(px.bar(seg, x="segment", y="count"))

        # -------------------------------
        # DELAYS
        # -------------------------------
        st.header("🚚 Delivery Performance")

        orders["delay"] = pd.to_datetime(orders["delivery_date"]) - pd.to_datetime(orders["promised_date"])
        orders["delay_days"] = orders["delay"].dt.days

        st.plotly_chart(px.histogram(orders, x="delay_days"))

        orders["sla"] = orders["delay_days"] > 0
        st.plotly_chart(px.bar(orders.groupby("city")["sla"].mean().reset_index(),
                               x="city", y="sla"))

        # -------------------------------
        # COMPLAINTS
        # -------------------------------
        st.header("⚠️ Complaints Analysis")

        st.plotly_chart(px.bar(comp["issue_type"].value_counts().reset_index(),
                               x="index", y="issue_type"))

        # -------------------------------
        # COURIER
        # -------------------------------
        st.header("🚛 Courier Performance")

        st.plotly_chart(px.bar(courier, x="courier_partner", y="sla_breach_rate"))
        st.plotly_chart(px.bar(courier, x="courier_partner", y="complaint_rate"))

        # -------------------------------
        # HUB
        # -------------------------------
        st.header("🏭 Hub Analysis")

        st.plotly_chart(px.scatter(hub, x="failed_attempts", y="rto_count"))

        # -------------------------------
        # FUNNEL
        # -------------------------------
        st.header("🔄 Funnel Analysis")

        delayed = orders[orders.delay_days > 0]
        merged = delayed.merge(comp, on="order_id", how="left")

        pct = merged["ticket_id"].notnull().mean() * 100
        st.metric("% Delayed → Complaints", round(pct,2))

        merged2 = comp.merge(nps, on="order_id")
        pct2 = (merged2.score <= 6).mean() * 100
        st.metric("% Complaints → Detractors", round(pct2,2))

        repeat = cust[cust.segment=="Repeat"].shape[0] / len(cust) * 100
        st.metric("Repeat Rate", round(repeat,2))

        st.success("🎯 Final Insight: Delays drive complaints → complaints drive detractors → impacts retention")
