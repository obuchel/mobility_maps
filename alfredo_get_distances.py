import json
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import pandas as pd
import matplotlib.pyplot as plt
'''
coords={}
with open("all_coordinates2.json","r") as f:
    coords=json.load(f)
'''

kkeys={}
with open("timeseries_density.json","r") as f:
    data0=json.load(f)
    for el in data0:
        #kkeys[el["key"]]=el["density"][69][1]
        print(el)


bridge=pd.read_csv("/Users/olgabuchel/Sites/sg-social-distancing2/alfredo/communities_degrees_Apr05-11.csv")
print(bridge)
cbgs_coms={}
#node_id  cluster
for item in bridge.iterrows():
    if "com_"+str(item[1]["cluster"]).split(".")[0] not in list(cbgs_coms.keys()):
        cbgs_coms["com_"+str(item[1]["cluster"]).split(".")[0]]=[str(item[1]["node_id"])]
    else:
        cbgs_coms["com_"+str(item[1]["cluster"]).split(".")[0]].append(str(item[1]["node_id"]))
#print(cbgs_coms)


distances={}        
with open("/Users/olgabuchel/Sites/sg-social-distancing2/alfredo/non_home_8_months.json","r") as f:
    distances=json.load(f)
    print(distances.keys())

kkeys={}
for el in list(cbgs_coms.keys()):
    kkeys[el]=[]
    for item in cbgs_coms[el]:
        try:
            kkeys[el].append(distances[item])
        except:
            continue
#print(kkeys)
kkeys0={}
for item in list(kkeys.keys()):
    dd3=[]
    for el in kkeys[item]:
        try:
            #print(el)
            #print(distances[el])
            dd=pd.DataFrame([el])
            dd3.append(dd)
        except:
            print("failed")
            continue
    d4=pd.concat(dd3)
    cols=d4.columns
    means=[]
    for m in cols:
        d5=d4[m].mean()
        means.append(d5)
    print(item,means)
    kkeys0[item]=means
    ll=range(1,len(means)+1)
    plt.plot(ll,means)
    plt.title(item)
    plt.savefig("non_home_"+item)
    plt.close()
    #plt.show()
with open("non_home_means.json","w") as fp:
    json.dump(kkeys0,fp)
    
'''    
map_data=gpd.read_file("Apr05-11_large_simplified_data_added.json")
print(map_data)
def explode(indata):
    indf = gpd.GeoDataFrame.from_file(indata)
    outdf = gpd.GeoDataFrame(columns=indf.columns)
    for idx, row in indf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row,ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            multdf = gpd.GeoDataFrame(columns=indf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs,ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom,'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf,ignore_index=True)
    return outdf

print(explode("Apr05-11_large_simplified_data_added.json"))
'''    
#get file with communities and degrees from sand shark
#make kkeys for communities and cbgs
#make a dictionary for communities. add all timelines from distances for communities
#add all timelines, replace all nans with 0.
#df['MyColumn'].sum()
#df["columnname"].mean()
