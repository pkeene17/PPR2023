import numpy as np
import pandas as pd
from datetime import datetime as dt
from cleanAttendance import clean_DF
import dplython as dplyr
from functools import reduce

#helper to convert time strings to ints
def time_convert(times):
    for i in range(len(times)):
        tstmp = dt.strptime(str(times[i]),'%m/%d/%Y')
        times[i] = int(tstmp.strftime('%Y%m%d'))
    return times    

#load files
fileDir = 'C:/Users/KEENEPLA/Downloads/'
attendance = pd.read_csv(fileDir+'/programattendance.csv')
#schedule = pd.read_csv(fileDir+'programschedule.csv')
amenity = pd.read_csv(fileDir+'amenity.csv')
#fix that mess
#cap it at 20k because I dont feel like cleaning this whole dataset (multiple misformatted lines)
attendance = clean_DF(attendance[:][0:12000])

#make program filters
baskBool = attendance['Program']=='Basketball'
descBool = attendance['Description']=='Open Gym'
openBool = attendance['Program']=='Public / Open Programming'
progBool = np.logical_or(baskBool,openBool)
#convert dates to integers
times = attendance['AttendanceWeekDate'].copy()
times = time_convert(times)
attendance['AttendanceWeekDate'] = times
startSat = 20220903
endSat = 20230401
satList = np.arange(startSat,endSat,7)
sunList = satList+1
#make date range filter
satBool = [elem in satList for elem in attendance['AttendanceWeekDate']]
sunBool = [elem in sunList for elem in attendance['AttendanceWeekDate']]
dateBool = np.logical_or(satBool,sunBool)
#make facility filter
amenityGyms = amenity['AmenityType']=='Gymnasium'
facilityList = np.unique(amenity['Facility'][amenityGyms])
#preset boolean array
gymBool = np.squeeze(np.zeros((len(attendance),1),dtype=bool))
#loop through all unique facilities in amenities and add them to the bool array
for ifac in range(len(facilityList)):
    fac = facilityList[ifac]
    gymBool = np.logical_or(attendance['Facility']==fac,gymBool)
#combine and apply filters
index = np.logical_and(np.logical_and(np.logical_or(progBool,descBool),dateBool),gymBool)
attendance=attendance[index]
#do some maths
attendanceSum = attendance.groupby("ProgKey")['UniqueIndividualCount'].sum()
attendanceSum = attendanceSum.to_frame('Total # Participants')
attendanceMean = attendance.groupby("ProgKey")['UniqueIndividualCount'].mean()
attendanceMean = attendanceMean.to_frame('Mean # Participants')
attendanceMed = attendance.groupby("ProgKey")['UniqueIndividualCount'].median()
attendanceMed = attendanceMed.to_frame('Median # Participants')
attendanceMax = attendance.groupby("ProgKey")['UniqueIndividualCount'].max()
attendanceMax = attendanceMax.to_frame('Max # Participants')
attendanceMin = attendance.groupby("ProgKey")['UniqueIndividualCount'].min()
attendanceMin = attendanceMin.to_frame('Min # Participants')
#merge the arrays
mathsdf=reduce(lambda left,right: pd.merge(left,right,how='inner',on=['ProgKey']),
             [attendanceSum,attendanceMean,attendanceMed,attendanceMax,attendanceMin])
outdf = pd.merge(attendance.iloc[:,1:8].drop_duplicates(),mathsdf,how='inner',on='ProgKey')
#print to csv
outdf.to_csv(fileDir+'weekend program numbers 2022-2023.csv')
