import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# 1. PAGE CONFIG
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide") [cite: 1]

# 2. SLIDE NAVIGATION LOGIC
if "page" not in st.session_state:
    st.session_state.page = 0 [cite: 1]

def next_page():
    st.session_state.page += 1 [cite: 1]

def prev_page():
    st.session_state.page -= 1

# -------------------------------
# SLIDE 1: INTRO (Background & Context)
# -------------------------------
if st.session_state.page == 0:
    st.title("📦 Seashells Logistics - Case Story") [cite: 1]
    st.markdown("""
    ## 📖 Background & Business Context
    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India. [cite: 1]
    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand. [cite: 2]
    
    ### Leadership Concerns:
    - 📉 Declining customer satisfaction (NPS) [cite: 3]
    - ⚠️ Increase in customer complaints [cite: 3]
    - 🔁 Rising Return-to-Origin (RTO) rates [cite: 3]
    - 👥 Drop in repeat customer usage [cite: 3]
    - 🏭 Operational inefficiencies across hubs and courier partners [cite: 3]
    
    🎯 **Goal:** Diagnose root causes and improve performance before next peak season. [cite: 3]
    """)
    if st.button("➡️ Start Analysis"):
        next_page()

# -------------------------------
# SLIDE 2: DATA ENGINE (Upload & Summary)
# -------------------------------
elif st.session_state.page == 1:
    st.title("📊 Slide 2: Data Upload & Exploration") [cite: 1]
    st.sidebar.header("Upload Datasets") [cite: 1]

    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"]) [cite: 4]
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"]) [cite: 4]
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"]) [cite: 4]
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"]) [cite: 4]
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"]) [cite: 4]
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"]) [cite: 4]

    def load_data(file):
        return pd.read_csv(file) [cite: 5]

    def dataset_summary(df, name):
        st.subheader(f"📊 {name} Summary") [cite: 6]
        col1, col2 = st.columns(2)
        with col1:
            st.write("Shape:", df.shape)
            st.write("Columns:", df.columns.tolist())
        with col2:
            st.write("Missing Values:")
            st.write(df.isnull().sum()) [cite: 6]
        st.write("Statistical Summary:")
        st.dataframe(df.describe(include='all')) [cite: 6]

    def clean_data(df):
        df_clean = df.copy() [cite: 7]
        num_cols = df_clean.select_dtypes(include=np.number).columns
        cat_cols = df_clean.select_dtypes(exclude=np.number).columns
        if len(num_cols) > 0:
            imputer_num = IterativeImputer(random_state=0)
            df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols])
        if len(cat_cols) > 0:
            imputer_cat = SimpleImputer(strategy='most_frequent') [cite: 7]
            df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols])
        return df_clean

    datasets = {}
    if orders_file: datasets["Orders"] = load_data(orders_file) [cite: 8]
    if customers_file: datasets["Customers"] = load_data(customers_file)
    if nps_file: datasets["NPS"] = load_data(nps_file)
    if complaints_file: datasets["Complaints"] = load_data(complaints_file) [cite: 8]
    if hub_file: datasets["Hub Performance"] = load_data(hub_file)
    if courier_file: datasets["Courier Performance"] = load_data(courier_file)

    st.session_state.datasets = datasets [cite: 8]

    if datasets:
        st.header("📌 Raw Data Overview")
        for name, df in datasets.items():
            with st.expander(f"{name} Dataset"):
                dataset_summary(df, name) [cite: 9]

    st.header("🧹 Data Cleaning")
    clean_toggle = st.toggle("Enable Data Cleaning (ML-based Imputation)") [cite: 9]
    if clean_toggle and datasets:
        st.success("Data Cleaning Activated ✅")
        for name, df in datasets.items():
            cleaned_df = clean_data(df) [cite: 10]
            with st.expander(f"{name} Cleaned Dataset"):
                dataset_summary(cleaned_df, name)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"): prev_page()
    with col2:
        if st.button("➡️ Go to Storyboard"): next_page()

# -------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD
# -------------------------------
elif st.session_state.page == 2:
    st.markdown("# 📘 Business Case Storyboard (Final)") [cite: 18]
    data = st.session_state.get("datasets", {})

    if not data:
        st.warning("Upload datasets first") [cite: 19]
    else:
        orders = data.get("Orders", pd.DataFrame()) [cite: 19]
        nps = data.get("NPS", pd.DataFrame())
        complaints = data.get("Complaints", pd.DataFrame())
        hubs = data.get("Hub Performance", pd.DataFrame())
        courier = data.get("Courier Performance", pd.DataFrame())

        def find_col(df, keywords):
            for col in df.columns:
                for k in keywords:
                    if k in col.lower(): return col [cite: 20]
            return None

        # Column Detection Logic
        nps_score = find_col(nps, ["score"]) [cite: 21]
        nps_date = find_col(nps, ["date"])
        issue_col = find_col(complaints, ["issue", "type"])
        on_time = "on_time_delivery" [cite: 22]
        failed = "failed_attempts"
        rto = "rto_count"

        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        if nps_score:
            total = len(nps)
            promoters = nps[nps[nps_score] >= 9].shape[0]
            detractors = nps[nps[nps_score] <= 6].shape[0]
            overall_nps = ((promoters - detractors) / total) * 100 if total else 0 [cite: 25]
            st.metric("Overall NPS", round(overall_nps, 2))
            if nps_date:
                nps[nps_date] = pd.to_datetime(nps[nps_date], errors="coerce")
                nps["month"] = nps[nps_date].dt.to_period("M")
                monthly = nps.groupby("month").apply(lambda x: ((x[x[nps_score] >= 9].shape[0] - x[x[nps_score] <= 6].shape[0]) / len(x)) * 100) [cite: 26]
                st.line_chart(monthly)

        st.markdown("## 🚚 Section B: Operational Performance") [cite: 27]
        if on_time in hubs.columns:
            hubs["sla_breach"] = 1 - hubs[on_time] [cite: 22]
            st.bar_chart(hubs.set_index("city")["sla_breach"]) [cite: 28]

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back"): prev_page()
        with col2:
            if st.button("➡️ Go to Detailed Answers"): next_page()

# -------------------------------
# SLIDE 4: DETAILED BUSINESS ANSWERS
# -------------------------------
elif st.session_state.page == 3:
    st.markdown("# 📘 Detailed Business Answers") [cite: 29]
    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.markdown("""
    ### Observation:
    Tier-2 cities have significantly higher complaint rates [cite: 30]

    ### 1. Is it due to specific courier partners?
    **Insight:** Yes — courier performance is a major driver in Tier-2. [cite: 30]

    ### 2. Is it due to hub inefficiencies?
    **Insight:** Yes — hub inefficiency (sorting delays, capacity constraints) is a key factor. [cite: 31]

    ### 3. Is it due to delivery attempt failures?
    **Insight:** Yes — delivery failures (address issues, customer unavailability) are major contributors. [cite: 31]
    """)

    st.markdown("## 🔄 Section D: End-to-End Funnel Analysis") [cite: 32]
    st.markdown("""
    - **Delayed Orders vs Complaints:** High sensitivity indicates delay is a primary trigger. [cite: 32]
    - **Complaints vs Detractors:** Reflects post-issue experience quality. [cite: 33]
    - **Repeat Usage:** Complaints lead to customer churn and loss of revenue. [cite: 33]
    """)

    st.markdown("## 💡 Section E: Business Recommendations") [cite: 33]
    st.markdown("""
    - **Quick Wins:** Fix worst performing couriers; improve address validation. [cite: 34]
    - **Long Term:** Strengthen Tier-2 infrastructure; implement AI smart routing. [cite: 34]
    - **KPIs to Track:** NPS, SLA Breach %, Complaint Rate, RTO %, Repeat Purchase Rate. [cite: 34]
    """)

    if st.button("⬅️ Back to Start"):
        st.session_state.page = 0
        st.rerun()
