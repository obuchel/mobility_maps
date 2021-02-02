import json

kkeys={}
with open("timeseries_density.json","r") as f:
    data0=json.load(f)
    for el in data0:
        kkeys[el["key"]]=el["density"][69][1]
        print(el["density"][69][0])

with open("Apr05-11_2_small_simplified2_2.json","r") as f:
    data=json.load(f)
    print(data)
    for el in data["features"]:
        try:
            el["properties"]["apr"]=int(el["properties"]["Apr11_diff"])
            #print(el["properties"]["apr"])
            #kkeys["com_"+el["properties"]["GEOID"].split("_")[1]]
        except:
            print(el["properties"])
            continue
    with open("Apr05-11_2_small_simplified2_4.json","w") as d:
        json.dump(data,d)
