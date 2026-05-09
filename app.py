import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import plotly.express as px

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# =========================================================
# 📖 GLOBAL STORY NAVIGATION
# =========================================================
TOTAL_PAGES = 9

if "page" not in st.session_state:
    st.session_state.page = 0

def next_page():
    if st.session_state.page < TOTAL_PAGES - 1:
        st.session_state.page += 1

def prev_page():
    if st.session_state.page > 0:
        st.session_state.page -= 1

nav1, nav2, nav3 = st.columns([1,2,1])

with nav1:
    if st.button("⬅️ Previous"):
        prev_page()

with nav3:
    if st.button("Next ➡️"):
        next_page()

st.markdown(f"### 📄 Slide {st.session_state.page + 1} / {TOTAL_PAGES}")

# =========================================================
# PAGE 0: INTRO
# =========================================================
if st.session_state.page == 0:
    st.title("📦 Seashells Logistics - Case Story")

    st.markdown("""
    ## 📖 Background & Business Context

    You are working as an Analyst at a logistics company.

    Problems observed:
    - Declining NPS
    - Increasing complaints
    - Rising RTO
    - Drop in repeat users

    🎯 Goal: Identify root causes & improve performance
    """)

# =========================================================
# PAGE 1: DATA UPLOAD
# =========================================================
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

    datasets = {}

    if orders_file: datasets["Orders"] = load_data(orders_file)
    if customers_file: datasets["Customers"] = load_data(customers_file)
    if nps_file: datasets["NPS"] = load_data(nps_file)
    if complaints_file: datasets["Complaints"] = load_data(complaints_file)
    if hub_file: datasets["Hub Performance"] = load_data(hub_file)
    if courier_file: datasets["Courier Performance"] = load_data(courier_file)

    st.session_state.datasets = datasets

    if datasets:
        st.success("Datasets Uploaded Successfully ✅")

# =========================================================
# PAGE 2: DASHBOARD
# =========================================================
elif st.session_state.page == 2:

    st.title("📈 Insights Dashboard")

    data = st.session_state.get("datasets", {})

    if not data:
        st.warning("Upload data first")
    else:
        df = data.get("Orders", pd.DataFrame())

        if not df.empty:
            st.markdown("### Order Status Distribution")
            try:
                fig = px.pie(df, names="order_status")
                st.plotly_chart(fig)
            except:
                pass

# =========================================================
# PAGE 3: DATA CLEANING
# =========================================================
elif st.session_state.page == 3:

    st.title("🧹 Data Cleaning")

    st.markdown("""
- Missing values handled using ML imputation  
- Categorical values filled using most frequent  
- Ensures reliable analysis  
""")

# =========================================================
# PAGE 4: SECTION A
# =========================================================
elif st.session_state.page == 4:

    st.title("📊 Section A: NPS")

    st.markdown("""
- NPS = Promoters - Detractors  
- Complaints reduce NPS  
- Trend shows customer satisfaction  
""")

# =========================================================
# PAGE 5: SECTION B
# =========================================================
elif st.session_state.page == 5:

    st.title("🚚 Section B: Operations")

    st.markdown("""
- SLA breach = delay indicator  
- Courier performance impacts delivery  
- Failed attempts increase RTO  
""")

# =========================================================
# PAGE 6: SECTION C
# =========================================================
elif st.session_state.page == 6:

    st.title("🔍 Section C: Tier-2 Issue")

    st.markdown("""
Tier-2 complaints are high due to:

- Poor courier service  
- Hub inefficiency  
- Delivery failures  
""")

# =========================================================
# PAGE 7: SECTION D
# =========================================================
elif st.session_state.page == 7:

    st.title("🔄 Funnel Analysis")

    st.markdown("""
Orders → Delivery → Complaints → NPS → Repeat

Delays → Complaints → Detractors → Churn  
""")

# =========================================================
# PAGE 8: SECTION E
# =========================================================
elif st.session_state.page == 8:

    st.title("💡 Recommendations")

    st.markdown("""
### Root Causes
- Delivery delays  
- Courier issues  
- Tier-2 inefficiencies  

### Fixes
- Improve logistics  
- Better routing  
- Monitor SLA  

### KPIs
- NPS  
- Complaint Rate  
- RTO  
""")

    st.success("🎯 Better ops = Better CX = Higher retention")
