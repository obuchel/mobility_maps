






import shapely.geometry as geom
import numpy as np
import geopandas as gpd
import pandas as pd
unit_square = np.array([(0,0), (0,1), (1,1), (1,0)])
unit_hole = unit_square * .5 + .25
smaller_hole = unit_hole * .25

# reverse the order of the holes
pgon1 = geom.Polygon(shell=unit_square, holes=[unit_hole, smaller_hole])
pgon2 = geom.Polygon(shell=unit_square, holes=[smaller_hole, unit_hole])


print(pgon1.almost_equals(pgon2))
print(pgon1.equals(pgon2))
print(pgon1.equals_exact(pgon2, 0.8))
#https://github.com/Toblerity/Shapely/issues/535
#https://stackoverflow.com/questions/27152904/calculate-overlapped-area-between-two-rectangles

from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

ra = Rectangle(3., 3., 5., 5.)
rb = Rectangle(1., 1., 4., 3.5)
# intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy

print(area(ra, rb))
#  0.5 
from shapely.geometry import Polygon

polygon = Polygon([(-63, 43), (-65, 45), (-65, 44), (-63, 43)])
other_polygon = Polygon([(-63, 43), (-65, 44), (-65.5, 44.5), (-63.5, 43.5)])
intersection = polygon.difference(other_polygon)
print(intersection)
print(intersection.area)
arr=[]
#https://shapely.readthedocs.io/en/latest/manual.html#object.intersection
df = gpd.read_file('Mar08-14_large_simplified.json')
df2 = gpd.read_file('Mar01-07_large_simplified.json')
df3 = gpd.read_file('May24-30_large_simplified.json')
df4 = gpd.read_file('Sep27-Oct3_large_simplified.json')
print(df,df2)
for el in df.iterrows():
    for el2 in df2.iterrows():
        for el3 in df3.iterrows():
            for el4 in df4.iterrows():
                try:
                    if "com" in el[1]["GEOID"] and "com" in el2[1]["GEOID"] and "com" in el3[1]["GEOID"] and "com" in el4[1]["GEOID"]:
                        intersection = el2[1]["geometry"].difference(el[1]["geometry"])
                        #print(intersection)
                        
                        intersection2 = intersection.difference(el3[1]["geometry"])
                        intersection3 = intersection2.difference(el4[1]["geometry"])
                        #almost_equals=el2[1]["geometry"].almost_equals(el[1]["geometry"])
                        if intersection3.area>0:
                            print(el[1]["GEOID"],el2[1]["GEOID"],el3[1]["GEOID"],el4[1]["GEOID"],intersection3.area,intersection3)
                            arr.append([el[1]["GEOID"]+"-"+el2[1]["GEOID"]+"-"+el3[1]["GEOID"]+"-"+el4[1]["GEOID"],intersection3])


                        
                except:
                    continue

print(arr)

df5=pd.DataFrame(arr,columns=["GEOID","geometry"])

#from shapely import wkt
#df['geometry'] = df['geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df5, geometry='geometry')

gdf.to_file("output_polygons1.json", driver="GeoJSON")
# 0.5

'''
from functools import partial
import shapely.ops
import pyproj

# Suppose geometry is an instance of shapely.geometry.Geometry
tfm = partial(pyproj.transform, 
              pyproj.Proj(init="epsg:4326"), 
              pyproj.Proj(init="epsg:3031"))
reprojected = shapely.ops.transform(tfm, geometry)
'''
