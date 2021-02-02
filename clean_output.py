

import json

arr=[]
arr0={}
features=[]
dd={
  "type": "FeatureCollection",
  "features": []
}
with open("output_polygons.json","r") as fp:
    data=json.load(fp)
    for el in data["features"]:
        #print(el["type"])
        if el["properties"]["GEOID"] not in list(arr0.keys()):
            arr0[el["properties"]["GEOID"]]=[]
            try:
                for ele in el["geometry"]["geometries"]:            
                    if ele['type']=="Polygon":
                        arr0[el["properties"]["GEOID"]].append(el["properties"]["GEOID"])
                        ata=el["properties"]["GEOID"]+"_"+str(len(arr0[el["properties"]["GEOID"]]))
                        el["properties"]={"GEOID":ata}
                        el["geometry"]=ele
                        features.append(el)
            except:
                continue
#print(features)
dd["features"]=features
#print(dd)

with open("output_cleaned.json","w") as fp:
    json.dump(dd,fp)
