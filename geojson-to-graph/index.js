const fs = require('fs')
const readlineSync = require('readline-sync');

type_dict = {
    "0": 0.1325, // Private
    "1": 0.11,  // Bus
    "2": 0.0846 // Rail
}

const epsilon = 0.5;

// p1 = [lon, lat]
// Això son quilòmetres!!!!!!! 
function Dist(p1, p2){
    var lat1 = p1[0] * Math.PI / 180, lon1 = p1[1] * Math.PI / 180, lat2 = p2[0] * Math.PI / 180, lon2 = p2[1] * Math.PI / 180;
    var dlon = lon2 - lon1;
    var dlat = lat2 - lat1;

    var a = Math.pow(Math.sin(dlat / 2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dlon / 2), 2);
    var c = 2 * Math.asin(Math.sqrt(a));

    var r = 6371;

    return(c * r);
}

function GetFinalLineData(line, firstIndex){
    var stations = line["stations"];
    var first = stations[firstIndex];

    var result = [];
    var stats = [...stations];

    result.push(stats[firstIndex]);
    stats.splice(firstIndex, 1);


    while(stats.length > 0){

        var min = Infinity;
        var index = -1;
        var i = 0;
        stats.forEach((st) => {
            d = Dist(first["coords"], st["coords"])
            if(d < min){
                min = d;
                index = i;
            }
            i = i + 1;
        });
        
        firstIndex = index;

        result.push(stats[firstIndex]);
        stats.splice(firstIndex, 1);
    }

    console.log(result);
    return result;
}

function CreateLine(name, type, totalTypes, agency){

    console.log("Include " + agency + " - " + name + "? ");
    include = readlineSync.question("");
    if(include == ""){
        if(totalTypes[type] === undefined){
            console.log("(0: P, 1: B, 2: R) Set type for " + agency + " - " + name);

            totalTypes[type] = {}

            totalTypes[type]["co2km"] = type_dict[readlineSync.question("")];
            console.log("Set km/h: ");
            
            kmh = parseFloat(readlineSync.question("")) / 3.6;
            totalTypes[type]["velocity"] = kmh;
        }
    
        return {
            name: name,
            co2kmp: totalTypes[type]["co2km"],
            velocity: totalTypes[type]["velocity"],
            stations: [],
            edges: [],
        }
    } else {
        ignoredLines.push(agency + "-" + name);
        return false;
    }    
}

function GetStartIndex(line){    
    var minIndex = -1;
    var minDistance = Infinity;

    var stations = line["stations"];

    for(var j = 0; j < line.stations.length; j++){

        var firstIndex = j;
        var first = stations[firstIndex];

        var stats = [...stations];
    
        stats.splice(firstIndex, 1);
    
        while(stats.length > 0){
            var min = Infinity;
            var index = -1;
            var i = 0;
            stats.forEach((st) => {
                d = Dist(first["coords"], st["coords"])
                if(d < min){
                    min = d;
                    index = i;
                }
                i = i + 1;
            });
            
            firstIndex = index;
    
            stats.splice(firstIndex, 1);

            if(min < minDistance){
                minDistance = min;
                minIndex = j;
            }
        }
    
    }

    return minIndex;
}

let finalInfo = {
    lines: {},
    stations: [],
    edges: []
}

let ignoredLines = []

function convert(file){
    const json = JSON.parse(fs.readFileSync("./geojson/" + file));
    
    const features = json["features"];
    const agency = file.replace(/\.[^/.]+$/, "")

    console.log("Converting " + agency);

    let routeTypes = {}
    

    features.forEach((feature) => {
        // Aconseguim les features que son punts
        let type = feature["geometry"]["type"]
        if(type == "Point"){
            // console.log(feature)
            let coords = feature["geometry"]["coordinates"]
            
            let featureRoutes = feature["properties"]["routes"]
            featureRoutes.forEach((featureRoute) => {
                let shortName = featureRoute["route_short_name"];

                if(ignoredLines.includes(agency + "-" + shortName)) return;

                if(finalInfo.lines[shortName] === undefined){
                    var newLine = CreateLine(shortName, featureRoute["route_type"], routeTypes, agency)
                    if(newLine){
                        finalInfo.lines[shortName] = newLine;
                        console.log("Created line " + shortName);
                    } else {
                        return;
                    }
                    
                }

                // Add feature to selected line
                finalInfo.lines[shortName]["stations"].push({
                    name: feature["properties"]["stop_name"],
                    coords: coords,
                })
            });
        }
    });
}


fs.readdir('./geojson/', (err, files) => {
    files.forEach(file => {
        convert(file);
    });

    var n = 0;

    for (const [key, value] of Object.entries(finalInfo["lines"])) {
        first = GetStartIndex(value);
        value.edges = GetFinalLineData(value, first);

        for(var i = 0; i < value.edges.length; i++){
            finalInfo.stations.push(value.edges[i]);
            if(i < value.edges.length - 1){
                var d = Dist(value.edges[i]["coords"], value.edges[i+1]["coords"]);
                var c2km = d * value.co2kmp;
                var vel = value.velocity;
                finalInfo.edges.push([i + n, i + n + 1, d, c2km, vel]);
            }
        }

        n += value.edges.length;    
    }

    for(var i = 0; i < finalInfo.stations.length; i++){
        for(var j = 0; j < i; j++){
            var d = Dist(finalInfo.stations[i]["coords"], finalInfo.stations[j]["coords"])
            if(d < epsilon){
                finalInfo.edges.push([i, j, d, 0, 1.3]);
            }
        }
    }

    // console.log(JSON.stringify(finalInfo));

    resultGraph = {
        size: finalInfo.stations.length,
        nodes: finalInfo.stations,
        edges: finalInfo.edges,
    }

    result = JSON.stringify(resultGraph);

    fs.writeFileSync("./result.json", result);
});