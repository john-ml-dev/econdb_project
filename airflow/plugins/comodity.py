import requests 
import pandas as pd
import json

def run_fetch_comodity():
    comodities = ["CRUDEOIL","GASOLINE","NATGAS","TOTCRUDE","TOTPRODS","GASDIES"]
    for comodity in comodities:
        fetch_comodity(comodity=comodity) 
 
def fetch_comodity(comodity:str ="GASOLINE" ):
    """Fetches comodity data from econdb.com
    :param comodity:str: a comodity index
        options for comodity:
            gasoline        -> "GASOLINE"
            natural gas     -> "NATGAS"
            total crude     -> "TOTCRUDE"
            total oil       -> "TOTPRODS"
            Gas/diesel oil  -> "GASDIES"
    """
    # extracting country details from csv located in input directory
    countries = pd.read_csv("/opt/airflow/input/countries.csv", names=["country","code"], index_col='code')
    # extracting country codes and converting them to a list 
    country_codes = list(countries.index)
    
    # creating empty dictionary to hold the results
    results = dict()
    try:
    # iterating over all country codes and requesting their data
        for code in country_codes:
            print(f"fetching {comodity}.... -> {code}")
            link = f"https://www.econdb.com/widgets/energy-storage/data/?commodity={comodity}&country={code}"
   
            # fetching data
            data = requests.get(link)
            
            # check if response from server was successful( i.e status code = 200)
            if data.status_code == 200:
                # getting json component of fetched data
                data = data.json()
                # getting the data part of the json
                data = data['plots'][0]['data']

                # check if data is not empty
                if len(data) !=0:
                    
                    # extracting range component of data and creating min and max components
                    for item in data:
                        # first value of range
                        item['min']= item['range'][0]
                        # second value of range
                        item['max']= item['range'][1]
                        # delete range from data item
                        del item['range']
                    
                    # append data for the given country code to results
                    results[code] = {
                        "code":code,
                        "data":data
                        }
                    # print(results)
        
    # incase user exists out of program (already downloaded data gets written to file)
    except KeyboardInterrupt:
            with open(f'airflow/output/{comodity}.json', mode='w') as f:
                json.dump(results, f, indent=2)  

    except Exception as e:
        print(e)
    # writing results to file    
    with open(f'airflow/output/{comodity}.json', mode='w') as f:
        json.dump(results, f, indent=2)

