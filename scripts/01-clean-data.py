# ============= PREAMBLE =============
# Last Edited By: Luca Carnegie
# Date: March 28, 2025
# Description: 
#             - Script to clean and merge temperature and sakura blooming data
#             - Loads temperature data and filters for January
#             - Loads sakura (cherry blossom) data
#             - Merges datasets by station name and year
# ====================================

import pandas as pd
import numpy as np

## LOAD DATA ##

df_modern_temp = pd.read_csv("data/raw_data/cookson_cleaned_csvs/temperatures-modern.csv") # Load modern temperature
df_modern_blooming = pd.read_csv("data/raw_data/cookson_cleaned_csvs/sakura-modern.csv") # Load modern blooming data
df_historical_temp = pd.read_csv("data/raw_data/cookson_cleaned_csvs/sakura-historical.csv") # Load historical temperature data

print("Modern Temp data\n" + str(df_modern_temp.head())) # Print first 5 rows of modern temperature data
print()
print("Modern bloom data\n" + str(df_modern_blooming.head())) # Print first 5 rows of modern blooming data
print()
print("Historical temp/bloom data\n" + str(df_historical_temp.head())) # Print first 5 rows of historical temperature data

## TRANSFORM HISTORICAL DATA ##

# Merge reconstructed temp with observed temp into one col (prioritize observed)
# If observed temp is NaN, fill with reconstructed temp
df_historical_temp["temp_march"] = df_historical_temp["temp_c_obs"].combine_first(df_historical_temp["temp_c_recon"])

# convert day of year (where not NaN) to integer
df_historical_temp["flower_doy"] = df_historical_temp["flower_doy"].astype("Int64")

# convert temp_march, temp_c_obs and temp_c_recon (where not NaN) to floats, fill flower_date with <NA>
df_historical_temp["flower_date"] = df_historical_temp["flower_date"].fillna(pd.NA)
df_historical_temp["temp_march"] = df_historical_temp["temp_march"].astype("Float64")
df_historical_temp["temp_c_obs"] = df_historical_temp["temp_c_obs"].astype("Float64")
df_historical_temp["temp_c_recon"] = df_historical_temp["temp_c_recon"].astype("Float64")

# drop unnecessary columns
df_historical_temp = df_historical_temp.drop(columns=["study_source", "flower_source_name", "flower_source", "temp_c_obs", "temp_c_recon"])

# reorder columns
df_historical_temp = df_historical_temp[["year", "flower_date", "flower_doy", "temp_march"]]

# rename cols
df_historical_temp = df_historical_temp.rename(columns={"temp_march": "avg_temp_march_c"})

# cut off to 1952 and earlier (the rest we have modern data for)
df_historical_bloom = df_historical_temp[df_historical_temp["year"] <= 1952]

## TRANSFORM MODERN DATA ##

### Filter modern temp data to just Kyoto and March Temps (same as historical) 
df_modern_temp = df_modern_temp[df_modern_temp["station_name"] == "Kyoto"]
df_modern_temp = df_modern_temp[df_modern_temp["month"] == "Mar"]
df_modern_temp = df_modern_temp[df_modern_temp["year"] >= 1953] # cut off to 1953 and later (the rest we have historical data for)
df_modern_temp = df_modern_temp.drop(columns=["station_id", "station_name", "month", "month_date"])

### Filter modern flowering data to just Kyoto and March Temps 
df_modern_blooming = df_modern_blooming[df_modern_blooming["station_name"] == "Kyoto"]
df_modern_blooming = df_modern_blooming.drop(columns=["station_id", "station_name", "latitude", "longitude", "full_bloom_date", "full_bloom_doy"])

### Merge modern temp and flowering data
df_modern_bloom = df_modern_blooming.merge(df_modern_temp, how="inner", on=["year"])

### rename cols
df_modern_bloom = df_modern_bloom.rename(columns={"mean_temp_c": "avg_temp_march_c"})

## MERGE DATASETS ##

df_flower = pd.concat([df_historical_bloom, df_modern_bloom], ignore_index=True)

# change day of year to integer
df_flower["flower_doy"] = df_flower["flower_doy"].astype("Int64")
df_flower["flower_date"] = df_flower["flower_date"].fillna(pd.NA) # fill flower_date with <NA>

## SAVE DATA ##
# Save cleaned data to CSV files
df_flower.to_csv("data/analysis_data/clean_data.csv", index=False) # Save cleaned data to CSV file