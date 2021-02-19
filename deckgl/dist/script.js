function hexToRgb(c){
    if(/^#([a-f0-9]{3}){1,2}$/.test(c)){
        if(c.length== 4){
            c= '#'+[c[1], c[1], c[2], c[2], c[3], c[3]].join('');
        }
        c= '0x'+c.substring(1);
	//console.log([[(c>>16)&255, (c>>8)&255, c&255].join(',')]);
	var xx=[(c>>16)&255, (c>>8)&255, c&255].join(',').split(",");
        return [Number(xx[0]),Number(xx[1]),Number(xx[2])];
    }
    return [128,128,128];
}
/*
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    console.log(result);
    return result ? [Number(result[1]),Number(result[2]),Number(result[3])] : [128, 128, 128]
}
*/
//console.log( hexToRgb("#FFFFFF"));
const deckgl = new deck.DeckGL({
  mapboxApiAccessToken: 'pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoiY2pudzRtaWloMDAzcTN2bzN1aXdxZHB5bSJ9.2bkj3IiRC8wj3jLThvDGdA',
  mapStyle: 'mapbox://styles/mapbox/dark-v9',
  longitude: -95,
  latitude: 35,
  zoom: 3,
  //minZoom: 3,
  //maxZoom: 15,
  pitch: 40.5
});

const data0 = d3.csv('write_airports_rels_kepler11_11.csv');
const data2 = d3.json('Apr05-11_2_small_simplified2_2_new.json');
//console.log(data2);
const OPTIONS = ['radius', 'coverage', 'upperPercentile'];
const OPTIONS2 = ['november','october','september','august','july','june','may'];

/*
const COLOR_RANGE = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];
*/
//#FFFFB2,#FED976,#FEB24C,#FD8D3C,#F03B20,#BD0026
const COLOR_RANGE =[[255,255,178],[254,217,118],[254,178,76],[253,141,60],[240,59,32],[189,0,38]];
var layer;
OPTIONS.forEach(key => {
  document.getElementById(key).oninput = renderLayer;
});
document.getElementsByName('date').forEach(key => {
  this.onchange = renderLayer;
});

d3.select("#radius").attr("value",5000);
var radiobtn = document.getElementById("november");
radiobtn.checked = true;
d3.select("#control-panel:nth-child(2)").attr("visibility","hidden");
renderLayer();
//d3.select("#radius").attr("value",5000);
//function renderLayer () {
//document.addEventListener("DOMContentLoaded", function(){
function renderLayer (e) {
    //    alert("kkk");
    var arr=document.getElementsByName('date');
    var ch;
    var name;
    for (var x=0; x<arr.length; x++){
	if (arr[x].checked==true){
	    ch=arr[x].value;
            //name=arr[x].id;
	}

    }
    if (ch=="11") {

	var data=data0;
    } else {

var data=d3.csv('write_airports_rels_kepler11_'+ch+'.csv')
    }
    
 const options = {};
  OPTIONS.forEach(key => {
    const value = +document.getElementById(key).value;
    document.getElementById(key + '-value').innerHTML = value;
    options[key] = value;
  });

//Apr05-11_2_small_simplified2_2.json
layer = new GeoJsonLayer({
    id: 'geojson-layer',
    data:data2,
    stroked: false,
    filled: true,
    extruded: false,
    wireframe: true,
    getFillColor: d => hexToRgb(d.properties.color),
    opacity: 0.8,
    getLineColor: [255, 255, 255],
    getLineWidth: 1,
    lineWidthScale: 20,
    opacity: 0.2,
    pickable: true
  });
//    console.log(layer)
//});
//function renderLayer () {

//source,target,date,source_lat,source_lon,target_lat,target_lon,weight
  const hexagonLayer = new deck.HexagonLayer({
    id: 'heatmap',
      colorRange: COLOR_RANGE,
      colorDomain:[0,20,1000,2000,5000],
    data,
      elevationRange: [0, 5000],
      elevationScale: 150,
      //radius: 5000,
      //colorScaleType: 'linear',
    extruded: true,
    pickable: true,  
    getPosition: d => [Number(d.target_lon), Number(d.target_lat)],
    getElevationWeight: point => Number(point.weight),
    elevationAggregation: 'SUM',
    elevationScaleType: 'linear',
    getColorWeight: point => Number(point.weight)*100,
    colorAggregation: 'SUM',
    colorScaleType: 'quantile',
    transitions: {
		getElevationValue: { duration: 1000 }
      },
    //  getColorValue: point => Number(point.weight),
    opacity: 0.3,
    onClick: (event) => { console.log(event); return true; },  
    ...options
  });

  deckgl.setProps({
      layers: [layer,hexagonLayer]
  });
}
