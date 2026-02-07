# Superposed Epoch Analysis (SEA)

This repository provides a **Python implementation of Superposed Epoch Analysis (SEA)** to examine the relationship between **extreme inflation (CPI) events** and **GDP growth deviations** using standardized anomalies and Monte Carlo significance testing.

The project is designed to be **reproducible, research-oriented, and suitable for academic or portfolio use**.

---

## Overview

Superposed Epoch Analysis is an event-based statistical method widely used in:

- Economics and macroeconometrics
- Climate and environmental sciences
- Space and solar physics
- Event-driven time-series analysis

In this project, SEA is applied to test whether **extreme inflation events** are systematically associated with **abnormal GDP growth patterns**.

---

## Methodology

The analysis follows these steps:

### 1. Data Standardization
- CPI and GDP series are converted to z-scores to remove scale effects.

### 2. Event Identification
- Extreme inflation events are defined as years where:

  `|CPI_z| ≥ 1.5`

### 3. Epoch Construction
- For each event year, a symmetric time window is extracted:

  `t = [-k, ..., 0, ..., +k]`

- Here:
  - `t = 0` represents the event year
  - `k` is the number of years before and after the event

### 4. Composite Signal Calculation
- GDP anomalies are averaged across all event windows to obtain a composite response.

### 5. W-Statistic
- The W-statistic measures the deviation of GDP at the event year relative to surrounding background years.

### 6. Monte Carlo Randomization Test
- Event years are randomly sampled to generate a null distribution.
- Statistical significance is assessed using a p-value.

---

## Repository Structure

```

Superposed-Epoch-Analysis/
│
├── data/
│   └── data.xlsx                 # Input dataset (raw data)
│
├── src/
│   └── sea.py                    # SEA implementation (main code)
│
├── results/
│   └── figures/                  # Saved plots
│
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── .gitignore                    # Ignored files
└── LICENSE                       # MIT License

````

---

## Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
````

### Required Packages

* numpy
* pandas
* scipy
* matplotlib

---

## Usage

### Input Data Format

The input dataset must contain the following columns:

| Column | Description         |
| ------ | ------------------- |
| Year   | Observation year    |
| CPI    | Inflation rate (%)  |
| GDP    | GDP growth rate (%) |

### Running the Analysis

```bash
python SEA.py
```

---

## Outputs

The script generates:

* Composite GDP response plot relative to inflation events
* Null distribution of the W-statistic
* Console output including:

  * Observed W-statistic
  * Monte Carlo p-value
  * Hypothesis test conclusion

---

## Statistical Hypotheses

* **Null Hypothesis (H₀):**
  Extreme inflation events are not associated with systematic GDP deviations.

* **Alternative Hypothesis (H₁):**
  Extreme inflation events are associated with statistically significant GDP deviations.

---

## Author

**CH Pranav**
Applied Statistics • Econometrics • Time-Series Analysis

---
