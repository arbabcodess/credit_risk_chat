import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_cleaning import clean_loan_data
from ecl_calculator import calculate_ecl
from visualization import plot_ecl_curve
from chat_module import get_recommendation

# ------------------------------------------------------------
# Streamlit App Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Credit Risk Analyst System", layout="wide")

# App Header
st.title("💳 Credit Risk Analyst Dashboard")
st.markdown(
    """
    Analyze loan portfolio risk, compute ECL by segment, visualize results, 
    and generate AI-based recommendations for smarter credit decisions.
    """
)

# ------------------------------------------------------------
# 1️⃣ File Upload Section
# ------------------------------------------------------------
uploaded_file = st.file_uploader("📁 Upload your loan dataset (CSV)", type=["csv"])

# Store uploaded data in session
if uploaded_file is not None:
    if "raw_df" not in st.session_state:
        st.session_state.raw_df = pd.read_csv(uploaded_file)
        st.session_state.cleaned_df = clean_loan_data(st.session_state.raw_df)
        st.session_state.ecl_df = None  # reset previous ECL results
else:
    st.info("👆 Please upload your dataset to start the analysis.")

# Proceed if data is uploaded
if "cleaned_df" in st.session_state:
    st.subheader("📋 Raw Data Preview")
    st.dataframe(st.session_state.raw_df.head())

    # ------------------------------------------------------------
    # 2️⃣ Select segmentation column
    # ------------------------------------------------------------
    st.subheader("🔍 ECL Analysis Setup")
    segment_col = st.selectbox(
        "Select a column to segment users by:",
        st.session_state.cleaned_df.columns,
        key="segment_select"
    )

    # ------------------------------------------------------------
    # 3️⃣ Calculate ECL
    # ------------------------------------------------------------
    if st.button("📊 Calculate ECL"):
        with st.spinner("⚙️ Calculating Expected Credit Loss (ECL)..."):
            ecl_df = calculate_ecl(st.session_state.cleaned_df, segment_col)
            st.session_state.ecl_df = ecl_df  # store results
        st.success("✅ ECL Calculation Completed!")

    # ------------------------------------------------------------
    # 4️⃣ Display Results + Plot + Download
    # ------------------------------------------------------------
    if st.session_state.get("ecl_df") is not None:
        ecl_df = st.session_state.ecl_df

        st.subheader("📈 ECL Results by Segment")
        st.dataframe(ecl_df)

        st.subheader("📉 ECL Curve Visualization")
        fig = plot_ecl_curve(ecl_df, f"ECL by {segment_col.title()}")
        st.pyplot(fig)

        csv = ecl_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Download ECL Results as CSV",
            data=csv,
            file_name=f"ecl_results_by_{segment_col}.csv",
            mime="text/csv"
        )

        # ------------------------------------------------------------
        # 5️⃣ AI Recommendations (no reload now)
        # ------------------------------------------------------------
        st.subheader("🤖 AI-Powered Recommendations")

        segment_selected = st.selectbox(
            "Select a segment for AI analysis:", ecl_df["Segment"], key="segment_ai"
        )
        row = ecl_df[ecl_df["Segment"] == segment_selected].iloc[0]

        if st.button("🧠 Generate Recommendation", key="generate_ai"):
            with st.spinner("Analyzing segment with Hugging Face model..."):
                suggestion = get_recommendation(
                    segment_selected,
                    row["ECL"],
                    row["PD"],
                    row["LGD"]
                )
                st.session_state.recommendation = suggestion  # store in session
            st.success("✅ Recommendation Generated!")

        # If a recommendation is stored, display it
        if "recommendation" in st.session_state:
            st.write(st.session_state.recommendation)
