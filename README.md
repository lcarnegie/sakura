# Warming Degrees and Flowering Trees 
Understanding Temperature's Role in Earlier Cherry Blossom Blooming Times in Kyoto, Japan

## Overview
This project examines the relationship between temperature and cherry blossom (sakura) flowering dates in Kyoto, Japan, analyzing a comprehensive dataset spanning nearly 1200 years from 812 CE to the present day. By modeling flowering day as a function of mean March temperatures, we identify significant trends that have implications for both the traditional practice of hanami (flower-viewing) and local ecosystems. Our analysis reveals a significant inverse relationship between March temperatures and sakura bloom dates, with warmer temperatures consistently associated with earlier flowering times. Our findings demonstrate the need for cultural adaptation to shifting bloom schedules due to climate change and highlight the consideration of extensive historical climate data in the process of developing accurate predictive models.

For this work, our group won 'Best Data Visualization' out of 5 other teams in our class, awarded by our Professor, Dr. Tao Wang.

## File Structure and Workflow
The repository is structured as follows:

- `analysis_data` contains the processed datasets used for analysis
- `raw_data` contains historical sakura blooming records and modern meteorological datasets
cookson/ contains data compiled by Alex Cookson, including:
    - `cookson_cleaned_csvs/` with cleaned CSV files
    - `very_raw_data/` with original source files and cleaning scripts
- `paper` contains the main Quarto document (with final code), reference bibliography, and final PDF
- `scripts` contains rough Python notebooks for data exploration, visualization, and modeling

Our workflow involved merging historical records with modern meteorological data, exploring relationships through visualization, and developing predictive models to quantify the relationship between temperature and bloom timing.

## Reproducing Graphs and Tables
Here is a brief guide to reproducing our analysis:

Clone this repository to your computer

Install Python 3.10+ and the libraries indicated in the data-setup chunk at the top of paper.qmd (pandas, numpy, matplotlib, seaborn, statsmodels)

In scripts, run each of the notebooks in numerical order to:

1. `01-process-data.ipynb`: Clean and merge datasets
2. `02-produce-csv.ipynb`: Generate analysis datasets
3. `03-explore-data.ipynb`: Create exploratory visualizations
4. `04-model-data.ipynb`: Fit regression models and evaluate performance
