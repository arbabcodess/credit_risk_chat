import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_cleaning import clean_loan_data
from ecl_calculator import calculate_ecl
from visualization import plot_ecl_curve
from chat_module import get_recommendation
from auth_module import login_ui, current_user

# App config
st.set_page_config(page_title="Credit Risk Analyst System", layout="wide")
st.title("💳 Credit Risk Analyst Dashboard")
st.markdown(
    "Analyze loan portfolio risk, compute ECL by segment, visualize results, and get AI recommendations."
)

# ---------------------------
# Authentication (sidebar)
# ---------------------------
logged_in = login_ui()
user = current_user()

if not logged_in:
    st.warning("Please sign in from the sidebar to access the dashboard.")
    st.stop()  # stops execution for non-logged-in users

# From here onwards, the user is authenticated
st.sidebar.success(f"Signed in: {user['display_name']} ({user['role'].upper()})")

# ---------------------------
# Upload & session handling
# ---------------------------
uploaded_file = st.file_uploader("📁 Upload your loan dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    if "raw_df" not in st.session_state:
        st.session_state.raw_df = pd.read_csv(uploaded_file)
        st.session_state.cleaned_df = clean_loan_data(st.session_state.raw_df)
        st.session_state.ecl_df = None
else:
    st.info("👆 Please upload your dataset to start the analysis.")

if "cleaned_df" in st.session_state:
    st.subheader("📋 Raw Data Preview")
    st.dataframe(st.session_state.raw_df.head())

    st.subheader("🔍 ECL Analysis Setup")
    segment_col = st.selectbox("Select a column to segment users by:", st.session_state.cleaned_df.columns)

    # Only CRO can trigger policy changes / downloads in this demo (example policy)
    cro_only = (user["role"] == "cro")

    if st.button("📊 Calculate ECL"):
        with st.spinner("⚙️ Calculating Expected Credit Loss (ECL)..."):
            ecl_df = calculate_ecl(st.session_state.cleaned_df, segment_col)
            st.session_state.ecl_df = ecl_df
        st.success("✅ ECL Calculation Completed!")

    if st.session_state.get("ecl_df") is not None:
        ecl_df = st.session_state.ecl_df
        st.subheader("📈 ECL Results by Segment")
        st.dataframe(ecl_df)

        st.subheader("📉 ECL Curve Visualization")
        fig = plot_ecl_curve(ecl_df, f"ECL by {segment_col.title()}")
        st.pyplot(fig)

        csv = ecl_df.to_csv(index=False).encode("utf-8")
        # Download available to both, but show a warning to analyst about restricted actions
        st.download_button("💾 Download ECL Results as CSV", data=csv, file_name=f"ecl_results_by_{segment_col}.csv")

        st.subheader("🤖 AI-Powered Recommendations")
        segment_selected = st.selectbox("Select a segment for AI analysis:", ecl_df["Segment"], key="segment_ai")
        row = ecl_df[ecl_df["Segment"] == segment_selected].iloc[0]

        if st.button("🧠 Generate Recommendation", key="generate_ai"):
            with st.spinner("Analyzing with LLM..."):
                suggestion = get_recommendation(segment_selected, row["ECL"], row["PD"], row["LGD"])
                st.session_state.recommendation = suggestion
            st.success("✅ Recommendation Generated!")

        if "recommendation" in st.session_state:
            st.write(st.session_state.recommendation)

        # Example CRO-only action: apply policy change (just a demo)
        if cro_only:
            st.markdown("---")
            st.subheader("🔐 CRO Actions")
            st.write("As CRO you can record a policy action for the selected segment.")
            action = st.selectbox("Select action", ["No change", "Increase interest by 1%", "Reduce disbursement by 20%"])
            if st.button("Apply Action"):
                # In a real app you would save this to DB or create a report
                st.success(f"Policy action '{action}' recorded for segment {segment_selected} (demo).")
        else:
            st.info("Only users with the CRO role can record policy actions in this demo.")