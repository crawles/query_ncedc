"""
example
~~~~~~~~~~~~~~~~~
Example searching NCEDC database for seismic events matching provided times
"""
from obspy.core.utcdatetime import UTCDateTime
import query
import io_utils
from obspy.fdsn import Client
import numpy as np

times = array([UTCDateTime(2002, 1, 8, 11, 58, 44, 870000),
       UTCDateTime(2002, 1, 8, 13, 43, 42, 870000),
       UTCDateTime(2002, 1, 8, 23, 53, 47, 870000),
       UTCDateTime(2002, 1, 9, 23, 52, 33, 870000),
       UTCDateTime(2002, 1, 10, 6, 53, 35, 870000)], dtype=object)

client = Client("NCEDC")
times = np.unique(times)
starttime = sorted(times)[0]
endtime = sorted(times)[-1]

# parkfield
lat = 36.003368
lon = -120.56023
minlat = lat - 1
maxlat = lat + 1
minlon = lon - 1
maxlon = lon + 1

all_events = query.query_events(client,np.min(times),np.max(times),minlat,maxlat,minlon,maxlon)
assoc_events = query.find_associated_events(times,all_events,delta_time = 10) # seconds
