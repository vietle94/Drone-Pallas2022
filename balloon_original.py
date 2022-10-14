import matplotlib.dates as mdates
from matplotlib import animation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.colors import LogNorm
%matplotlib qt

# %%
path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\20220928/'

# %%
files = glob.glob(path + '/**/*.csv', recursive=True) + \
    glob.glob(path + '/**/*.txt', recursive=True)
files
# %%

bme = pd.read_csv(*[x for x in files if 'BME' in x])
bme.dropna(axis=0, inplace=True)
bme['datetime'] = pd.to_datetime(bme['date'] + ' ' + bme['time'])

# %%
cpc = pd.read_csv(*[x for x in files if 'CPC' in x])
cpc['datetime'] = pd.to_datetime(cpc['date_time'])

# %%
pop = pd.read_csv(*[x for x in files if 'HK' in x])
pop['datetime'] = pd.to_datetime(pop['DateTime'], unit='s')
pop_binedges = '0.132	0.144	0.158	0.174	0.191	0.209	0.229	0.27	0.324	0.473	0.594	1.009	1.294	1.637	2.148	2.864	3.648'
pop_binedges = np.fromstring(pop_binedges, dtype=float, sep="\t")
pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2
dlog_bin = np.log10(pop_binedges[1:]) - np.log10(pop_binedges[:-1])
pop_binlab = ['b0', 'b1', 'b2',
              'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13',
              'b14', 'b15']

for particle_size, each_dlog_bin in zip(pop_binlab, dlog_bin):
    pop[particle_size] = pop[particle_size]/(pop[' POPS_Flow']*16.6667) / each_dlog_bin

# %%
minicda = pd.read_csv([x for x in files if 'minicda' in x][0], skiprows=1, header=None, dtype=str)
minicda.dropna(axis=0, inplace=True)
minicda[0] = pd.to_datetime(minicda[0], format="%Y%m%d%H%M%S")
minicda = minicda.rename(columns={0: 'datetime'})

cda_midbin = '0.147178	0.148512	0.14984	0.151149	0.152463	0.153736	0.155037	0.156353	0.157733	0.159147	0.160631	0.162104	0.163632	0.165116	0.166619	0.168103	0.169663	0.171215	0.172809	0.174372	0.175972	0.177499	0.17899	0.180473	0.181989	0.183515	0.185125	0.18674	0.188361	0.189958	0.191562	0.193131	0.194757	0.196404	0.198108	0.199817	0.201587	0.203405	0.205329	0.207304	0.209425	0.211626	0.213932	0.216303	0.218782	0.221367	0.224093	0.226903	0.229915	0.233032	0.236228	0.23945	0.242773	0.246132	0.249607	0.253107	0.256744	0.260442	0.264187	0.267911	0.271706	0.275499	0.279403	0.283227	0.287138	0.290997	0.294872	0.29859	0.30237	0.306117	0.310001	0.313851	0.317863	0.321889	0.326007	0.330069	0.334253	0.338447	0.34288	0.347352	0.352069	0.356884	0.361907	0.366927	0.372137	0.377479	0.383123	0.38886	0.395014	0.40144	0.408224	0.415169	0.422523	0.430111	0.438266	0.446544	0.455456	0.464683	0.47431	0.483937	0.494039	0.504239	0.515062	0.525963	0.537475	0.549211	0.561363	0.573305	0.585638	0.597968	0.610797	0.623491	0.637091	0.650905	0.665095	0.679159	0.693809	0.708272	0.723433	0.738634	0.754816	0.771442	0.788866	0.806406	0.825041	0.844056	0.864269	0.884896	0.907133	0.930247	0.954702	0.979641	1.006303	1.033916	1.063887	1.094818	1.128497	1.163781	1.201442	1.239666	1.280344	1.321963	1.366094	1.410407	1.457152	1.504424	1.552681	1.599797	1.647969	1.695302	1.74325	1.790112	1.838436	1.886361	1.934874	1.982394	2.030952	2.078624	2.127138	2.174776	2.224535	2.274453	2.325111	2.374953	2.426211	2.476709	2.528855	2.580825	2.635387	2.690558	2.747551	2.803991	2.862899	2.922291	2.984056	3.046042	3.113385	3.182289	3.254006	3.326432	3.402919	3.479686	3.56089	3.643269	3.731866	3.82319	3.919206	4.01622	4.118729	4.222422	4.329813	4.437176	4.549892	4.663274	4.778641	4.892855	5.010383	5.12713	5.24763	5.367036	5.491243	5.615306	5.74164	5.86515	5.99241	6.118721	6.248725	6.377145	6.511253	6.646127	6.784049	6.920263	7.061721	7.203762	7.351069	7.498659	7.655424	7.815799	7.983194	8.152294	8.331328	8.513941	8.705466	8.90023	9.109121	9.324911	9.550495	9.779767	10.021903	10.269101	10.529969	10.793235	11.071817	11.35364	11.642367	11.92479	12.214337	12.498558	12.785157	13.062966	13.34801	13.628646	13.909346	14.181604	14.459354	14.731797	15.008272	15.280104	15.564339	15.849489	16.142262	16.431695	16.733284	17.03231	17.334961	17.635557'
cda_midbin = np.fromstring(cda_midbin, dtype=float, sep="\t")

minicda = minicda.iloc[:, np.r_[0:257]]

for i in minicda.columns[1:]:
    minicda[i] = minicda[i].apply(int, base=16)

cda_binedges = np.append(np.append(cda_midbin[0] - (- cda_midbin[0] + cda_midbin[1])/2,
                                   (cda_midbin[:-1] + cda_midbin[1:])/2), (cda_midbin[-1] - cda_midbin[-2])/2 + cda_midbin[-1])
dlog_bin = np.log10(cda_binedges[1:]) - np.log10(cda_binedges[:-1])

for particle_size, each_dlog_bin in zip(minicda.columns[1:], dlog_bin):
    minicda[particle_size] = minicda[particle_size] / each_dlog_bin / 10 / 46.67

# %%

myFmt = mdates.DateFormatter('%H:%M')
fig = plt.figure(figsize=(16, 9))
ax4 = fig.add_subplot(427)
ax1 = fig.add_subplot(421, sharex=ax4)
ax2 = fig.add_subplot(423, sharex=ax4)
ax3 = fig.add_subplot(425, sharex=ax4)
ax5 = fig.add_subplot(222, sharex=ax4)
ax6 = fig.add_subplot(224)

for var, ax_ in zip(['press_bme', 'temp_bme', 'rh_bme'], [ax1, ax2, ax3]):
    ax_.plot(bme['datetime'], bme[var], '.')
    ax_.set_ylabel(var)
    ax_.xaxis.set_major_formatter(myFmt)

ax4.plot(cpc['datetime'], cpc['N conc(1/ccm)'], '.')
ax4.set_yscale('log')
ax4.set_ylim([10, 10000])
ax4.set_yticks([10, 100, 1000, 10000])
ax4.set_ylabel('N conc(1/ccm) CPC')

for ax_ in [ax1, ax2, ax3, ax4]:
    ax_.grid()
    ax_.xaxis.set_major_formatter(myFmt)

minicda_avg = minicda.set_index('datetime').resample('5min').mean().reset_index()
p = ax5.pcolormesh(minicda_avg['datetime'], cda_midbin,
                   minicda_avg.iloc[:, 1:].T, norm=LogNorm(vmax=10, vmin=0.01), cmap='jet')
ax5.set_yscale('log')
ax5.xaxis.set_major_formatter(myFmt)
ax5.set_ylabel('Size (um)')
cbar = fig.colorbar(p, ax=ax5)
cbar.ax.set_ylabel('dN/dlogDp from miniCDA', rotation=90)

pop_avg = pop.set_index('datetime').resample('5min').mean().reset_index()
pop_time = pop_avg['datetime'] + pd.Timedelta('2hour')
p = ax6.pcolormesh(pop_time, pop_midbin, pop_avg[pop_binlab].T, norm=LogNorm(
    vmax=10, vmin=0.01), cmap='jet')
ax6.set_yscale('log')
ax6.xaxis.set_major_formatter(myFmt)
ax6.set_xlim(ax5.get_xlim())
ax6.set_ylabel('Size (um)')
cbar = fig.colorbar(p, ax=ax6)
cbar.ax.set_ylabel('dN/dlogDp from POP', rotation=90)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle(str(cpc['datetime'][0].date()), weight='bold')
fig.savefig(path + 'quicklook.png', dpi=500)

# %%
pop[pop_binlab]


# # %%
# for var, ax_ in zip(['press_bme', 'temp_bme', 'rh_bme', 'N conc(1/ccm) CPC'], ax.flatten()):
#     ax_.plot(df_full['datetime'], df_full[var], '.')
#     ax_.set_ylabel(var)
#     ax_.xaxis.set_major_formatter(myFmt)
# ax[-1].set_yscale('log')
# ax[-1].set_ylim([0, 1000])
# ax[-1].set_yticks([1, 10, 100, 1000])
# # ax[1].plot(df_full['datetime'], df_full['temp_bme'], '.')
# # ax[2].plot(df_full['datetime'], df_full['press_bme'], '.')
# # ax[3].plot(df_full['datetime'], df_full['rh_bme'], '.')
# for ax_ in ax.flatten():
#     ax_.grid()
# fig.tight_layout()
#
# # %%
# df_full = cpc.merge(bme, on='datetime', how='outer').merge(
#     pop, on='datetime', how='outer').merge(minicda, on='datetime', how='outer')
# df_full.drop(columns=['date_time', 'date', 'time'], inplace=True)
#
# # %%
# df_full = df_full.rename(columns={'N conc(1/ccm)': 'N conc(1/ccm) CPC'})
# myFmt = mdates.DateFormatter('%H:%M')
# fig, ax = plt.subplots(4, 1, figsize=(16, 9), sharex=True)
# for var, ax_ in zip(['press_bme', 'temp_bme', 'rh_bme', 'N conc(1/ccm) CPC'], ax.flatten()):
#     ax_.plot(df_full['datetime'], df_full[var], '.')
#     ax_.set_ylabel(var)
# ax[-1].set_yscale('log')
# ax[-1].set_ylim([0, 1000])
# ax[-1].set_yticks([1, 10, 100, 1000])
# # ax[1].plot(df_full['datetime'], df_full['temp_bme'], '.')
# # ax[2].plot(df_full['datetime'], df_full['press_bme'], '.')
# # ax[3].plot(df_full['datetime'], df_full['rh_bme'], '.')
# for ax_ in ax.flatten():
#     ax_.grid()
# fig.tight_layout()
# fig.savefig(path + 'quicklook.png', dpi=500)
#
# # %%
# # path = r'C:\Users\le\OneDrive - Ilmatieteen laitos\Campaigns\Pace2022\FMI balloon payload\20220917/'
# #
# # # %%
# # files = glob.glob(path + '/**/*.csv', recursive=True) + \
# #     glob.glob(path + '/**/*.txt', recursive=True)
#
# # %%
#
#
# # %%
#
#
# # %%
# temp = df_bin.set_index('datetime').resample('5min').mean().reset_index()
# # fig, ax = plt.subplots(figsize=(16, 9))
# # fig, ax = plt.subplots(5, 1, figsize=(16, 9), sharex=True)
# fig = plt.figure(figsize=(16, 9))
# ax1 = fig.add_subplot(421)
# ax2 = fig.add_subplot(423, sharex=ax1)
# ax3 = fig.add_subplot(425, sharex=ax1)
# ax4 = fig.add_subplot(427, sharex=ax1)
# ax5 = fig.add_subplot(122)
# for var, ax_ in zip(['press_bme', 'temp_bme', 'rh_bme', 'N conc(1/ccm) CPC'],
#                     [ax1, ax2, ax3, ax4]):
#     ax_.plot(df_full['datetime'], df_full[var], '.')
#     ax_.set_ylabel(var)
#     ax_.xaxis.set_major_formatter(myFmt)
#
# ax4.set_yscale('log')
# ax4.set_ylim([0, 1000])
# ax4.set_yticks([1, 10, 100, 1000])
# # ax[1].plot(df_full['datetime'], df_full['temp_bme'], '.')
# # ax[2].plot(df_full['datetime'], df_full['press_bme'], '.')
# # ax[3].plot(df_full['datetime'], df_full['rh_bme'], '.')
# for ax_ in [ax1, ax2, ax3, ax4, ax5]:
#     ax_.grid()
# # fig.tight_layout()
# points, = ax5.plot(cda_midbin, temp.iloc[0, 1:].values, '.')
# ax5.set_xscale('log')
# ax5.set_yscale('log')
# ax5.set_ylabel('dN/dlogDp miniCDA')
# ax5.set_ylim([0, 100000])
# ax5.set_yticks([1, 10, 100, 1000, 10000, 100000])
# line1 = ax1.axvline(x=temp.loc[0, 'datetime'], c='red')
# line2 = ax2.axvline(x=temp.loc[0, 'datetime'], c='red')
# line3 = ax3.axvline(x=temp.loc[0, 'datetime'], c='red')
# line4 = ax4.axvline(x=temp.loc[0, 'datetime'], c='red')
#
#
# def animate(i):
#     points.set_data(cda_midbin, temp.iloc[i, 1:].values)
#     ax5.set_title(str(temp.loc[i, 'datetime']))
#     line1.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line2.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line3.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line4.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     return points,
#
#
# # call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(fig, animate,
#                                frames=temp.shape[0], interval=500, blit=True)
# anim.save(path + 'minicda_animation.gif')
#
# # %%
# fig, ax = plt.subplots()
# ax.pcolormesh(df_bin['datetime'], bins, df_bin.iloc[:, 1:].T, norm=LogNorm(), cmap='jet')
# ax.set_yscale('log')
# ax.set_ylim(bottom=0.1)
#
#
# # %%
# temp
#
# # %%
#
#
# # %%
# pop_binedges = '0.132	0.144	0.158	0.174	0.191	0.209	0.229	0.27	0.324	0.473	0.594	1.009	1.294	1.637	2.148	2.864	3.648'
# pop_binedges = np.fromstring(pop_binedges, dtype=float, sep="\t")
# pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2
# dlog_bin = np.log10(pop_binedges[1:]) - np.log10(pop_binedges[:-1])
# pop_binlab = ['b0', 'b1', 'b2',
#               'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13',
#               'b14', 'b15']
#
# # %%
# for particle_size, each_dlog_bin in zip(pop_binlab, dlog_bin):
#     pop[particle_size] = pop[particle_size]/(pop.iloc[:, 9]*16.6667) / each_dlog_bin
#
# # %%
# pop_avg = pop.set_index('datetime').resample('5min').mean().reset_index()
#
# # %%
# temp = df_bin.set_index('datetime').resample('5min').mean().reset_index()
# fig = plt.figure(figsize=(16, 9))
# ax1 = fig.add_subplot(421)
# ax2 = fig.add_subplot(423, sharex=ax1)
# ax3 = fig.add_subplot(425, sharex=ax1)
# ax4 = fig.add_subplot(427, sharex=ax1)
# ax5 = fig.add_subplot(222)
# ax6 = fig.add_subplot(224)
# for var, ax_ in zip(['press_bme', 'temp_bme', 'rh_bme', 'N conc(1/ccm) CPC'],
#                     [ax1, ax2, ax3, ax4]):
#     ax_.plot(df_full['datetime'], df_full[var], '.')
#     ax_.set_ylabel(var)
#     ax_.xaxis.set_major_formatter(myFmt)
#
# ax4.set_yscale('log')
# ax4.set_ylim([0, 1000])
# ax4.set_yticks([1, 10, 100, 1000])
# # ax[1].plot(df_full['datetime'], df_full['temp_bme'], '.')
# # ax[2].plot(df_full['datetime'], df_full['press_bme'], '.')
# # ax[3].plot(df_full['datetime'], df_full['rh_bme'], '.')
# for ax_ in [ax1, ax2, ax3, ax4, ax5]:
#     ax_.grid()
# # fig.tight_layout()
# points_pop, = ax5.plot(bins, temp.iloc[0, 1:].values, '.')
# ax5.set_xscale('log')
# ax5.set_yscale('log')
# ax5.set_ylabel('dN/dlogDp miniCDA')
# ax5.set_ylim([0, 100000])
# ax5.set_yticks([1, 10, 100, 1000, 10000, 100000])
#
# points, = ax6.plot(pop_midbin, pop[pop_binlab].values, '.')
# ax6.set_xscale('log')
# ax6.set_yscale('log')
# ax6.set_ylabel('dN/dlogDp miniCDA')
# ax6.set_ylim([0, 100000])
# ax6.set_yticks([1, 10, 100, 1000, 10000, 100000])
#
# line1 = ax1.axvline(x=temp.loc[0, 'datetime'], c='red')
# line2 = ax2.axvline(x=temp.loc[0, 'datetime'], c='red')
# line3 = ax3.axvline(x=temp.loc[0, 'datetime'], c='red')
# line4 = ax4.axvline(x=temp.loc[0, 'datetime'], c='red')
#
#
# def animate(i):
#     points.set_data(bins, temp.iloc[i, 1:].values)
#     ax5.set_title(str(temp.loc[i, 'datetime']))
#     points_pop.set_data(pop_midbin, pop[pop_binlab].values)
#     ax5.set_title(str(temp.loc[i, 'datetime']))
#     line1.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line2.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line3.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     line4.set_xdata([temp.loc[i, 'datetime'], temp.loc[i, 'datetime']])
#     return points,
#
#
# # call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(fig, animate,
#                                frames=temp.shape[0], interval=500, blit=True)
# anim.save(path + 'minicda_animation.gif')
#
# # %%
# temp.iloc[0, 'datetime']
