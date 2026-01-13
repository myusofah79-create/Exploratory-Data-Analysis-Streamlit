import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from io import StringIO

st.set_page_config(page_title="Analyze Your Data", layout="wide")

st.title("📊 Analyze Your Data")
st.write("Upload a CSV or Excel file to explore your data interactively")

# =====================
# File Upload
# =====================
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

def load_data(file):
    ext = Path(file.name).suffix.lower()
    if ext == ".csv":
        return pd.read_csv(file)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file)

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("✅ File uploaded successfully")

    # =====================
    # Data Preview
    # =====================
    st.header("🔍 Data Preview")
    st.dataframe(df.head())

    # =====================
    # Data Overview
    # =====================
    st.header("📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    # =====================
    # Dataset Info
    # =====================
    st.header("📦 Dataset Info")
    buffer = StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    # =====================
    # Statistical Summary (Numerical)
    # =====================
    st.header("📈 Statistical Summary (Numerical)")
    num_cols = df.select_dtypes(include=np.number).columns

    if len(num_cols) > 0:
        st.dataframe(df[num_cols].describe())
    else:
        st.info("No numerical columns found.")

    # =====================
    # Statistical Summary (Non-Numerical)
    # =====================
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns

    if len(cat_cols) > 0:
        st.header("📋 Statistical Summary (Non-Numerical)")
        st.dataframe(df[cat_cols].describe())
    else:
        st.info("No non-numerical columns found.")

    # =====================
    # Select Columns
    # =====================
    st.header("✂️ Select Columns for Analysis")
    selected_cols = st.multiselect(
        "Choose columns",
        df.columns.tolist()
    )

    if selected_cols:
        st.dataframe(df[selected_cols].head())

    # =====================
    # Visualization
    # =====================
    st.header("📊 Data Visualization")

    chart_type = st.radio(
        "Select Chart Type",
        [
            "Line Chart",
            "Scatter Chart",
            "Bar Chart",
            "Histogram",
            "Box Plot",
            "Area Chart",
            "Violin Plot",
            "Correlation Heatmap"
        ],
        horizontal=True
    )

    x_axis = st.selectbox("Select X-Axis", df.columns)
    y_axis = st.selectbox("Select Y-Axis", df.columns)

    fig, ax = plt.subplots(figsize=(10, 5))

    if chart_type == "Line Chart":
        ax.plot(df[x_axis], df[y_axis])

    elif chart_type == "Scatter Chart":
        ax.scatter(df[x_axis], df[y_axis])

    elif chart_type == "Bar Chart":
        ax.bar(df[x_axis], df[y_axis])

    elif chart_type == "Histogram":
        ax.hist(df[x_axis], bins=30)

    elif chart_type == "Box Plot":
        sns.boxplot(x=df[x_axis], ax=ax)

    elif chart_type == "Area Chart":
        ax.fill_between(range(len(df[y_axis])), df[y_axis])

    elif chart_type == "Violin Plot":
        sns.violinplot(x=df[x_axis], ax=ax)

    elif chart_type == "Correlation Heatmap":
        corr = df.select_dtypes(include=np.number).corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        st.pyplot(fig)
        st.stop()

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{chart_type} of {x_axis} vs {y_axis}")

    st.pyplot(fig)
