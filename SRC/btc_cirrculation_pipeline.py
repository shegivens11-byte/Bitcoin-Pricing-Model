"""This file is the data pipeline for the current amount of BTC in circulation over time.
It outputs a CSV with two columns: date, btc_in_circulation"""
import requests
import pandas as pd

#API for the number of bitcoin in circulation (current amount mined).
#Source: https://www.blockchain.com/explorer/charts/total-bitcoins
url_numbtc = "https://api.blockchain.info/charts/total-bitcoins?timespan=all&format=json"

#Check response
response = requests.get(url_numbtc, timeout=30)
print(response.status_code)
#The following gives output if csv does not complie.
#Uncomment it and run if problems occur.
print(response.headers.get("content-type"))
print(response.url)
print(repr(response.text[:500]))

#Parse json
nbtc_data = response.json()
values = nbtc_data["values"]

#Build dataframe
nbtc_df = pd.DataFrame(values)
nbtc_df["date"] = pd.to_datetime(nbtc_df["x"], unit="s")
nbtc_df = nbtc_df.rename(columns={"y": "btc_in_circulation"})[["date", "btc_in_circulation"]]

"""NOTE: Blockchain.com calculates this figure via theoretical block reward set by BTC protocol, not via counting actual num of coins.
Hence, the num inculdes coins that are lost and/or unspendable."""

#Sanity Check
print(nbtc_df.head())
print(nbtc_df.tail())
print(len(nbtc_df), "rows")

#Push to CSV
nbtc_df.to_csv("btc_circulating.csv", index=False)
