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



#Function to retrieve data from a dataset and do some clean ups

def extract_data(url, filetype, skip_row, separator, del_columns):
    """
    This fucntion is used to retrieve data into a pandas dataframe. It considers the file type
    and ensures the required data is retrieved.

        Parameters:
            a. url: Accepts a string url which is either a filepath or web url
            b. filetype: accepts a string value. Either 'excel' or 'csv'. Any other type returns an error
            c. skip_row: this accepts an integer value of the number of row headers to skip.
            d. separator: this accepts a string containing the regex that separates columns on a csv file

        Returns:
            df_countries (pandas.core.frame.DataFrame): Pandas Dataframe of the original dataframe
            df_year (pandas.core.frame.DataFrame): The transpose of the original dataframe
    
    
    """

    #in the bid to make the function more flexible, this conditional statement checks
    #for filetype as specified and uses it to know what method to call to retrieve the data
    if(filetype == 'excel'):
        df = pd.read_excel(url, skiprows=skip_row)
    elif filetype == 'csv':
        df = pd.read_csv(url, sep=separator)
    else:
        print('Unrecognized file type')

    #dropped rows that have maximum of 2 NAs
    df.dropna(thresh=2)

    #assigned the original dataframe to a new variable
    df_countries = df
    
    #drop columns that are not needed as specified
    df = df.drop(del_columns, axis=1)
    
    #the second dataframe is the transpose of the original dataframe
    df_year = df.transpose()
    
    #Since the index of the original became the header of the transpose
    #the first row is used for as the header. For this assignment, we assume that the first
    #row would always be the country name
    df_year = df_year.rename(columns=df_year.iloc[0])
    df_year = df_year.drop(index=df_year.index[0], axis=0)
    df_year = df_year.reset_index()
    df_year = df_year.rename(columns={"index":"Year"})
    
    #return the 2 dataframes
    return df_countries, df_year


#Function to extract data of country and year of interest of interest

def country_data(data, entity, column1, column2):
    
    """
    This fucntion is used to retrieve data for specific countries and years or specific years and countries
    and puts it into a dataframe. It is a function used to extract a subset of data of interest from the
    original dataframe

        Parameters:
            a. data: accepts a pandas dataframe. This is usually the original dataframe with all the data required
            b. entity: accepts a list of countries or years we would want to extract data for. However, you should
                note that if entity is a list of countries, then, the dataframe with country name as column should he used
                else, the dataframe with years as column
            c. column1: the desired column to be extracted
            d. column2: the second column to be extracted

        Returns:
            df_countries (pandas.core.frame.DataFrame): Pandas Dataframe of the selected countries and years
    """
    
    #extracts a dataframe of 2 columns
    df = data[[column1, column2]]
    
    #create a new dataframe to hold our results
    dfO = pd.DataFrame(columns=[column1, column2])
    
    #a for loop to iterate through the list of countries/years provided
    for e in entity:
        dfO = pd.concat([dfO, df.loc[df[column1] == e]])
    return dfO






