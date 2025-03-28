# ============= PREAMBLE =============
# Last Edited By: Chris Lu
# Date: March 25, 2025
# Description: Script to clean and merge temperature and sakura blooming data
#             - Loads temperature data and filters for January
#             - Loads sakura (cherry blossom) data
#             - Merges datasets by station name and year
# ====================================

import pandas as pd
import numpy as np

## LOAD DATA ##

df_modern_temp = pd.read_csv("data/raw data/cookson_cleaned_csvs/temperatures-modern.csv") # Load modern temperature
df_modern_blooming = pd.read_csv("data/raw data/cookson_cleaned_csvs/sakura-modern.csv") # Load modern blooming data
df_historical_temp = pd.read_csv("data/raw data/cookson_cleaned_csvs/sakura-historical.csv") # Load historical temperature data

print("Modern Temp data\n" + str(df_modern_temp.head())) # Print first 5 rows of modern temperature data
print()
print("Modern bloom data\n" + str(df_modern_blooming.head())) # Print first 5 rows of modern blooming data
print()
print("Historical temp/bloom data\n" + str(df_historical_temp.head())) # Print first 5 rows of historical temperature data

## HISTORICAL DATA ##

# drop unnecessary columns
df_historical_temp = df_historical_temp.drop(columns=["study_source", "flower_source_name", "flower_source"])

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

# reorder columns
df_historical_temp = df_historical_temp[["year", "flower_date", "flower_doy", "temp_march", "temp_c_obs", "temp_c_recon"]]

# cut off to 1952 and earlier (the rest we have modern data for)
df_historical_temp = df_historical_temp[df_historical_temp["year"] <= 1952]


