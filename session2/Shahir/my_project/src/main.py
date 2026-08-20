import pandas as pd 
import matplotlib.pyplot as plt


df=pd.read_csv('env/crime_incidents_messy.csv')
plt.hist(df['latitude'])
plt.show()