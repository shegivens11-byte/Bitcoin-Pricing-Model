"""This file creates two combined databases (CSV files) for unique addresses and number of BTC in circulation, both over time. 
The first CSV (BTC_Data.csv) entry's  hold every date from both btc_circulating.csv and num_unique_addresses.csv.
The Second CSV (BTC_Data_Agg.csv) entry's hold only data where the data appeared in both btc.circulating.csv and num_unique_addresses.csv
The output is two CSVs (BTC_Data.csv & BTC_Data_Agg.csv)"""

import pandas as pd

#CSV file names
WALLETS_CSV = "num_unique_addresses.csv"
SUPPLY_CSV = "btc_circulating.csv"
OUTPUT_CSV1 = "BTC_Data.csv"
OUTPUT_CSV2 = "BTC_Data_Agg.csv"

#Read in CSVs for num unique addresses and num btc in curculation
nwallets = pd.read_csv(WALLETS_CSV, parse_dates=["date"])
nbtc = pd.read_csv(SUPPLY_CSV, parse_dates=["date"])
    #The two CSV files have report differing times. Match on date only
nwallets["date"] = nwallets["date"].dt.normalize()
nbtc["date"] = nbtc["date"].dt.normalize()
    #If a date appears multiple times, keep last value for the day
nwallets = nwallets.groupby("date", as_index=False).last()
nbtc = nbtc.groupby("date", as_index=False).last()

#Merge CSV files to combined_data and combined_data_agg
    #combined_data uses every date from both CSVs.
    #combined_data_agg uses dates that are only in BOTH CSVs.
combined_data_agg = pd.merge(nwallets, nbtc, on="date", how="inner")
combined_data_agg = combined_data_agg.sort_values("date").reset_index(drop=True)
combined_data = pd.merge(nwallets, nbtc, on="date", how="outer")
combined_data = combined_data.sort_values("date").reset_index(drop=True)

#Sanity Check for combined data and aggregated data - checks: 
# num unique addresses rows, 
# btc circulating rows, 
# combined data rows, 
# aggregated combined data rows,
# range of dates for combined data,
# range of dates for aggregated combined data,
# num of missing values for combined data,
# num of missing values for aggregated combined data,
# head of combined data, 
# tail of combined data,
# head of aggregated combined data,
# tail of agrregated combined data.
print(f"Wallets rows {len(nwallets)}")
print(f"Supply rows {len(nbtc)}")
print(f"Combined rows {len(combined_data)}")
print(f"Aggregated combined rows {len(combined_data_agg)}")
print(f"Date range for combined rows {combined_data['date'].min().date()} to {combined_data['date'].max().date()}")
print(f"Date range for aggregated combined rows {combined_data_agg['date'].min().date} to {combined_data_agg['date'].max().date()}")
print(f"Missing values in combined data\n{combined_data.isna().sum()}")
print(f"Missing values in aggregated combined data\n{combined_data_agg.isna().sum()}")
print(combined_data.head())
print(combined_data.tail())
print(combined_data_agg.head())
print(combined_data_agg.tail())


#Push to CSV
combined_data.to_csv(OUTPUT_CSV1, index=False)
combined_data_agg.to_csv(OUTPUT_CSV2, index=False)
