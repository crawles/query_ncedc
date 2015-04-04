"""
query
~~~~~~~~~~~~~~~~~
Contains functions for querying data from NCDEC.
"""
import datetime
import numpy as np

def query_events(client,start,stop,minlat,maxlat,minlon,maxlon):
    """ Query range start to stop """
    start = start.datetime
    stop  = stop.datetime
    events = client.get_events(starttime=start, endtime=stop,\
        minlatitude  = minlat, maxlatitude  = maxlat,\
        minlongitude = minlon, maxlongitude = maxlon)
    return events


def event_data(e):
    """ Parse event and get event data """
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

def find_associated_events(times,all_events,delta_time):
    """ For each time in times, find nearest event.
    Return: [time,delta_time,[etime,latitude,longitude,depth,mag]] """
    associated_events = []
    for time in times:
        event_dist, nearest_event = find_nearest_event(time,all_events)
        if event_dist < delta_time: #seconds
            associated_events.append([time,event_dist,nearest_event])
        else:
            associated_events.append([time,None,None])
    return associated_events
