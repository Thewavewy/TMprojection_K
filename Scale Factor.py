## โปรแกรมสุ่มหาค่าเฉลี่ย scale factor
# แต่ละโซนจะมีค่าเฉลี่ย scale factor ไม่เท่ากัน ก่อนใช้ในงาน pyproj ต้องหาค่าเฉลี่ยทุกครั้ง
# กรุณาใส่ขอบเขต lat lon max, min ก่อนใช้งาน

# all พิกัด ใส่เป็นทศนิยมในรูปแบบ decimal(dd) และ zone
print('------- เริ่มโปรแกรม --------')
lat_min = float(input('ใส่ lat_min:'))
lat_max = float(input('ใส่ lat_max:'))
lon_min = float(input('ใส่ lon_min:'))
lon_max = float(input('ใส่ lon_max:'))
zone = int(input('ใส่เลขโซน:'))
n = int(input('จำนวนสุ่ม:'))

import math
import random

def utm_sf(lat,lon,k0,zone):
    a = 6378137 #m in WGS84
    b = 6356752.3142 #m in WGS84
    cen = ((zone-30)*6)-3
    lon = cen - lon
    e2 = (a**2 - b**2) / b**2
    n = e2 * (math.cos(math.radians(lat))**2)
    F2 = (1 + (n**2)) / 2
    L2 = (math.radians(lon) * math.cos(math.radians(lat))) ** 2
    t = math.tan(math.radians(lat))
    F4 = (5 - (4 * (t**2)) + (n**2) * (9 - 24 * (t**2))) / 12
    k = k0 * (1 + (F2 * L2 * (1 + F4 * L2)))
    return k

# random n จากขอบเขต
sum_sf = []
for j in range(n):
    lat_v =list()
    lon_v =list()
    sum_r = 0
    for i in range(1,n+1):
        lat_r = float(round(lat_min + (lat_max - lat_min)*random.uniform(0,1),3))
        lon_r = float(round(lon_min + (lon_max - lon_min)*random.uniform(0,1),3))
        lat_v.append(lat_r)
        lon_v.append(lon_r)
        i += 1
    for i in range(len(lat_v)):
        sf_r = utm_sf(lat_v[i],lon_v[i],0.9996,zone)
        se_r = 1 - sf_r
        sum_r = sum_r+se_r
    mean_sf_r = round(abs(1-(sum_r/n)),8)
    sum_sf.append(mean_sf_r)
result = round(sum(sum_sf)/n,8)
print('ค่า k ที่ต้องใส่ไปใน QGIS ='+' '+str(result)+'\n')
print('pyproj code')
print('+proj=tmerc +lat_0=0.0 +lon_0='+str(((zone-30)*6)-3)+' k0='+str(result)+' x_0=500000 y_0=0 +a=6378137.0 +b=6356752.3142 +units=m +no_defs')