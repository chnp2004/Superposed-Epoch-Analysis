# Superposed Epoch Analysis (SEA)

This repository provides a **Python implementation of Superposed Epoch Analysis (SEA)** to study the relationship between **extreme inflation (CPI) events** and **GDP growth deviations** using standardized anomalies and Monte Carlo significance testing.

The implementation is suitable for **academic research, reproducible analysis, and portfolio demonstration**.

---

## 📌 Overview

Superposed Epoch Analysis is an event-based statistical technique widely used in:

- Economics & Macroeconometrics  
- Climate and environmental sciences  
- Space and solar physics  
- Event-driven time-series analysis  

In this project, SEA is applied to test whether **extreme inflation events** are systematically associated with **abnormal GDP growth behavior**.

---

## 📊 Methodology

The analysis follows these steps:

1. **Data Standardization**  
   - CPI and GDP series are converted to z-scores.

2. **Event Identification**  
   - Extreme inflation events are defined as:
     ```
     |CPI_z| ≥ 1.5
     ```

3. **Epoch Construction**  
   - For each event year, a symmetric window is extracted:
     ```
     t = [-k, ..., 0, ..., +k]
     ```

4. **Composite Signal Calculation**  
   - GDP anomalies are averaged across all events.

5. **W-Statistic**  
   - Measures deviation of GDP at the event year relative to surrounding background years.

6. **Monte Carlo Randomization Test**  
   - Random event years are sampled to generate a null distribution.
   - Statistical significance is evaluated using a p-value.

---

## 📁 Repository Structure


---

## ⚙️ Requirements

Install dependencies using:

```bash
pip install -r requirements.txt

