import numpy as np
import pandas as pd

def copyAddresses(aciFname,qryFname):
    #set paths
    folder = "C:/Users/KEENEPLA/Downloads/"
    fileToRead = folder+aciFname
    fileToWrite = folder+qryFname

    #load files
    writeFile = pd.read_csv(fileToWrite)
    readFile = pd.read_csv(fileToRead)

    #get confirmation numbers to search
    search_criteria = writeFile.PayPalPaymentID

    #save column names for later
    writeColnames = writeFile.columns.values

    #clean the columns a little
    confNums = readFile[:,0]
    droprows = np.where(confNums==' ')[0]
    confNums = np.delete(confNums,droprows)
    confNums = [int(i[1:]) for i in confNums]
    confNums = np.asarray(confNums)
    readFile = readFile.drop(droprows)

    writeConf = writeFile[:,4]
    writeConf = np.asarray(writeConf)

    #convert to numpy
    readFile = readFile.to_numpy()
    writeFile = writeFile.to_numpy()
    #realized later that dataframes weren't working because of a stupid formatting issue
    #this works so I'm not going to fix it

    #loop through confirmation numbers and get address info
    for iID in search_criteria:
        wInd = np.where(writeConf==iID)[0]
        ind = np.where(confNums==iID)[0]
        add1 = readFile[ind,3]
        add2 = readFile[ind,4]
        city = readFile[ind,5]
        state = readFile[ind,6]
        zc = readFile[ind,7]
        #save to out file
        writeFile[wInd,11] = add1+add2
        writeFile[wInd,12] = state
        writeFile[wInd,13] = city
        writeFile[wInd,14] = zc

    #add the column names back in and write
    writedf = pd.DataFrame(writeFile,columns = writeColnames)
    writedf.to_csv(folder+"qryPermitFinancialTransactions_FY2023_depositsonline.csv")


def main():
    #take input from user for filenames
    print("enter custom aci report filename: ")
    aciFname = input()
    print("enter query filename: ")
    qryFname = input()
    copyAddress(aciFname,qryFname)

#driver
main()
