# coding:utf-8

import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange # import lagrange function

# data import
data_path='data.csv'
data_import=pd.read_csv(data_path)
data=data_import

# process missing value
def ployinterp_column(s,n,k=3):
    # using lagrange function on interpolation
    # s: inputdata(column vector), n: the location(index) of paticular number, k: order of langrange func. 
    y=s[list(range(n-k,n))+list(range(n+1,n+1+k))] # choose the data you need to construct L-func. 
    y=y[y.notnull()] # eliminate the Nan data
    if k==1:
        result=sum(y)/len(y) # when k is equal to 1, this method is equal to the average method 
    else:
        temp=y.index-1
        y_index=y.index-(y.index-1)[1]  # to generate the 'x' to construct L-func. 
        result=lagrange(y_index,list(y))(k+1) # construct the L-func and get the estimator
    return result

# traverse it, find it and fix it
for i in data.columns:
	for j in range(len(data)):
		if (data[i].isnull())[j]:
			data[i][j]=ployinterp_column(data[i],j)

# test if there is missing data now
for i in data.columns:
	for j in range(len(data)):
		if (data[i].isnull())[j]:
			print 'OMG!'

data.to_csv('data_preprocessed.csv')

# draw the picture 
plt.plot(data.Num,data.Price)
plt.show()