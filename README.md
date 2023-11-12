
<br />
 <p align="center">
  <h1 align="center">CO₂ Route Calculator</h1>
    <p align="center">
    UPC Sostenible Challenge - Datathon 2023
    <br />
</p>

We're excited to submit our comprehensive solution to address the complexities of urban mobility for UPC students. This ReadMe document provides an overview of the work we've done and the contents of our submission.

# Overview of the project

## 1. Understanding Transportation Choices
In this section, we present a detailed analysis of the factors influencing students' transportation choices. We've explored various aspects such as , convenience, comfortability and environmental consciousness.

## 2. Data Visualization Solution
We've developed a powerful data visualization solution to summarize the people flow generated daily by UPC students, categorized by transportation mode. 

## 3. Carbon Footprint Calculator
We've carefully considered the use of GTFS data, to build our CO2 calculator, with the help of other AI tools. The proposal includes detailed explanations, supported by data and reasoning.

## Conclusion
We appreciate the opportunity to contribute to the Urban Mobility Challenge and are eager to receive your feedback. We hope that our comprehensive solution aligns with the goals of improving urban mobility for UPC students while minimizing environmental impact.

# Contents

## Generating data

We made an extensive Python script collection for extracting data from the provided datasets.

In the `script` folder, there are some scripts that parse the date and converts it into a more readable format for Kepler. Some of the more important scripts are:
- `generate_boxes.py` generates and extrapolates all information about the location of the students. It does geodecoding for translating postal codes into bounding boxes of global coordinates, and then it assigns random locations for each student inside that area. It generates the file `boxes.csv`
- `analysis.py` generates the final data for the visualization. It gets from our dynamic model the approximation of the carbon footprint of each student, and then it writes all the data into `cp-uni.csv`

All the other python scripts are auxiliary to these two.

## The dynamic model

We extracted data from the datasets of TMB Metro lines, TMB Bus lines, TRAM, Rodalies and FGC. Our model generates an unified .json that contains a dataset that represents a weighted graph. Each node represents an station, and each edge is a connection between two stations connected by a line of any service. The edges also have weights about the carbon footprint made by traversing with that line, and also the estimated distance and time to traverse.

Later, we applied a weighted Dijkstra algorithm to find the most optimal environment friendly route. This model takes to consideration if it is better to walk or ride a bike to a nearby station, an also takes in consideration if it is better in some cases to go by car.

To generate the graph, we used [gtfs-to-geojson](https://github.com/BlinkTagInc/gtfs-to-geojson/) to transform all gtfs files into geojson and then we parsed it ourself by the method described above. This code is written with JavaScript and can be found in the folder `geojson-to-graph`. You can run it by placing all the .geojson files into `geojson-to-graph/geojson` folder, and then running
```
npm install
node index.js
```
Then the algorithm will ask for every line if you want to include it or not (leave it blank if you want to include). Sometimes it might ask about the type of line. This is used for the approximation of the carbon footprint, so answer what it may seem more similar to the type of transport. And then, it will ask about the average speed of the line.

## Visualization of data

The dynamic model outputs a `result.json` file that can be visualized. We used [kepler.gl](https://kepler.gl/) for this task.

The visualizator can be found in the folder `data-visualizer`, and can be run with

```
npm install
npm start
```

## Web calculator

Finally, for integrating all of these small projects, we made an small web calculator integrated with [OpenStreetMap](https://www.openstreetmap.org/) for computing using our dynamic model an estimate of the carbon footprint of the commuters of UPC (and of any location registred by OpenStreetMap inside Catalonia in general).

The frontend of this calculator is written with [Vue](https://vuejs.org/). It can be found in the folder `upc-sostenible-vis` and the backend is an small Python script written with [Flask](https://flask.palletsprojects.com/en/3.0.x/) and it can be found in `scripts/app.py`.

For launching the development environment of the front-end use
```
npm install
npm run dev
```

and run the `app.py` python script for the backend.