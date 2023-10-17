#helper to clean up programattendance.csv

import numpy as np
import pandas as pd

def clean_DF(df,sep='   '):
    vect = df['Program'].copy()
    #make new columns
    df.insert(3,"Description",'nan',False)
    df.insert(4,"Staff",'nan',False)
    df.insert(5,"Gender",'nan',False)
    df.insert(6,"Age",'nan',False)
    df.insert(7,"ProgKey",'nan',False)
    for i in range(len(vect)):
        #split the string based on sep
        currStr = vect[i]
        currStr.replace('      ','   ')
        currStr.replace('    ','   ')
        splitStr = currStr.split(sep)
        #seperate age and unique id
        age = splitStr[4]
        tmp = age.replace('(','')
        cleanAge = tmp.replace(')','')
        justAge = cleanAge.split('#')[0]
        key = cleanAge.split('#')[1]
        #assign values to new columns
        df.iloc[i,3]=splitStr[1]
        df.iloc[i,4]=splitStr[2]
        df.iloc[i,5]=splitStr[3]
        df.iloc[i,6]=justAge
        df.iloc[i,2]=splitStr[0]
        df.iloc[i,7]=key
    return df
    
    
