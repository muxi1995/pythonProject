import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import xarray as xr
import pyreadr
import pandas as pd

#read data of corrdinate
result = pyreadr.read_r("/work/u/herm/results/corrd_lai_lt_spei_intersect forest age 90m.RData")
dt=result['dds']
print(dt)

# read cor_data
xadv = xr.open_dataset("/work/u/herm/results/interaction/cor_LAI_SPEI/cor_spei_lai_2013/cor_LAI_SPEI_2.nc")
r=xadv.SPEI_cor[0,:,:]
scale=xadv.SPEI_cor[:,:,2]
lon=xadv.lon
lat=xadv.lat
lon_grid, lat_grid = np.meshgrid(lon, lat)
lon_values = lon_grid.ravel()
lat_values = lat_grid.ravel()
lonlat_values = np.column_stack((lon_values, lat_values))
# 定义你关注的格点的经纬度
selected_lons =dt.corrd_lon
selected_lats = dt.corrd_lat
# 先将selected_lons和selected_lats组合成一个二维数组
selected_lonlat = np.column_stack((selected_lons, selected_lats))

#interest_lon = [ 90, 135, -45, -90, -135]
#interest_lat = [0, 30, 60, -30, -60]

# 查找这些坐标在数据中的索引
#lon_index = [np.argmin(np.abs(lon-l)) for l in interest_lon]
#lat_index = [np.argmin(np.abs(lat-l)) for l in interest_lat]

# 获取这些坐标对应的数据
#interest_data = data[lat_index, lon_index]

# 绘制所有数据的填色图
plt.pcolormesh(lon, lat, data)
# 查找这些坐标在数据中的索引
lon_index = [np.argmin(np.abs(lon-l)) for l in selected_lons]
lat_index = [np.argmin(np.abs(lat-l)) for l in selected_lats]
plt.scatter(interest_lon, interest_lat, c=interest_data, s=100, edgecolors='k')
# 获取这些坐标对应的数据
interest_data = data[lat_index, lon_index]

# 创建一个mask，其形状和lon和lat的形状相同
mask = np.zeros_like(lon, dtype=bool)

# 使用np.isin找出lon和lat中与selected_lonlat匹配的位置
mask = np.isin(lonlat_values, selected_lonlat).all(axis=-1)


# 使用掩膜来选择你关注的格点
selected_data = np.ma.masked_where(np.logical_not(mask), r)


mpl.rcParams["font.family"] = 'Arial'  # 默认字体类型
mpl.rcParams["mathtext.fontset"] = 'cm'  # 数学文字字体
mpl.rcParams["font.size"] = 12
mpl.rcParams["axes.linewidth"] = 1


# 绘制填色图
plt.pcolormesh(lon, lat, selected_data)
plt.colorbar()
plt.show()
