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
from datapackage import Package
import pandas_datareader.data as web
import datetime
from main_functions import *

##########################################################################################
##########################################################################################



################
##### SHIFT DATA
################

# Create shifted dataset

cols_to_drop = ['adjusted_close', 'open', 'high', 'low', 'close', 'date', 'vix_open', 'vix_high', 'vix_low']

data_tmp = stock_data.join(alt_data).drop(labels = cols_to_drop, axis = 1)

data_shifted = data_tmp.shift(-pred_period) # KEY STEP!!! MAKE SURE THIS IS CORRECT!!!

del data_tmp

# Add the unshifted adjusted close values
# i.e. use features from a certain time ago to predict the current price

data_shifted = data_shifted.join(stock_data.adjusted_close).dropna(axis = 0)

# Create the training set

train = data_shifted.iloc[pred_period:, :].sort_index()

# Create the test set

test = data_shifted.iloc[:pred_period, :].sort_index()

###############
##### SAVE DATA
###############

train.to_csv('data/train.csv', sep=',', header=True, index=True)

test.to_csv('data/test.csv', sep=',', header=True, index=True)

#####
