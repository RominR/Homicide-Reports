#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 08:47:51 2022

@author: rominrajbhandari
"""

#Let us first import the libraries that are required.

#standard libraries
import pandas as pd

#setting directory
import os
os.getcwd()
os.chdir('/Users/romin/Library/Datasets')

import mysql.connector as msql
#We cannot import the above library until it is installed. Use 'conda install -c anaconda mysql-connector-python' in Anaconda Terminal.

from mysql.connector import Error
#------------------------------------------------------------------------------------------------------------------------------------------------------

#Reading & importing the dataset
Homicide_Reports = pd.read_csv('HomicideReports.csv')
Homicide_Reports.info() #Checking the summary of the dataset
Homicide_Reports.iloc[0] #Chekcing the first row of the dataset.
#------------------------------------------------------------------------------------------------------------------------------------------------------

#Creating a connection object to connect to MySQL. The connect() constructor creates a connection to the MySQL and returns a MySQL Connection object.
try:
    conn = msql.connect(host = 'localhost', user = 'root', password = 'MyPassword')
                                       
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("Create DATABASE Homicide_Reports")
        print('Database is created')
except Error as e:
    print("Error while connecting to MySQL", e)
    
'''If gotten the following error message: then run this query in MySQL.:
    
"ALTER USER 'root'@'localhost' 
IDENTIFIED WITH mysql_native_password BY 'password;" 

#'root' is the my username and 'localhost' is just the localhost.

Authentication plugin 'caching_sha2_password' cannot be loaded: 
    dlopen(/opt/anaconda3/lib/plugin/caching_sha2_password.so, 0x0002): 
        tried: '/opt/anaconda3/lib/plugin/caching_sha2_password.so' (no such file),
        '/usr/local/lib/caching_sha2_password.so' (no such file),
        '/usr/lib/caching_sha2_password.so' (no such file)'''
#------------------------------------------------------------------------------------------------------------------------------------------------------
      
#Create a table under Homicide_Reports database and Import the CSV data into the MySQL table
#We will create an HomicideReports table under the Homicide_Reports database and insert the records in MySQL with below python code. 

try:
    conn = msql.connect(host = 'localhost', user = 'root', password = 'MyPassword', database = 'Homicide_Reports')   
    if conn.is_connected():
        cursor = conn.cursor()
        #url = https://www.tutorialspoint.com/python_data_access/python_mysql_cursor_object.htm
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS HomicideReports')
        print("Creating table...")
    #In the below line passing the create table statement which I want to create
        cursor.execute('''CREATE TABLE HomicideReports (Record_ID MEDIUMINT NOT NULL, Agency_Code VARCHAR(255) NOT NULL,
                       Agency_Name VARCHAR(255) NOT NULL, Agency_Type VARCHAR(255) NOT NULL, City VARCHAR(255) NOT NULL,
                       State VARCHAR(255) NOT NULL, Year SMALLINT NOT NULL, Month VARCHAR(255) NOT NULL,
                       Incident MEDIUMINT NOT NULL, Crime_Type VARCHAR(255) NOT NULL,
                       Crime_Solved VARCHAR(255) NOT NULL, Victim_Sex VARCHAR(255), Victim_Age MEDIUMINT NOT NULL,
                       Victim_Race VARCHAR(255), Victim_Ethnicity VARCHAR(255), Perpetrator_Sex VARCHAR(255) NOT NULL,
                       Perpetrator_Age MEDIUMINT, Perpetrator_Race VARCHAR(255), Perpetrator_Ethnicity VARCHAR(255),
                       Relationship VARCHAR(255), Weapon VARCHAR(255), Victim_Count TINYINT NOT NULL, Perpetrator_Count TINYINT NOT NULL,
                       Record_Source VARCHAR(255) NOT NULL, PRIMARY KEY(Record_ID))''')       
        print("Table is created.")
    #Loop through the dataframe.
        for i, row in Homicide_Reports.iterrows():
    #%s and %d is a placeholder. %d for integer values and %s for string values, %f for a floating point value, %b for binary data and %% just to insert a percent symbol.
    #url = https://stackoverflow.com/questions/20818155/not-all-parameters-were-used-in-the-sql-statement-python-mysql
            sql = '''INSERT INTO Homicide_Reports.HomicideReports
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'''
            cursor.execute(sql, tuple(row))
            print('Row Inserted')
    #The connection is not auto committed by default, so we must commit to save our changes.  It is used to commit the changes made to the table. Without using commit(), no changes will be made in the table.
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let us see if all the rows have been imported.
query1 = "SELECT COUNT(*) FROM Homicide_Reports.HomicideReports;"
cursor.execute(query1)
#Fetch all the records
result = cursor.fetchall()
result
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Query the table to make sure that our inserted data has been saved correctly.  

#Execute query
query2 = "SELECT * FROM Homicide_Reports.HomicideReports;"
cursor.execute(query2)

#Fetch all the records
result = cursor.fetchall()
result
for i in result:
    print(i)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#Let us solve some questions on Homicide_Reports.
#Insert few additional rows(values) in the database.
query3 = '''INSERT INTO Homicide_Reports.HomicideReports(Record_ID, Agency_Code, Agency_Name, 
Agency_Type, City, State, Year, Month, Incident, Crime_Type, Crime_Solved,
Victim_Sex, Victim_Age, Victim_Race, Victim_Ethnicity, Perpetrator_Sex, 
Perpetrator_Age, Perpetrator_Race, Perpetrator_Ethnicity, Relationship, Weapon,
Victim_Count, Perpetrator_Count, Record_Source)
VALUES(638455, 'MI83087', 'Detriot', 
'Municipal Police', 'Detroit', 'Michigan', 2002, 'August', 5, 'Murder or Manslaughter', 'Yes', 
'Female', 21, 'White', 'Not Hispanic', 'Male', 18, 'White', 'Hispanic', 'Friend', 'Handgun', 1, 2, 'FBI')'''
                                                           
cursor.execute(query3)
conn.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

query4 = '''INSERT INTO Homicide_Reports.HomicideReports VALUES(638456, 'MI83086', 'Detriot', 'Municipal Police',
'Detroit', 'Michigan', 2001, 'April' , 5, 'Murder or Manslaughter', 'No', 'Female', 21, 'White', 'Not Hispanic',
'Male', 18, 'White', 'Non Hispanic', 'Neighbor', 'Handgun', 2, 1, 'FBI')'''
cursor.execute(query4)
conn.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

query5 = '''INSERT INTO Homicide_Reports.HomicideReports(Record_ID, Agency_Code, Agency_Name, 
Agency_Type, City, State, Year, Month, Incident, Crime_Type, Crime_Solved,
Victim_Sex, Victim_Age, Victim_Race, Victim_Ethnicity, Perpetrator_Sex, 
Perpetrator_Race, Relationship, Weapon,
Victim_Count, Perpetrator_Count, Record_Source)
VALUES(638457, 'MI83089', 'Detriot', 
'Municipal Police', 'Detroit', 'Michigan', 2002, 'August' , 5, 'Murder or Manslaughter', 'Yes', 
'Female', 21, 'White', 'Not Hispanic', 'Male', 'White', 'Friend', 'Handgun', 1, 2, 'FBI')'''

cursor.execute(query5)
conn.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Let us make sure if the following row has been inserted.
Homicide_Reports[Homicide_Reports['Record_ID'] == 638459]



        
        
        
        
        
        
        
        
        
        
        








