import pandas as pd
import numpy as np
df = pd.read_csv('Book1.csv',sep=';')

conditions = [
    (df['MainIAActivityCode'] == '1.(c)'),
    (df['MainIAActivityCode'] == '1.(a)') | (df['MainIAActivityCode'] == '1.(b)'),
    (df['MainIAActivityCode'] == '2.(a)') | (df['MainIAActivityCode'] == '2.(b)' )|(df['MainIAActivityCode'] == '2.(c)') | (df['MainIAActivityCode'] == '2.(d)' )|(df['MainIAActivityCode'] == '2.(e)') | (df['MainIAActivityCode'] == '2.(f)'),
    (df['MainIAActivityCode'] == '3.(c)') | (df['MainIAActivityCode'] == '3.(g)'),
    (df['MainIAActivityCode'] == '5.(a)') | (df['MainIAActivityCode'] == '5.(b)') |(df['MainIAActivityCode'] == '5.(c)') | (df['MainIAActivityCode'] == '5.(d)' )|(df['MainIAActivityCode'] == '5.(e)') | (df['MainIAActivityCode'] == '5.(f)')| (df['MainIAActivityCode'] == '5.(g)'),
    (df['MainIAActivityCode'] == '6.(a)') | (df['MainIAActivityCode'] == '6.(b)' )|(df['MainIAActivityCode'] == '6.(c)'),
    (df['MainIAActivityCode'] == '4.(c)') | (df['MainIASubActivityName'] == 'Acids' ),
    ]

# create a list of the values we want to assign for each condition
values = ['Power plant(unspecified)', 'Refineries and steam cracker', 'Steel and Iron', 'Cement', 'Other','Pulp and Paper','Ammonia']
values2 = ["3-8%","3-13%","17-35%","14-33%","0","7-20%","100%"]
# create a new column and use np.select to assign values to it using our lists as arguments
df['Category'] = np.select(conditions, values)
df['Concentration'] = np.select(conditions, values2)
df.fillna(0, inplace=True)

for i in range(0,len(df.index)):
  #specify which power plant by looking in the columns "industrial category" and "industrial category (Niklas)"
  if df['Category'][i]=='Power plant(unspecified)':
      if ('NGCC' in str(df['industrial category'][i]))  | ('NGCC' in str(df['industrial category (Niklas)'][i])):
         df['Category'][i] = 'NGCC power plant'
         df['Concentration'][i] = "3-4%"
      if ('Coal' in str(df['industrial category'][i]))  | ('Coal' in str(df['industrial category (Niklas)'][i])):
         df['Category'][i] = 'Coal power plant'
         df['Concentration'][i] = "12-15%"
      if ('IGCC' in str(df['industrial category'][i]))  | ('IGCC' in str(df['industrial category (Niklas)'][i])):
         df['Category'][i] = 'IGCC power plant'
         df['Concentration'][i] = "40%"

  #if no catgory specified yet, then check if it is "Ethylene Oxide" or "Hydrogen plant"
  if df['Category'][i]=='0':
     if ('Ethylene' in str(df['industrial category'][i]))  | ('Ethylene' in str(df['industrial category (Niklas)'][i])):
         df['Category'][i] = 'Ethylene Oxide'
         df['Concentration'][i] = "100%"
     if ('Hydrogen' in str(df['industrial category'][i]))  | ('Hydrogen' in str(df['industrial category (Niklas)'][i])):
         df['Category'][i] = 'Hydrogen plant'
         df['Concentration'][i] = "100%"
     
# if no category yet assigned, then classify it as "other"
df['Category'] = df['Category'].replace('0','Other')
df['Concentration'] = df['Concentration'].replace('0',"n/a")
df.to_csv('output.csv',sep=';',index=False)
