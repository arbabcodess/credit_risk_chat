import matplotlib.pyplot as plt

def plot_ecl_curve(ecl_df, title="ECL Curve by Segment"):
    """
    Plots Expected Credit Loss (ECL) values across segments using matplotlib.
    Handles large or multi-dimensional segment labels gracefully.
    """

    if ecl_df is None or ecl_df.empty:
        raise ValueError("ECL DataFrame is empty or missing.")

    # Sort by ECL descending for better visualization
    ecl_df = ecl_df.sort_values(by="ECL", ascending=False)

    plt.figure(figsize=(10, 5))

    # Use bar chart if there are too many segments
    if len(ecl_df) > 10:
        plt.bar(ecl_df["Segment"], ecl_df["ECL"])
    else:
        plt.plot(ecl_df["Segment"], ecl_df["ECL"], marker="o", linewidth=2)

    plt.title(title, fontsize=12, fontweight="bold")
    plt.xlabel("Segment", fontsize=10)
    plt.ylabel("Expected Credit Loss (ECL)", fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    return plt
