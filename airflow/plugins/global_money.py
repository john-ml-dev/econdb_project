"""Fetches Global Money Supply"""
import requests
import pandas as pd


def fetch_global_money(file_path: str = "global_money_supply.csv"):
    """fetches global money supply from https://www.econdb.com/world-indicators
    Args:
        file_path:
            name or file directory to save data to
    """
    # request global money supply
    re = requests.get("https://www.econdb.com/widgets/global-money-supply/data")

    # extract the json content
    gms = re.json()

    # extract the global money supply data
    gms = gms["plots"][0]["data"]

    # create a pandas dataframe from data
    df = pd.DataFrame(gms)

    # reshape dataframe for easy plotting in PowerBI
    # pd.melt converts all currency heading to a column called Codes and their corresponding values in
    # into a column called GMS whiles preserving the Date column 
    df = pd.melt(df, id_vars=["Date"], var_name="Code", value_name="GMS")

    # write data to csv file
    df.to_csv(file_path, index=False)
