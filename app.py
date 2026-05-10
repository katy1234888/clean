import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import plotly.express as px

# 1. PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# 2. HELPER FUNCTIONS (Defined at top to prevent NameErrors)
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
            if k in col.lower():
                return col
    return None

# 3. NAVIGATION STATE
if "page" not in st.session_state:
    st.session_state.page = 1

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
    st.title("📦 Slide 1: Seashells Logistics - Case Story")
    st.markdown("""
    ## 📖 Background & Business Context
    You are working as an Analyst at a mid-sized logistics company operating across Tier-1 and Tier-2 cities in India[cite: 1].
    Over the past 3 months (October–December), the company has experienced a significant increase in order volumes due to festive demand[cite: 2].
    
    ### Leadership Concerns:
    - 📉 Declining customer satisfaction (NPS) [cite: 3]
    - ⚠️ Increase in customer complaints [cite: 3]
    - 🔁 Rising Return-to-Origin (RTO) rates [cite: 3]
    - 👥 Drop in repeat customer usage [cite: 3]
    - 🏭 Operational inefficiencies across hubs and courier partners [cite: 3]
    
    🎯 **Goal:** Diagnose root causes and improve performance before next peak season[cite: 3].
    """)
    st.button("➡️ Start: Upload Dataset", on_click=next_page)

# -------------------------------
# SLIDE 2: DATASET UPLOAD
# -------------------------------
elif st.session_state.page == 2:
    st.title("📊 Slide 2: Data Upload & Exploration")
    
    with st.sidebar:
        st.header("Upload Datasets")
        orders_file = st.file_uploader("Upload Orders Data", type=["csv"])
        customers_file = st.file_uploader("Upload Customers Data", type=["csv"])
        nps_file = st.file_uploader("Upload NPS Data", type=["csv"])
        complaints_file = st.file_uploader("Upload Complaints Data", type=["csv"])
        hub_file = st.file_uploader("Upload Hub Performance Data", type=["csv"])
        courier_file = st.file_uploader("Upload Courier Performance Data", type=["csv"])

    if "datasets" not in st.session_state:
        st.session_state.datasets = {}

    if orders_file: st.session_state.datasets["Orders"] = load_data(orders_file)
    if customers_file: st.session_state.datasets["Customers"] = load_data(customers_file)
    if nps_file: st.session_state.datasets["NPS"] = load_data(nps_file)
    if complaints_file: st.session_state.datasets["Complaints"] = load_data(complaints_file)
    if hub_file: st.session_state.datasets["Hub Performance"] = load_data(hub_file)
    if courier_file: st.session_state.datasets["Courier Performance"] = load_data(courier_file)

    if st.session_state.datasets:
        st.header("📌 Raw Data Overview")
        for name, df in st.session_state.datasets.items():
            with st.expander(f"{name} Dataset"):
                dataset_summary(df, name)

    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Back", on_click=prev_page)
    with col2: st.button("➡️ Next: Business Storyboard", on_click=next_page)

# -------------------------------
# SLIDE 3: BUSINESS CASE STORYBOARD
# -------------------------------
elif st.session_state.page == 3:
    st.title("📈 Slide 3: Business Case Storyboard")
    data = st.session_state.get("datasets", {})
    
    if not data:
        st.warning("Please upload datasets on Slide 2 first[cite: 12].")
    else:
        # ORIGINAL LOGIC FOR STORYBOARD STARTS HERE [cite: 18, 19]
        hubs = data.get("Hub Performance", pd.DataFrame())
        st.markdown("## 📊 Section A: NPS & Customer Experience [cite: 24]")
        st.markdown("## 🚚 Section B: Operational Performance [cite: 27]")
        
        if "on_time_delivery" in hubs.columns:
            hubs["sla_breach"] = 1 - hubs["on_time_delivery"] [cite: 22, 28]
            st.bar_chart(hubs.set_index("city")["sla_breach"])

    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Back", on_click=prev_page)
    with col2: st.button("➡️ Next: Detailed Answers", on_click=next_page)

# -------------------------------
# SLIDE 4: DETAILED ANSWERS
# -------------------------------
elif st.session_state.page == 4:
    st.title("📘 Slide 4: Detailed Business Answers")
    
    st.markdown("## 🔍 Section C: Problem Deep Dive [cite: 30]")
    st.markdown("""
    ### Observation:
    Tier-2 cities have significantly higher complaint rates[cite: 30].

    1. **Courier Partners:** Performance is a major driver in Tier-2 regions[cite: 30].
    2. **Hub Inefficiencies:** Sorting delays and capacity constraints lead to systemic delays[cite: 31].
    3. **Delivery Failures:** Failed attempts correlate with customer frustration[cite: 31].
    """)
    
    st.markdown("## 🔄 Section D: End-to-End Funnel Analysis [cite: 32]")
    st.markdown("## 💡 Section E: Business Recommendations [cite: 33]")
    
    st.success("Executive Summary: Operational inefficiencies in Tier-2 are the primary drivers of decline[cite: 35].")

    if st.button("⬅️ Return to Start"):
        st.session_state.page = 1
        st.rerun()
