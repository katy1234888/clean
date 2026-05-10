import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# 1. PAGE CONFIG (Must be the first Streamlit command)
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide") [cite: 1]

# 2. HELPER FUNCTIONS (Defined at top to work on all slides)
def load_data(file):
    return pd.read_csv(file) [cite: 5]

def dataset_summary(df, name):
    st.subheader(f"📊 {name} Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Shape:", df.shape)
        st.write("Columns:", df.columns.tolist())
    with col2:
        st.write("Missing Values:")
        st.write(df.isnull().sum()) [cite: 6]
    st.write("Statistical Summary:")
    st.dataframe(df.describe(include='all'))

def find_col(df, keywords):
    for col in df.columns: [cite: 19]
        for k in keywords:
            if k in col.lower():
                return col [cite: 20]
    return None

# 3. NAVIGATION LOGIC
if "page" not in st.session_state:
    st.session_state.page = 1 [cite: 1]

def next_page():
    st.session_state.page += 1
    st.rerun()

def prev_page():
    st.session_state.page -= 1
    st.rerun()

# -------------------------------
# SLIDE 1: INTRO
# -------------------------------
if st.session_state.page == 1:
    st.title("📦 Slide 1: Seashells Logistics - Case Story") [cite: 1]
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
    st.button("➡️ Start: Upload Dataset", on_click=next_page) [cite: 4]

# -------------------------------
# SLIDE 2: DATASET UPLOAD
# -------------------------------
elif st.session_state.page == 2:
    st.title("📊 Slide 2: Data Upload & Exploration") [cite: 5]
    st.sidebar.header("Upload Datasets") [cite: 5]

    orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"]) [cite: 5]
    customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"]) [cite: 5]
    nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"]) [cite: 5]
    complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"]) [cite: 5]
    hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"]) [cite: 5]
    courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"]) [cite: 5]

    # Persistent storage in session state
    if "datasets" not in st.session_state:
        st.session_state.datasets = {} [cite: 8]

    if orders_file: st.session_state.datasets["Orders"] = load_data(orders_file) [cite: 8]
    if customers_file: st.session_state.datasets["Customers"] = load_data(customers_file) [cite: 8]
    if nps_file: st.session_state.datasets["NPS"] = load_data(nps_file) [cite: 8]
    if complaints_file: st.session_state.datasets["Complaints"] = load_data(complaints_file) [cite: 8]
    if hub_file: st.session_state.datasets["Hub Performance"] = load_data(hub_file) [cite: 8]
    if courier_file: st.session_state.datasets["Courier Performance"] = load_data(courier_file) [cite: 8]

    if st.session_state.datasets:
        st.header("📌 Raw Data Overview")
        for name, df in st.session_state.datasets.items():
            with st.expander(f"{name} Dataset"):
                dataset_summary(df, name) [cite: 9]

    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Back", on_click=prev_page)
    with col2: st.button("➡️ Next: Business Storyboard", on_click=next_page)

# -------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD
# -------------------------------
elif st.session_state.page == 3:
    st.markdown("# 📘 Slide 3: Business Case Storyboard (Final)") [cite: 18]
    data = st.session_state.get("datasets", {}) [cite: 19]
    
    if not data:
        st.warning("Please upload datasets on Slide 2 first")
    else:
        # ORIGINAL SECTION A & B LOGIC
        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        hubs = data.get("Hub Performance", pd.DataFrame()) [cite: 19]
        
        st.markdown("## 🚚 Section B: Operational Performance") [cite: 28]
        if "on_time_delivery" in hubs.columns:
            hubs["sla_breach"] = 1 - hubs["on_time_delivery"] [cite: 22]
            st.bar_chart(hubs.set_index("city")["sla_breach"]) [cite: 28]

    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Back", on_click=prev_page)
    with col2: st.button("➡️ Next: Detailed Answers", on_click=next_page)

# -------------------------------
# SLIDE 4: DETAILED BUSINESS ANSWERS
# -------------------------------
elif st.session_state.page == 4:
    st.markdown("# 📘 Slide 4: Detailed Business Answers") [cite: 30]
    
    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.markdown("""
    ### Observation:
    Tier-2 cities have significantly higher complaint rates [cite: 30]

    1. **Specific Courier Partners?**
       - **Insight**: Yes — courier performance is a major driver in Tier-2. [cite: 30]
    2. **Hub Inefficiencies?**
       - **Insight**: Yes — sorting delays and capacity constraints lead to systemic delays. [cite: 31]
    3. **Delivery Attempt Failures?**
       - **Insight**: Yes — failed delivery attempts correlate strongly with customer frustration. [cite: 31]
    """)

    st.markdown("## 🔄 Section D: End-to-End Funnel Analysis") [cite: 32]
    st.markdown("Orders → Delivery → Complaints → NPS → Repeat Orders") [cite: 32]

    st.markdown("## 💡 Section E: Business Recommendations") [cite: 34]
    st.success("Executive Summary: Operational inefficiencies in Tier-2 are the primary drivers of decline.") [cite: 35]

    st.button("⬅️ Back to Start", on_click=lambda: st.session_state.update({"page": 1}))
