
##########################################################################################
##########################################################################################

# Set up the environment

import sys

# Add path for python to look into for modules installed using pip

sys.path.append('/usr/local/lib/python3.7/site-packages/')

import os
import pandas as pd

##########################################################################################
##########################################################################################

# Change into the correct directory

if os.getcwd() != os.path.expanduser('~') + '/finpy/':
    os.chdir(os.path.expanduser('~') + '/finpy/')
else:
    pass

###################
##### READ THE DATA
###################

data = pd.read_csv('data/filt_data.csv', sep=',', index_col=0)

####################
##### SHIFT THE DATA
####################

# Define the variable of interest

target_stock = 'MSFT'

target = target_stock + '_adjusted_close'

##########################################################################################

# Set prediction period (in days)

pred_period = 30

# Create shifted dataset

data_shifted = data.shift(-pred_period) # KEY STEP!!! MAKE SURE THIS IS CORRECT!!!

data_shifted['price'] = data[target]

data_shifted.dropna(axis = 0, inplace=True)

##########################################################################################

# Create the training set

train = data_shifted.iloc[pred_period:, :].sort_index()

# Create the test set

test = data_shifted.iloc[:pred_period, :].sort_index()

print('Training set dimensions:', train.shape)

print('Test set dimensions:', test.shape)

###################
##### SAVE THE DATA
###################

train.to_csv('data/train.csv', sep=',', header=True, index=True)

test.to_csv('data/test.csv', sep=',', header=True, index=True)

#####
