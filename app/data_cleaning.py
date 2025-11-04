import pandas as pd
import numpy as np

def clean_loan_data(df):
    """
    Cleans and prepares the 14-column Credit Risk dataset for analysis.
    Handles missing values, standardizes text columns, and ensures correct data types.
    """

    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Check for expected columns
    expected_cols = [
        "person_age", "person_gender", "person_education", "person_income",
        "person_emp_exp", "person_home_ownership", "loan_amnt",
        "loan_intent", "loan_int_rate", "loan_percent_income",
        "cb_person_cred_hist_length", "credit_score",
        "previous_loan_defaults_on_file", "loan_status"
    ]

    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in dataset: {missing_cols}")

    # ------------------------------
    # 1️⃣ Handle missing values
    # ------------------------------
    # Numeric columns → fill with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    # Categorical columns → fill with mode
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # ------------------------------
    # 2️⃣ Clean and normalize categorical fields
    # ------------------------------
    df['person_gender'] = df['person_gender'].str.strip().str.lower()
    df['person_home_ownership'] = df['person_home_ownership'].str.strip().str.upper()
    df['loan_intent'] = df['loan_intent'].str.strip().str.upper()
    df['person_education'] = df['person_education'].str.strip().str.title()
    df['previous_loan_defaults_on_file'] = df['previous_loan_defaults_on_file'].str.strip().str.title()

    # ------------------------------
    # 3️⃣ Fix data types
    # ------------------------------
    df['loan_status'] = df['loan_status'].astype(int)
    df['person_age'] = df['person_age'].astype(float)
    df['person_emp_exp'] = df['person_emp_exp'].astype(float)
    df['loan_amnt'] = df['loan_amnt'].astype(float)
    df['loan_int_rate'] = df['loan_int_rate'].astype(float)
    df['credit_score'] = df['credit_score'].astype(float)
    df['cb_person_cred_hist_length'] = df['cb_person_cred_hist_length'].astype(float)

    # ------------------------------
    # 4️⃣ Create derived / helper columns
    # ------------------------------
    # Create a loss_amount column (if loan_status = 0, assume 40% loss)
    df['loss_amount'] = np.where(df['loan_status'] == 0, df['loan_amnt'] * 0.4, 0)

    # ------------------------------
    # 5️⃣ Remove outliers (optional)
    # ------------------------------
    df = df[(df['loan_amnt'] > 1000) & (df['loan_amnt'] < 1000000)]
    df = df[df['credit_score'].between(300, 850)]

    # ------------------------------
    # 6️⃣ Reset index and return
    # ------------------------------
    df.reset_index(drop=True, inplace=True)
    print(f"✅ Data cleaned successfully. Shape: {df.shape}")
    return df

