import pandas as pd
import numpy as np

def calculate_ecl(df, segment_col):
    """
    Calculate PD (Probability of Default), LGD (Loss Given Default),
    EAD (Exposure at Default), and ECL (Expected Credit Loss)
    for each segment (e.g., loan_intent, education, gender).
    """

    # --- Sanity checks ---
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")
    if segment_col not in df.columns:
        raise ValueError(f"Column '{segment_col}' not found in dataset.")
    if "loan_status" not in df.columns:
        raise ValueError("Column 'loan_status' is required but missing.")
    if "loan_amnt" not in df.columns:
        raise ValueError("Column 'loan_amnt' is required but missing.")

    # Convert numeric columns safely
    numeric_cols = ["loan_amnt", "loan_int_rate", "credit_score", "person_income"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace NaNs
    df = df.fillna({
        "loan_int_rate": df["loan_int_rate"].mean() if "loan_int_rate" in df else 0,
        "loan_amnt": df["loan_amnt"].mean(),
    })

    results = []
    grouped = df.groupby(segment_col)

    for segment, group in grouped:
        total_loans = len(group)

        # PD = Probability of Default
        pd_value = (group["loan_status"] == 0).mean()

        # LGD = base 35%, adjusted slightly by interest rate if available
        avg_rate = group["loan_int_rate"].mean() if "loan_int_rate" in group else 0
        lgd_value = 0.35 + (avg_rate / 100) * 0.05

        # EAD = average loan amount
        ead_value = group["loan_amnt"].mean()

        # ECL = PD × LGD × EAD
        ecl = pd_value * lgd_value * ead_value

        results.append({
            "Segment": str(segment),
            "Total Loans": total_loans,
            "PD": round(pd_value, 4),
            "LGD": round(lgd_value, 4),
            "EAD": round(ead_value, 2),
            "ECL": round(ecl, 2)
        })

    if not results:
        raise ValueError("No valid segments found in dataset.")

    result_df = pd.DataFrame(results).sort_values(by="ECL", ascending=False)
    return result_df
