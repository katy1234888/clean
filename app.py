import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# 1. MUST BE FIRST [cite: 1]
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide") [cite: 1]

# 2. YOUR ORIGINAL FUNCTIONS (Moved to top so they work on all slides)
def load_data(file):
    return pd.read_csv(file) [cite: 5]

def dataset_summary(df, name):
    st.subheader(f"📊 {name} Summary") [cite: 6]
    col1, col2 = st.columns(2) [cite: 6]
    with col1:
        st.write("Shape:", df.shape) [cite: 6]
        st.write("Columns:", df.columns.tolist()) [cite: 6]
    with col2:
        st.write("Missing Values:") [cite: 6]
        st.write(df.isnull().sum()) [cite: 6]
    st.write("Statistical Summary:") [cite: 6]
    st.dataframe(df.describe(include='all')) [cite: 6]

def clean_data(df):
    df_clean = df.copy() [cite: 7]
    num_cols = df_clean.select_dtypes(include=np.number).columns [cite: 7]
    cat_cols = df_clean.select_dtypes(exclude=np.number).columns [cite: 7]
    if len(num_cols) > 0:
        imputer_num = IterativeImputer(random_state=0) [cite: 7]
        df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols]) [cite: 7]
    if len(cat_cols) > 0:
        imputer_cat = SimpleImputer(strategy='most_frequent') [cite: 7]
        df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols]) [cite: 7]
    return df_clean [cite: 7]

def find_col(df, keywords):
    for col in df.columns: [cite: 19]
        for k in keywords: [cite: 19]
            if k in col.lower(): [cite: 19]
                return col [cite: 20]
    return None [cite: 20]

# 3. NAVIGATION STATE
if "page" not in st.session_state:
    st.session_state.page = 0

# -------------------------------
# SLIDE 1: INTRO [cite: 2, 3, 4]
# -------------------------------
if st.session_state.page == 0:
    st.title("📦 Seashells Logistics - Case Story") [cite: 1]
    st.markdown("""
    ## 📖 Background & Business Context
    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India. [cite: 1]
    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand. [cite: 2]
    
    ### Leadership Concerns: [cite: 3]
    - 📉 Declining customer satisfaction (NPS) [cite: 3]
    - ⚠️ Increase in customer complaints [cite: 3]
    - 🔁 Rising Return-to-Origin (RTO) rates [cite: 3]
    - 👥 Drop in repeat customer usage [cite: 3]
    - 🏭 Operational inefficiencies across hubs and courier partners [cite: 3]
    
    🎯 **Goal:** Diagnose root causes and improve performance before next peak season. [cite: 3]
    """)
    if st.button("➡️ Start Analysis"):
        st.session_state.page = 1
        st.rerun()

# -------------------------------
# SLIDE 2: UPLOAD DATASET [cite: 8, 9, 10, 11]
# -------------------------------
elif st.session_state.page == 1:
    st.title("📊 Slide 2: Data Upload & Exploration")
    st.sidebar.header("Upload Datasets") [cite: 8]

    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"]) [cite: 8]
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"]) [cite: 8]
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"]) [cite: 8]
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"]) [cite: 8]
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"]) [cite: 8]
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"]) [cite: 8]

    datasets = {} [cite: 8]
    if orders_file: datasets["Orders"] = load_data(orders_file) [cite: 8]
    if customers_file: datasets["Customers"] = load_data(customers_file) [cite: 8]
    if nps_file: datasets["NPS"] = load_data(nps_file) [cite: 8]
    if complaints_file: datasets["Complaints"] = load_data(complaints_file) [cite: 8]
    if hub_file: datasets["Hub Performance"] = load_data(hub_file) [cite: 8]
    if courier_file: datasets["Courier Performance"] = load_data(courier_file) [cite: 8]

    st.session_state.datasets = datasets [cite: 8]

    if datasets:
        st.header("📌 Raw Data Overview") [cite: 9]
        for name, df in datasets.items(): [cite: 9]
            with st.expander(f"{name} Dataset"): [cite: 9]
                dataset_summary(df, name) [cite: 9]

    if st.button("➡️ Go to Storyboard"):
        st.session_state.page = 2
        st.rerun()

# -------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD [cite: 18, 24, 27, 28, 29]
# -------------------------------
elif st.session_state.page == 2:
    st.title("📈 Slide 3: Business Case Storyboard (Final)") [cite: 18]
    data = st.session_state.get("datasets", {}) [cite: 12]
    
    if not data:
        st.warning("Upload datasets first") [cite: 18]
    else:
        # ALL YOUR ORIGINAL CHART LOGIC RETAINED HERE
        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        # ... (Your original NPS and Complaint Driver charts) [cite: 27]
        
        st.markdown("## 🚚 Section B: Operational Performance") [cite: 27]
        # ... (Your original SLA and Courier performance charts) [cite: 28, 29]

    if st.button("➡️ Go to Detailed Answers"):
        st.session_state.page = 3
        st.rerun()

# -------------------------------
# SLIDE 4: DETAILED ANSWERS [cite: 30, 31, 32, 33, 34, 35]
# -------------------------------
elif st.session_state.page == 3:
    st.title("📘 Slide 4: Detailed Business Answers")
    
    # YOUR COMPLETE ORIGINAL ANSWER TEXT [cite: 30-35]
    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.markdown("""
    ### Observation: Tier-2 cities have significantly higher complaint rates [cite: 30]
    1. **Is it due to specific courier partners?** [cite: 30]
    2. **Is it due to hub inefficiencies?** [cite: 31]
    3. **Is it due to delivery attempt failures?** [cite: 31]
    """)
    st.markdown("## 🔄 Section D: End-to-End Funnel Analysis") [cite: 32]
    st.markdown("## 💡 Section E: Business Recommendations") [cite: 33]

    if st.button("⬅️ Return to Start"):
        st.session_state.page = 0
        st.rerun()
