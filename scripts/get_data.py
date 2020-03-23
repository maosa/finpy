
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

# Change into the correct directory

import os

if os.getcwd() == os.path.expanduser('~') + '/finpy/scripts':
    pass
else:
    os.chdir(os.path.expanduser('~') + '/finpy/scripts')

print('Current working directory:', os.getcwd())

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

startTime = datetime.datetime.now()

###############
##### FRED DATA
###############

fred = {
    'DGS6MO' : 'six_month_us_bond', # 6-Month Treasury Constant Maturity Rate
    'DGS1MO' : 'ten_month_us_bond', # 1-Month Treasury Constant Maturity Rate
    'DGS1' : 'one_yr_us_bond', # 1-Year Treasury Constant Maturity Rate
    'DGS2' : 'two_yr_us_bond',
    'DGS5' : 'five_yr_us_bond', # 5-Year Treasury Constant Maturity Rate
    'DGS10' : 'ten_yr_us_bond',
    'DGS20' : 'twenty_yr_us_bond', # 20-Year Treasury Constant Maturity Rate
    'VXTYN' : 'ten_yr_tr_note_vol_fut', # CBOE 10-Year Treasury Note Volatility Futures
    'DGS30' : 'thirty_yr_us_bond',
    'T10Y3M' : 'ten_yr_minus_3_month_us_bond',

    'SP500' : 'SP500',
    'DJIA' : 'DJIA',
    'NASDAQCOM' : 'NASDAQ',
    'NIKKEI225' : 'nikkei_225', # Nikkei Stock Average, Nikkei 225
    'VXVCLS' : 'sp500_3_month_vol', # CBOE S&P 500 3-Month Volatility Index
    'VXDCLS' : 'djia_vol', # CBOE DJIA Volatility Index
    'VXNCLS' : 'nsdaq_vol', # CBOE NASDAQ 100 Volatility Index
    'RVXCLS': 'russel_2k_vol', # CBOE Russell 2000 Volatility Index

    'VIXCLS' : 'vix',
    'OVXCLS' : 'oil_etf_vol',
    'GVZCLS' : 'gold_etf_vol',
    'VXFXICLS' : 'china_etf_vol',
    'VXEEMCLS' : 'emer_markets_etf_vol', # CBOE Emerging Markets ETF Volatility Index
    'RVXCLS' : 'russel_2k_etf_vol',
    'VXXLECLS' : 'energy_etf_vol',

    'GOLDAMGBD228NLBM' : 'gold_morning',
    'GOLDPMGBD228NLBM' : 'gold_afternoon',

    'DCOILWTICO' : 'crude_oil_texas',
    'DCOILBRENTEU' : 'crude_oil_brent',
    'DHHNGSP' : 'hh_natural_gas',

    'BAMLHYH0A0HYM2TRIV' : 'high_yield_master_II_tri',
    'BAMLCC0A0CMTRIV' : 'corporate_master_tri',
    'WLEMUINDXD' : 'economic_uncertainty_index',
    'DPCREDIT' : 'primary_credit_risk', # Primary Credit Rate
    'WLEMUINDXD' : 'economic_uncertainty_index', # Equity Market-related Economic Uncertainty Index
    'WILL5000INDFC' : 'wilshire_5k', # Wilshire 5000 Total Market Full Cap Index
    'TEDRATE' : 'ted_spread', # TED Spread
    'DAAA' : 'aaa_corp_bond_yield', # Moody's Seasoned Aaa Corporate Bond Yield
    'DBAA' : 'baa_corp_bond_yield', # Moody's Seasoned Baa Corporate Bond Yield
    'BAA10Y' : 'baa_corp_bond_yield_rel',
    'BAMLH0A0HYM2' : 'high_yield_opt_adj_spread', # ICE BofA US High Yield Index Option-Adjusted Spread
    'USD3MTD156N' : '3_month_libor' # 3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar
}

all_fred = []

for f in fred.keys():
    print('Pulling FRED data for', f)
    fred_tmp = web.DataReader(f, 'fred', start_date, end_date)
    fred_tmp.dropna(axis=0, inplace=True)

    # Check dates and reverse if necessary
    first = fred_tmp.index[0]
    last = fred_tmp.index[fred_tmp.shape[0] - 1]
    if first > last:
        fred_tmp.sort_index(ascending=True, inplace=True)
    else:
        pass

    name_tmp = fred[f]
    fred_tmp.columns = [name_tmp]
    # Exponential moving average and rolling standard deviation
    fred_tmp[name_tmp + '_ema_20'] = fred_tmp[name_tmp].ewm(span = 20, adjust = False).mean()
    fred_tmp[name_tmp + '_ema_50'] = fred_tmp[name_tmp].ewm(span = 50, adjust = False).mean()
    fred_tmp[name_tmp + '_ema_100'] = fred_tmp[name_tmp].ewm(span = 100, adjust = False).mean()
    fred_tmp[name_tmp + '_std_20'] = fred_tmp[name_tmp].rolling(window = 20).std()
    fred_tmp[name_tmp + '_std_50'] = fred_tmp[name_tmp].rolling(window = 50).std()
    fred_tmp[name_tmp + '_std_100'] = fred_tmp[name_tmp].rolling(window = 100).std()

    # Check dates and reverse if necessary
    first = fred_tmp.index[0]
    last = fred_tmp.index[fred_tmp.shape[0] - 1]
    if first < last:
        fred_tmp.sort_index(ascending=False, inplace=True)
    else:
        pass

    all_fred.append(fred_tmp)


del fred_tmp, name_tmp, first, last

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
    'DEXTHUS', # thai baht
    'DEXTAUS', # new taiwan dollar
    'DEXSFUS', # south african rand
    'DEXHKUS', # hong kong dollar
    'DEXMAUS', # malaysian ringgit
    'DEXSDUS', # swidish krona
    'DEXSIUS' # singapore dollar
    'DEXNOUS', # norwegian krone
    'DEXDNUS', # danish krone
    'DEXSLUS', # sri lankan rupee
    'DEXUSNZ', # new zeland dollar
]

all_forex = []

for f in forex:
    print('Pulling FOREX data for', f)
    forex_tmp = web.DataReader(f, 'fred', start_date, end_date)
    forex_tmp.dropna(axis=0, inplace=True)

    # Check dates and reverse if necessary
    first = forex_tmp.index[0]
    last = forex_tmp.index[forex_tmp.shape[0] - 1]
    if first > last:
        forex_tmp.sort_index(ascending=True, inplace=True)
    else:
        pass

    name_tmp = f[3:]
    forex_tmp.columns = [name_tmp]
    # Exponential moving average and rolling standard deviation
    forex_tmp[name_tmp + '_ema_20'] = forex_tmp[name_tmp].ewm(span = 20, adjust = False).mean()
    forex_tmp[name_tmp + '_ema_50'] = forex_tmp[name_tmp].ewm(span = 50, adjust = False).mean()
    forex_tmp[name_tmp + '_ema_100'] = forex_tmp[name_tmp].ewm(span = 100, adjust = False).mean()
    forex_tmp[name_tmp + '_std_20'] = forex_tmp[name_tmp].rolling(window = 20).std()
    forex_tmp[name_tmp + '_std_50'] = forex_tmp[name_tmp].rolling(window = 50).std()
    forex_tmp[name_tmp + '_std_100'] = forex_tmp[name_tmp].rolling(window = 100).std()

    # Check dates and reverse if necessary
    first = forex_tmp.index[0]
    last = forex_tmp.index[forex_tmp.shape[0] - 1]
    if first < last:
        forex_tmp.sort_index(ascending=False, inplace=True)
    else:
        pass

    all_forex.append(forex_tmp)


del forex_tmp, name_tmp

forex_data = pd.concat(all_forex, axis=1)

forex_data.sort_index(ascending=False, inplace=True)

# Join FRED and FOREX data

fred_forex = fred_data.join(forex_data)

###################
##### ALPHA VANTAGE
###################

# Get stock data

stocks = [
    'AMZN',
    'MSFT',
    'AAPL',
    # 'GOOGL',
    'WMT',
    # 'GS',
    'JPM'
]

all_stocks = []

for s in stocks:
    print('Pulling data for', s)
    stock_tmp = alpha_wrangle(stock=s, start=start_date, end=end_date)
    time.sleep(10)
    # Get data for vairous indicators
    bb = get_bb(stock=s, start=start_date, end=end_date)
    time.sleep(10)
    rsi = get_rsi(stock=s, start=start_date, end=end_date)
    time.sleep(10)
    adx = get_adx(stock=s, start=start_date, end=end_date)
    time.sleep(10)
    macd = get_macd(stock=s, start=start_date, end=end_date)
    # Join everything together
    stock_tmp = stock_tmp.join(bb).join(rsi).join(adx).join(macd)
    # Add to list
    all_stocks.append(stock_tmp)
    # Pauses are needed to prevent AlphaVantage API overload
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

endTime = datetime.datetime.now()

print('Time taken to retrieve the data:', endTime - startTime)

#####
