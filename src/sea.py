import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

# Load data
print("=== STEP 1: DATA LOADING ===")
data = pd.read_excel('C:\\Users\\chakr\\OneDrive\\Documents\\PRANAV\\Research Papers\\Superposed epoch analysis\\code\\data\\data.xlsx')
print("Raw Data (First 5 rows):\n", data.head())

# Standardize data
print("\n=== STEP 2: DATA STANDARDIZATION ===")
for col in ['CPI', 'GDP']:
    data[f'{col}_z'] = zscore(data[col])
    print(f"\n{col} Standardization:")
    print(f"Mean ({col}): {data[col].mean():.2f}%")
    print(f"Std Dev ({col}): {data[col].std():.2f}%")
print("\nStandardized Data (First 5 rows):\n", data[['Year', 'CPI_z', 'GDP_z']].head())

# Identify events
print("\n=== STEP 3: EVENT IDENTIFICATION ===")
threshold = 1.5
events_high = data[data['CPI_z'] >= threshold]
events_low = data[data['CPI_z'] <= -threshold]
events = pd.concat([events_high, events_low])

print("\nNull Hypothesis (H₀):")
print("There is no association between extreme inflation events (≥1.5σ) and GDP growth patterns")
print("\nAlternative Hypothesis (Hₐ):")
print("Extreme inflation events are associated with systematic GDP growth deviations")

print(f"\nIdentified Events ({len(events)}):")
print(events[['Year', 'CPI', 'CPI_z']].to_string(index=False))

def sea_analysis(data, events, window=3, n_iter=1000):
    print("\n=== STEP 4: EPOCH CONSTRUCTION ===")
    epoch_matrix = []
    valid_events = []
    
    # Generate column labels dynamically based on window size
    time_points = [f"t-{i}" for i in range(window, 0, -1)] + ["t0"] + [f"t+{i}" for i in range(1, window+1)]
    
    for idx, event in events.iterrows():
        center = event.name
        start = center - window
        end = center + window + 1
        
        if start >= 0 and end <= len(data):
            epoch = data.iloc[start:end]['GDP_z'].values
            epoch_matrix.append(epoch)
            valid_events.append(event['Year'])
            print(f"\nEvent {event['Year']} (CPI: {event['CPI']:.1f}%):")
            print(f"Epoch window: {data.iloc[start]['Year']}-{data.iloc[end-1]['Year']}")
            print("GDP_z values:", np.round(epoch, 2))
        else:
            print(f"Skipping event {event['Year']} - insufficient data window")

    epoch_matrix = np.array(epoch_matrix)
    print("\nFinal Epoch Matrix:")
    print(pd.DataFrame(epoch_matrix, 
                      columns=time_points,
                      index=valid_events))

    # Composite signal
    print("\n=== STEP 5: COMPOSITE SIGNAL CALCULATION ===")
    composite = np.nanmean(epoch_matrix, axis=0)
    print("Composite GDP_z values:")
    print(pd.Series(composite, index=time_points))

    # W-statistic calculation
    print("\n=== STEP 6: W-STATISTIC CALCULATION ===")
    event_years = epoch_matrix[:, window]
    background = np.delete(epoch_matrix, window, axis=1)
    
    diffs = []
    for e, b_row in zip(event_years, background):
        diffs.extend([e - b for b in b_row])
    
    W = (np.mean(diffs) * np.sqrt(len(diffs))) / np.std(diffs)
    print(f"W-statistic = {W:.3f}")
    
    # Randomization test
    print("\n=== STEP 7: RANDOMIZATION TEST ===")
    np.random.seed(42)
    null_dist = []
    
    for i in range(n_iter):
        # Random event years
        random_events = np.random.choice(len(data), size=len(events), replace=False)
        
        # Calculate random W
        rand_diffs = []
        for center in random_events:
            start = max(0, center - window)
            end = min(len(data), center + window + 1)
            epoch = data.iloc[start:end]['GDP_z'].values
            if len(epoch) == 2*window + 1:
                rand_event = epoch[window]
                rand_background = np.delete(epoch, window)
                rand_diffs.extend([rand_event - b for b in rand_background])
        
        if rand_diffs:
            rand_W = (np.mean(rand_diffs) * np.sqrt(len(rand_diffs))) / np.std(rand_diffs)
            null_dist.append(rand_W)

    # Calculate p-value
    extreme_count = sum(np.abs(null_dist) >= np.abs(W))
    p_value = (extreme_count + 1) / (n_iter + 1)
    
    print("\n=== STATISTICAL INFERENCE ===")
    print(f"Observed W-statistic: {W:.3f}")
    print(f"P-value: {p_value:.4f}")
    print("\nConclusion:")
    if p_value < 0.05:
        print("Reject H₀: Significant association between inflation extremes and GDP patterns")
    else:
        print("Fail to reject H₀: No significant association detected")
    print(f"(Significance level α = 0.05)")

    # Plot results
    plt.figure(figsize=(12, 5))
    
    # Composite signal plot
    plt.subplot(1, 2, 1)
    time_indices = np.arange(-window, window+1)
    plt.plot(time_indices, composite, 'o-', label='Composite Signal')
    plt.axhline(0, color='grey', linestyle='--')
    plt.axvline(0, color='red', linestyle=':', label='Event Year')
    plt.title('Composite GDP Response')
    plt.xlabel('Years Relative to Event')
    plt.ylabel('Standardized GDP')
    plt.xticks(time_indices)
    plt.legend()
    
    # Null distribution plot
    plt.subplot(1, 2, 2)
    plt.hist(null_dist, bins=30, edgecolor='black')
    plt.axvline(W, color='red', linestyle='--', label='Observed W')
    plt.title('Null Distribution of W-Statistic')
    plt.xlabel('W-Statistic Value')
    plt.ylabel('Frequency')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

    return W, p_value

# Run analysis with 3-year window and 10000 iterations
print("\n=== MAIN ANALYSIS ===")
W, p = sea_analysis(data, events, window=3, n_iter=10000)
