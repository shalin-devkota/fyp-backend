import pandas as pd
import json
import os

json_file_path = "/home/genvenom/fyp-backend/sectors.json"
with open(json_file_path, "r") as json_file:
    sectors = json.load(json_file)

csv_file_path = os.path.join("/home/genvenom/fyp-backend/ml/data/stocks.csv")
stock_df = pd.read_csv(csv_file_path)


def get_sector(stock_symbol):
    for sector, symbols in sectors.items():
        if stock_symbol in symbols:
            return sector
    return "N/A" 

stock_df["Sector"] = stock_df["Symbol"].apply(
    get_sector
)  

updated_csv_file_path = os.path.join("..", "..", "data", "updated_stock.csv")
stock_df.to_csv(updated_csv_file_path, index=False)

print(f"Updated CSV saved to {updated_csv_file_path}")
