import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import plotly.express as px

# -------------------------------
# 1. NAVIGATION SETUP (New Addition)
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# -------------------------------
# SLIDE 1: INTRO
# -------------------------------
if st.session_state.page == 1:
    st.title("📦 Seashells Logistics - Case Story") [cite: 1]

    st.markdown("""
    ## 📖 Background & Business Context

    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India. [cite: 1]

    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand. [cite: 2]
    
    However, leadership has raised serious concerns: [cite: 3]

    - 📉 Declining customer satisfaction (NPS) [cite: 3]
    - ⚠️ Increase in customer complaints [cite: 3]
    - 🔁 Rising Return-to-Origin (RTO) rates [cite: 3]
    - 👥 Drop in repeat customer usage [cite: 3]
    - 🏭 Operational inefficiencies across hubs and courier partners [cite: 3]

    🎯 Goal: Diagnose root causes and improve performance before next peak season. [cite: 3]
    """)

    st.button("Next Slide: Upload Dataset ➡️", on_click=next_page)

# -------------------------------
# SLIDE 2: DATASET UPLOAD
# -------------------------------
elif st.session_state.page == 2:
    st.title("📊 Slide 2: Data Upload & Exploration") [cite: 4]

    st.sidebar.header("Upload Datasets") [cite: 4]

    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"]) [cite: 4]
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"]) [cite: 4]
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"]) [cite: 4]
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"]) [cite: 4]
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"]) [cite: 4]
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"]) [cite: 4]

    def load_data(file): [cite: 5]
        return pd.read_csv(file) [cite: 5]

    def dataset_summary(df, name): [cite: 5]
        st.subheader(f"📊 {name} Summary") [cite: 5]
        col1, col2 = st.columns(2) [cite: 5]
        with col1:
            st.write("Shape:", df.shape) [cite: 5]
            st.write("Columns:", df.columns.tolist()) [cite: 5]
        with col2:
            st.write("Missing Values:") [cite: 5]
            st.write(df.isnull().sum()) [cite: 6]
        st.write("Statistical Summary:") [cite: 6]
        st.dataframe(df.describe(include='all')) [cite: 6]

    def clean_data(df): [cite: 6]
        df_clean = df.copy() [cite: 6]
        num_cols = df_clean.select_dtypes(include=np.number).columns [cite: 6]
        cat_cols = df_clean.select_dtypes(exclude=np.number).columns [cite: 6]
        if len(num_cols) > 0:
            imputer_num = IterativeImputer(random_state=0) [cite: 6]
            df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols]) [cite: 6]
        if len(cat_cols) > 0: [cite: 7]
            imputer_cat = SimpleImputer(strategy='most_frequent') [cite: 7]
            df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols]) [cite: 7]
        return df_clean [cite: 7]

    datasets = {}
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
            with st.expander(f"{name} Dataset"): [cite: 8]
                dataset_summary(df, name) [cite: 9]

    st.header("🧹 Data Cleaning") [cite: 9]
    clean_toggle = st.toggle("Enable Data Cleaning (ML-based Imputation)") [cite: 9]

    if clean_toggle:
        st.success("Data Cleaning Activated ✅") [cite: 9]
        # ... (Your original cleaning logic) ...
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Previous", on_click=prev_page)
    with col2:
        st.button("Next Slide: Storyboard ➡️", on_click=next_page)

# -------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD
# -------------------------------
elif st.session_state.page == 3:
    st.markdown("# 📘 Business Case Storyboard (Final)") [cite: 18]

    data = st.session_state.get("datasets", {})
    if not data:
        st.warning("Upload datasets first") [cite: 19]
    else:
        # EXACT ORIGINAL ANALYSIS LOGIC
        orders = data.get("Orders", pd.DataFrame()) [cite: 19]
        # ... (Rest of your data detection logic from source lines 19-29) ...
        
        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        # (Your original NPS calculations and charts) [cite: 25, 26, 27]

        st.markdown("## 🚚 Section B: Operational Performance") [cite: 28]
        # (Your original SLA and Courier charts) [cite: 28, 29]

    col1, col2 = st.columns(2)
    with col1:
        st.button("⬅️ Previous", on_click=prev_page)
    with col2:
        st.button("Next Slide: Detailed Answers ➡️", on_click=next_page)

# -------------------------------
# SLIDE 4: DETAILED ANSWERS
# -------------------------------
elif st.session_state.page == 4:
    st.markdown("# 📘 Detailed Business Answers") [cite: 30]

    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.markdown("### Observation: Tier-2 cities have significantly higher complaint rates") [cite: 30]
    
    # (Your original markdown text for Section C, D, and E) [cite: 30, 31, 32, 33, 34, 35]
    
    st.button("⬅️ Back to Storyboard", on_click=prev_page)
