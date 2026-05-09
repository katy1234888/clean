import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import plotly.express as px

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

# =========================================================
# 📖 SLIDE CONTROL (ONLY ADDITION)
# =========================================================
TOTAL_PAGES = 3

if "page" not in st.session_state:
    st.session_state.page = 0

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Previous"):
        if st.session_state.page > 0:
            st.session_state.page -= 1

with col3:
    if st.button("Next ➡️"):
        if st.session_state.page < 2:
            st.session_state.page += 1

st.markdown(f"### 📄 Slide {st.session_state.page + 1} / 3")

# =========================================================
# SLIDE 1: INTRO (UNCHANGED)
# =========================================================
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

# =========================================================
# SLIDE 2: BUSINESS CASE STORYBOARD (UNCHANGED LOGIC)
# =========================================================
elif st.session_state.page == 1:

    st.markdown("# 📘 Business Case Storyboard (Final)")

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

            courier_col = find_col(courier, ["courier"])
            delay_col = find_col(courier, ["delay"])
            complaint_rate_col = find_col(courier, ["complaint"])

            repeat_col = find_col(customers, ["repeat"])
            city_tier_col = find_col(orders, ["tier"])

            hub_city = "city"
            on_time = "on_time_delivery"
            failed = "failed_attempts"
            rto = "rto_count"

            if on_time in hubs.columns:
                hubs["sla_breach"] = 1 - hubs[on_time]

            if delivery_col and promised_col:
                orders[delivery_col] = pd.to_datetime(orders[delivery_col], errors="coerce")
                orders[promised_col] = pd.to_datetime(promised_col, errors="coerce")
                orders["delay"] = (orders[delivery_col] - orders[promised_col]).dt.days.fillna(0)
            else:
                orders["delay"] = 0

            st.markdown("## 📊 Section A: NPS & Customer Experience")

            if nps_score:
                promoters = nps[nps[nps_score] >= 9].shape[0]
                detractors = nps[nps[nps_score] <= 6].shape[0]
                total = len(nps)
                overall_nps = ((promoters - detractors) / total) * 100 if total else 0
                st.metric("Overall NPS", round(overall_nps, 2))

            if issue_col:
                st.bar_chart(complaints[issue_col].value_counts())

            st.markdown("## 🚚 Section B: Operational Performance")

            if "sla_breach" in hubs.columns:
                st.bar_chart(hubs.set_index(hub_city)["sla_breach"])

            if courier_col and delay_col:
                st.bar_chart(courier.set_index(courier_col)[delay_col])

            if failed in hubs.columns and rto in hubs.columns:
                st.write(hubs[[failed, rto]].corr())

            st.markdown("## 🔄 Section D: Funnel Analysis")

            if order_id and comp_order:
                delayed = orders[orders["delay"] > 0]
                delayed_comp = delayed.merge(complaints, left_on=order_id, right_on=comp_order)
                pct1 = (len(delayed_comp) / len(delayed)) * 100 if len(delayed) else 0
                st.metric("% Delayed → Complaints", round(pct1, 2))

    except Exception as e:
        st.warning(f"Storyboard Error: {e}")

# =========================================================
# SLIDE 3: DETAILED ANSWERS (UNCHANGED TEXT)
# =========================================================
elif st.session_state.page == 2:

    st.markdown("## 🔍 Section C: Problem Deep Dive")

st.markdown("""
### Observation:
Tier-2 cities have significantly higher complaint rates
""")

st.markdown("""
### 1. Is it due to specific courier partners?

Analysis Logic:
- Filter Tier-2 orders
- Join with complaints
- Check complaint distribution by courier

Insight:
If certain courier partners dominate complaints in Tier-2:
Yes — courier performance is a major driver

Interpretation:
Some courier partners may have:
- Poor last-mile reach
- Inexperienced delivery agents
- Weak infrastructure in Tier-2 regions

These partners perform fine in Tier-1 but struggle in Tier-2
""")

st.markdown("""
### 2. Is it due to hub inefficiencies?

Analysis Logic:
- Look at hubs serving Tier-2 cities
- Check on_time_delivery (low means bad)
- Check sla_breach (high means bad)

Insight:
If certain hubs show low on-time delivery and high SLA breach:
Yes — hub inefficiency is a key factor

Interpretation:
- Poor sorting or dispatch delays
- Capacity constraints
- Inefficient routing

This leads to systemic delays before last-mile delivery
""")

st.markdown("""
### 3. Is it due to delivery attempt failures?

Analysis Logic:
- Use failed_attempts
- Use rto_count

Insight:
If Tier-2 shows high failed attempts and high RTO:
Yes — delivery failures are a major contributor

Interpretation:
- Address issues
- Customer unavailability
- Poor communication

Failed delivery → Customer frustration → Complaint
""")

st.markdown("""
### Final Conclusion:

Weak courier performance
+ Hub inefficiencies
+ High failed deliveries
= Higher complaints in Tier-2 cities
""")

# =====================================================
# SECTION D
# =====================================================
st.markdown("## 🔄 Section D: End-to-End Funnel Analysis")

st.markdown("""
Orders → Delivery → Complaints → NPS → Repeat Orders
""")

st.markdown("""
### 1. What percentage of delayed orders result in complaints?

Formula:
(delayed orders with complaints / total delayed orders) * 100

Insight:
- High percentage means customers are highly sensitive to delays
- Low percentage means delays are tolerated

Business Meaning:
Delivery delay is a primary trigger of complaints
""")

st.markdown("""
### 2. What percentage of complaints turn into detractors?

Formula:
(detractors from complaints / total complaints) * 100

Insight:
- High percentage means complaint handling is poor
- Low percentage means support recovers customer trust

Business Meaning:
This reflects post-issue experience quality
""")

st.markdown("""
### 3. How does this impact repeat usage?

Logic:
Compare repeat rate of customers with complaints vs without complaints

Insight:
Lower repeat rate after complaints indicates customer churn

Funnel:
Delayed Delivery → Complaint Raised → Low NPS → Customer does NOT return

This directly impacts revenue
""")

# =====================================================
# SECTION E
# =====================================================
st.markdown("## 💡 Section E: Business Recommendations")

st.markdown("""
### 1. Top 3 Root Causes of Declining Customer Experience

1. Delivery delays caused by hub inefficiency and courier delays
2. Poor courier performance with high delay and complaint rates
3. Delivery failures such as high failed attempts and RTO
""")

st.markdown("""
### 2. Quick Wins (Short-Term Fixes)

- Fix worst performing courier partners
- Reduce failed deliveries through better address validation
- Improve SLA tracking with real-time alerts
""")

st.markdown("""
### 3. Long-Term Strategic Improvements

- Strengthen Tier-2 logistics infrastructure
- Use AI-based smart routing to predict delays
- Improve last-mile delivery experience with better tracking
""")

st.markdown("""
### 4. Suggested KPIs to Track

Customer Metrics:
- NPS
- Detractor percentage

Operational Metrics:
- SLA breach percentage
- On-time delivery percentage

Efficiency Metrics:
- Complaint rate
- Failed attempt rate
- RTO percentage

Growth Metric:
- Repeat purchase rate
""")

st.markdown("""
### Final Executive Summary:

The analysis shows that declining customer experience is driven by operational inefficiencies, especially in Tier-2 cities, where poor courier performance, hub delays, and high failed deliveries lead to increased complaints, lower NPS, and reduced repeat usage.
""")
