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

# Define start/end dates

start_date = '2015-01-01'

end_date = datetime.datetime.today().date()

##########################################################################################
##########################################################################################

###########
##### BONDS
###########

# 10 year US Government Bond Yields (long-term interest rate)
# https://datahub.io/core/bond-yields-us-10y#python

# ten_yr_us_bond = get_bonds(package='https://datahub.io/core/bond-yields-us-10y/datapackage.json',
#                            freq='monthly_csv')


# 10y UK Government Bond Yields (long-term interest rate)
# https://datahub.io/core/bond-yields-uk-10y#python

# ten_yr_uk_bond = get_bonds(package='https://datahub.io/core/bond-yields-uk-10y/datapackage.json',
#                            freq='quarterly_csv')


# 2-Year Treasury Constant Maturity Rate (DGS2)
# https://fred.stlouisfed.org/series/DGS2

two_yr_us_bond = web.DataReader('DGS2', 'fred', start_date, end_date)


# 10-Year Treasury Constant Maturity Rate (DGS10)
# https://fred.stlouisfed.org/series/DGS10

ten_yr_us_bond = web.DataReader('DGS10', 'fred', start_date, end_date)


# 30-Year Treasury Constant Maturity Rate (DGS30)
# https://fred.stlouisfed.org/series/DGS30

thirty_yr_us_bond = web.DataReader('DGS30', 'fred', start_date, end_date)

########################
##### VOLATILITY INDEXES
########################

# VIX - CBOE Volatility Index
# https://datahub.io/core/finance-vix#python

vix = get_vix(start=start_date, end=end_date)

# CBOE Volatility Index: VIX
# https://fred.stlouisfed.org/series/VIXCLS

# vix = web.DataReader('VIXCLS', 'fred', start_date, end_date)

# CBOE Crude Oil ETF Volatility Index
# https://fred.stlouisfed.org/series/OVXCLS

oil_etf_vol = web.DataReader('OVXCLS', 'fred', start_date, end_date)

# CBOE Gold ETF Volatility Index
# https://fred.stlouisfed.org/series/GVZCLS

gold_etf_vol = web.DataReader('GVZCLS', 'fred', start_date, end_date)

# CBOE China ETF Volatility Index
# https://fred.stlouisfed.org/series/VXFXICLS

china_etf_vol = web.DataReader('VXFXICLS', 'fred', start_date, end_date)

# CBOE Emerging Markets ETF Volatility Index
# https://fred.stlouisfed.org/series/VXEEMCLS

emer_markets_etf_vol = web.DataReader('VXEEMCLS', 'fred', start_date, end_date)

# CBOE Russell 2000 Volatility Index
# https://fred.stlouisfed.org/series/RVXCLS

russel_2k_etf_vol = web.DataReader('RVXCLS', 'fred', start_date, end_date)

# CBOE Energy Sector ETF Volatility Index
# https://fred.stlouisfed.org/series/VXXLECLS

energy_etf_vol = web.DataReader('VXXLECLS', 'fred', start_date, end_date)

####################
##### MARKET INDEXES
####################

# # Get Dow Jones index data from AlphaVantage

# d_jones = alpha_wrangle(stock='DJI')

# # Get S&P500 index data from AlphaVantage

# sp500 = alpha_wrangle(stock='INX')

# S&P500
# https://fred.stlouisfed.org/series/SP500

sp500 = web.DataReader('SP500', 'fred', start_date, end_date)

# Dow Jones Industrial Average
# https://fred.stlouisfed.org/series/DJIA

d_jones = web.DataReader('DJIA', 'fred', start_date, end_date)

# NASDAQ
# https://fred.stlouisfed.org/series/NASDAQCOM

nasdaq = web.DataReader('NASDAQCOM', 'fred', start_date, end_date)

####################
##### OTHER FEATURES
####################

crude_oil_texas = web.DataReader('DCOILWTICO', 'fred', start_date, end_date)

gold_morning = web.DataReader('GOLDAMGBD228NLBM', 'fred', start_date, end_date)

gold_afternoon = web.DataReader('GOLDPMGBD228NLBM', 'fred', start_date, end_date)

crude_oil_brent = web.DataReader('DCOILBRENTEU', 'fred', start_date, end_date)

hh_natural_gas = web.DataReader('DHHNGSP', 'fred', start_date, end_date)

high_yield_master_II_tri = web.DataReader('BAMLHYH0A0HYM2TRIV', 'fred', start_date, end_date)

corporate_master_tri = web.DataReader('BAMLCC0A0CMTRIV', 'fred', start_date, end_date)

economic_uncertainty_index = web.DataReader('WLEMUINDXD', 'fred', start_date, end_date)

#################
##### NATURAL GAS
#################

# Natural gas prices
# https://datahub.io/core/natural-gas#python

# nat_gas = get_nat_gas()

#########
##### OIL
#########

# Get NASDAQ Commodity Crude Oil Index ER (NQCICLER)

# oil = get_oil()

###################
##### ALPHA VANTAGE
###################

# Get stock data

stock = 'AMZN'

stock_data = alpha_wrangle(stock=stock, start=start_date, end=end_date)

# Get data for vairous indicators

rsi = get_rsi(stock=stock, start=start_date, end=end_date)

bb = get_bb(stock=stock, start=start_date, end=end_date)

adx = get_adx(stock=stock, start=start_date, end=end_date)

macd = get_macd(stock=stock, start=start_date, end=end_date)

###########
##### FOREX
###########

# Get forex data

usd_eur = web.DataReader('DEXUSEU', 'fred', start_date, end_date) # euro

cny_usd = web.DataReader('DEXCHUS', 'fred', start_date, end_date) # chinese yuan

jpy_usd = web.DataReader('DEXJPUS', 'fred', start_date, end_date) # japanese yen

cad_usd = web.DataReader('DEXCAUS', 'fred', start_date, end_date) # canadian dollar

usd_gbp = web.DataReader('DEXUSUK', 'fred', start_date, end_date) # british pounds

krw_usd = web.DataReader('DEXKOUS', 'fred', start_date, end_date) # south korean won

mxn_usd = web.DataReader('DEXMXUS', 'fred', start_date, end_date) # mexican peso

brl_usd = web.DataReader('DEXBZUS', 'fred', start_date, end_date) # brazilian real

inr_usd = web.DataReader('DEXINUS', 'fred', start_date, end_date) # indian rupee

aud_usd = web.DataReader('DEXUSAL', 'fred', start_date, end_date) # australian dollar

chf_usd = web.DataReader('DEXSZUS', 'fred', start_date, end_date) # swiss franc

thb_usd = web.DataReader('DEXTHUS', 'fred', start_date, end_date) # thai baht

twd_usd = web.DataReader('DEXTAUS', 'fred', start_date, end_date) # new taiwan dollar

zar_usd = web.DataReader('DEXSFUS', 'fred', start_date, end_date) # south african rand

hkd_usd = web.DataReader('DEXHKUS', 'fred', start_date, end_date) # hong kong dollar

myr_usd = web.DataReader('DEXMAUS', 'fred', start_date, end_date) # malaysian ringgit

sek_usd = web.DataReader('DEXSDUS', 'fred', start_date, end_date) # swidish krona

sgd_usd = web.DataReader('DEXSIUS', 'fred', start_date, end_date) # singapore dollar

nok_usd = web.DataReader('DEXNOUS', 'fred', start_date, end_date) # norwegian krone

dkk_usd = web.DataReader('DEXDNUS', 'fred', start_date, end_date) # danish krone

lkr_usd = web.DataReader('DEXSLUS', 'fred', start_date, end_date) # sri lankan rupee

nzd_usd = web.DataReader('DEXUSNZ', 'fred', start_date, end_date) # new zeland dollar

###############
##### JOIN DATA
###############

other = crude_oil_texas.join(gold_morning).join(gold_afternoon).join(crude_oil_brent).join(hh_natural_gas)

other = other.join(high_yield_master_II_tri).join(corporate_master_tri).join(economic_uncertainty_index)

other.sort_index(ascending=False, inplace=True)

# Join forex data

forex = usd_eur.join(cny_usd).join(jpy_usd).join(cad_usd).join(usd_gbp).join(krw_usd).join(mxn_usd)

forex = forex.join(brl_usd).join(inr_usd).join(aud_usd).join(chf_usd).join(thb_usd).join(twd_usd)

forex = forex.join(zar_usd).join(hkd_usd).join(myr_usd).join(sek_usd).join(sgd_usd).join(nok_usd)

forex.join(dkk_usd).join(lkr_usd).join(nzd_usd)

forex.sort_index(ascending=False, inplace=True)

##### Join all datasets ####

# Set prediction period (in days)

pred_period = 30

# Join volatility datasets

vol_data = vix.join(oil_etf_vol).join(gold_etf_vol).join(china_etf_vol)

vol_data = vol_data.join(emer_markets_etf_vol).join(russel_2k_etf_vol).join(energy_etf_vol)#.dropna(axis=0)

# Join major index data

index_data = sp500.join(d_jones).join(nasdaq)

# Join all extra datasets

technical_ind = bb.join(rsi).join(adx).join(macd)

# Join all of the above together

alt_data = index_data.join(vol_data).join(technical_ind).join(other).join(forex)

# Add this to the stock data

cols_to_drop = ['open', 'high', 'low', 'close', 'date', 'vix_open', 'vix_high', 'vix_low']

data = stock_data.join(alt_data).drop(labels = cols_to_drop, axis = 1).dropna(axis=0)

# Rename columns from FRED (Federal Reserve Economics Data)



###################
##### SAVE THE DATA
###################

data.to_csv('data/all_data.csv', sep=',', header=True, index=True)

#####
