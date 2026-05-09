import streamlit as st
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

st.title("📦 Seashells Logistics - Data Dashboard")

# -------------------------------
# FILE UPLOAD SECTION
# -------------------------------
st.sidebar.header("Upload Datasets")

orders_file = st.sidebar.file_uploader("Upload Orders Data", type=["csv"])
customers_file = st.sidebar.file_uploader("Upload Customers Data", type=["csv"])
nps_file = st.sidebar.file_uploader("Upload NPS Data", type=["csv"])
complaints_file = st.sidebar.file_uploader("Upload Complaints Data", type=["csv"])
hub_file = st.sidebar.file_uploader("Upload Hub Performance Data", type=["csv"])
courier_file = st.sidebar.file_uploader("Upload Courier Performance Data", type=["csv"])


# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
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

    # Separate numeric and categorical
    num_cols = df_clean.select_dtypes(include=np.number).columns
    cat_cols = df_clean.select_dtypes(exclude=np.number).columns

    # Numerical Imputation (ML-based)
    if len(num_cols) > 0:
        imputer_num = IterativeImputer(random_state=0)
        df_clean[num_cols] = imputer_num.fit_transform(df_clean[num_cols])

    # Categorical Imputation
    if len(cat_cols) > 0:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df_clean[cat_cols] = imputer_cat.fit_transform(df_clean[cat_cols])

    return df_clean


# -------------------------------
# LOAD DATA
# -------------------------------
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


# -------------------------------
# SHOW RAW DATA SUMMARIES
# -------------------------------
if datasets:
    st.header("📌 Raw Data Overview")

    for name, df in datasets.items():
        with st.expander(f"{name} Dataset"):
            dataset_summary(df, name)

# -------------------------------
# DATA CLEANING SECTION
# -------------------------------
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

else:
    st.info("Toggle the switch to clean data")


# -------------------------------
# OPTIONAL: DOWNLOAD CLEAN DATA
# -------------------------------
if clean_toggle and cleaned_datasets:
    st.header("⬇️ Download Cleaned Data")

    for name, df in cleaned_datasets.items():
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {name} Cleaned Data",
            data=csv,
            file_name=f"{name}_cleaned.csv",
            mime='text/csv'
        )
