#import pandas as pd
#import numpy as np
import datetime
import view
import get_fin_data
import stock_module
import options_module
import derivative_module

def pipe():
    ticker = view.select_stock()
    today = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(years = 5)

    data = get_fin_data.get_stock(ticker, start_date, today)
    data = get_fin_data.clean_data()
    data_price_series = get_fin_data.get_data_price()

'''
    if ticker == stock:
        get_stock_return = stock_module.calculate_stock_return(data_price_series)
        get_stock_cumreturn = stock_module.calculate_cumulative_stock_return(data_price_series)

    elif ticker == option:
        get_options_return = options_module.calculate_options_return(data_price_series)
        get_options_cumreturn = options_module.calculate_cumulative_options_return(data_price_series)

    elif ticker == derivative:
        get_derivative_return = derivative_module.calculate_derivative_return(data_price_series)
        get_derivative_cumreturn = derivative_module.calculate_cumulative_derivative_return(data_price_series)
'''

    view.post_info(data)
    view.post_info(price_return)
    view.post_info(price_cumulative_return)


if __name__ == '__main__':
    pipe()
