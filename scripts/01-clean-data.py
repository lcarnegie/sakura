import pandas as pd

# Load temperature data
temperature_path = "temperatures-modern.xlsx"
xls = pd.ExcelFile(temperature_path)
df_temp = xls.parse('temperatures-modern')

# Filter for January
january_df = df_temp[df_temp['month'] == 'Jan']
january_table_extended = january_df[['station_name', 'year', 'month', 'month_date', 'mean_temp_c']]

# Display the cleaned January dataset
print("January Temperatures Sample:")
print(january_table_extended.head())

# Load sakura data
sakura_path = "sakura-modern.csv"
sakura_df = pd.read_csv(sakura_path)

# Display the sakura data
print("\\nSakura Data Sample:")
print(sakura_df.head())

# Merge on station_name and year
merged_df = pd.merge(sakura_df, january_table_extended, on=['station_name', 'year'], how='inner')

# Display the merged dataset
print("\\nMerged Data Sample:")
print(merged_df.head())