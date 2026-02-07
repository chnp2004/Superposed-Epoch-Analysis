"""
Superposed Epoch Analysis (SEA)
--------------------------------
Analyzes the association between extreme inflation events (CPI)
and GDP growth deviations using standardized anomalies.

Author: <Your Name>
License: MIT
"""

from typing import Tuple, List
import numpy as np
import pandas as pd
from scipy.stats import zscore
import matplotlib.pyplot as plt
import logging

# ------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Data Utilities
# ------------------------------------------------------------------
def load_and_standardize(filepath: str) -> pd.DataFrame:
    """
    Load dataset and standardize CPI and GDP columns.

    Parameters
    ----------
    filepath : str
        Path to Excel file containing Year, CPI, GDP columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with standardized CPI_z and GDP_z columns.
    """
    data = pd.read_excel(filepath)

    for col in ["CPI", "GDP"]:
        data[f"{col}_z"] = zscore(data[col], nan_policy="omit")

    return data


def identify_events(data: pd.DataFrame, threshold: float = 1.5) -> pd.DataFrame:
    """
    Identify extreme CPI events based on z-score threshold.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset with CPI_z column.
    threshold : float
        Z-score threshold for extreme events.

    Returns
    -------
    pd.DataFrame
        DataFrame containing extreme CPI events.
    """
    return data[(data["CPI_z"] >= threshold) | (data["CPI_z"] <= -threshold)]


# ------------------------------------------------------------------
# SEA Core Analysis
# ------------------------------------------------------------------
def superposed_epoch_analysis(
    data: pd.DataFrame,
    events: pd.DataFrame,
    window: int = 3,
    n_iter: int = 10000,
    seed: int = 42
) -> Tuple[float, float, np.ndarray, List[float]]:
    """
    Perform Superposed Epoch Analysis (SEA).

    Parameters
    ----------
    data : pd.DataFrame
        Full dataset containing GDP_z.
    events : pd.DataFrame
        Event years identified from CPI extremes.
    window : int
        Number of years before and after event.
    n_iter : int
        Number of Monte Carlo iterations.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    W : float
        Observed W-statistic.
    p_value : float
        Monte Carlo p-value.
    composite : np.ndarray
        Composite GDP response.
    null_dist : list
        Null distribution of W-statistics.
    """
    np.random.seed(seed)

    epoch_matrix = []

    for idx in events.index:
        start, end = idx - window, idx + window + 1
        if start >= 0 and end <= len(data):
            epoch_matrix.append(data.iloc[start:end]["GDP_z"].values)

    if not epoch_matrix:
        raise ValueError("No valid epochs could be constructed.")

    epoch_matrix = np.array(epoch_matrix)
    composite = np.mean(epoch_matrix, axis=0)

    # W-statistic
    event_values = epoch_matrix[:, window]
    background = np.delete(epoch_matrix, window, axis=1)

    diffs = np.concatenate([event_values[i] - background[i] for i in range(len(event_values))])
    W = (np.mean(diffs) * np.sqrt(len(diffs))) / np.std(diffs)

    # Monte Carlo randomization
    null_dist = []
    for _ in range(n_iter):
        random_centers = np.random.choice(len(data), len(events), replace=False)
        rand_diffs = []

        for c in random_centers:
            s, e = c - window, c + window + 1
            if s >= 0 and e <= len(data):
                epoch = data.iloc[s:e]["GDP_z"].values
                rand_diffs.extend(epoch[window] - np.delete(epoch, window))

        if rand_diffs:
            null_dist.append(
                (np.mean(rand_diffs) * np.sqrt(len(rand_diffs))) / np.std(rand_diffs)
            )

    p_value = (np.sum(np.abs(null_dist) >= abs(W)) + 1) / (n_iter + 1)

    return W, p_value, composite, null_dist


# ------------------------------------------------------------------
# Visualization
# ------------------------------------------------------------------
def plot_sea_results(composite: np.ndarray, null_dist: List[float], W: float, window: int) -> None:
    """Plot composite signal and null distribution."""
    x = np.arange(-window, window + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x, composite, marker="o")
    plt.axhline(0, linestyle="--")
    plt.axvline(0, linestyle=":")
    plt.title("Composite GDP Response")
    plt.xlabel("Years Relative to Event")
    plt.ylabel("Standardized GDP")

    plt.subplot(1, 2, 2)
    plt.hist(null_dist, bins=30)
    plt.axvline(W, linestyle="--")
    plt.title("Null Distribution of W-statistic")
    plt.xlabel("W value")

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# Main execution
# ------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("Running Superposed Epoch Analysis")

    df = load_and_standardize("data.xlsx")
    events = identify_events(df, threshold=1.5)

    W, p, composite, null = superposed_epoch_analysis(
        df, events, window=3, n_iter=10000
    )

    logger.info(f"W-statistic = {W:.3f}")
    logger.info(f"P-value = {p:.4f}")

    plot_sea_results(composite, null, W, window=3)
