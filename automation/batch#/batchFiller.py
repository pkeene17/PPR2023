#associate batch numbers with merchantID and payment amount

import numpy as np
import pandas as pd
from datetime import datetime as dt

#helper to covert the money columns into floats
def money_convert(vect):
    for i in range(len(vect)):
        tmp = vect[i]
        tmp = tmp.replace('$','')
        tmp = tmp.replace(',','')
        tmp = tmp.replace(' ','')
        tmp = tmp.replace('(','')
        tmp = tmp.replace(')','')
        vect[i] = float(tmp)
    return vect

#helper to convert account names into reference numbers
def ref_num_convert(accountStr):
    if accountStr == ' MasterCard':
        out = 40084550
    elif accountStr == ' Visa':
        out = 40084550
    elif accountStr == ' Discover':
        out = 40084550
    elif accountStr == ' American Express':
        out = 4377928767
    else:
        out = 0
    return out

#helper to loop through a vector and convert account names
def convert_loop(accType):
    for i in range(len(accType)):
        accType[i] = ref_num_convert(accType[i])
    return accType

#helper to convert dates-readFile
def time_convertRF(times):
    for i in range(len(times)):
        tstmp = dt.strptime(times[i][1:11],'%m/%d/%Y')
        times[i] = tstmp.strftime('%Y%m%d')
    return times

#helper to convert dates-writeFile
def time_convertWF(times):
    for i in range(len(times)):
        tstmp = dt.strptime(times[i],'%m/%d/%Y')
        times[i] = tstmp.strftime('%Y%m%d')
    return times

def fill_batch(aciFname,qryFname):
    #load data
    folder = "C:/Users/KEENEPLA/Downloads/"
    readFname = aciFname
    writeFname = qryFname
    readFile = pd.read_csv(folder+readFname)
    writeFile = pd.read_csv(folder+writeFname)

    #convert dates to integers
    timesRF = readFile[' Transaction Date & Time'].copy()
    timesRF = time_convertRF(timesRF)
    readFile[' Transaction Date & Time'] = timesRF
    timesWF = writeFile['Posting Date'].copy()
    timesRF = time_convertWF(timesWF)
    writeFile['Posting Date'] = timesWF

    #get date range from the aci report
    #aci reports are organized by date
    dateStart = readFile[' Transaction Date & Time'][0]
    dateEnd = readFile[' Transaction Date & Time'][np.shape(readFile)[0]-1]
    dateIndex = np.logical_and(writeFile['Posting Date']<=dateEnd,writeFile['Posting Date']>=dateStart)

    #get list of batch numbers
    batchList = np.unique(readFile[' Batch #'])
    #convert the account types to their ref numbers
    accType = readFile[' Account Type'].copy()
    accType = convert_loop(accType)
    readFile[' Account Type'] = accType

    #cast some columns as floats
    writeMoney = writeFile[' Amount'].copy()
    writeMoney = money_convert(writeMoney)
    writeFile[' Amount'] = writeMoney
    readMoney = readFile[' Base Payment Amount'].copy()
    readMoney = money_convert(readMoney)
    readFile[' Base Payment Amount'] = readMoney

    #loop through batches
    for ibatch in batchList:
        #index rows for this batch
        batchRows = readFile[readFile[' Batch #']==ibatch]
        #get the date of this batch
        batchDate = np.unique(batchRows[' Settlement Date'])
        #throw an error if more than one date is associated with a batch
        if len(batchDate) != 1:
            print(batchDate)
            raise Exception("Invalid Number of Dates Found: Program Terminated")
        #get the merchant IDs in this batch
        merchants = np.unique(batchRows[' Account Type'])
        #loop through merchant IDs and sum the payments
        for imerch in merchants:
            #index rows in this batch that match this merchant ID
            ind = batchRows[' Account Type']==imerch
            #sum payments from this merchant
            paidAmt = np.sum(batchRows[' Base Payment Amount'][ind])
            #search for row with merchant ID and the exact amount and a blank batch field in write file
            indextmp1 = np.logical_and(writeFile[' Customer Reference']==imerch,writeFile[' Amount']==paidAmt)
            #search within date range
            indextmp2 = np.logical_and(dateIndex,indextmp1)
            index = np.logical_and(indextmp2,writeFile['Batch Number'].isna())        
            #only write data if one match is found; otherwise leave blank
            if np.sum(index)==1:
                #gotta break this into steps or pandas freaks out
                #which is an objectively funny image if you think about it
                tmp = writeFile['Batch Number'].copy()
                tmp[index] = ibatch
                tmpdate = writeFile['Settlement Date'].copy()
                tmpdate[index] = batchDate
                writeFile['Batch Number'] = tmp
                writeFile['Settlement Date'] = tmpdate

    writeFile.to_csv(folder+"Online Payment Logs_batched.csv")
        
def main():
    #take input for filenames
    print("enter custom aci report filename: ")
    aciFname = str(input())
    print("enter data to be filled's filename: ")
    qryFname = str(input())
    fill_batch(aciFname,qryFname)

#driver
main()



