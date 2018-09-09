'''
    Extracts data from the HTML table on coinmarketcap.com
    given the id of the cryptocurrency and begin date for parsing:
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from argparse import ArgumentParser, ArgumentTypeError
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
import pandas_datareader.data as web
from math import log

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True

    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False     
    else:
        raise ArgumentTypeError('Boolean value expected.')

'''
    Gets arguments from the terminal.
'''
def get_args():
    parser = ArgumentParser()
    parser.add_argument("-save", type=str2bool, help=("Save data sheet " 
                        "('True' or 'False')"), required=True)
    parser.add_argument("-start", help=("Enter the first day you want to begin"
                        "collecting price data. For instance 20131227"), 
                        type=int, required=True)
    parser.add_argument("-crypto_id", help=("Choose a coin. Acceptable entries"
                        " are 'bitcoin', 'ethereum', 'tron', 'iota','eos' and"
                        " 'ripple'"), type=str, required=True)
    parser.add_argument("-optimizer", help=("Choose an optimization method. "
                        "Acceptable entries are: 'adam' and 'lbfgs'."), 
                        type=str)
    parser.add_argument("-network", help=("Choose an RNN method. Acceptable "
                        "entries are: 'lstm' and 'gru'."), type=str)
    args = parser.parse_args()
    
    return args

def pass_legal_args():
    args = get_args()
    cryptos = ['bitcoin', 'tron', 'iota', 'eos', 'ripple']
    optims = ["adam", "lbfgs"] # Acceptable optimization methods
    rnns = ["lstm", "gru"] # Acceptable recurrent net methods
    assert args.crypto_id.lower() in cryptos, ("\nAcceptable entries for "
                                               "cryptos are 'bitcoin', 'tron',"
                                               " 'iota', 'eos', 'ripple'. You "
                                               "entered: " + args.crypto_id)
    assert args.optimizer.lower() in optims, ("\nAcceptable entries for "    
                                              "optimizer are: 'adam' and "
                                              "'lbfgs'. You entered: " +
                                              args.optimizer)
    assert args.network.lower() in rnns, ("\nAcceptable entries for network: "
                                          "are 'lstm' and 'gru'. You "
                                          "entered: " + args.network) 
    
    return args

def get_url(now, start_date, coin_id):
    month, day = now.month, now.day
    if now.month < 10:
        month = str(0) + str(month)
    else:
        pass

    if now.day < 10:
        day = str(0) + str(day)
    else:
        pass

    end_date = str(now.year) + month + day
    url = 'https://coinmarketcap.com/currencies/' + coin_id + \
          '/historical-data/' + '?start=' + str(start_date) +'&end=' + \
          end_date
    
    return(url)

def get_df(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"lxml")
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 
                  'Market Cap']
    print(tabulate(df, headers='keys', tablefmt='psql'))
    
    return(df)

def log_transform(num, base=10):
    return log(num, base)

'''
    Takes the log scale of the columns: Open, High, Low, Close in the dataframe
    with default base: 10. (Applies the log transform function to many columns)
'''
def scale_to_log(df):
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 
                                               'Low', 'Close']].applymap(
                                                                log_transform)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    return df
    
def main():
    args = pass_legal_args()
    now = datetime.now()
    start_date = args.start
    coin_id = args.crypto_id.lower()
    url = get_url(now, start_date, coin_id)
    df = get_df(url)
    # timestamps and stores the csv file
    if args.save == True:
        location = 'allTime_' + coin_id + str(now.year) + str(now.month) \
                   + str(now.day) + '.csv'
        df.to_csv(location)
    else:
        pass
        
    # plots with plotly:
    df = df.iloc[::-1] # reverses the time order of the dataframe
    data = [go.Scatter(x=df.Date, y=df.Close)]
    py.iplot(data)

if __name__ == "__main__":
    main()
