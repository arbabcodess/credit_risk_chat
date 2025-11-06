import sys, os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Ensure imports work regardless of where Streamlit runs
# -------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# -------------------------------------------------------
# Internal module imports (from /app folder)
# -------------------------------------------------------
from data_cleaning import clean_loan_data
from ecl_calculator import calculate_ecl
from visualization import plot_ecl_curve
from chat_module import get_recommendation
from auth_module import login_ui, current_user
from storage import save_ecl_results, load_all_results  # ✅ new for saving/viewing history

# -------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------
st.set_page_config(page_title="Credit Risk Analyst System", layout="wide")
st.title("💳 Credit Risk Analyst Dashboard")
st.markdown(
    """
Analyze loan portfolio risk, compute Expected Credit Loss (ECL) by segment, 
and generate AI-powered recommendations for credit policies.
"""
)

# -------------------------------------------------------
# Authentication (Sidebar)
# -------------------------------------------------------
logged_in = login_ui()
user = current_user()

if not logged_in:
    st.warning("Please sign in from the sidebar to access the dashboard.")
    st.stop()

st.sidebar.success(f"Signed in as: {user['display_name']} ({user['role'].upper()})")

# -------------------------------------------------------
# File Upload Section
# -------------------------------------------------------
st.header("📂 Upload Loan Dataset")

uploaded_file = st.file_uploader("📁 Upload your loan dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    if "raw_df" not in st.session_state:
        st.session_state.raw_df = pd.read_csv(uploaded_file)
        st.session_state.cleaned_df = clean_loan_data(st.session_state.raw_df)
        st.session_state.ecl_df = None

    st.subheader("📋 Raw Data Preview")
    st.dataframe(st.session_state.raw_df.head())

    st.subheader("🔍 ECL Analysis Setup")
    segment_col = st.selectbox(
        "Select a column to segment users by:", st.session_state.cleaned_df.columns
    )

    cro_only = (user["role"] == "cro")

    # -------------------------------------------------------
    # ECL Calculation
    # -------------------------------------------------------
    if st.button("📊 Calculate ECL"):
        with st.spinner("⚙️ Calculating Expected Credit Loss (ECL)..."):
            try:
                ecl_df = calculate_ecl(st.session_state.cleaned_df, segment_col)
                st.session_state.ecl_df = ecl_df
                st.success("✅ ECL Calculation Completed!")

                # ✅ Save results for this user
                save_ecl_results(
                    username=user["username"],
                    role=user["role"],
                    segment_col=segment_col,
                    ecl_df=ecl_df
                )
                st.info("📁 Results saved to history.")

            except Exception as e:
                st.error(f"❌ ECL calculation failed: {type(e).__name__}: {e}")
                st.stop()

    # -------------------------------------------------------
    # Display Results + Visualization
    # -------------------------------------------------------
    if st.session_state.get("ecl_df") is not None:
        ecl_df = st.session_state.ecl_df

        st.subheader("📈 ECL Results by Segment")
        st.dataframe(ecl_df)

        st.subheader("📉 ECL Curve Visualization")
        try:
            fig = plot_ecl_curve(ecl_df, f"ECL by {segment_col.title()}")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"⚠️ Plotting failed: {e}")

        # Download button
        csv = ecl_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "💾 Download ECL Results as CSV",
            data=csv,
            file_name=f"ecl_results_by_{segment_col}.csv",
            mime="text/csv",
        )

        # -------------------------------------------------------
        # AI Recommendations Section
        # -------------------------------------------------------
        st.subheader("🤖 AI-Powered Recommendations")

        if "Segment" not in ecl_df.columns:
            st.warning("⚠️ 'Segment' column missing in ECL results. Cannot generate AI recommendations.")
        else:
            segment_selected = st.selectbox(
                "Select a segment for AI analysis:", ecl_df["Segment"], key="segment_ai"
            )
            row = ecl_df[ecl_df["Segment"] == segment_selected].iloc[0]

            if st.button("🧠 Generate Recommendation", key="generate_ai"):
                with st.spinner("Analyzing with Hugging Face model..."):
                    try:
                        suggestion = get_recommendation(
                            segment_selected,
                            row.get("ECL", 0),
                            row.get("PD", 0),
                            row.get("LGD", 0)
                        )
                        st.session_state.recommendation = suggestion
                        st.success("✅ Recommendation Generated!")
                    except Exception as e:
                        st.error(f"❌ Error generating recommendation: {e}")

            if "recommendation" in st.session_state:
                st.markdown("### 💡 Model Suggestion:")
                st.write(st.session_state.recommendation)

        # -------------------------------------------------------
        # CRO Policy Actions
        # -------------------------------------------------------
        if cro_only:
            st.markdown("---")
            st.subheader("🔐 CRO Policy Actions")
            st.write("As CRO, you can record a policy action for the selected segment.")
            action = st.selectbox(
                "Select Action",
                ["No change", "Increase interest by 1%", "Reduce disbursement by 20%"]
            )
            if st.button("Apply Action"):
                st.success(f"📘 Policy action '{action}' recorded for segment {segment_selected}.")
        else:
            st.info("Only CRO users can record policy actions in this demo.")

    # -------------------------------------------------------
    # CRO View All User Submissions
    # -------------------------------------------------------
    if cro_only:
        st.markdown("---")
        st.subheader("📜 View All User Submissions")

        history_df = load_all_results()
        if history_df.empty:
            st.info("No ECL results have been saved yet.")
        else:
            st.dataframe(history_df)

            selected_user = st.selectbox(
                "Filter by user (optional):",
                ["All"] + list(history_df["username"].unique())
            )

            if selected_user != "All":
                filtered_df = history_df[history_df["username"] == selected_user]
                st.dataframe(filtered_df)

            csv_data = history_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "💾 Download All Results (CSV)",
                data=csv_data,
                file_name="all_ecl_history.csv"
            )

else:
    st.info("👆 Please upload your dataset to start the analysis.")
