import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import merge_sensor_data as merge_sensor_data

# %%
merge_sensor_data(dir_in, dir_out)
df = pd.read_csv(r'C:\Users\le\Desktop\Drone-Pallas2022/latest_merged.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

var1 = 'temp_bme_BME_BP3'
var2 = 'rh_bme_BME_BP3'
vary = 'press_bme_BME_BP3'
fig = plt.figure(figsize=(12, 12))
gs = GridSpec(8, 12)
ax1 = fig.add_subplot(gs[:-2, :])
ax1.set_ylabel(vary)
ax1.set_xlabel(var1)
ax1_twin = ax1.twiny()
ax1_twin.set_xlabel(var2)
ax2 = fig.add_subplot(gs[-1:, ::])
ax2_twin = ax2.twinx()
ax2.set_ylabel(var1)
ax2_twin.set_ylabel(var2)
# fig.subplots_adjust(hspace=3)
for ax_ in [ax1, ax1_twin, ax2, ax2_twin]:
    ax_.grid()


def animate(i):
    ax1.plot(df[var1], df[vary], c='blue')
    ax1.xaxis.label.set_color('blue')
    ax1.tick_params(axis='x', colors='blue')

    ax1_twin.plot(df[var2], df[vary], c='red')
    ax1_twin.xaxis.label.set_color('red')
    ax1_twin.tick_params(axis='x', colors='red')

    ax2.plot(df['datetime'], df[var1], c='blue')
    ax2.yaxis.label.set_color('blue')
    ax2.tick_params(axis='y', colors='blue')

    ax2_twin.plot(df['datetime'], df[var2], c='red')
    ax2_twin.yaxis.label.set_color('red')
    ax2_twin.tick_params(axis='y', colors='red')


ani = FuncAnimation(fig, animate, interval=5000)
plt.show()
