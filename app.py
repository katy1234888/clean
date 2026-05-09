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
        # 📊 ADVANCED ANALYSIS SECTION (DO NOT MODIFY ABOVE CODE)
        # =========================================================

        st.markdown("## 🧠 Advanced Business Analysis")

        # Load datasets safely
        orders = data.get("Orders")
        customers = data.get("Customers")
        nps = data.get("NPS")
        complaints = data.get("Complaints")
        hubs = data.get("Hub Performance")
        courier = data.get("Courier Performance")

        # =========================================================
        # SECTION A: NPS & CUSTOMER EXPERIENCE
        # =========================================================
        st.markdown("## 📊 Section A: NPS & Customer Experience")

        try:
            # 1. Overall NPS
            promoters = nps[nps["score"] >= 9].shape[0]
            detractors = nps[nps["score"] <= 6].shape[0]
            total = len(nps)

            overall_nps = ((promoters - detractors) / total) * 100

            st.metric("Overall NPS Score", round(overall_nps, 2))

            st.info("📖 Story: Overall customer sentiment is measured using NPS. A lower score indicates rising dissatisfaction and potential churn risk.")

            # 2. Monthly Trend
            nps["date"] = pd.to_datetime(nps["date"])
            nps["month"] = nps["date"].dt.to_period("M")

            monthly_nps = nps.groupby("month").apply(
                lambda x: ((x[x["score"] >= 9].shape[0] - x[x["score"] <= 6].shape[0]) / len(x)) * 100
            )

            st.line_chart(monthly_nps)

            st.info("📖 Story: Month-on-month decline signals worsening customer experience during peak demand.")

            # 3. Segment-wise NPS
            merged = nps.merge(customers, on="customer_id")

            segment_nps = merged.groupby("segment").apply(
                lambda x: ((x[x["score"] >= 9].shape[0] - x[x["score"] <= 6].shape[0]) / len(x)) * 100
            )

            st.bar_chart(segment_nps)

            st.info("📖 Story: Identifying low NPS segments helps target high-risk customer groups.")

            # 4. Complaint Drivers
            driver_counts = complaints["issue_type"].value_counts()
            st.bar_chart(driver_counts)

            st.info("📖 Story: Top complaint categories reveal key dissatisfaction drivers.")

            # 5. Relationship Analysis
            merged_all = orders.merge(complaints, on="order_id", how="left").merge(nps, on="order_id", how="left")

            corr = merged_all[["delivery_delay", "score"]].corr()

            st.write("Correlation Matrix:", corr)

            st.info("📖 Story: Delivery delays directly impact complaints and NPS scores.")

        except Exception as e:
            st.warning(f"Section A Error: {e}")

        # =========================================================
        # SECTION B: OPERATIONAL PERFORMANCE
        # =========================================================
        st.markdown("## 🚚 Section B: Operational Performance")

        try:
            # SLA breaches
            sla = orders.groupby("city")["delivery_delay"].mean().sort_values(ascending=False)
            st.bar_chart(sla)

            st.info("📖 Story: Cities with highest delays indicate operational inefficiencies.")

            # Courier Performance
            courier_delay = courier.groupby("partner")["delay_rate"].mean()
            courier_complaints = courier.groupby("partner")["complaint_rate"].mean()

            st.bar_chart(courier_delay)
            st.bar_chart(courier_complaints)

            st.info("📖 Story: Poor courier performance is a major contributor to bad customer experience.")

            # Failed Delivery vs RTO
            relation = orders[["failed_attempts", "rto_flag"]].corr()
            st.write("Failed Attempts vs RTO:", relation)

            st.info("📖 Story: Higher failed attempts strongly increase RTO probability.")

        except Exception as e:
            st.warning(f"Section B Error: {e}")

        # =========================================================
        # SECTION C: DEEP DIVE (TIER-2 ISSUE)
        # =========================================================
        st.markdown("## 🔍 Section C: Tier-2 City Deep Dive")

        try:
            tier2 = orders[orders["city_tier"] == "Tier-2"]

            complaint_rate = tier2.merge(complaints, on="order_id").shape[0] / len(tier2)

            st.metric("Tier-2 Complaint Rate", round(complaint_rate, 2))

            st.info("📖 Story: Tier-2 cities show higher complaints, indicating systemic inefficiencies.")

            # Check courier issue
            courier_issue = tier2.groupby("courier_partner")["delivery_delay"].mean()
            st.bar_chart(courier_issue)

            st.info("📖 Story: Certain courier partners are underperforming in Tier-2 regions.")

        except Exception as e:
            st.warning(f"Section C Error: {e}")

        # =========================================================
        # SECTION D: FUNNEL ANALYSIS
        # =========================================================
        st.markdown("## 🔄 Section D: End-to-End Funnel")

        try:
            # Delayed → Complaints
            delayed = orders[orders["delivery_delay"] > 0]
            delayed_complaints = delayed.merge(complaints, on="order_id")

            pct_delay_complaint = (len(delayed_complaints) / len(delayed)) * 100

            st.metric("% Delayed Orders → Complaints", round(pct_delay_complaint, 2))

            # Complaints → Detractors
            comp_nps = complaints.merge(nps, on="order_id")
            detractors = comp_nps[comp_nps["score"] <= 6]

            pct_detractors = (len(detractors) / len(comp_nps)) * 100

            st.metric("% Complaints → Detractors", round(pct_detractors, 2))

            # Repeat impact
            repeat = customers["repeat_flag"].mean() * 100
            st.metric("Repeat Customer %", round(repeat, 2))

            st.info("""
            📖 Story:
            - Delays → Complaints → Detractors → Lower Repeat Usage  
            - This creates a negative feedback loop impacting revenue growth.
            """)

        except Exception as e:
            st.warning(f"Section D Error: {e}")
