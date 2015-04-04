import datetime
from obspy.fdsn import Client
import io_utils
import numpy as np
from collections import defaultdict
import pandas as pd

#data_dir = 'data/parkfield_sub'
#data_dir = 'data/parkfield/2002_reloc_sub123/'
data_dir = '../../kpick/data/parkfield/reloc/2002Events_reloc'
hs,zs = io_utils.read_sac_dir(data_dir, readZ = True)

lat = 36.003368
lon = -120.56023
minlat = lat - 1
maxlat = lat + 1
minlon = lon - 1
maxlon = lon + 1

client = Client("NCEDC")
times = []
times_evid = {}
for tr in zs:
    times.append(tr.stats.starttime)
    times_evid[str(tr.stats.starttime)] = tr.stats.evid
times = np.unique(times)
starttime = sorted(times)[0]
endtime = sorted(times)[-1]


#def second_difference(timea,timeb):
#    dtime = timea.datetime - timeb.datetime
#    return dtime.seconds
#
#def events_near_time(time):
#    start = time.datetime - datetime.timedelta(minutes = 1) 
#    end   = time.datetime + datetime.timedelta(minutes = 1) 
#    try:
#        events = client.get_events(starttime=start, endtime=end,\
#            minlatitude  = minlat, maxlatitude  = maxlat,\
#            minlongitude = minlon, maxlongitude = maxlon)
#        return events
#    except:
#        print "Couldn't get data for {}".format(time)
#        return None
#
#
#
#def get_event(time):
#    e = events_near_time(time)
#    if not e:
#        return None
#    if len(e) > 1:
#        print "Time {} has multiple events associated with it!".format(time)
#    e = e[0]
#    # origins
#    origins   = e.origins[0]
#    etime     = origins.time
#    depth     = origins.depth
#    latitude  = origins.latitude
#    longitude = origins.longitude
#    # magnitude
#    try:
#        mag = e.magnitudes[0].mag
#    except:
#        mag = e.magnitudes
#    dtime = second_difference(etime,time)
#    return [dtime,[etime,latitude,longitude,depth,mag]]

def query_events(start,stop):
    start = start.datetime
    stop  = stop.datetime
    events = client.get_events(starttime=start, endtime=stop,\
        minlatitude  = minlat, maxlatitude  = maxlat,\
        minlongitude = minlon, maxlongitude = maxlon)
    return events


def event_data(e):
    """ Parse event and get nearest event data """
    origins   = e.origins[0]
    etime     = origins.time
    depth     = origins.depth
    latitude  = origins.latitude
    longitude = origins.longitude
    try:
        mag = e.magnitudes[0].mag
    except:
        mag = e.magnitudes
    return [etime,latitude,longitude,depth,mag]

def find_nearest_event(time,all_events):
    """ Find nearest event in all_events to time """
    dist_to_time = []
    dt_time = time.datetime
    for e in all_events: 
        otime = e.origins[0].time.datetime
        dtime = dt_time - otime
        dist_to_time.append(abs(dtime.total_seconds()))
    nearest_event = all_events[np.argmin(dist_to_time)]
    return [min(dist_to_time),event_data(nearest_event)]

def find_associated_events(times):
    associated_events = []
    for time in times:
        event_dist, nearest_event = find_nearest_event(time,all_events)
        if event_dist < 60:
            associated_events.append([time,event_dist,nearest_event])
        else:
            associated_events.append([time,None,None])
    return associated_events
            

all_events = query_events(min(times),max(times))
assoc_events = find_associated_events(times)

#a=times[0].datetime
#b=times[9].datetime
#
#raw_input('got here')
#es = {}
#es_null = []
#event_data = {}
#for t in times:
#    ev = get_event(t)
#    if ev:
#        evid = times_evid[str(t)]
#        es[evid] = (ev)
#        event_data[evid] = ev[1][1:-1]
#    else:
#        es_null.append(None)
#
#es_all = {}
#for ei in es:
#    if es[ei][0] < 10:
#        es_all[ei] = es[ei]
#
#event_df = pd.DataFrame.from_dict(event_data,orient='index')
#event_df.to_csv('events.csv',header=False)
#
#
#### Get stations ###
#for ei in es:
#    evid = tr.stats.evid
#    lat = tr.stats.sac.evla
#    lon = tr.stats.sac.evlo
#    dep = tr.stats.sac.depmen
#    print evid,lat,lon,dep
#    event_data[evid] = (lat,lon,dep)
