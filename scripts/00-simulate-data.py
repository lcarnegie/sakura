# ============= PREAMBLE =============
# Last Edited By: Luca Carnegie
# Date: March 28, 2025
# Description: 
#       - Simulation script that generates synthetic cherry blossom 
#         flowering data for Kyoto from 800 to 2024 CE, including dates 
#         and temperatures. 
#       - Creates visualizations showing historical flowering patterns 
#         and climate relationships.
# ====================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Create a function to generate simulated data
def generate_kyoto_data(start_year=800, end_year=2024):
    # Lists to store our data
    years = []
    dates = []
    day_of_years = []
    march_temps = []
    
    # Generate data for each year
    for year in range(start_year, end_year + 1):
        # Skip some years to simulate missing data
        if random.random() < 0.1:  # 10% chance to skip a year
            continue
            
        # Generate date of flowering
        # Earlier dates in recent years to simulate climate change effect
        base_day = 111  # Day of year from example (April 20)
        
        # Add some climate change effect - earlier blooming in recent years
        climate_effect = int((year - start_year) / 100)  # Roughly 1 day earlier per century
        
        # Add some random variation
        random_variation = np.random.normal(0, 7)  # Standard deviation of 7 days
        
        day_of_year = max(60, base_day - climate_effect - random_variation)  # Ensure not before March 1
        
        # Convert day of year to date
        date = datetime(year, 1, 1) + timedelta(days=int(day_of_year) - 1)
        date_str = f"{year}-{date.month:02d}-{date.day:02d}"
        
        # Generate March temperature
        # Baseline temperature with some warming trend and random variation
        base_temp = 12.0  # Base temperature for ancient records
        warming_trend = 0.01 * (year - start_year)  # About 1°C per 100 years
        random_temp_variation = np.random.normal(0, 1.5)  # Random variation
        
        march_temp = base_temp + warming_trend + random_temp_variation
        
        # Store the data
        years.append(year)
        dates.append(date_str)
        day_of_years.append(int(day_of_year))
        march_temps.append(round(march_temp, 1))
    
    # Create DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Date_of_Flowering': dates,
        'Day_of_Year': day_of_years,
        'March_Temp_C': march_temps
    })
    
    return df

# Generate the data
df = generate_kyoto_data(800, 2024)

# Display the first few rows
print("First 5 rows of the dataset:")
print(df.head())

# Sample Visualization 1: Time series of flowering dates over the centuries
plt.figure(figsize=(12, 6))
plt.scatter(df['Year'], df['Day_of_Year'], alpha=0.5, color='pink')
plt.plot(df['Year'], df['Day_of_Year'].rolling(30).mean(), color='red', linewidth=2)
plt.title('Cherry Blossom Flowering Dates in Kyoto (800-2024)', fontsize=15)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Day of Year', fontsize=12)
plt.grid(True, alpha=0.3)
plt.gca().invert_yaxis()  # Invert y-axis so earlier dates are higher
plt.savefig('flowering_dates_timeline.png', dpi=300, bbox_inches='tight')
plt.show()

# Sample Visualization 2: Relationship between March temperature and flowering date
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='March_Temp_C', y='Day_of_Year', alpha=0.5, hue='Year', palette='viridis')
plt.title('Relationship Between March Temperature and Cherry Blossom Flowering Date', fontsize=15)
plt.xlabel('March Temperature (°C)', fontsize=12)
plt.ylabel('Day of Year', fontsize=12)
plt.grid(True, alpha=0.3)
plt.gca().invert_yaxis()  # Invert y-axis so earlier dates are higher
plt.savefig('temp_vs_flowering.png', dpi=300, bbox_inches='tight')
plt.show()

# Sample Visualization 3: Distribution of flowering dates by century
df['Century'] = (df['Year'] // 100) + 1  # Calculate century
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='Century', y='Day_of_Year')
plt.title('Distribution of Cherry Blossom Flowering Dates by Century', fontsize=15)
plt.xlabel('Century', fontsize=12)
plt.ylabel('Day of Year', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.gca().invert_yaxis()  # Invert y-axis so earlier dates are higher
plt.savefig('flowering_by_century.png', dpi=300, bbox_inches='tight')
plt.show()

# Summary statistics
print("\nSummary statistics:")
print(df.describe())