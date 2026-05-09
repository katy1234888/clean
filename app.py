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

    # ✅ SESSION FIX (ADDED ONLY)
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

    # ✅ ADDED NAVIGATION BUTTON (NO CHANGE TO EXISTING LOGIC)
    if st.button("➡️ Advanced Analysis Story"):
        next_page()

# -------------------------------
# PAGE 3: ADVANCED STORY (YOUR EXISTING ONE - UNTOUCHED)
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

        st.header("📊 NPS Analysis")

        promoters = nps[nps.score >= 9].shape[0]
        detractors = nps[nps.score <= 6].shape[0]
        total = len(nps)

        overall_nps = ((promoters - detractors) / total) * 100
        st.metric("Overall NPS", round(overall_nps,2))

        nps["date"] = pd.to_datetime(nps["response_date"])
        nps["month"] = nps["date"].dt.to_period("M")

        trend = nps.groupby("month").size().reset_index(name="count")
        st.plotly_chart(px.line(trend, x="month", y="count"))

        st.header("🚚 Delivery Performance")

        orders["delay"] = pd.to_datetime(orders["delivery_date"]) - pd.to_datetime(orders["promised_date"])
        orders["delay_days"] = orders["delay"].dt.days

        st.plotly_chart(px.histogram(orders, x="delay_days"))

    # ✅ NEW BUTTON TO NEXT PAGE
    if st.button("➡️ Q&A Storyboard"):
        next_page()

# -------------------------------
# PAGE 4: NEW Q&A STORYBOARD (ADDED ONLY)
# -------------------------------
elif st.session_state.page == 4:

    st.title("📖 Business Q&A Storyboard")

    data = st.session_state.get("datasets", {})

    if not data:
        st.warning("Please upload data first")
    else:

        orders = data.get("Orders", pd.DataFrame())
        nps = data.get("NPS", pd.DataFrame())
        customers = data.get("Customers", pd.DataFrame())
        complaints = data.get("Complaints", pd.DataFrame())

        # Q1
        st.header("Q1️⃣ What is the overall NPS?")
        if not nps.empty:
            promoters = nps[nps["score"] >= 9].shape[0]
            detractors = nps[nps["score"] <= 6].shape[0]
            total = len(nps)
            nps_score = ((promoters - detractors) / total) * 100
            st.metric("Overall NPS", round(nps_score, 2))

        # Q2
        st.header("Q2️⃣ How is NPS changing over time?")
        if not nps.empty:
            nps["date"] = pd.to_datetime(nps["response_date"])
            nps["month"] = nps["date"].dt.to_period("M")
            trend = nps.groupby("month").size().reset_index(name="responses")
            st.plotly_chart(px.line(trend, x="month", y="responses"))

        # Q3
        st.header("Q3️⃣ Which cities have highest issues?")
        if not orders.empty:
            city_counts = orders["city"].value_counts().reset_index()
            city_counts.columns = ["city", "orders"]
            st.plotly_chart(px.bar(city_counts, x="city", y="orders"))

        # Q4
        st.header("Q4️⃣ Are delays a major issue?")
        if not orders.empty:
            orders["delay"] = pd.to_datetime(orders["delivery_date"]) - pd.to_datetime(orders["promised_date"])
            orders["delay_days"] = orders["delay"].dt.days
            st.plotly_chart(px.histogram(orders, x="delay_days"))

        # Q5
        st.header("Q5️⃣ What are customers complaining about?")
        if not complaints.empty:
            comp_counts = complaints["issue_type"].value_counts().reset_index()
            comp_counts.columns = ["issue", "count"]
            st.plotly_chart(px.pie(comp_counts, names="issue", values="count"))

        # Q6
        st.header("Q6️⃣ Do delays lead to complaints?")
        if not orders.empty and not complaints.empty:
            delayed = orders.copy()
            delayed["delay"] = pd.to_datetime(delayed["delivery_date"]) - pd.to_datetime(delayed["promised_date"])
            delayed["delay_days"] = delayed["delay"].dt.days
            delayed_orders = delayed[delayed["delay_days"] > 0]
            merged = delayed_orders.merge(complaints, on="order_id", how="left")
            pct = merged["ticket_id"].notnull().mean() * 100
            st.metric("% Delayed → Complaints", round(pct, 2))

        # Q7
        st.header("Q7️⃣ Do complaints create detractors?")
        if not complaints.empty and not nps.empty:
            merged = complaints.merge(nps, on="order_id", how="inner")
            detractor_pct = (merged["score"] <= 6).mean() * 100
            st.metric("% Complaints → Detractors", round(detractor_pct, 2))

        # Q8
        st.header("Q8️⃣ Are customers coming back?")
        if not customers.empty:
            repeat_rate = (customers["segment"] == "Repeat").mean() * 100
            st.metric("Repeat Rate", round(repeat_rate, 2))

        st.success("📌 Final Insight: Delays → Complaints → Low NPS → Lower Retention")
