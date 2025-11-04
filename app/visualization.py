import matplotlib.pyplot as plt


def plot_ecl_curve(ecl_df, title="ECL Curve by Segment"):
    """
    Plots ECL values across segments using matplotlib.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(ecl_df['Segment'], ecl_df['ECL'], marker='o')
    plt.title(title)
    plt.xlabel('User Segment')
    plt.ylabel('Expected Credit Loss')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    return plt
