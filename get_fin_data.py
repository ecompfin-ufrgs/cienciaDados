#Gustavo Pery
# function to download financial information about a given asset

import yfinance as yf
import pandas as pd

def get_stock() -> pd.DataFrame:
    
    """
    This function will generate financial information (such as prices - Open, High, Low, Close and Adj Close - and transactions volume) about a given asset
    in a pandas df.
    Args:
        
    """
    ticker = str(input('\nB3 stock code'))
    initial_date = str(input('\nInicial date format as YYYY-MM-DD'))
    final_date = str(input('\nFinal date format as YYYY-MM-DD'))
    interval = str(input('\nChoose an interval: 1h, 1d, 5d, 1wk, 1mo, 3mo'))

    prices = pd.DataFrame(yf.download(ticker+'.SA', initial_date, final_date, interval=interval))
    prices['Ticker'] = ticker

    return prices
    
#def clean_data(data: pandas.DataFrame) -> pandas.DataFrame:
#    pass
#
#               Isso aqui eu não entendi muito bem, é pre limpar a memória?


def get_data_price() -> pd.core.series.Series:
        
    """
    This function will generate an adjusted closing prices in a pandas series of a given asset.
    Args:
        
    """
    ticker = str(input('\nB3 stock code'))
    initial_date = str(input('\nInicial date format as YYYY-MM-DD'))
    final_date = str(input('\nFinal date format as YYYY-MM-DD'))
    interval = str(input('\nChoose an interval: 1h, 1d, 5d, 1wk, 1mo, 3mo'))

    prices = pd.Series(yf.download(ticker+'.SA', initial_date, final_date, interval=interval)['Adj Close'])
    

    return prices
