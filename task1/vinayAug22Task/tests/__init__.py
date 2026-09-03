# Used Car Market Dashboard
## Project File Overview

### 1. data_cleaning.py

Purpose:
Clean the raw Kaggle used-car dataset and prepare it
for analysis and visualization.

Main steps:

1. Load raw data
2. Select useful columns
3. Clean column names
4. Remove duplicate records
5. Clean categorical values
6. Convert numeric columns
7. Remove invalid values
8. Handle missing values
9. Create derived columns
10. Validate the dataset
11. Generate quality report
12. Save processed dataset


### 2. analysis_visualization.py

Purpose:
Analyze the cleaned dataset and create reusable
Matplotlib visualizations.

Analysis:
- Dataset size
- Price statistics
- Brand distribution
- Fuel distribution
- Transmission distribution
- Body type distribution
- City distribution

Customer visualizations:
- Price distribution
- Price vs vehicle age
- Price vs mileage
- Average price by fuel
- Average price by transmission

Seller / Dealer visualizations:
- Listings by brand
- Average price by brand
- Listings by price segment
- Fuel distribution

Market visualizations:
- Listings by city
- Average price by city
- Price vs mileage by fuel


### 3. dashboard/app.py

Purpose:
Create the interactive Streamlit dashboard.

Responsibilities:
- Load processed data
- Provide stakeholder selection
- Provide filters
- Filter the dataset
- Display KPIs
- Call visualization functions
- Display Matplotlib graphs

Stakeholder perspectives:

Customer:
Understand prices and vehicle characteristics.

Seller / Dealer:
Understand inventory, brands and price segments.

Market Analyst:
Understand geographic and market-level patterns.


### Overall Flow

Raw Kaggle Data
        ↓
data_cleaning.py
        ↓
Clean Processed Data
        ↓
analysis_visualization.py
        ↓
Analysis + Matplotlib Graphs
        ↓
dashboard/app.py
        ↓
Interactive Streamlit Dashboard
