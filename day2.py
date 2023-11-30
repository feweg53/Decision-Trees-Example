from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
from utils import informationFunctions as infFunc
# from utils import getEntropy


baseDir = 'c:/development/dod/'
fname = 'sample.xlsx'

def attachDummies(df,col,retainColsIfMoreThanTwo=True):
    '''
    Takes in a pandas dataframe and returns
    a dataframe with the passed in column
    converted to a binary column for the unique values.
    If the unique values is 2, then one of the columns
    is dropped.
    '''
    uniqueVals = df[col].unique() #save a list of the unique values from passed in column
    df2 = pd.get_dummies(df[col], dtype=int)

    if len(uniqueVals) == 2: #if there are only 2 unique values, then we will append only one column to the dataframe
        colToAdd = uniqueVals[0]
        df = pd.concat((df,df2[colToAdd]),axis=1)
        colToAdd = [colToAdd]
    elif len(uniqueVals) > 2 and not retainColsIfMoreThanTwo:
        colToAdd = uniqueVals[1:]
        df = pd.concat((df,df2[colToAdd]),axis=1)
    df.drop(col,axis=1,inplace=True)
    
    for addedCol in colToAdd:
        print(addedCol,'should be renamed to',col)
        df.rename(columns={addedCol:f"{col}_{addedCol}"},inplace=True)
    return df

data = pd.read_excel(f'{baseDir}{fname}')

ycol = 'Target'


# allcols = data.columns
# for col in allcols:
#     if col == ycol:
#         continue
#     data = attachDummies(data,col)

for col in data.columns:
    if col != ycol:
        infoGain = infFunc.getInformationGain(data,col,ycol)
        print(col,'infogain is',infoGain)

# # cols = data.columns

# # for _,row in data.iterrows():
# #     for col in cols:
# #         print(row[col],end='\t')
# #     print()


# # xcols = ['Head','Body','Color']
# # ycol = 'Target'
# xcols = []
# for col in data.columns:
#     xcols.append(col)

# data.to_excel(f"{baseDir}/output/remapped_data.xlsx")

# X, y = data[xcols], data[ycol]
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, y)
# # isPlot = tree.plot_tree(clf)

# plt.figure()
# tree.plot_tree(clf,filled=True)  
# plt.savefig(f'{baseDir}/output/tree.png',bbox_inches = "tight")