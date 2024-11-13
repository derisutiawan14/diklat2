#import library
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timedelta

#memuat data
data_folder = 'D:/DIKLAT FPIK/'
output_folder = 'D:/DIKLAT FPIK/SST/'

suhu_file = data_folder + 'METOFFICE-GLO-SST-L4-REP-OBS-SST_1719550047211.nc'
klo_file = data_folder + 'c3s_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M_1719550376022.nc'
angin_file = data_folder + 'cmems_obs-wind_glo_phy_my_l4_P1M_1719553944710.nc'

# Load datasets
suhu_ds = xr.open_dataset(suhu_file)
klo_ds = xr.open_dataset(klo_file)
angin_ds = xr.open_dataset(angin_file)

# Load variables
lon_sst = suhu_ds['longitude'].values
lat_sst = suhu_ds['latitude'].values
lon_sst, lat_sst = np.meshgrid(lon_sst, lat_sst[::-1])

lon_chl = klo_ds['longitude'].values
lat_chl = klo_ds['latitude'].values
lon_chl, lat_chl = np.meshgrid(lon_chl, lat_chl)

lon_wind = angin_ds['longitude'].values
lat_wind = angin_ds['latitude'].values
lon_wind, lat_wind = np.meshgrid(lon_wind, lat_wind[::-1])

time = klo_ds['time'].values
time = np.array([datetime(1970, 1, 1) + timedelta(seconds=t) for t in time])
timevec = np.array([[t.year, t.month, t.day] for t in time])

chl = klo_ds['CHL'].values.transpose((1, 0, 2))[::-1, :, :]
u10 = angin_ds['eastward_wind'].values.transpose((1, 0, 2))[::-1, :, :]
v10 = angin_ds['northward_wind'].values.transpose((1, 0, 2))[::-1, :, :]

sstk = suhu_ds['analysed_sst'].values
sstM = []
for y in range(2007, 2017):
    for m in range(1, 13):
        ind = np.where((timevec[:, 0] == y) & (timevec[:, 1] == m))[0]
        sstM.append(np.mean(sstk[:, :, ind], axis=2))
sstM = np.array(sstM).transpose((1, 2, 0))[::-1, :, :]
sst = sstM - 273.15

#fungsi windstress
def windstress(u, v):
    rho_air = 1.225  # Air density in kg/m^3
    cd = 1.2e-3  # Drag coefficient
    tau_x = rho_air * cd * u * np.abs(u)
    tau_y = rho_air * cd * v * np.abs(v)
    return tau_x, tau_y

#fungsi cdtdim
def cdtdim(lat, lon, unit='m'):
    R = 6371000  # Earth's radius in meters
    lat = np.radians(lat)
    lon = np.radians(lon)
    dlat = np.gradient(lat, axis=0)
    dlon = np.gradient(lon, axis=1)
    dx = R * np.cos(lat) * dlon
    dy = R * dlat
    if unit == 'km':
        dx /= 1000
        dy /= 1000
    return dx, dy

#fungsi ekman (untuk ekman pumping dan ekman transport)
def ekman(lat, lon, u, v):
    rho_air = 1.225  # Air density in kg/m^3
    f = 1e-4  # Coriolis parameter (approx.)
    tau_x, tau_y = windstress(u, v)
    U_ekman = tau_y / (rho_air * f)
    V_ekman = -tau_x / (rho_air * f)
    dx, dy = cdtdim(lat, lon, 'm')
    dU_dx = np.gradient(U_ekman, dx, axis=1)
    dV_dy = np.gradient(V_ekman, dy, axis=0)
    W_ekman = dU_dx + dV_dy
    return U_ekman, V_ekman, W_ekman

#hitung parameter
# Wind stress, N/m^2
tau_x, tau_y = windstress(u10, v10)
mag_tau = np.hypot(tau_x, tau_y)
angin = np.hypot(u10, v10)

# Wind stress curl, N/m^3
dx_wind, dy_wind = cdtdim(lat_wind, lon_wind, 'm')
d_tau_xx, d_tau_xy = np.gradient(tau_x)
d_tau_yx, d_tau_yy = np.gradient(tau_y)
tau_curl = (d_tau_yx / dx_wind) - (d_tau_xy / dy_wind)

# Ekman Pumping (UE & VE, m^2/s; wE, m/s)
U_ekman, V_ekman, W_ekman = ekman(lat_wind, lon_wind, u10, v10)

# Upwelling transport, 10^6 m^3/s = 1 Sv
upw = W_ekman * np.abs(dx_wind) * np.abs(dy_wind) * 1e-6
upw[upw <= 0] = np.nan  # Only upwelling (positive value)

# SST gradient, °C/km
dx_sst, dy_sst = cdtdim(lat_sst, lon_sst, 'km')
sst_x, sst_y = np.gradient(sst)
dsst_xdx = sst_x / dx_sst
dsst_ydy = sst_y / dy_sst
sst_grad = np.hypot(dsst_xdx, dsst_ydy)

# Climatology calculation function
def monthly_anom(data, time):
    monthly_clim = np.zeros((data.shape[0], data.shape[1], 12))
    anom = np.zeros_like(data)
    for month in range(1, 13):
        monthly_data = data[:, :, np.where(timevec[:, 1] == month)[0]]
        monthly_clim[:, :, month - 1] = np.mean(monthly_data, axis=2)
        anom[:, :, np.where(timevec[:, 1] == month)[0]] = monthly_data - monthly_clim[:, :, month - 1][:, :, np.newaxis]
    return monthly_clim, anom

variables = {
    "chl": chl,
    "sst": sst,
    "sst_grad": sst_grad,
    "u10": u10,
    "v10": v10,
    "tau_x": tau_x,
    "tau_y": tau_y,
    "mag_tau": mag_tau,
    "tau_curl": tau_curl,
    "U_ekman": U_ekman,
    "V_ekman": V_ekman,
    "W_ekman": W_ekman,
    "upw": upw
}

results = {}
for var_name, var_data in variables.items():
    monthly, anom = monthly_anom(var_data, time)
    results[var_name + "_monthly"] = monthly
    results[var_name + "_anom"] = anom

#visualisasi peta
def plot_map(data, lon, lat, title, cmap, cbar_label, cbar_lim, quiver_data=None, quiver_scale=1):
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([105, 114, -11, -7], crs=ccrs.PlateCarree())
    p = ax.pcolormesh(lon, lat, data, cmap=cmap, transform=ccrs.PlateCarree())
    cb = fig.colorbar(p, ax=ax, orientation='vertical', pad=0.05)
    cb.set_label(cbar_label)
    p.set_clim(cbar_lim)
    if quiver_data:
        q_lon, q_lat, q_u, q_v = quiver_data
        ax.quiver(q_lon, q_lat, q_u, q_v, color='k', scale=quiver_scale, transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE)
    ax.gridlines(draw_labels=True)
    plt.title(title)
    plt.show()

#plotting peta suhu dan angin
for nt in range(1):  # Sst Angin
    sst_monthly = results["sst_monthly"][:, :, nt]
    u10_monthly = results["u10_monthly"][:, :, nt]
    v10_monthly = results["v10_monthly"][:, :, nt]
    
    plot_map(sst_monthly, lon_sst, lat_sst, 'Sea Surface Temperature (°C)', 'RdBu_r',
             'Sea surface temperature (°C)', [27, 31],
             quiver_data=(lon_wind[::1, ::1], lat_wind[::1, ::1], u10_monthly[::1, ::1], v10_monthly[::1, ::1]), quiver_scale=10)

#plotting peta klorofil
for nt in range(1):  # Chl 
    chl_monthly = results["chl_monthly"][:, :, nt]
    
    plot_map(chl_monthly, lon_chl, lat_chl, 'Chlorophyll-a Concentration Anomaly', 'YlGn',
             'Chlorophyll-a Concentration Anomaly', [0, 1])

#menyimpan gambar
for nt in range(1):  # Sst Angin
    sst_monthly = results["sst_monthly"][:, :, nt]
    u10_monthly = results["u10_monthly"][:, :, nt]
    v10_monthly = results["v10_monthly"][:, :, nt]
    
    fig = plt.figure()
    plot_map(sst_monthly, lon_sst, lat_sst, 'Sea Surface Temperature (°C)', 'RdBu_r',
             'Sea surface temperature (°C)', [27, 31],
             quiver_data=(lon_wind[::1, ::1], lat_wind[::1, ::1], u10_monthly[::1, ::1], v10_monthly[::1, ::1]), quiver_scale=10)
    fig.savefig(output_folder + 'Suhu2' + time[nt].strftime('%m') + '.png', transparent=True)
    plt.close(fig)

for nt in range(1):  # Chl 
    chl_monthly = results["chl_monthly"][:, :, nt]
    
    fig = plt.figure()
    plot_map(chl_monthly, lon_chl, lat_chl, 'Chlorophyll-a Concentration Anomaly', 'YlGn',
             'Chlorophyll-a Concentration Anomaly', [0, 1])
    fig.savefig(output_folder + 'Suhu' + time[nt].strftime('%m') + '.png', transparent=True)
    plt.close(fig)
