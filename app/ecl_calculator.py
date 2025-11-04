import pandas as pd


def calculate_ecl(df, segment_col):
    """
    Calculate PD (Probability of Default), LGD (Loss Given Default),
    EAD (Exposure at Default), and ECL (Expected Credit Loss)
    for each user segment (e.g. loan_intent, education, gender).
    """

    if segment_col not in df.columns:
        raise ValueError(f"Column '{segment_col}' not found in dataset.")

    results = []
    grouped = df.groupby(segment_col)

    for segment, group in grouped:
        total_loans = len(group)

        # PD = Probability of Default
        pd_value = (group['loan_status'] == 0).mean()  # since 0 = default

        # LGD = Loss Given Default (use average loss / loan amount)
        lgd_value = group.loc[group['loan_status'] == 0, 'loss_amount'].mean(
        ) / group['loan_amnt'].mean() if (group['loan_status'] == 0).any() else 0

        # EAD = Exposure at Default = average loan amount
        ead_value = group['loan_amnt'].mean()

        # ECL = PD × LGD × EAD
        ecl = pd_value * lgd_value * ead_value

        results.append({
            'Segment': segment,
            'Total Loans': total_loans,
            'PD': round(pd_value, 4),
            'LGD': round(lgd_value, 4),
            'EAD': round(ead_value, 2),
            'ECL': round(ecl, 2)
        })

    result_df = pd.DataFrame(results).sort_values(by='ECL', ascending=False)
    return result_df
