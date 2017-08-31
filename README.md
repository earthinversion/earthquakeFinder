# Earthquake Finder
Author: _Utpal Kumar_

Contributor: _Nguyễn Công Nghĩa_

This program can be used to obtain the earthquake information from various sources. The user can search for any event for given time range, magnitude range, depth range, geographical area. It can also obtain the focal mechanism solutions for the given parameters. It gives the output file (catalog.txt by default) where all the information is stored. It also plots the output (both with the focal mechanism and without it.)
This program makes use of the __obspy__ module of __Python__ and retrieve data from the [International Seismological Center (ISC) server](http://www.isc.ac.uk/iscbulletin/search/catalogue/)

## Examples:
### To run with default parameters
`python3 earthquakeFinder.py`

### To obtain the earthquake info between today, March 2016 to the current time
`python3 earthquakeFinder.py st=2016/3`

### To obtain the earthquake info between 2016, march, 29 to 2016, september, 22
`python3 earthquakeFinder.py st=2016/3/29,et=2016/9/22`

### To obtain the catalog for magnitudes between 4-9 and with focal mechanism
`python3 earthquakeFinder.py mxmag=9,mnmag=4,fm=yes`

### To obtain catalog for magnitude 4-7, and within radius of 10 (default) and central coordinates 22(lat),121(lon) with focal mechanism
`python3 earthquakeFinder.py mxmag=7,mnmag=4,clat=22,clon=121,mxrad=80,fm=yes`

### Parameters to change (default values in the braces):
mnla(-90),mxla(90),mnlo(-180),mxlo(180),mndep(0),mxdep(700),mnmag(4),mxmag(10),mnrad(0),mxrad(10),clat(None),clon(None),st(-1 month),et (current time),fm(no)

### Output format of the catalog
Without Focal Mechanism -> "_YEAR_ _MONTH_ _DAY_ _HOUR_ _MINUTES_ _SECONDS_ _LONGITUDE_ (in deg) _LATITUDE_(in deg) _DEPTH_(in km) _MAG_TYPE_ _MAG_ _EVENT_NAME_."

With Focal Mechanism -> "_YEAR_ _MONTH_ _DAY_ _HOUR_ _MIN_ _SEC_ _LONGITUDE_ _LATITUDE_ _DEPTH_ _EXP_(Nm) _M0_ _MAG_ _Mrr_ _Mtt_ _Mpp_ _Mrt_ _Mtp_ _Mpr_ _Str1_ _Dip1_ _Rake1_ _Str2_ _Dip2_ _Rake2_."

### Requirements
1. Python 3: Can be obtained from [here.](https://www.python.org/downloads/)
2. Extra Modules
    (a) requests: `pip install requests`
    (b) pandas: `pip install pandas`
    (c) obspy: `pip install obspy`



