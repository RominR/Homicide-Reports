#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 08:27:40 2022

@author: rominrajbhandari
"""
#Let us first import the libraries that are required.

#standard libraries
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from numpy.random import randn

#statistics
from scipy import stats

#plotting
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#setting directory
import os
os.getcwd()
os.chdir('/Users/romin/Library/Datasets')

#datetime
import datetime

#Regular expression
import re
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Reading the dataset
#url = https://www.kaggle.com/murderaccountability/homicide-reports/code
Homicide_Reports = pd.read_csv('HomicideReports.csv')
Homicide_Reports.info() #Checking the summary of the dataset.

pd.options.display.max_columns = 6 #Displaying the number of columns in the output section.
Homicide_Reports.head(5) #Displaying the first five rows. 

#Got DtypeWarning: Columns (16) i.e. 'Perpetrator Age' has mixed data types. Let us see what is happening.

Homicide_Reports['Perpetrator Age'].apply(type).value_counts()
#As we can see there are mixed types of integer and string. Let us fix this.

#Now, let us see how the string values look like.

#Adding new column to see the data types in the dataset.
Homicide_Reports['MixedDataType'] = Homicide_Reports['Perpetrator Age'].apply(type)
Homicide_Reports.MixedDataType.unique() #Checking if the column is added to the dataset.

#Let's check only the string values and find if any observations contain the alphanumeric and special characters.
Homicide_Reports[(Homicide_Reports.MixedDataType == str) & (Homicide_Reports['Perpetrator Age'].str.findall("[a-zA-Z]")) | (Homicide_Reports['Perpetrator Age'].str.findall("[^a-zA-Z0-9]+"))]
#There is one row which has special characters. Let's see what that special character is.
Homicide_Reports.iloc[634666] #It is either empty or space. Let's find out what that is.
Homicide_Reports[Homicide_Reports['Perpetrator Age'] == ''] #It is not the empty observation.
Homicide_Reports[Homicide_Reports['Perpetrator Age'] == ' '] #It is the observation that contains space character.

#Also, let us try to find if there are any NaN values. This part was already found when .unique() function was run in the code above.
Homicide_Reports[Homicide_Reports['Perpetrator Age'].isnull()]
Homicide_Reports[Homicide_Reports['Perpetrator Age'] == None]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Now, let us work on resolving it.

#Since it is only one row, we can either drop it and give the value using mode.
#let us replace it. We cannot use fillnaI() because it is not a NaN value.
Homicide_Reports['Perpetrator Age'].replace({' ': Homicide_Reports['Perpetrator Age'].mode()[0]}, inplace = True)

#Also, let us convert all the string values to integer.
Homicide_Reports['Perpetrator Age'] = Homicide_Reports['Perpetrator Age'].astype(int)

#Dropping MixedDataType as we don't need it anymore.
Homicide_Reports.drop('MixedDataType', axis = 1, inplace = True)

'''If we had not eliminated space character from the column, then we would have to go through other route which is below:
homicidereports['Perpetrator Age'] = pd.to_numeric(homicidereports['Perpetrator Age'], errors = 'coerce').astype('Int64').astype(int)
But it is better that we remove any other dtypes besides int because 'Age' can never be any other dtypes besides int.'''

def data_check():
    for col in Homicide_Reports.columns:
        if (Homicide_Reports[col].dtypes == 'object'):
            if (Homicide_Reports[(Homicide_Reports[col] == '') | (Homicide_Reports[col].str.findall("[^a-zA-Z0-9 ]+"))][[col]]).empty:
                print(f"Column '{col}' is empty.\n\n")
            elif (len(Homicide_Reports[(Homicide_Reports[col] == '') | (Homicide_Reports[col].str.findall("[^a-zA-Z0-9 ]+"))][[col]]) ==
                  len(Homicide_Reports[(Homicide_Reports[col] == '') | (Homicide_Reports[col].str.findall("[\:\.\(\)\-\&\'\,\/]+"))][[col]])):
                print(f'''Column '{col}' is not empty.\nBut the length of both the columns matches.
                      Now, let's check if there is just a special character in any of the rows.\n\n"''')
                for spec_char in list(":.()-&',/"):
                    if not (Homicide_Reports[Homicide_Reports[col] == spec_char][col]).empty:
                        print(f"There is just a '{spec_char}' character in one of the rows. See the result below:")
                        print(Homicide_Reports[Homicide_Reports[col] == spec_char][col],"\n\n")
                    else:
                        print(f"There is no just '{spec_char}' character in any row. See the empty series below:")
                        print(Homicide_Reports[Homicide_Reports[col] == spec_char][col],"\n\n")
            else:
                print(f'''The length of {col} columns don't match. There may be a different special character than
                      what is provided in the 'elif' above.\n\n''')
              
data_check()
            
#In the above code, I am checking if any of the rows in different columns contain only special characters. 

#It looks like none of the column need to be cleaned as it appears the there aren't any issue.


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#We worked on the Data type warning and did some data preparation. Now, let us now work on the visualization questions.

#Find the distribution of total number of crime each year.
sns.histplot(data = Homicide_Reports['Year'], kde = True)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Find the total crime, total solved, unsolved crimes in each year and plot it in the graph.

# Step1: Find total number of crime solved in different year.
Homicide_Reports['Crime Solved'].unique()
crime_solved = Homicide_Reports[Homicide_Reports['Crime Solved'] == 'Yes']['Year'].value_counts(sort = False)
crime_solved = DataFrame(crime_solved).reset_index()
crime_solved.rename(columns = {'index': 'Year', 'Year': 'Total_Crime_Solved'}, inplace = True)
crime_solved

# Step2: Find total number of crime that were not solved in different year.
crime_unsolved = Homicide_Reports[Homicide_Reports['Crime Solved'] == 'No']['Year'].value_counts(sort = False)
crime_unsolved = DataFrame(crime_unsolved).reset_index().rename({'index': 'Year', 'Year': 'Total_Crime_Unsolved'}, axis = 1)
crime_unsolved

#Step3: Find total crime
total_crime = Homicide_Reports['Year'].value_counts(sort = False)
total_crime = DataFrame(total_crime).reset_index().rename({'index': 'Year', 'Year': 'Total_Crime'}, axis = 1)
total_crime

#Step 4: let us plot barplot
fig1, ax1 = plt.subplots(figsize = (20,10))
sns.barplot(data = total_crime, x = 'Year', y = 'Total_Crime', saturation = 1, color = 'red', label = 'Total Crime', ax = ax1, estimator = sum)
sns.barplot(data = crime_solved, x = 'Year', y = 'Total_Crime_Solved', saturation = 0.5, color = 'yellow', label = 'Total Crime Solved', ax = ax1, estimator = sum)
sns.barplot(data = crime_unsolved, x = 'Year', y = 'Total_Crime_Unsolved', color = 'blue', label = 'Total Crime Unsolved', ax = ax1, estimator = sum)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 60)
plt.legend()
#It looks like there is positive correlations between total crime and crime being solved/unsolved.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let us make the graph more easier to understand. But, first we need to concatenate the above 3 dataframes.
df_concat = pd.concat([total_crime, crime_solved[['Total_Crime_Solved']], crime_unsolved[['Total_Crime_Unsolved']]], axis = 1)
df_concat

#Now, let us plot barplot
fig2, ax2 = plt.subplots(figsize = (20,10))
tidy = df_concat.melt(id_vars = 'Year').rename(columns = str.title) 
sns.barplot(data = tidy, x = 'Year', y = 'Value', hue = 'Variable', ax = ax2, orient = 'v', estimator = sum)


#Let us plot horizontal barplot
fig3, ax3 = plt.subplots(figsize = (14,12))
tidy = df_concat.melt(id_vars = 'Year').rename(columns = str.title) 
sns.barplot(data = tidy, x = 'Value', y = 'Year', hue = 'Variable', orient = 'h', ax = ax3, estimator = sum)

#Or we can also use matplotlib.
df_concat.set_index('Year').plot(kind = 'barh', figsize = (10, 12))
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Plotting the agencies that were investigating in the crimes.
Homicide_Reports['Agency Type'].value_counts().plot(kind = 'barh', color = ['r', 'g', 'c', 'b', 'y', 'black'])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Plotting the types of crime commited and if that crime was solved or not. Also check if the perpetrator's race.
Homicide_Reports['Crime Type'].unique() #Checking the unique values before performing the operations
Homicide_Reports['Crime Solved'].unique()
Homicide_Reports['Perpetrator Race'].unique()

#Now, plotting
sns.catplot(data = Homicide_Reports, x = 'Crime Type', kind = 'count', hue = 'Crime Solved', col = 'Perpetrator Race', sharey = False)
#From the plot, we can say that when the perpetrator race is 'Unknown', the crime is less likely to be solved.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let's find out which race group has been a victim the most.
Homicide_Reports['Victim Race'].unique() #Checking the unique values before performing the operations

plt.figure(figsize = (8, 4))
sns.countplot(data = Homicide_Reports, y = 'Victim Race')
plt.show()

#OR
fig4, ax4 = plt.subplots(figsize = (8,4))
sns.countplot(data = Homicide_Reports, x = 'Victim Race', ax = ax4)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation = 90)
plt.show()

#OR
Homicide_Reports['Victim Race'].value_counts().plot(kind = 'barh', color = ['r', 'g', 'b', 'c', 'm'])

#Black and White are the most victims. Let's find out if perpetrator kills the people from same race or different.
Homicide_Reports.info()
Homicide_Reports[['Month', 'State', 'Incident', 'Crime Type', 'Weapon']]
Homicide_Reports['Victim Race'].unique()
Homicide_Reports['Perpetrator Race'].unique()

fig4, ax4 = plt.subplots(figsize = (8,4))
sns.countplot(data = Homicide_Reports, x = 'Perpetrator Race', hue = 'Victim Race', ax = ax4)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation = 30)
plt.show()

#It looks like perpetrator kills the victims from same race more than any other.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#It is time to find out if perpetrator and victims are from the same family.
Homicide_Reports['Relationship'].unique()

fig4, ax4 = plt.subplots(figsize = (8,4))
sns.countplot(data = Homicide_Reports, x = 'Relationship', palette='flare', ax = ax4,
              order = Homicide_Reports.Relationship.value_counts(ascending = False).index)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation = 90)
plt.show()

#If we discard 'Unknown' relationship, the people who know the perpetrator slightly have been the victim and also, the people who are stranger to the perpetrator have been murdered.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Now, let us check that based on the perpetrator race, what is the perpetrator's relationship with the victim they murdered.
plot = sns.countplot(data = Homicide_Reports, x = 'Perpetrator Race', hue = 'Relationship', palette = 'Paired',
              order = Homicide_Reports['Perpetrator Race'].value_counts(ascending = False).index,
              hue_order = Homicide_Reports['Relationship'].value_counts(ascending = False).index)
plot.set_xticklabels(plot.get_xticklabels(), rotation = 90)
sns.move_legend(plot, "center left", bbox_to_anchor = (1.25, 0.5), ncol = 2, frameon = False)
plt.show()

'''Looking at the white and black race, the top four victims killed by white race perpetrator are Acquaintance, Stranger, Unknown and Wife respectively,
whereas, the top four victims killed by black race perpetrator are Acquaintance, Unknown, Stranger, and Friend.'''
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#What types of weapons were used to harm victims.
Homicide_Reports.Weapon.unique() #Checking the unique values before performing the operations

sns.countplot(data = Homicide_Reports, y = 'Weapon', palette = 'rainbow', order = Homicide_Reports['Weapon'].value_counts().index)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Find the month that either solved or didn't solve the crime and if the victims in those crimes were male, female or unknown.

Homicide_Reports['Crime Solved'].unique() #Checking the unique values before performing the operations
Homicide_Reports['Victim Sex'].unique()   #Checking the unique values before performing the operations

# In order to solve the question,converting month to numerical value and adding the column in the dataset, so that I can get the result in order.

month_to_num = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May':5,
                'June': 6, 'July': 7, 'August': 8, 'September': 9,
                'October': 10, 'November': 11, 'December': 12}
Homicide_Reports['Month In Number'] = Homicide_Reports['Month'].map(month_to_num)
Homicide_Reports['Month In Number'].unique()  #Checking the unique values before performing the operations

#Change the position of a column 'Month In String' next to 'Month' column.
new_column_position = ['Record ID', 'Agency Code', 'Agency Name', 'Agency Type', 'City',
       'State', 'Year', 'Month', 'Month In Number', 'Incident', 'Crime Type', 'Crime Solved',
       'Victim Sex', 'Victim Age', 'Victim Race', 'Victim Ethnicity',
       'Perpetrator Sex', 'Perpetrator Age', 'Perpetrator Race',
       'Perpetrator Ethnicity', 'Relationship', 'Weapon', 'Victim Count',
       'Perpetrator Count', 'Record Source']
Homicide_Reports = Homicide_Reports.reindex(columns = new_column_position)
#Checking if the position of 'Month In String' column changed.
Homicide_Reports.info()

#Now,
sns.set_style('darkgrid')
sns.catplot(data = Homicide_Reports, x = 'Crime Solved', order = ['Yes', 'No'], 
            col = 'Month', col_order= month_to_num.keys(), col_wrap= 3, 
            hue = 'Victim Sex', kind = 'count', palette = 'Accent',
            aspect = 2, height = 4, sharey = False, sharex = False)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#There are some people who are in the dataset, but it cannot be seen in the plot. Let's see what is going on.
Homicide_Reports[Homicide_Reports['Victim Sex'] == 'Unknown'] #There are 984 Unknown victims. Let's see how they fall in each month.

sns.catplot(data = Homicide_Reports[Homicide_Reports['Victim Sex'] == 'Unknown'],
            x = 'Crime Solved', order = ['Yes', 'No'], col = 'Month', col_order = month_to_num.keys(),
            col_wrap= 4, kind = 'count', palette = 'Accent', aspect = 1, height = 4, sharex = False, sharey = False)

#In every month from whole 34 years, it applear that when the victim sex is unknown, the rate of crime not being solved is higher.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let's see the 'Text tables' for the above solution
Homicide_Reports.groupby(['Month', 'Crime Solved', 'Victim Sex'])['Crime Solved'].count().sort_index(level = 0).head(20)

Homicide_Reports.groupby(['Month In Number', 'Crime Solved', 'Victim Sex'])[['Crime Solved']].count().head(20)

#Moving all the indexes in the column and storing them into 'df' variable.
df = Homicide_Reports.groupby(['Month', 'Crime Solved', 'Victim Sex'])[['Crime Solved']].count().rename(columns = {'Crime Solved': 'Total'}).reset_index()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Finding the max number of female murdered.
df[(df['Victim Sex'] == 'Female')]['Total'].max()

#Finding the month where those max number of female murdered and if there crime was solved. Note that this number for month of July is from whole 34 years.
df[(df['Total'] == 9798)]

#Finding the max number of male murdered.
df[df['Victim Sex'] == 'Male']['Total'].max()

#Finding the month where those max number of male murdered and if there crime was solved. Note that this number for month of July is from whole 34 years.
df[df['Total'] == 31639]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Using pairplt, lets pair the columns below with each other in the plot.
df = Homicide_Reports[['Record ID', 'Year', 'Incident', 'Victim Age', 'Victim Count', 'Perpetrator Count']]

sns.pairplot(df)
plt.title('Homicide Crimes During 1980-2014')
plt.show()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#let us the connection between Perpetrator Count and Victim Count
sns.scatterplot(data = Homicide_Reports, x = 'Victim Count', y = 'Perpetrator Count')

#This is suprising outcome. As the perpetrator decreases victim count decrease.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let us analyze the total crime solve/unsolved per year.
crime_solved_count = Homicide_Reports.groupby(['Year', 'Crime Solved'])[['Incident']].sum().reset_index()
crime_solved_count.info()
sns.scatterplot(data = crime_solved_count, x = 'Year', y = 'Incident', hue = 'Crime Solved')

#It looks like as the world enters to the advancement of new technology, there is higher chances of solving the crime.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Finding total incident per year.
plt.figure(figsize = (10, 8))
sns.barplot(data = Homicide_Reports, x = 'Year', y = 'Incident', estimator = sum)
plt.xticks(rotation = 45)
plt.title('Yearly Crime in US\n1980-2014')
plt.show()

'''
After 9/11 incident occured in 2001, we can see the soaring crime rate as compared to
those years before 1999. Also, as we can see that after the financial crisis that happened
in 2008, the crime rate sstarted increasing.
If we can see from 1991 to 1999, the crime rate was decreasing in good rate. It could be
because the country had a good financial stability or maybe there was an effective governing
bodies who applied strict rules to prevent such crimes.
'''
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let's find out the State Wide Crime rate.
Homicide_Reports[['State', 'Incident']]
order = Homicide_Reports.groupby('State')['Incident'].sum().sort_values(ascending = False).index

plt.figure(figsize = (10, 8))
sns.barplot(data = Homicide_Reports, x = 'State', y = 'Incident', estimator = sum, order = order) #If we don't use estimator = sum, then it will calculate 'mean' by default.
plt.xticks(rotation = 'vertical')
plt.title('State Wide Crime Rate\n1980-2014')
plt.show()

#Checking if the above plot is matching with the text table below.
Homicide_Reports.groupby('State')['Incident'].sum().sort_values(ascending = False)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Saving this cleaned dataframe to csv
Homicide_Reports.to_csv(r'/Users/romin/Library/Mobile Documents/com~apple~CloudDocs/Python/Python_Bootcamp_10-7-2020/Datasets/Homicide_CleanDataset.csv',
                        index = False)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






