import obspy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd

from mpl_toolkits.basemap import Basemap
from obspy.imaging.beachball import beach
from matplotlib import cm


def qplot(lat=None, lon=None, dep=None, mag = None, focal = None,
            ulat=None, ulon=None, llat=None, llon=None,  scale="local",
            min_dep = None, max_dep = None, topo = False, filename = None, minmag = None, maxmag = None
            ):
    """
    Earthquake (eq) Quick(q) plot the catalogue data in map.
    eqqplot(lat, lon, dep, mag, focal, scale, ulat, ulon, llat, llon)
    Required input:
    :lat (list): latitude of the earthquakes
    :lon (list): longitude of the earthquakes
    Optional input:
    :param ulat (float): upper right latitude of the map
    :param ulon (float): upper right longitude of the map
    :param llat (float): lower left latitude of the map
    :param llon (float): lower left longitude of the map
    dep (list): depth of the earthquakes
    mag (list): Mw of the earthquakes
    focal (list): focal mechanism of the earthquakes. From obspy documentation:
    Focal mechanism that is either number of mechanisms (NM) by 3
        (strike, dip, and rake) or NM x 6 (M11, M22, M33, M12, M13, M23 - the
        six independent components of the moment tensor, where the coordinate
        system is 1,2,3 = Up,South,East which equals r,theta,phi -
        Harvard/Global CMT convention). The relation to Aki and Richards
        x,y,z equals North,East,Down convention is as follows: Mrr=Mzz,
        Mtt=Mxx, Mpp=Myy, Mrt=Mxz, Mrp=-Myz, Mtp=-Mxy.
        The strike is of the first plane, clockwise relative to north.
        The dip is of the first plane, defined clockwise and perpendicular to
        strike, relative to horizontal such that 0 is horizontal and 90 is
        vertical. The rake is of the first focal plane solution. 90 moves the
        hanging wall up-dip (thrust), 0 moves it in the strike direction
        (left-lateral), -90 moves it down-dip (normal), and 180 moves it
        opposite to strike (right-lateral).

    Example:


    Coded by Nguyen Cong Nghia - IESAS 2017

    """

    fig = plt.figure(figsize=(15,15))
    ax = plt.gca()

#Convert all parameters to list:
    if type(lat) != list:
        lat = [lat]
        lon = [lon]

#Create the local when there is no limit
    if ulat == None:
        ulat = max(lat) + 3
    if ulon == None:
        ulon = max(lon) + 3
    if llat == None:
        llat = min(lat) - 3
    if llon == None:
        llon = min(lon) - 3

    ex_factor = np.sqrt((ulon - llon)**2 - (ulat - llat)**2)
    if ex_factor > 200:
        scale = "global"
#Number of events
    n = len(lat)

#Draw the basemap base on scale
    if scale == "global":
        min_marker_size = 1
        min_width = 100000
        m = Basemap(projection="robin", lat_0 = 0, lon_0 = 0, resolution ='c')
        m.drawparallels([-60,-30,0,30,60], labels = [True, False, True, False],zorder = 10)
        m.drawmeridians([-90,0,90], labels = [False, True, False, True],zorder = 10)
    elif scale == "local":
        min_marker_size = 1.5
        min_width = 120000
        m = Basemap(projection="merc", llcrnrlon= llon,llcrnrlat= llat, urcrnrlon= ulon, urcrnrlat=ulat, resolution ='i')
        m.drawparallels(np.arange(int(llat),int(ulat),np.ceil((ulat-llat)/5))+1, labels = [True, False, True, False],zorder = 10)
        m.drawmeridians(np.arange(int(llon),int(ulon),np.ceil((ulon-llon)/5))+1, labels = [False, True, False, True],zorder = 10)

#Include the topo
    if topo == True:
        m.etopo()
    else:
        m.fillcontinents(color='gray', zorder = 3)
        m.drawcoastlines(zorder = 4)

#Draw map boundary, continents, coastlines and countries
    m.drawmapboundary(zorder = 2)
    m.drawcountries(zorder = 5)

#Get earthquake color
    dep_r = [x for x in dep if isinstance(x, (int, float))]
    if min_dep == None:
        min_dep = min(dep_r)
        max_dep = max(dep_r)
    col = []
    for i in range(0, n):
        try:
            col.append(cm.jet(dep[i]/max_dep))
        except:
            col.append([0,0,0,1])

#Get earthquake size
    msize = []
    if mag is not None:
        if minmag is not None:
            minmag = min(mag)
        if maxmag is not None:
            maxmag = max(mag)

    for i in range(0, n):
        if mag == None:
            msize.append(min_marker_size)
        else:
            try:
                msize.append(((mag[i] - min(mag) + 1) * min_marker_size)*2)
            except:
                msize.append(min_marker_size*2)

#Draw the earthquake
    if focal is None:
        for i in range(0, n):
            x,y = m(lon[i], lat[i])
            m.plot(x, y, "o",color = col[i], zorder = 50, markersize = msize[i], markeredgecolor='black', markeredgewidth=0.01)

#Get the focal mechanism size
    if focal is not None:
        f_width = []
        for i in range(0, n):
            try:
                f_width.append((mag[i] - min(mag) + 1)*min_width)
            except:
                f_width.append(min_width)

#Draw the focal mechanism
    if focal is not None:
        x,y = m(lon, lat)
        for i in range(0, n):
            try:
                ball = beach(focal[i], xy=(x[i], y[i]), width=f_width[i], linewidth=1, facecolor = col[i])
                ax.add_collection(ball)
            except:
                pass

#Draw the point legend:
    if focal is None:

        EQmag1 = ((5 - min(mag) + 1) * min_marker_size)*2  # eq magnitude 5
        EQmag2 = ((6 - min(mag) + 1) * min_marker_size)*2  # eq magnitude 6
        EQmag3 = ((7 - min(mag) + 1) * min_marker_size)*2  # eq magnitude 7

        m.plot([], [], "bo", markersize = EQmag1 , label='Mw = 5')
        m.plot([], [], "bo", markersize = EQmag2 , label='Mw = 6')
        m.plot([], [], "bo", markersize = EQmag3 , label='Mw = 7')
        plt.legend()

#Draw the focal mechanism legend
    if focal is not None:
        pass


#Draw the color bar
    if scale == 'global':
        ax1 = fig.add_axes([0.15, 0.25, 0.7, 0.01])
    else:
        ax1 = fig.add_axes([0.15, 0.10, 0.7, 0.01])
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=min_dep, vmax=max_dep)
    cb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')
    cb.set_label("Depth (km)")

#Save the map
    if filename is not None:
        plt.savefig(filename, dpi = 200, bbox_inches = "tight")
    else:
        plt.show()


def cinput(inp):
    df = pd.read_csv(inp, delimiter=' *; *', engine='python')
    lon = list(df['LONGITUDE'])
    lat = list(df['LATITUDE'])
    dep = list(df['DEPTH'])
    mag = list(df['MAG'])
    if 'Str1' in df.columns:
        focal = list(df[['Str1','Dip1','Rake1']].values)
        return lon, lat, dep, mag, focal
    else:
        focal = None
        return lon, lat, dep, mag, focal

def eqqplot(cata, pic):
    lon, lat, dep, mag, focal = cinput(cata)
    qplot(lon = lon, lat = lat, dep = dep, mag = mag, focal = focal, filename = pic)

