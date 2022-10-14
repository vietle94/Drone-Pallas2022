import geopy.distance
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gpxpy
import gpxpy.gpx
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

myFmt = mdates.DateFormatter('%H:%M')
%matplotlib qt

# %%
dir = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\balloon_logs/'
file = dir + '00000020.log.gpx'

# %%
the_map = create_folium_map()
for track in read_gpx_file(file):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(the_map, segment, color_by='elevation')

# the_map.save(dir + 'map_elevation.html')


# %%
time = track['segments'][0]['time']
elevation = track['segments'][0]['elevation']
time = np.array(time)
elevation = np.array(elevation)
delta_time = np.array([x.total_seconds() for x in (time[1:] - time[:-1])])
w = (elevation[1:] - elevation[:-1])/delta_time

data = pd.DataFrame({'time': time, 'elevation': elevation,
                    'latlon': track['segments'][0]['latlon']})
data = data.drop_duplicates(subset=['time'])
data = data.reset_index(drop=True)
w = (data['elevation'].values[1:] - data['elevation'].values[:-1]) / \
    np.array([x.total_seconds() for x in np.diff(data['time'])])
distance = np.array([geopy.distance.geodesic(data['latlon'].values[i],
                    data['latlon'].values[0]).km*1000 for i in range(len(data))])
v = (distance[1:] - distance[:-1])/np.array([x.total_seconds() for x in np.diff(data['time'])])

# %%
fig, ax = plt.subplots(4, 1, figsize=(16, 9), sharex=True)

ax[0].plot(data['time'], distance)
ax[0].set_ylabel('Distance [m]')
ax[1].plot(track['segments'][0]['time'], track['segments'][0]['elevation'])
ax[1].set_ylabel('Elevation [m]')

ax[2].plot(data['time'][1:], v)
ax[2].set_ylabel('Horizontal speed [m/s]')
ax[3].plot(data['time'][1:], w)
ax[3].set_ylabel('Vertical speed [m/s]')
ax[3].set_xlim([pd.to_datetime('2022-10-10 10:23:58'),
               pd.to_datetime('2022-10-10 12:30:58')])
ax[3].xaxis.set_major_formatter(myFmt)
for ax_ in ax.flatten():
    ax_.grid()
fig.tight_layout()
fig.savefig(dir + 'trajectory_detail_zoomed.png', dpi=500)
