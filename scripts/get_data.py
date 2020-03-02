
##########################################################################################
##########################################################################################

# Set up the environment

import sys

# Add path for python to look into for modules installed using pip

sys.path.append('/usr/local/lib/python3.7/site-packages/')

# Setup AlphaVantage

from alpha_vantage.timeseries import TimeSeries # https://www.alphavantage.co/documentation/
from alpha_vantage.techindicators import TechIndicators # https://github.com/RomelTorres/alpha_vantage

api_key = '2HTD0A5HTZ0MZW19'

ts = TimeSeries(key=api_key, output_format='pandas')

ti = TechIndicators(key=api_key, output_format='pandas')

# Import other libraries

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import time
from main_functions import *

##########################################################################################
##########################################################################################

# Define start/end dates

start_date = '2015-01-01'

end_date = datetime.datetime.today().date()

##########################################################################################
##########################################################################################

###############
##### FRED DATA
###############

fred = {
    'DGS2' : 'two_yr_us_bond',
    'DGS10' : 'ten_yr_us_bond',
    'DGS30' : 'thirty_yr_us_bond',
    'VIXCLS' : 'vix',
    'OVXCLS' : 'oil_etf_vol',
    'GVZCLS' : 'gold_etf_vol',
    'VXFXICLS' : 'china_etf_vol',
    'VXEEMCLS' : 'emer_markets_etf_vol',
    'RVXCLS' : 'russel_2k_etf_vol',
    'VXXLECLS' : 'energy_etf_vol',
    'SP500' : 'SP500',
    'DJIA' : 'DJIA',
    'NASDAQCOM' : 'NASDAQ',
    'DCOILWTICO' : 'crude_oil_texas',
    'GOLDAMGBD228NLBM' : 'gold_morning',
    'GOLDPMGBD228NLBM' : 'gold_afternoon',
    'DCOILBRENTEU' : 'crude_oil_brent',
    'DHHNGSP' : 'hh_natural_gas',
    'BAMLHYH0A0HYM2TRIV' : 'high_yield_master_II_tri',
    'BAMLCC0A0CMTRIV' : 'corporate_master_tri',
    'WLEMUINDXD' : 'economic_uncertainty_index'
}

all_fred = []

for f in fred.keys():
    print('Pulling data for', f)
    fred_tmp = web.DataReader(f, 'fred', start_date, end_date)
    fred_tmp.columns = [fred[f]]
    all_fred.append(fred_tmp)

del fred_tmp

fred_data = pd.concat(all_fred, axis=1)

fred_data.sort_index(ascending=False, inplace=True)

###########
##### FOREX
###########

forex = [
    'DEXUSEU', # euro
    'DEXCHUS', # chinese yuan
    'DEXJPUS', # japanese yen
    'DEXCAUS', # canadian dollar
    'DEXUSUK', # british pounds
    'DEXKOUS', # south korean won
    'DEXMXUS', # mexican peso
    'DEXBZUS', # brazilian real
    'DEXINUS', # indian rupee
    'DEXUSAL', # australian dollar
    'DEXSZUS', # swiss franc
#     'DEXTHUS', # thai baht
#     'DEXTAUS', # new taiwan dollar
    'DEXSFUS', # south african rand
    'DEXHKUS', # hong kong dollar
    'DEXMAUS', # malaysian ringgit
#     'DEXSDUS', # swidish krona
    'DEXSIUS' # singapore dollar
#     'DEXNOUS', # norwegian krone
#     'DEXDNUS', # danish krone
#     'DEXSLUS', # sri lankan rupee
#     'DEXUSNZ', # new zeland dollar
]

all_forex = []

for f in forex:
    print('Pulling data for', f)
    forex_tmp = web.DataReader(f, 'fred', start_date, end_date)
    forex_tmp.columns = [f[3:]]
    all_forex.append(forex_tmp)

del forex_tmp

forex_data = pd.concat(all_forex, axis=1)

forex_data.sort_index(ascending=False, inplace=True)

###############
##### JOIN DATA
###############

fred_forex = fred_data.join(forex_data)

###################
##### ALPHA VANTAGE
###################

# Get stock data

stocks = ['AMZN', 'MSFT', 'AAPL', 'GOOGL', 'WMT', 'GS', 'JPM']

all_stocks = []

for s in stocks:
    print('Pulling data for', s)
    stock_tmp = alpha_wrangle(stock=s, start=start_date, end=end_date)
    time.sleep(5)
    # Get data for vairous indicators
    bb = get_bb(stock=s, start=start_date, end=end_date)
    time.sleep(5)
    rsi = get_rsi(stock=s, start=start_date, end=end_date)
    time.sleep(5)
    adx = get_adx(stock=s, start=start_date, end=end_date)
    time.sleep(5)
    macd = get_macd(stock=s, start=start_date, end=end_date)
    # Join everything together
    stock_tmp = stock_tmp.join(bb).join(rsi).join(adx).join(macd)
    # Add to list
    all_stocks.append(stock_tmp)
    # Pause to prevent AlphaVantage API overload
    time.sleep(10)

del stock_tmp, bb, rsi, adx, macd

stock_data = pd.concat(all_stocks, axis=1)

#######################
##### JOIN ALL DATASETS
#######################

# Drop some columns from stock_data

# cols_to_drop = ['open', 'high', 'low', 'close', 'date', 'vix_open', 'vix_high', 'vix_low']

# stock_data.drop(labels = cols_to_drop, axis = 1)

# Add alt_data to the stock_data

data = stock_data.join(fred_forex).dropna(axis=0)

###################
##### SAVE THE DATA
###################

data.to_csv('../data/all_data.csv', sep=',', header=True, index=True)

#####
