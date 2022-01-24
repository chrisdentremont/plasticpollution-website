import numpy as np
import pandas as pd
from sklearn import linear_model

def importSheets():
    #Importing and creating DataFrames to use for linear regression
    path1 = 'datasheets/global-plastics-production.csv'
    path2 = 'datasheets/plastic-waste-per-capita.csv'
    path3 = 'datasheets/mismanaged-waste-global-total.csv'
    path4 = 'datasheets/per-capita-plastic-waste-vs-gdp-per-capita.csv'

    #CSV representing global plastic production (input feature)
    df1 = pd.read_csv(path1)

    #CSV representing plastic waste per capita (input feature)
    df2 = pd.read_csv(path2)

    #CSV representing global mismanaged waste (predicted output value)
    df3 = pd.read_csv(path3)

    #CSV representing population for each country (input feature)
    df4 = pd.read_csv(path4)
    df4 = df4[df4['Year'] == 2010]

    #Create main DataFrame with important features
    newFrame = [df2["Entity"], df2["Code"], df2["Per capita plastic waste (kg/person/day)"], df3["Mismanaged waste (% global total)"]]
    newHeaders = ["Entity", "Code", "Per capita plastic waste (kg/person/day)", "Mismanaged waste (% global total)"]
    df5 = pd.concat(newFrame, axis=1, keys=newHeaders)
    df5.insert(1, 'Global plastics production (million tonnes)', 313000000)

    #Merge the population DataFrame to be included in main DataFrame
    newDf = pd.merge(df5, df4[['Entity', 'Total population (Gapminder, HYDE & UN)']], on='Entity', how='left')
    newDf = newDf[pd.notna(newDf['Total population (Gapminder, HYDE & UN)'])]

    return newDf

def calculate(plasticProduced, wastePerPerson, population):
    newDf = importSheets()

    #Multiple Linear Regression
    X = newDf[['Global plastics production (million tonnes)', 'Per capita plastic waste (kg/person/day)', 'Total population (Gapminder, HYDE & UN)']]
    y = newDf['Mismanaged waste (% global total)']

    #Fit the above columns to a multiple linear regression model to be able to predict plastic wasted
    regression = linear_model.LinearRegression()
    regression.fit(X, y)

    return regression.predict([[plasticProduced, wastePerPerson, population]])