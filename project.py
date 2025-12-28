import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. RECORDING DAILY ATTENDANCE (FOR A MONTH) ---
students = ['Ansh', 'Bobby', 'Chandra', 'Prem', 'Aman']

# Create 20 business days (approx. 1 month of school/work)
month_dates = pd.date_range(start="2024-01-01", periods=20, freq='B')

# Generate random attendance: 1 for Present, 0 for Absent
# (85% chance of being present)
np.random.seed(42) # Keeps data consistent
data = np.random.choice([0, 1], size=(20, 5), p=[0.15, 0.85])

# Create the Monthly DataFrame
df = pd.DataFrame(data, index=month_dates, columns=students)

# --- 2. CALCULATING PRESENCE/ABSENCE RATES ---
# Calculate percentage for each student
presence_rate = (df.sum() / len(month_dates)) * 100
absence_rate = 100 - presence_rate

# --- 3. VISUALIZING STUDENT & MONTHLY TRENDS ---
plt.figure(figsize=(12, 6))

# Plot 1: Monthly Attendance per Student (Performance)
plt.subplot(1, 2, 1)
plt.bar(students, presence_rate, color='skyblue', edgecolor='black')
plt.axhline(75, color='red', linestyle='--', label='75% Goal') # Threshold line
plt.title('Monthly Attendance Percentage')
plt.ylabel('Rate (%)')
plt.ylim(0, 100)
plt.legend()

# Plot 2: Daily Trend (Showing how attendance changed over the month)
plt.subplot(1, 2, 2)
daily_total = df.sum(axis=1) # Count how many came each day
plt.plot(month_dates.strftime('%d-%b'), daily_total, marker='o', color='green')
plt.title('Monthly Attendance Trend (Daily)')
plt.ylabel('Students Present')
plt.xticks(rotation=45) # Tilt dates so they fit

plt.tight_layout()
plt.show()


print("--- Monthly Analytics Report ---")
print(f"Average Class Attendance: {presence_rate.mean()}%")
print("\nIndividual Percentages:")
print(presence_rate)