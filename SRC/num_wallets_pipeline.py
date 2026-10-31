"""This file is the data pipeline for the number of unique wallets on the Blockchain over time.
It ouputs a CSV with two columns: date, unique_addresses."""
import requests
import pandas as pd

#API for the number of unique wallets on the Blockchain.
#Source: https://www.blockchain.com/explorer/charts/n-unique-addresses

url_nwallets = "https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json"

#Check response
response = requests.get(url_nwallets, timeout=30)
print(response.status_code)
#The following gives output if csv does not complie.
#Uncomment and run if problems occur.
"""print(response.headers.get("content-type"))
print(response.url)
print(repr(response.text[:500]))"""

#Parse JSON
nwallets_data = response.json()
values = nwallets_data["values"]


#Build dataframe
nwallets_df = pd.DataFrame(values)
nwallets_df["date"] = pd.to_datetime(nwallets_df["x"], unit="s")
nwallets_df = nwallets_df.rename(columns={"y": "num_unique_addresses"})
nwallets_df = nwallets_df[["date", "num_unique_addresses"]]

#Sanity Check
print(nwallets_df.head())
print(nwallets_df.tail())
print(len(nwallets_df), "rows")

#Push to CSV
nwallets_df.to_csv("num_unique_addresses.csv", index=False)