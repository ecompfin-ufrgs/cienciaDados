# Joao and Matheus: 2023-02-17
# function to calculate the return of a call or put

import pandas as pd
import numpy as np
import warnings 

def get_options_return(price_series: pd.core.series.Series) -> pd.core.series.Series:
    
    """
    This function calculate the return (percentage variation) of a prices series of stock options

    Args:
        price_series: a pandas Series dtype float64
    """
    
    try:
        return_series = np.log(price_series).diff().fillna(0)
    except (TypeError, AttributeError, ValueError):
        return_series = -1
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
    
    return return_series


def get_options_cumreturn(price_series: pd.core.series.Series) -> pd.core.series.Series:
    
    """
    This function calculate the cumulative return (percentage variation) of a prices series of stock options

    Args:
        price_series: a pandas Series dtype float64
    """
    
    try:
        return_series = np.log(price_series).diff().fillna(0)
        cum_return = np.exp(np.cumsum(return_series)) - 1
    except (TypeError, AttributeError, ValueError):
        cum_return = -1
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
    
    return cum_return
