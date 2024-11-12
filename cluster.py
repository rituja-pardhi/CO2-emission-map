import pandas as pd
from sklearn.cluster import DBSCAN

csv_name = 'output.csv'
clustered_csv_name = 'output_clustered.csv'

start_year = int(2007)
end_year = int(2017)

years = [str(i) for i in range(start_year,end_year+1)]
column_names = ['FacilityID','FacilityName', 'Lat', 'Long','Category','Concentration','cluster','height_07','height_08','height_09','height_10','height_11','height_12','height_13','height_14','height_15','height_16','height_17', *years] #column names for final csv file

df = pd.read_csv(csv_name, sep=';')

long = df.columns.get_loc('Long')
lat = df.columns.get_loc('Lat')
X = (df.iloc[:, [long,lat]].values)

X = X.astype(float)
cluster = DBSCAN(eps=0.1, min_samples=2).fit(X) #returns the clusters of facilities that are near to each other (-1 if the facility was not clustered with anything)

df['cluster'] = cluster.labels_ #store cluster number assigned to each facility

df1 = df[['FacilityID','Category','cluster']]
#create column to save the sum of all emissions for that cluster in year 2017 (can be assigned to the column 2017 and overwrite later for clustered facilities)
df['height_07']=df['2007']    
df['height_08']=df['2008']    
df['height_09']=df['2009']    
df['height_10']=df['2010']    
df['height_11']=df['2011']    
df['height_12']=df['2012']    
df['height_13']=df['2013']    
df['height_14']=df['2014']    
df['height_15']=df['2015']    
df['height_16']=df['2016']    
df['height_17']=df['2017']      
K={}
for i in range(0,max(df1['cluster'])+1):
    L = df1.index[df1['cluster']==i].tolist()

    categs = set(df1['Category'][L].tolist())
    if len(categs) >0 :
       K[i]=len(categs)                 #dictionary that stores the {cluster number,no. of unique categories in that cluster}

K = sorted(K.items(), key=lambda x: x[1], reverse=True) #sorted by no. of unique categories in that cluster in decending order

for i in K:
    L = df1.index[df1['cluster']==i[0]].tolist()
    categs = list(set(df1['Category'][L].tolist())) #list of all the unique categories in that cluster (i[0] returns the cluster number)
    df2 = df1.iloc[L,:] #new df containg only rows that are in the cluster numbered i[0]
    
    for c in categs:
        L2 = df2.index[df2['Category']==c].tolist() #L2 has index of all the facilities in that cluster with category c
        mean_long = df['Long'][L2].mean()
        mean_lat = df['Lat'][L2].mean()
        df['height_07'][L2]=int(df['2007'][L2].sum()) #update the value in col height_07 as the sum of all the emissions 
        df['height_08'][L2]=int(df['2008'][L2].sum())
        df['height_09'][L2]=int(df['2009'][L2].sum())
        df['height_10'][L2]=int(df['2010'][L2].sum())
        df['height_11'][L2]=int(df['2011'][L2].sum())
        df['height_12'][L2]=int(df['2012'][L2].sum())
        df['height_13'][L2]=int(df['2013'][L2].sum())
        df['height_14'][L2]=int(df['2014'][L2].sum())
        df['height_15'][L2]=int(df['2015'][L2].sum())
        df['height_16'][L2]=int(df['2016'][L2].sum())
        df['height_17'][L2]=int(df['2017'][L2].sum())
        means = [ mean_long, mean_lat ]         # mean of all the coordinates in that cluster with category c
    
    new_coord=[]

        #new_coord stores the new coordinate values 
        #new_coord stores 7 values (because the highest value of categs found 7)

    new_coord.append([means[0],means[1]])           
    new_coord.append([means[0],means[1]+0.07])  #0.08
    new_coord.append([means[0]+0.05,means[1]+0.035]) #0.05,0.04
    new_coord.append([means[0]-0.05,means[1]+0.035]) #0.05,0.04

    new_coord.append([means[0],means[1]-0.07])
    new_coord.append([means[0]+0.05,means[1]-0.035]) #0.05,0.04
    new_coord.append([means[0]-0.05,means[1]-0.035]) #0.05,0.04

        #update coordinate values in the dataset with new_coord
        #the actual number of categories in that cluster might be less than 7 (take first n with n as the lenth of unique categories)

    for c in range(0,len(categs)):
        L2 = df2.index[df2['Category']==categs[c]].tolist()
        df['Long'][L2] = new_coord[c][0]
        df['Lat'][L2] = new_coord[c][1]
  
    
#create the updated csv file
clustered_df = df.reindex(columns=column_names)
clustered_df.to_csv(clustered_csv_name, encoding='utf-8', sep=';', index=False)