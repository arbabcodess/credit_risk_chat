import os
import pandas as pd
from datetime import datetime

DATA_FILE = "user_ecl_history.csv"


def save_ecl_results(username, role, segment_col, ecl_df):
    """Append ECL results for a user to persistent CSV storage."""
    if ecl_df is None or ecl_df.empty:
        return

    # Add metadata columns
    ecl_df = ecl_df.copy()
    ecl_df["username"] = username
    ecl_df["role"] = role
    ecl_df["segment_col"] = segment_col
    ecl_df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save or append to CSV
    if not os.path.exists(DATA_FILE):
        ecl_df.to_csv(DATA_FILE, index=False)
    else:
        existing = pd.read_csv(DATA_FILE)
        combined = pd.concat([existing, ecl_df], ignore_index=True)
        combined.to_csv(DATA_FILE, index=False)


def load_all_results():
    """Load all saved ECL results."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)


def load_user_results(username):
    """Load results for a specific user."""
    df = load_all_results()
    if df.empty:
        return df
    return df[df["username"] == username]
