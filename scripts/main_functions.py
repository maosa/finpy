
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

##########################################################################################
##########################################################################################

# RMSE function

def RMSE(observations, predictions):
    return np.sqrt(((predictions - observations) ** 2).mean())

##########################################################################################
##########################################################################################

# Define a function to pull and wrangle Alpha Vantage data

def alpha_wrangle(stock, start, end):

    # Check start/end dates format

    if isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()


    if isinstance(end, datetime.date):
        pass
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # Data pulling and wrangling

    # Get an object with the daily data and another with the call's metadata

    data, _ = ts.get_daily_adjusted(symbol = stock, outputsize = 'full')

    data.index = pd.to_datetime(data.index, format = '%Y-%m-%d').date

    # Rename columns for consistency and easier manipulation

    data.columns = [c.replace(' ', '_')[3:] for c in data.columns]

    # data.drop(labels = ['dividend_amount', 'split_coeff'], axis = 1, inplace = True)

    data['date'] = data.index

    # Subset table based on dates

    mask = (data['date'] >= start) & (data['date'] <= end)

    data = data.loc[mask]

    # Add extra columns with more data

    data['daily_range'] = abs(data.high - data.low)

    data['relative_returns'] = data['adjusted_close'].pct_change(1)

    # Log returns - First the logarithm of the prices is taken and then
    # the difference of consecutive (log) observations

    data['log_returns'] = np.log(data['adjusted_close']).diff()

#     data['cumsum_log_returns'] = data['log_returns'].cumsum()

#     # Moving averages

#     data['sma_20'] = data['adjusted_close'].rolling(window = 20).mean()

#     data['sma_50'] = data['adjusted_close'].rolling(window = 50).mean()

#     data['sma_100'] = data['adjusted_close'].rolling(window = 100).mean()

    # Exponential moving average

    data['ema_20'] = data['adjusted_close'].ewm(span = 20, adjust = False).mean()

    data['ema_50'] = data['adjusted_close'].ewm(span = 50, adjust = False).mean()

    data['ema_100'] = data['adjusted_close'].ewm(span = 100, adjust = False).mean()

    data.drop(labels = ['date'], axis=1, inplace=True)

    data.columns = [stock + '_' + c for c in data.columns]

    return data

##########################################################################################
##########################################################################################

# Get Bollinger Bands from Alpha Vantage

# https://www.investopedia.com/articles/technical/04/030304.asp

def get_bb(stock, start, end):

    # Check start/end dates format

    if isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()


    if isinstance(end, datetime.date):
        pass
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # Data pulling and wrangling

    bb, _ = ti.get_bbands(symbol=stock, interval='daily', matype=1)

    bb.index = pd.to_datetime(bb.index, format = '%Y-%m-%d').date

    # Rename columns for consistency and easier manipulation

    bb.columns = [c.replace(' ', '_').lower() for c in bb.columns]

    # Subset table based on dates

    bb['date'] = bb.index

    mask = (bb['date'] >= start) & (bb['date'] <= end)

    bb = bb.loc[mask]

    bb.drop(labels = ['date'], axis=1, inplace=True)

    bb.columns = [stock + '_' + c for c in bb.columns]

    return bb

##########################################################################################
##########################################################################################

# Get RSI from Alpha Vantage

# https://www.investopedia.com/articles/active-trading/042114/
# overbought-or-oversold-use-relative-strength-index-find-out.asp

def get_rsi(stock, start, end):

    # Check start/end dates format

    if isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()


    if isinstance(end, datetime.date):
        pass
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # Data pulling and wrangling

    rsi, _ = ti.get_rsi(symbol=stock, interval='daily')

    rsi.index = pd.to_datetime(rsi.index, format = '%Y-%m-%d').date

    # Rename columns for consistency and easier manipulation

    rsi.columns = [c.replace(' ', '_') for c in rsi.columns]

    # Subset table based on dates

    rsi['date'] = rsi.index

    mask = (rsi['date'] >= start) & (rsi['date'] <= end)

    rsi = rsi.loc[mask]

    rsi.drop(labels = ['date'], axis=1, inplace=True)

    rsi.sort_index(ascending=False, inplace=True)

    rsi.columns = [stock + '_' + c for c in rsi.columns]

    return rsi

##########################################################################################
##########################################################################################

# Get ADX from Alpha Vantage

# https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp

def get_adx(stock, start, end):

    # Check start/end dates format

    if isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()


    if isinstance(end, datetime.date):
        pass
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # Data pulling and wrangling

    adx, _ = ti.get_adx(symbol=stock, interval='daily')

    adx.index = pd.to_datetime(adx.index, format = '%Y-%m-%d').date

    # Rename columns for consistency and easier manipulation

    adx.columns = [c.replace(' ', '_') for c in adx.columns]

    # Subset table based on dates

    adx['date'] = adx.index

    mask = (adx['date'] >= start) & (adx['date'] <= end)

    adx = adx.loc[mask]

    adx.drop(labels = ['date'], axis=1, inplace=True)

    adx.sort_index(ascending=False, inplace=True)

    adx.columns = [stock + '_' + c for c in adx.columns]

    return adx

##########################################################################################
##########################################################################################

# Get MACD from Alpha Vantage

# https://www.investopedia.com/articles/forex/05/macddiverge.asp

def get_macd(stock, start, end):

    # Check start/end dates format

    if isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()


    if isinstance(end, datetime.date):
        pass
    else:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # Data pulling and wrangling

    macd, _ = ti.get_macd(symbol=stock, interval='daily')

    macd.index = pd.to_datetime(macd.index, format = '%Y-%m-%d').date

    # Rename columns for consistency and easier manipulation

    macd.columns = [c.replace(' ', '_') for c in macd.columns]

    # Subset table based on dates

    macd['date'] = macd.index

    mask = (macd['date'] >= start) & (macd['date'] <= end)

    macd = macd.loc[mask]

    macd.drop(labels = ['MACD_Hist', 'MACD_Signal', 'date'], axis = 1, inplace = True)

    macd.columns = [stock + '_' + c for c in macd.columns]

    return macd

##########################################################################################
##########################################################################################

# Get bond data from datahub.io

def get_bonds(package, freq, start, end):

    bond_data = Package(package)

    # Convert to pandas dataframe

    bond_data = pd.DataFrame(bond_data.get_resource(freq).read())

    # Data wrangling

    bond_data.columns = ['date', 'yield']

    bond_data['date'] = pd.to_datetime(bond_data['date'], format = '%Y-%m-%d')

    bond_data.index = bond_data['date']

    bond_data['day'] = bond_data.index.day

    bond_data['month'] = bond_data.index.month

    bond_data['year'] = bond_data.index.year

    bond_data.drop(labels = ['date', 'day'], axis = 1, inplace = True)

    bond_data = bond_data.loc[bond_data.year >= datetime.datetime.strptime(start, '%Y-%m-%d').date().year]

    return bond_data

##########################################################################################
##########################################################################################



##########################################################################################
##########################################################################################
