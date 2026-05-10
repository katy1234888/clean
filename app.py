import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# --- STEP 1: INITIAL CONFIG ---
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide") [cite: 1]

# --- STEP 2: NAVIGATION STATE ---
if "page" not in st.session_state:
    st.session_state.page = 0 [cite: 1]

def next_page():
    st.session_state.page += 1 [cite: 1]

# --- STEP 3: REUSABLE FUNCTIONS ---
def load_data(file):
    return pd.read_csv(file) [cite: 5]

def dataset_summary(df, name):
    st.subheader(f"📊 {name} Summary") [cite: 5]
    col1, col2 = st.columns(2)
    with col1:
        st.write("Shape:", df.shape) [cite: 5]
    with col2:
        st.write("Missing Values:")
        st.write(df.isnull().sum()) [cite: 6]
    st.write("Statistical Summary:")
    st.dataframe(df.describe(include='all')) [cite: 5]

def clean_data(df):
    df_clean = df.copy() [cite: 7]
    num_cols = df_clean.select_dtypes(include=np.number).columns [cite: 7]
    cat_cols = df_clean.select_dtypes(exclude=np.number).columns [cite: 7]
    if len(num_cols) > 0:
        imputer_num = IterativeImputer(random_state=0)
        df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols]) [cite: 7]
    if len(cat_cols) > 0:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols]) [cite: 7]
    return df_clean [cite: 7]

def find_col(df, keywords):
    for col in df.columns: [cite: 19]
        for k in keywords: [cite: 19]
            if k in col.lower(): [cite: 19]
                return col [cite: 20]
    return None [cite: 20]

# --- SLIDE 1: INTRO ---
if st.session_state.page == 0:
    st.title("📦 Seashells Logistics - Case Story") [cite: 1]
    st.markdown("""
    ## 📖 Background & Business Context
    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India. 
    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand. [cite: 2]
    
    ### Leadership Concerns:
    - 📉 Declining customer satisfaction (NPS) [cite: 3]
    - ⚠️ Increase in customer complaints [cite: 3]
    - 🔁 Rising Return-to-Origin (RTO) rates [cite: 3]
    - 👥 Drop in repeat customer usage [cite: 3]
    - 🏭 Operational inefficiencies across hubs and courier partners [cite: 3]
    
    🎯 Goal: Diagnose root causes and improve performance before next peak season.
    """) [cite: 3]
    if st.button("➡️ Start Analysis"):
        next_page() [cite: 4]

# --- SLIDE 2: DATASET UPLOAD ---
elif st.session_state.page == 1:
    st.title("📊 Data Upload & Exploration") [cite: 4]
    st.sidebar.header("Upload Datasets") [cite: 4]
    
    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"]) [cite: 4]
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"]) [cite: 4]
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"]) [cite: 4]
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"]) [cite: 4]
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"]) [cite: 4]
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"]) [cite: 4]

    datasets = {} [cite: 7]
    if orders_file: datasets["Orders"] = load_data(orders_file) [cite: 7]
    if customers_file: datasets["Customers"] = load_data(customers_file) [cite: 7]
    if nps_file: datasets["NPS"] = load_data(nps_file) [cite: 7]
    if complaints_file: datasets["Complaints"] = load_data(complaints_file) [cite: 8]
    if hub_file: datasets["Hub Performance"] = load_data(hub_file) [cite: 8]
    if courier_file: datasets["Courier Performance"] = load_data(courier_file) [cite: 8]

    st.session_state.datasets = datasets [cite: 8]

    if datasets:
        st.header("📌 Raw Data Overview") [cite: 8]
        for name, df in datasets.items():
            with st.expander(f"{name} Dataset"):
                dataset_summary(df, name) [cite: 9]

    if st.button("➡️ Go to Storyboard"):
        next_page() [cite: 11]

# --- SLIDE 3: BUSINESS CASE STORYBOARD ---
elif st.session_state.page == 2:
    st.markdown("# 📘 Business Case Storyboard (Final)") [cite: 18]
    data = st.session_state.get("datasets", {}) [cite: 18]
    
    if not data:
        st.warning("Upload datasets first") [cite: 18]
    else:
        # Detect Columns Logic
        orders = data.get("Orders", pd.DataFrame()) [cite: 18]
        nps = data.get("NPS", pd.DataFrame()) [cite: 18]
        complaints = data.get("Complaints", pd.DataFrame()) [cite: 18]
        hubs = data.get("Hub Performance", pd.DataFrame()) [cite: 18]
        courier = data.get("Courier Performance", pd.DataFrame()) [cite: 18]

        nps_score = find_col(nps, ["score"]) [cite: 20]
        issue_col = find_col(complaints, ["issue", "type"]) [cite: 20]

        # Section A: NPS
        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        if nps_score:
            total = len(nps) [cite: 24]
            promoters = nps[nps[nps_score] >= 9].shape[0] [cite: 24]
            detractors = nps[nps[nps_score] <= 6].shape[0] [cite: 24]
            overall_nps = ((promoters - detractors) / total) * 100 if total else 0 [cite: 25]
            st.metric("Overall NPS", round(overall_nps, 2)) [cite: 25]

        # Section B: Operational Performance
        st.markdown("## 🚚 Section B: Operational Performance") [cite: 27]
        if "on_time_delivery" in hubs.columns:
            hubs["sla_breach"] = 1 - hubs["on_time_delivery"] [cite: 22]
            st.bar_chart(hubs.set_index("city")["sla_breach"]) [cite: 28]

        if st.button("➡️ View Detailed Business Answers"):
            next_page()

# --- SLIDE 4: DETAILED BUSINESS ANSWERS ---
elif st.session_state.page == 3:
    st.markdown("# 📘 Detailed Business Answers") [cite: 30]
    
    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.markdown("""
    ### Observation:
    Tier-2 cities have significantly higher complaint rates [cite: 30]
    
    **1. Is it due to specific courier partners?**
    Yes — courier performance is a major driver. [cite: 30]
    
    **2. Is it due to hub inefficiencies?**
    Yes — hub inefficiency is a key factor. [cite: 31]
    
    **3. Is it due to delivery attempt failures?**
    Yes — delivery failures are a major contributor. [cite: 31]
    """)

    st.markdown("## 🔄 Section D: End-to-End Funnel Analysis") [cite: 31]
    st.markdown("Orders → Delivery → Complaints → NPS → Repeat Orders") [cite: 32]

    st.markdown("## 💡 Section E: Business Recommendations") [cite: 33]
    st.markdown("""
    1. Fix worst performing courier partners [cite: 34]
    2. Reduce failed deliveries through address validation [cite: 34]
    3. Strengthen Tier-2 logistics infrastructure [cite: 34]
    """)

    if st.button("⬅️ Restart Presentation"):
        st.session_state.page = 0
        st.rerun()
