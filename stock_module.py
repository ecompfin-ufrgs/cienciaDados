#import pandas as pd
#import numpy as np

def calculate_stock_return(price_series: pd.Series) -> pd.core.series.Series:
    '''
    This function calculates the log-return of a pandas.Series with "numpy.log()" 
    and return a pandas.Series.

    Arguments:
        price_series: a pandas.Series dtype float64
    '''
    return_series = np.log(price_series).diff().fillna(0)
  
    return return_series

def get_stock_cumreturn(price_series: pd.core.series.Series) -> pd.core.series.Series:
    '''
    This function calculates the cumulative sum of the log-return of a pandas.Series with "numpy.log()" 
    and return a pandas.Series. 

    Arguments:
        price_series: a pandas.Series dtype float64
    '''
    log_returns = np.log(price_series).diff().fillna(0)
    return_cumreturn = log_returns.cumsum()
    
    return return_cumreturn
