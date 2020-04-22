#!/usr/bin/env python
# coding: utf-8

# ##### Collecting Latest COVID-19 data

import requests
import pandas as pd

def getCovidDataFromWorldometers(url):
    resp = requests.get(url)
    dfs = pd.read_html(resp.text)
    df = dfs[0] #The first html table contains our data
    df.columns = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths',
           'Total Recovered', 'Active Cases', 'Serious,Critical',
           'Tot Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 'Tests/1M pop']

    #Remove comma and plus characters from 'New Cases' and 'New Deaths' field as comma and plus appear there
    #Also convert the column types from object to float (trying to convert to 'int' will result in error for NaN values)
    if (df['New Cases'].dtype == 'object'):
        df['New Cases'] = df['New Cases'].str.replace(',', '').str.replace('+', '')
        df['New Cases'] = df['New Cases'].astype(str).astype(float)

    if (df['New Deaths'].dtype == 'object'):
        df['New Deaths'] = df['New Deaths'].str.replace(',', '').str.replace('+', '')
        df['New Deaths'] = df['New Deaths'].astype(str).astype(float)

    #Remove the last record (Total:) as it is already available at top with 'World'
    df = df[df['Country']!='Total:']

    #Sort the dataframe in decreasing order of Tocal Cases
    df = df.sort_values('Total Cases', ascending=False)
    return df;

def main():
    covid_url = 'https://www.worldometers.info/coronavirus/'
    # covid_india_url = 'https://www.mygov.in/corona-data/covid19-statewise-status'

    dfCovid = getCovidDataFromWorldometers(covid_url)
    # Output the data as an xlsx file skipping the row index 0,1,2,...
    dfCovid.to_csv('Covid19-Data-Worldwide.csv', index=False);
    dfCovid.to_excel('Covid19-Data-Worldwide.xlsx', index=False);

if __name__ == '__main__':
    main()