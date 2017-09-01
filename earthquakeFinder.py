from __future__ import print_function
import requests
import os
import pandas as pd
import numpy as np
import datetime
import sys
import csv
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import warnings
'''
This program is handy for downloading the earthquake informations and catalog for given input.
If the user call the program without any input then it will run for the default parameters.
Default Parameters:
ending time(et): 6 months from now
starting time(st): current time
Minimum Latitude =-90
Maximum Latitude =90
Minimum Longitude =-180
Maximum Longitude =180
Minimum Depth =0
Maximum Depth =700
Minimum Magnitude =4
Maximum Magnitude =10
fm=no #No focal mechanism, if you want add fm=yes
# How to run the program:


# Examples:
## to run with default parameters
python3 earthquakeFinder.py

## to obtain the earthquake info between 2016, march, today's date to current time
python3 earthquakeFinder.py st=2016/3

## to obtain the earthquake info between 2016, march, 29 to 2016, september, 22
python3 earthquakeFinder.py st=2016/3/29,et=2016/9/22

## to obtain the catalog for magnitudes between 4-9 and with focal mechanism
python3 earthquakeFinder.py mxmag=9,mnmag=4,fm=yes

## to obtain catalog for magnitude 4-7, and within radius of 10 (default) and central coordinates 22(lat),121(lon) with focal mechanism
python3 earthquakeFinder.py mxmag=7,mnmag=4,clat=22,clon=121,mxrad=80,fm=yes

Parameters to change (default values in the braces):
mnla(-90),mxla(90),mnlo(-180),mxlo(180),mndep(0),mxdep(700),mnmag(4),mxmag(10),mnrad(0),mxrad(10),clat(None),clon(None),st(-1 month),et (current time),fm(no)
-Utpal Kumar
'''
###########################################################################################
warnings.filterwarnings("ignore")
sug='''Parameters to change (default values in the braces):
mnla(-90),mxla(90),mnlo(-180),mxlo(180),mndep(0),mxdep(700),mnmag(4),mxmag(10),mnrad(0),mxrad(10),clat(None),clon(None),st(-1 month),et (current time),fm(no)\n'''
print(sug)

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)
###########################################################################################
def num_events(out):
    with open(out) as f:
        for i, l in enumerate(f):
            pass
    return i
###########################################################################################

out = 'catalog.txt'

#Time input
now=datetime.datetime.utcnow()
before=monthdelta(now,-1)

startT=before
endT=now
#starting time values
stv=[startT.year,startT.month,startT.day,startT.hour,startT.minute,startT.second]
etv=[endT.year,endT.month,endT.day,endT.hour,endT.minute,endT.second]
# For rectangular search
mnlat = "-90"
mxlat = "90"
mnlon = "-180"
mxlon = "180"

# For circular search
minrad ="0"
maxrad="10"
clat=""
clon=""
# Depths
mnD = "0"
mxD = "700"

# magnitudes
mnM = "4"
mxM = "10"

#focal mechanism solution
fm="no"
###########################################################################################
#Reading the user inputs
th=1
try:
    if len(sys.argv)>th:
        userInput=sys.argv[th].split(",")
        for item in userInput:
            itmkey=item.split("=")[0]
            itmval=item.split("=")[1]
            if itmkey=="mnla":
                mnlat=itmval
            elif itmkey=="mxla":
                mxlat=itmval
            elif itmkey=="mnlo":
                mnlon=itmval
            elif itmkey=="mxlo":
                mxlon=itmval
            elif itmkey=="mndep":
                mnD=itmval
            elif itmkey=="mxdep":
                mxD=itmval
            elif itmkey=="mnmag":
                mnM=itmval
            elif itmkey=="mxmag":
                mxM=itmval
            elif itmkey=="mxrad":
                maxrad=itmval
            elif itmkey=="mnrad":
                minrad=itmval
            elif itmkey=="clat":
                clat=itmval
            elif itmkey=="clon":
                clon=itmval
            elif itmkey=="st":
                nw=itmval.split("/")
                stv[0:len(nw)]=itmval.split("/")
            elif itmkey=="et":
                ett=itmval.split("/")
                etv[0:len(ett)]=itmval.split("/")
            elif itmkey=="fm":
                fm=itmval
                print("Obtaining Focal Mechanism")
            elif itmkey=="outfile":
                out=itmval
                print("Output catalog file is {}".format(out))
    # makes the values lesser than 10, 2-digit
    for i in np.arange(len(stv)):
        if int(stv[i]) < 10:
            stv[i] = "%02d" % int(stv[i])
        if int(etv[i]) < 10:
            etv[i] = "%02d" % int(etv[i])
except:
    print("ERROR: Please enter the proper format!\n")
###########################################################################################


print("Start time: {}/{}/{}/{}/{}/{}".format(stv[0],stv[1],stv[2],stv[3],stv[4],stv[5]))
print("End time: {}/{}/{}/{}/{}/{}".format(etv[0],etv[1],etv[2],etv[3],etv[4],etv[5]))
if clat and clon:
    print("\nSearching for circular region:")
    print("Min radius= {}".format(float(minrad)))
    print("Max radius= {}".format(float(maxrad)))
    print("Central latitude= {}".format(float(clat)))
    print("Central longitude= {}".format(float(clon)))
else:
    print("\nSearching for rectangular region:")
    print("Min latitude= {}".format(float(mnlat)))
    print("Max latitude= {}".format(float(mxlat)))
    print("Min longitude= {}".format(float(mnlon)))
    print("Max longitude= {}\n".format(float(mxlon)))
print("Min depth= {}".format(mnD))
print("Max depth= {}".format(mxD))
print("Min magnitude= {}".format(mnM))
print("Max magnitude= {}\n".format(mxM))

if os.path.exists(out):
    os.remove(out)
###########################################################################################
def catalogDownloader(yearS=int(stv[0]), monthS=int(stv[1]), dayS=int(stv[2]), hourS=int(stv[3]), minuteS=int(stv[4]), secondS=float(stv[5]), yearE=int(etv[0]), monthE=int(etv[1]), dayE=int(etv[2]), hourE=int(etv[3]), minuteE=int(etv[4]),secondE=float(etv[5]),minlat=mnlat, maxlat=mxlat, minlon=mnlon, maxlon=mxlon,clat=clat,clon=clon,minrad=minrad,maxrad=maxrad, minD=float(mnD)*1000, maxD=float(mxD)*1000, minM=float(mnM), maxM=float(mxM)):
    if clat and clon:
        minlat=None
        maxlat=None
        minlon=None
        maxlon=None
        minrad=int(minrad)
        clat=float(clat)
        clon=float(clon)
        maxrad=int(maxrad)
    else:
        minlat=float(minlat)
        maxlat=float(maxlat)
        minlon=float(minlon)
        maxlon=float(maxlon)
        minrad=None
        clat=None
        clon=None
        maxrad=None
    try:
        tt1=UTCDateTime("{}-{}-{}T{}:{}:{}".format(yearS,monthS,int(dayS),hourS,minuteS,secondS))
        tt2=UTCDateTime("{}-{}-{}T{}:{}:{}".format(yearE,monthE,int(dayE),hourE,minuteE,secondE))
        client = Client("IRIS")
        catalog = client.get_events(starttime=tt1, endtime=tt2,minlatitude=minlat,maxlatitude=maxlat, minlongitude=minlon, maxlongitude=maxlon, latitude=clat, longitude=clon, minradius=minrad, maxradius=maxrad, mindepth=minD, maxdepth=maxD, minmagnitude=minM, maxmagnitude=maxM)
        eventinfo = [[] for i in range(len(catalog))]

        for i in np.arange(len(catalog)):
            arr = eventinfo[i]
            event = catalog[i]
            arr.append(event.origins[0]["time"].year)
            arr.append(event.origins[0]["time"].month)
            arr.append(event.origins[0]["time"].day)
            arr.append(event.origins[0]["time"].hour)
            arr.append(event.origins[0]["time"].minute)
            arr.append(event.origins[0]["time"].second)
            arr.append(event.origins[0]["longitude"])
            arr.append(event.origins[0]["latitude"])
            arr.append(event.origins[0]["depth"])
            arr.append(event.magnitudes[0]["magnitude_type"])
            arr.append(event.magnitudes[0]["mag"])
            arr.append(event.event_descriptions[0].text)
        # print(eventinfo)
        outcatalog = "catalog.txt"
        frmt = "YEAR;MONTH;DAY;HOUR;MINUTES;SECONDS;LONGITUDE;LATITUDE;DEPTH;MAG_TYPE;MAG;EVENT_NAME\n"
        with open(outcatalog, 'w') as file:
            file.write(frmt)
            for i in range(len(eventinfo)):
                out = "{:4d};{:2d};{:2d};{:2d};{:2d};{:5.2f};{:9.4f};{:9.4f};{:5.1f};{:5s};{:3.1f};{}".format(int(eventinfo[i][0]), int(eventinfo[i][1]), int(eventinfo[i][2]), int(eventinfo[i][3]), int(eventinfo[i][4]), float(eventinfo[i][5]), float(eventinfo[i][6]), float(eventinfo[i][7]), float(eventinfo[i][8]) / 1000, str(eventinfo[i][9]), float(eventinfo[i][10]), str(eventinfo[i][11]))
                # print(out)
                file.write(out + "\n")
    except:
        print("Failed to fetch the data! Try some other parameters")
###########################################################################################
def catalogDownloaderISC(yearS=stv[0], monthS=stv[1], dayS=stv[2], hourS=stv[3], minuteS=stv[4], secondS=stv[5], yearE=etv[0], monthE=etv[1], dayE=etv[2], hourE=etv[3], minuteE=etv[4],secondE=etv[5],minlat=mnlat, maxlat=mxlat, minlon=mnlon, maxlon=mxlon, minD=mnD, maxD=mxD, minM=mnM, maxM=mxM,maxrad=maxrad,clat=clat,clon=clon, outfile=out):
    if clat and clon:
        minlat=""
        maxlat=""
        minlon=""
        maxlon=""
        clat=int(clat)
        clon=int(clon)
        maxrad=int(maxrad)
        url2 = "searchshape=CIRC&"
    else:
        minlat=float(minlat)
        maxlat=float(maxlat)
        minlon=float(minlon)
        maxlon=float(maxlon)
        minrad=""
        clat=""
        clon=""
        maxrad=""
        url2 = "searchshape=RECT&"
    url1 = "http://isc-mirror.iris.washington.edu/cgi-bin/web-db-v4?request=COMPREHENSIVE&out_format=FMCSV&"
    # url2 = "searchshape=RECT&"
    url3 = "bot_lat={}&top_lat={}&left_lon={}&right_lon={}&".format(minlat, maxlat, minlon, maxlon)
    url4 = "ctr_lat={}&ctr_lon={}&radius={}&max_dist_units=deg&srn=&grn=&".format(clat,clon,maxrad)
    url5 = "start_year={}&start_month={}&start_day={}&start_time={}%3A{}%3A{}&end_year={}&end_month={}&end_day={}&end_time={}%3A{}%3A{}&".format(yearS, monthS, dayS, hourS, minuteS, secondS, yearE, monthE, dayE, hourE, minuteE, secondE)
    url6 = "min_dep={}&max_dep={}&min_mag={}&max_mag={}&req_mag_type=&req_mag_agcy=&include_links=off".format(minD, maxD, minM, maxM)

    url = url1 + url2 + url3 + url4 + url5 + url6
    temp1 = "temp1.tmp"
    temp2 = "temp2.tmp"
    r = requests.get(url)
    with open(temp1, "wb") as file:
        file.write(r.content)

    with open(temp1, 'r') as fin:
        data = fin.read().splitlines(True)
        if not "No events were found.\n" in data:
            with open(temp2, 'w') as fout:
                fout.writelines(data[27:-5])
                forward="go"
        else:
            sys.exit("No events Found!")
    df = pd.read_csv(temp2, header=None)
    df = df.replace(r'\s+$', np.nan, regex=True)  # replace all the empty strings with NaN
    df.dropna(subset=[[2, 3, 4, 5, 6, 9, 10, 11, 13]], inplace=True)  # remove all the rows containing NaN
    eventinfo = []
    eventinfo.append(list(df.iloc[:, 2].str.split("-").str[0]))
    eventinfo.append(list(df.iloc[:, 2].str.split("-").str[1]))
    eventinfo.append(list(df.iloc[:, 2].str.split("-").str[2]))
    eventinfo.append(list(df.iloc[:, 3].str.split(":").str[0]))
    eventinfo.append(list(df.iloc[:, 3].str.split(":").str[1]))
    eventinfo.append(list(df.iloc[:, 3].str.split(":").str[2]))
    dataindx = [5, 4, 6, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    for idx in dataindx:
        eventinfo.append(list(df.iloc[:, idx]))

    frmt = "YEAR; MONTH; DAY; HOUR; MIN; SEC; LONGITUDE; LATITUDE; DEPTH; EXP(Nm); M0; MAG; Mrr; Mtt; Mpp; Mrt; Mtp; Mpr; Str1; Dip1; Rake1; Str2; Dip2; Rake2\n"
    with open(outfile, 'w') as file:
        file.write(frmt)
        for x in zip(*eventinfo):
            file.write("{:4d};{:2d};{:2d};{:2d};{:2d};{:5.2f};{:9.4f};{:9.4f};{:5.1f};{:2d};{:5.3f};{:3.1f};{:6.3f};{:6.3f};{:6.3f};{:6.3f};{:6.3f};{:6.3f};{: 7.2f};{:5.2f};{:7.2f};{:7.2f};{:5.2f};{:7.2f}\n".format(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), float(x[5]), float(x[6]), float(x[7]), float(x[8]), int(x[9]), float(x[10]), float(x[11]), float(x[12]), float(x[13]), float(x[14]), float(x[15]), float(x[16]), float(x[17]), float(x[18]), float(x[19]), float(x[20]), float(x[21]), float(x[22]), float(x[23])))
    tmpfiles = ["temp1.tmp","temp2.tmp"]
    for x in tmpfiles:
        os.remove(x)
###########################################################################################
def EQFinder(yearS=stv[0], monthS=stv[1], dayS=stv[2], hourS=stv[3], minuteS=stv[4], secondS=stv[5], yearE=etv[0], monthE=etv[1], dayE=etv[2], hourE=etv[3], minuteE=etv[4],secondE=etv[5],minlat=mnlat, maxlat=mxlat, minlon=mnlon, maxlon=mxlon, minD=mnD, maxD=mxD, minM=mnM, maxM=mxM,clat=clat,clon=clon,maxrad=maxrad,minrad=minrad, outfile=out):
    if fm=="yes":
        try:
            catalogDownloaderISC(yearS=yearS, monthS=monthS, dayS=dayS, hourS=hourS, minuteS=minuteS, secondS=secondS, yearE=yearE, monthE=monthE, dayE=dayE, hourE=hourE, minuteE=minuteE,secondE=secondE,minlat=minlat, maxlat=maxlat, minlon=minlon, maxlon=maxlon,clat=clat,clon=clon,maxrad=maxrad, minD=minD, maxD=maxD, minM=minM, maxM=maxM, outfile=outfile)
        except:
            print("Unable to fetch the data from ISC")
            catalogDownloader(yearS=int(yearS), monthS=int(monthS), dayS=int(dayS), hourS=int(hourS), minuteS=int(minuteS), secondS=float(secondS), yearE=int(yearE), monthE=int(monthE), dayE=int(dayE), hourE=int(hourE), minuteE=int(minuteE),secondE=float(secondE),minlat=minlat, maxlat=maxlat, minlon=minlon, maxlon=maxlon,clat=clat,clon=clon,minrad=minrad,maxrad=maxrad, minD=float(minD), maxD=float(maxD), minM=float(minM), maxM=float(maxM))
    else:
        catalogDownloader(yearS=int(yearS), monthS=int(monthS), dayS=int(dayS), hourS=int(hourS), minuteS=int(minuteS), secondS=float(secondS), yearE=int(yearE), monthE=int(monthE), dayE=int(dayE), hourE=int(hourE), minuteE=int(minuteE),secondE=float(secondE),minlat=minlat, maxlat=maxlat, minlon=minlon, maxlon=maxlon,clat=clat,clon=clon,minrad=minrad,maxrad=maxrad, minD=float(minD), maxD=float(maxD), minM=float(minM), maxM=float(maxM))
##########################################################################################
if __name__=="__main__":
    EQFinder()
    if os.path.exists(out):
        num=num_events(out)
        print("Number of events found: {}".format(num))
        if 1<=num<15000:
            print("Plotting events...please wait...")
            import cat_plot
            fignm="EQmap.png"
            cat_plot.eqqplot(out, fignm)

