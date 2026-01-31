import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 1. LIST YOUR FILENAMES
# Make sure these match the names of the files you uploaded to the sidebar
files = ['KwhConsumptionBlower78_1.csv', 'KwhConsumptionBlower78_2.csv', 'KwhConsumptionBlower78_3.csv']

# Check if files exist to avoid errors
missing_files = [f for f in files if not os.path.exists(f)]
if missing_files:
    print(f"Error: The following files are missing in Colab: {missing_files}")
    print("Please upload them using the folder icon on the left sidebar.")
else:
    # 2. DATA LOADING & MERGING
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    # 3. DATA PREPROCESSING
    df['Timestamp'] = pd.to_datetime(df['TxnDate'] + ' ' + df['TxnTime'])
    df = df.sort_values('Timestamp').drop_duplicates('Timestamp')
    df.set_index('Timestamp', inplace=True)

    # Resampling to Hourly (Summing kWh)
    df_hourly = df['Consumption'].resample('H').sum().to_frame()
    df_hourly['Consumption'] = df_hourly['Consumption'].fillna(0)

    # 4. FEATURE ENGINEERING
    df_hourly['Hour'] = df_hourly.index.hour
    df_hourly['DayOfWeek'] = df_hourly.index.dayofweek
    df_hourly['Is_Weekend'] = df_hourly['DayOfWeek'].isin([5, 6])
    df_hourly['Date'] = df_hourly.index.date
    df_hourly['Rolling_24h'] = df_hourly['Consumption'].rolling(window=24).mean()
    df_hourly['Period'] = df_hourly['Hour'].apply(lambda x: 'Peak' if 9 <= x <= 18 else 'Off-Peak')

    # 5. ANOMALY DETECTION
    threshold = df_hourly['Consumption'].mean() + 3 * df_hourly['Consumption'].std()
    df_hourly['Is_Anomaly'] = df_hourly['Consumption'] > threshold

    # 6. VISUALIZATIONS
    # Time Series
    plt.figure(figsize=(15, 6))
    plt.plot(df_hourly.index, df_hourly['Consumption'], label='Hourly Consumption', alpha=0.5)
    plt.plot(df_hourly.index, df_hourly['Rolling_24h'], label='24h Trend', color='red')
    plt.title('Blower 78 Energy Consumption')
    plt.legend()
    plt.show() # In Colab, plt.show() displays it right in the notebook

    # Heatmap
    plt.figure(figsize=(10, 6))
    heatmap_data = df_hourly.pivot_table(index='Hour', columns='DayOfWeek', values='Consumption', aggfunc='mean')
    sns.heatmap(heatmap_data, cmap='YlOrRd')
    plt.title('Usage Intensity Heatmap')
    plt.show()

    # 7. SUMMARY REPORT
    print("\n--- PROJECT RESULTS ---")
    print(f"Avg Consumption: {df_hourly['Consumption'].mean():.2f} kWh")
    print(f"Anomalies Found: {df_hourly['Is_Anomaly'].sum()}")
    
    # Export results back to a CSV in Colab
    df_hourly.to_csv('processed_results.csv')
    print("\nResults saved to 'processed_results.csv' in the sidebar.")