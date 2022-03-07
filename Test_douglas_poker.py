import geopandas as gpd
from douglas_poker_function import get_points

shapfile_address=r' shapefile address'

lands=gpd.read_file(shapfile_address)
n=len(lands)
for i in range(n):

    land=lands.geometry[i]
    points=get_points(land)
    
    print('shape number '+str(i) )
    print(points)