#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 09:21:59 2022

@author: camaike
"""

#import the required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table



#Function to retrieve data from a dataset and do some clean ups

def extract_data(url, filetype, delete_columns, rows_to_skip, separator, indicator):
    '''
    This fucntion is used to retrieve data into a pandas dataframe. It considers the file type
    and ensures the required data is retrieved.

    Parameters
    ----------
    url : string
        Accepts a string url which is either a filepath or web url.
    filetype : string
        accepts a string value. Either 'excel' or 'csv'. Any other type returns an error.
    delete_columns : list
        The columns we want to get rid of.
    rows_to_skip : int
        this accepts an integer value of the number of row headers to skip..
    separator : string
        this accepts a string containing the regex that separates columns on a csv file.
    indicator : string
        the indicator of interest.

    Returns
    -------
    df1 : pandas.core.frame.DataFrame
        Pandas Dataframe of the original dataframe.
    df2 : pandas.core.frame.DataFrame
        The transpose of the original dataframe.

    '''

    #in the bid to make the function more flexible, this conditional statement checks
    #for filetype as specified and uses it to know what method to call to retrieve the data
    if(filetype == 'excel'):
        df = pd.read_excel(url, skiprows=3)
    elif filetype == 'csv':
        df = pd.read_csv(url, skiprows=4)
        df = df.loc[df['Indicator Name'] == indicator]
    else:
        print('Unrecognized file type')

  
    #dropping columns that are not needed. 
    df = df.drop(delete_columns, axis=1)

    #this extracts a dataframe with countries as column
    df1 = df
    
    #this section extract a dataframe with year as columns
    df2 = df.transpose()

    #removed the original headers after a transpose and dropped the row
    #used as a header
    df2 = df2.rename(columns=df2.iloc[0])
    df2 = df2.drop(index=df2.index[0], axis=0)
    df2 = df2.reset_index()
    df2 = df2.rename(columns={"index":"Year"})
    
    return df1, df2


#Function to extract data of country and year of interest of interest

def agg_data(attribute, entity, target_column, indicator):
    
    """
    This function is used to retrieve aggregated data into a pandas dataframe. The sample data retrieved
    using this function is what is used for our charts

        Parameters:
            a. attribute: A list of values i.e. countries or years that we want to consider
            b. entity: relates to the attribute c for countries and any other character for year
            c. target column: the column on the main dataframe that would be a point of reference

        Returns:
            df (pandas.core.frame.DataFrame): Pandas Dataframe of the aggregated data
    
    """

    #generate the original data from file/url
    df1, df2 = extract_data(url, filetype, delete_columns, 4, separator, indicator)
    
    #create a dataframe
    df = pd.DataFrame()
    
    if(entity == 'c'):
        #extract a dataframe of a list of countries
        for country in attribute:
            df = pd.concat([df, df1.loc[df1[target_column] == country]])
        df = df[[target_column] + years]
    else:
    #extract a dataframe of a list of years
        for year in attribute:
            df = pd.concat([df, df2.loc[df2[target_column] == year]])
        df = df[[target_column] + countries]
        
    return df


def sum_data(dataframe):
    
    """
    This function accepts 3 argument and return a new dataframe with an additional column. 
    Additional column could be the mean, mode, median or sd of each row 

        Parameters:
            a. dataframe: The original dataframe we want to sum its data
            b. columns_considered: this gives us the flexibility to choose the column we want to perform an operation on
            c. the type of operation i.e. mean, sum etc

        Returns:
            dataframe (pandas.core.frame.DataFrame): Pandas Dataframe of the aggregated data
    
    """
    
    dataframe['sum'] = dataframe.iloc[:, 1:].mean(axis=1)
    return dataframe


def plot_pie_chart(data, title, label):
    
    """
    This function plots a pie chart

        Parameters:
            a. data: The dataframe in considration
            b. title: the title of the pie chart
            c. Labels for the pie chart
    
    """
    
    plt.pie(data, labels=label, autopct='%1.3f%%', shadow=True, startangle=90)
    plt.title(title, fontsize='22')
    plt.show()


def plot_chart(data, x_data, y_data, kind, xlabel, ylabel, title):
    """
    This function plots a chart based on the kind specified

        Parameters:
            a. data: The dataframe in considration
            b. x_data: data of the x-axis
            c. y_data: data of the y-axis
            d. kind: the kind of chart to plot e.g. bar, line
    
    """
    
    data.plot(x_data, y_data, kind=kind)
    plt.legend(bbox_to_anchor=(1.01, 0.02, .4, .10), loc=3, ncol=1, mode="expand", borderaxespad=0.)
    plt.xticks(rotation='vertical')
    plt.xlabel(xlabel, fontsize='22')
    plt.ylabel(ylabel, fontsize='22')
    plt.title(title, fontsize='22')
    plt.savefig(title)
    plt.show()
    
    

#This function handles the descriptive statistics

def df_describe(data, filename):
    '''
    

    Parameters
    ----------
    data : TYPE
        Pandas dataframe with the result of the decriptive statistics.
    filename : String
        filename to be used to save the descriptive statistics.

    Returns
    -------
    None.

    '''

    #describe = dataframe.describe()

    #create a subplot without frame
    plot = plt.subplot(111, frame_on=False)

    #remove axis
    plot.xaxis.set_visible(False) 
    plot.yaxis.set_visible(False) 

    #create the table plot and position it in the upper left corner
    table(plot, data,loc='upper right')

    #save the plot as a png file
    plt.savefig(filename)
    
###------------------------------------Initializations------------------------------------####

#attributes initiatilization
countries = ['United States', 'Australia', 'Nigeria', 'United Kingdom']
years = ['2015', '2017', '2018', '2019', '2020']

#url/file path initialization
pop_url = 'https://api.worldbank.org/v2/en/indicator/SP.POP.GROW?downloadformat=excel'
arable_url = 'https://api.worldbank.org/v2/en/indicator/AG.LND.ARBL.ZS?downloadformat=excel'
cereal_url = 'https://api.worldbank.org/v2/en/indicator/AG.YLD.CREL.KG?downloadformat=excel'
url = 'API_19_DS2_en_csv_v2_4700503.csv'

#data clean up initialization
delete_columns = ['Country Code', 'Indicator Name', 'Indicator Code']
rows_to_skip_excel = 3
rows_to_skip_csv = 4
separator=''
filetype = 'csv'
operation = 'mean'

#visiualization initiatialization

#Retrieving of population dataframe
df_pop_countries = agg_data(countries, 'c', 'Country Name', 'Population growth (annual %)')
df_pop_years = agg_data(years, 'y', 'Year', 'Population growth (annual %)')

#Retrieving of arable land dataframe
df_arable_countries = agg_data(countries, 'c', 'Country Name', 'Arable land (% of land area)')
df_arable_years = agg_data(years, 'y', 'Year', 'Arable land (% of land area)')

#Retrieving of cereal yield dataframe
df_cereal_countries = agg_data(countries, 'c', 'Country Name', 'Cereal yield (kg per hectare)')
df_cereal_years = agg_data(years, 'y', 'Year', 'Cereal yield (kg per hectare)')

#for pie chart
data = sum_data(df_pop_countries)['sum']
label = sum_data(df_pop_countries)['Country Name']
title = 'Aggregate Population Growth'

#for the different plots - year
x_data_year = 'Year'
y_data_year = countries

#for the different plots - countries
x_data_country = 'Country Name'
y_data_country = years










