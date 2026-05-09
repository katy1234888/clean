import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import plotly.express as px

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# -------------------------------
# STORY STATE MANAGEMENT
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

    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India.

    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand.

    However, leadership has raised serious concerns:

    - 📉 Declining customer satisfaction (NPS)
    - ⚠️ Increase in customer complaints
    - 🔁 Rising Return-to-Origin (RTO) rates
    - 👥 Drop in repeat customer usage
    - 🏭 Operational inefficiencies across hubs and courier partners

    🎯 Goal: Diagnose root causes and improve performance before next peak season.
    """)

    if st.button("➡️ Start Analysis"):
        next_page()

# -------------------------------
# PAGE 1: DATA ENGINE
# -------------------------------
elif st.session_state.page == 1:

    st.title("📊 Data Upload & Exploration")

    st.sidebar.header("Upload Datasets")

    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"])
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"])
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"])
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"])
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"])
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"])

    def load_data(file):
        return pd.read_csv(file)

    def dataset_summary(df, name):
        st.subheader(f"📊 {name} Summary")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Shape:", df.shape)
            st.write("Columns:", df.columns.tolist())

        with col2:
            st.write("Missing Values:")
            st.write(df.isnull().sum())

        st.write("Statistical Summary:")
        st.dataframe(df.describe(include='all'))

    def clean_data(df):
        df_clean = df.copy()

        num_cols = df_clean.select_dtypes(include=np.number).columns
        cat_cols = df_clean.select_dtypes(exclude=np.number).columns

        if len(num_cols) > 0:
            imputer_num = IterativeImputer(random_state=0)
            df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols])

        if len(cat_cols) > 0:
            imputer_cat = SimpleImputer(strategy='most_frequent')
            df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols])

        return df_clean

    datasets = {}

    if orders_file:
        datasets["Orders"] = load_data(orders_file)
    if customers_file:
        datasets["Customers"] = load_data(customers_file)
    if nps_file:
        datasets["NPS"] = load_data(nps_file)
    if complaints_file:
        datasets["Complaints"] = load_data(complaints_file)
    if hub_file:
        datasets["Hub Performance"] = load_data(hub_file)
    if courier_file:
        datasets["Courier Performance"] = load_data(courier_file)

    # ✅ IMPORTANT FIX ADDED HERE
    st.session_state.datasets = datasets

    if datasets:
        st.header("📌 Raw Data Overview")
        for name, df in datasets.items():
            with st.expander(f"{name} Dataset"):
                dataset_summary(df, name)

    st.header("🧹 Data Cleaning")
    clean_toggle = st.toggle("Enable Data Cleaning (ML-based Imputation)")

    cleaned_datasets = {}

    if clean_toggle:
        st.success("Data Cleaning Activated ✅")
        for name, df in datasets.items():
            cleaned_datasets[name] = clean_data(df)

        st.header("📊 Cleaned Data Overview")
        for name, df in cleaned_datasets.items():
            with st.expander(f"{name} Cleaned Dataset"):
                dataset_summary(df, name)

    if clean_toggle and cleaned_datasets:
        st.header("⬇️ Download Cleaned Data")
        for name, df in cleaned_datasets.items():
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"Download {name} Cleaned Data",
                data=csv,
                file_name=f"{name}_cleaned.csv"
            )

    if st.button("➡️ Go to Insights Story"):
        next_page()

# -------------------------------
# PAGE 2: Q&A STORY DASHBOARD
# -------------------------------
elif st.session_state.page == 2:

    st.title("📈 Insights & Storytelling (Q&A)")

    st.markdown("## 🎯 Answering Business Questions")
    data = st.session_state.get("datasets", {})
    if not data:
        st.warning("Please upload datasets first")
    else:

        # -------------------------------
        # Q1: Order Status Distribution
        # -------------------------------
        st.markdown("### ❓ What is the Order Status Distribution?")
        try:
            df = data["Orders"]
            fig = px.pie(df, names="order_status", title="Order Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Orders dataset required")

        # -------------------------------
        # Q2: Orders by City
        # -------------------------------
        st.markdown("### ❓ Orders by City")
        try:
            city_counts = df["city"].value_counts().reset_index()
            city_counts.columns = ["city", "count"]
            fig = px.bar(city_counts, x="city", y="count", title="Orders by City")
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass

        # -------------------------------
        # Q3: Trend Over Time
        # -------------------------------
        st.markdown("### ❓ Delivery Trend Over Time")
        try:
            df["order_date"] = pd.to_datetime(df["order_date"])
            trend = df.groupby(df["order_date"].dt.date).size().reset_index(name="orders")
            fig = px.line(trend, x="order_date", y="orders", title="Order Trend")
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass

        # -------------------------------
        # KPI CARDS
        # -------------------------------
        st.markdown("### 📊 KPI Overview")
        col1, col2, col3 = st.columns(3)

        try:
            total_orders = len(df)
            delivered = df[df["order_status"] == "Delivered"].shape[0]
            rto = df[df["order_status"] == "RTO"].shape[0]

            col1.metric("Total Orders", total_orders)
            col2.metric("Delivered", delivered)
            col3.metric("RTO Orders", rto)
        except:
            pass

        st.success("🎯 Insight: These patterns help identify operational bottlenecks and customer experience issues.")
# =========================================================
# 📘 FINAL STORYBOARD (WITH ANSWERS + THEORY)
# =========================================================

st.markdown("# 📘 Business Case Storyboard (Final Answers)")

try:
    data = st.session_state.get("datasets", {})

    if not data:
        st.warning("Upload datasets first")
    else:
        orders = data.get("Orders", pd.DataFrame())
        customers = data.get("Customers", pd.DataFrame())
        nps = data.get("NPS", pd.DataFrame())
        complaints = data.get("Complaints", pd.DataFrame())
        hubs = data.get("Hub Performance", pd.DataFrame())
        courier = data.get("Courier Performance", pd.DataFrame())

        # -------------------------
        # COLUMN DETECTION
        # -------------------------
        def find_col(df, keywords):
            for col in df.columns:
                for k in keywords:
                    if k in col.lower():
                        return col
            return None

        order_id = find_col(orders, ["order"])
        comp_order = find_col(complaints, ["order"])
        nps_score = find_col(nps, ["score"])
        nps_date = find_col(nps, ["date"])
        issue_col = find_col(complaints, ["issue", "type"])

        delivery_col = find_col(orders, ["delivery"])
        promised_col = find_col(orders, ["promise"])

        hub_col = find_col(hubs, ["hub"])
        sla_col = find_col(hubs, ["sla", "breach", "violation"])

        courier_col = find_col(courier, ["courier"])
        delay_col = find_col(courier, ["delay"])
        complaint_rate_col = find_col(courier, ["complaint"])

        failed_col = find_col(hubs, ["fail"])
        rto_col = find_col(hubs, ["rto"])

        city_tier_col = find_col(orders, ["tier"])
        repeat_col = find_col(customers, ["repeat"])

        # -------------------------
        # DELAY CALCULATION
        # -------------------------
        if delivery_col and promised_col:
            orders[delivery_col] = pd.to_datetime(orders[delivery_col], errors="coerce")
            orders[promised_col] = pd.to_datetime(orders[promised_col], errors="coerce")
            orders["delay"] = (orders[delivery_col] - orders[promised_col]).dt.days.fillna(0)
        else:
            orders["delay"] = 0

        # =====================================================
        # SECTION A
        # =====================================================
        st.markdown("## 📊 Section A: NPS & Customer Experience")

        if nps_score:
            promoters = nps[nps[nps_score] >= 9].shape[0]
            detractors = nps[nps[nps_score] <= 6].shape[0]
            total = len(nps)

            overall_nps = ((promoters - detractors) / total) * 100 if total else 0
            st.metric("Overall NPS", round(overall_nps, 2))

            st.write("👉 NPS = %Promoters - %Detractors. Positive = good, Negative = poor CX.")

            if nps_date:
                nps[nps_date] = pd.to_datetime(nps[nps_date], errors="coerce")
                nps["month"] = nps[nps_date].dt.to_period("M")

                monthly = nps.groupby("month").apply(
                    lambda x: ((x[x[nps_score] >= 9].shape[0] - x[x[nps_score] <= 6].shape[0]) / len(x)) * 100
                )
                st.line_chart(monthly)

                st.write("👉 Trend shows whether customer experience is improving or declining.")

        if issue_col:
            st.write("Top Complaint Drivers")
            st.bar_chart(complaints[issue_col].value_counts())

            st.write("👉 These issues are main reasons for detractors.")

        st.write("👉 Relationship Insight: Delay ↑ → Complaints ↑ → NPS ↓")

        # =====================================================
        # SECTION B
        # =====================================================
        st.markdown("## 🚚 Section B: Operational Performance")

        if hub_col and sla_col:
            st.bar_chart(hubs.set_index(hub_col)[sla_col])
            st.write("👉 High SLA breach hubs cause delays and poor customer experience.")
        else:
            st.warning("SLA data not found — column may be named differently (e.g., breach_rate)")

        if courier_col and delay_col:
            st.bar_chart(courier.set_index(courier_col)[delay_col])
            st.write("👉 High delay courier = operational inefficiency.")

        if courier_col and complaint_rate_col:
            st.bar_chart(courier.set_index(courier_col)[complaint_rate_col])
            st.write("👉 High complaint courier = poor service quality.")

        if failed_col and rto_col:
            st.write(hubs[[failed_col, rto_col]].corr())
            st.write("👉 More failed attempts → higher RTO (returns).")

        # =====================================================
        # SECTION C
        # =====================================================
        st.markdown("## 🔍 Section C: Tier-2 Deep Dive")

        if city_tier_col and order_id and comp_order:
            tier2 = orders[orders[city_tier_col].astype(str).str.contains("2", na=False)]

            merged = tier2.merge(complaints, left_on=order_id, right_on=comp_order)

            st.write("👉 Tier-2 cities show higher complaints due to:")
            st.write("- Weak logistics network")
            st.write("- Courier inefficiency")
            st.write("- More failed deliveries")

        # =====================================================
        # SECTION D
        # =====================================================
        st.markdown("## 🔄 Section D: Funnel Analysis")

        if order_id and comp_order:
            delayed = orders[orders["delay"] > 0]
            delayed_comp = delayed.merge(complaints, left_on=order_id, right_on=comp_order)

            pct1 = (len(delayed_comp) / len(delayed)) * 100 if len(delayed) else 0
            st.metric("% Delayed → Complaints", round(pct1, 2))

        if comp_order and order_id and nps_score:
            comp_nps = complaints.merge(nps, left_on=comp_order, right_on=order_id)
            detractors = comp_nps[comp_nps[nps_score] <= 6]

            pct2 = (len(detractors) / len(comp_nps)) * 100 if len(comp_nps) else 0
            st.metric("% Complaints → Detractors", round(pct2, 2))

        if repeat_col:
            repeat_rate = customers[repeat_col].mean() * 100
            st.metric("Repeat Rate", round(repeat_rate, 2))

            st.write("👉 Poor experience reduces repeat customers.")

        # =====================================================
        # SECTION E
        # =====================================================
        st.markdown("## 💡 Section E: Business Recommendations")

        st.write("### 🔴 Root Causes")
        st.write("1. Delivery delays")
        st.write("2. Poor courier performance")
        st.write("3. Tier-2 inefficiencies")

        st.write("### ⚡ Quick Wins")
        st.write("- Fix worst courier partners")
        st.write("- Reduce failed deliveries")
        st.write("- Improve SLA tracking")

        st.write("### 🚀 Long-Term Fixes")
        st.write("- Strengthen Tier-2 infrastructure")
        st.write("- AI-based route optimization")
        st.write("- Real-time tracking")

        st.write("### 📊 KPIs")
        st.write("- NPS")
        st.write("- Delay %")
        st.write("- Complaint Rate")
        st.write("- SLA Breach %")
        st.write("- Repeat Rate")

except Exception as e:
    st.warning(f"Storyboard Error: {e}")
