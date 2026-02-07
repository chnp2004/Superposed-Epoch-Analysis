## 📊 Methodology

1. **Data Standardization**
   - CPI and GDP series are converted to z-scores.

2. **Event Identification**
   - Extreme inflation events are defined as:
     
     `|CPI_z| ≥ 1.5`

3. **Epoch Construction**
   - For each event year, a symmetric time window is extracted:
     
     `t = [-k, ..., 0, ..., +k]`
     
     where `t = 0` represents the event year.

4. **Composite Signal Calculation**
   - GDP anomalies are averaged across all events.

5. **W-Statistic**
   - Measures deviation of GDP at the event year relative to surrounding background years.

6. **Monte Carlo Randomization Test**
   - Random event years are sampled to generate a null distribution.
   - Statistical significance is evaluated using a p-value.
