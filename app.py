import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# --- STEP 1: SET PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# --- STEP 2: NAVIGATION STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = 0  # Start at Slide 1

if "datasets" not in st.session_state:
    st.session_state.datasets = {}

def move_page(page_num):
    st.session_state.page = page_num
    st.rerun()

# --- STEP 3: SHARED HELPER FUNCTIONS ---
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

def find_col(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col.lower(): return col
    return None

# ---------------------------------------------------------
# SLIDE 1: INTRO (Background & Business Context)
# ---------------------------------------------------------
if st.session_state.page == 0:
    st.title("📦 Slide 1: Seashells Logistics - Case Story")
    st.markdown("""
    ## 📖 Background & Business Context
    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India. 
    
    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand. [cite: 2]
    
    ### Leadership Concerns: [cite: 3]
    * 📉 **Declining customer satisfaction (NPS)**
    * ⚠️ **Increase in customer complaints**
    * 🔁 **Rising Return-to-Origin (RTO) rates**
    * 👥 **Drop in repeat customer usage**
    * 🏭 **Operational inefficiencies across hubs and courier partners**
    
    🎯 **Goal:** Diagnose root causes and improve performance before next peak season. [cite: 3, 4]
    """)
    if st.button("➡️ Start Analysis (Slide 2)"):
        move_page(1)

# ---------------------------------------------------------
# SLIDE 2: DATA ENGINE (Upload & Cleaning)
# ---------------------------------------------------------
elif st.session_state.page == 1:
    st.title("📊 Slide 2: Data Upload & Exploration")
    
    with st.sidebar:
        st.header("Upload Datasets")
        files = {
            "Orders": st.file_uploader("Upload Orders Data", type=["csv"]),
            "Customers": st.file_uploader("Upload Customers Data", type=["csv"]),
            "NPS": st.file_uploader("Upload NPS Data", type=["csv"]),
            "Complaints": st.file_uploader("Upload Complaints Data", type=["csv"]),
            "Hub Performance": st.file_uploader("Upload Hub Performance Data", type=["csv"]),
            "Courier Performance": st.file_uploader("Upload Courier Performance Data", type=["csv"])
        }

    # Load data into session state to persist it across slides
    for key, file in files.items():
        if file:
            st.session_state.datasets[key] = load_data(file) [cite: 5, 8]

    if st.session_state.datasets:
        st.success("Datasets Uploaded Successfully! ✅")
        for name, df in st.session_state.datasets.items():
            with st.expander(f"View {name} Dataset"):
                dataset_summary(df, name) [cite: 6, 9]

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to Intro"): move_page(0)
    with col2:
        if st.button("➡️ Go to Storyboard (Slide 3)"): move_page(2)

# ---------------------------------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD (Visual Dashboard)
# ---------------------------------------------------------
elif st.session_state.page == 2:
    st.title("📈 Slide 3: Business Case Storyboard (Final)") [cite: 18]
    data = st.session_state.get("datasets", {})
    
    if not data:
        st.warning("Please upload datasets on Slide 2 first")
    else:
        # Load local variables for original logic
        orders = data.get("Orders", pd.DataFrame())
        nps = data.get("NPS", pd.DataFrame())
        complaints = data.get("Complaints", pd.DataFrame())
        hubs = data.get("Hub Performance", pd.DataFrame())
        courier = data.get("Courier Performance", pd.DataFrame())

        # Logic for NPS & Operational Metrics
        st.markdown("## 📊 Section A: NPS & Customer Experience") [cite: 24]
        n_score = find_col(nps, ["score"]) [cite: 20]
        if n_score:
            total = len(nps)
            promoters = nps[nps[n_score] >= 9].shape[0]
            detractors = nps[nps[n_score] <= 6].shape[0]
            overall_nps = ((promoters - detractors) / total) * 100 if total else 0 [cite: 25]
            st.metric("Overall NPS", round(overall_nps, 2))

        st.markdown("## 🚚 Section B: Operational Performance") [cite: 28]
        if "on_time_delivery" in hubs.columns:
            hubs["sla_breach"] = 1 - hubs["on_time_delivery"]
            fig_hub = px.bar(hubs, x="city", y="sla_breach", title="SLA Breach by City")
            st.plotly_chart(fig_hub)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to Data Upload"): move_page(1)
    with col2:
        if st.button("➡️ View Detailed Answers (Slide 4)"): move_page(3)

# ---------------------------------------------------------
# SLIDE 4: DETAILED BUSINESS ANSWERS
# ---------------------------------------------------------
elif st.session_state.page == 3:
    st.title("📘 Slide 4: Detailed Business Answers")
    
    st.markdown("## 🔍 Section C: Problem Deep Dive") [cite: 30]
    st.info("**Observation:** Tier-2 cities have significantly higher complaint rates.") [cite: 30]
    
    tabs = st.tabs(["1. Courier Performance", "2. Hub Inefficiency", "3. Delivery Failures"])
    
    with tabs[0]:
        st.markdown("""
        **Insight:** Yes — courier performance is a major driver. 
        Some partners struggle in Tier-2 regions due to poor last-mile reach and inexperienced agents. [cite: 30]
        """)
    
    with tabs[1]:
        st.markdown("""
        **Insight:** Yes — sorting or dispatch delays at hubs lead to systemic delays before delivery. [cite: 31]
        """)
        
    with tabs[2]:
        st.markdown("""
        **Insight:** Yes — delivery failures (Address issues, customer unavailability) lead directly to frustration. [cite: 31]
        """)

    st.markdown("## 💡 Executive Summary")
    st.success("""
    The decline in customer experience is driven by operational inefficiencies in Tier-2 cities, 
    where poor courier performance and hub delays lead to reduced NPS and customer churn. [cite: 35]
    """)

    if st.button("⬅️ Back to Start"): move_page(0)
