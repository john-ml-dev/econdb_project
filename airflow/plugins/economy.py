import pandas as pd 
import os  

def fetch_gdp_data():
    """
    Fetches  Economic data from econdb.com
    
        "RGDP": "Real gross domestic product"
        "GDP" : "Gross domestic product"
        "CPI" : "Consumer price index"
        "URATE": "Unemployment"
        "RETA" : "Retail trade"
        "IP"   : "Industrial production"
        "GBAL" : "Government balance"
        "GDEBT": "Government debt"
        "CA"   : "Current account balance"
        "NIIP" :"Net international investment position"
        "Y10YD" : "Long term yield"
        "HOU"  : "House price"
        "OILPROD" : "Oil production"
        "PPI" : "Producer price index"
        "CONF": "Consumer confidence index"
        "RPUC": "Real public consumption"
        "RGFCF": "Real Gross Fixed Capital Formation"
        "POP" : "Population"
    """
    # load countries data from input directory
    df = pd.read_csv("/opt/airflow/input/countries.csv", names=["country","code"])
    # extract codes as list
    codes= list(df["code"])
    # various indicators(indexes)
    indexes = ["GDEBT","PPI","CONF","RGDP",'IP',"RETA","RPUC","RGFCF","CPI"]

    # loop over each item in indexes
    for item in indexes:
        print(item)
        # create empty dataframe to hold results
        result = pd.DataFrame()
        # create empty list to hold country codes that produced data
        col_name =[]
        try:
            
            # loop over codes in country codes
            for code in codes:
                # set the ticker for example PPIUS -> Producer Price Index for US
                ticker = f'{item}{code}'
                try:
                    # download data for ticker
                    df = pd.read_csv(
                    f'https://www.econdb.com/api/series/{ticker}/?format=csv&token={os.getenv("API_TOKEN")}',
                    index_col='Date', parse_dates=['Date'])
                    # check the number of items in the downloaded data
                    if len(df) != 0:
                        # append the code to column names if data is not empty
                        col_name.append(code)
                        # print(df.head())
                        print(f"fetching {item}.... -> {code}")
                        # join dataframes along the horizontal axis
                        result = pd.concat([result, df], axis=1)
                        # set index column names to col_name
                        result.columns = col_name
                    else:
                        # if data is empty
                        print(f"no data for {code}")
                # If program gets interrupted by user the already downloaded data is saved   
                except KeyboardInterrupt:
                    result.to_csv(f"/opt/airflow/output/csv/{item}.csv")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        # write data to csv
        result.to_csv(f"/opt/airflow/output/csv/{item}.csv")    
        