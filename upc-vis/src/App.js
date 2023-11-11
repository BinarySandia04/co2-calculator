import logo from './logo.svg';
import './App.css';

import React, { useEffect, useState } from "react";
import KeplerGl from "kepler.gl";
import { addDataToMap } from "kepler.gl/actions";
import { useDispatch } from "react-redux";
import helpers from "./helpers";

const DATA_URL = "Your data URL";

const sampleConfig = {
  visState: {
    filters: [
      {
        id: "dateFilter_id",
        dataId: "date_id",
        name: "",//the name of the column to be filtered
        type: "timeRange",//filter type to be use
      },
    ],
      
  },

  mapStyle: {
    styleType: 'light'
  }
};

function Map() {
  const dispatch = useDispatch();
  const [data, setData] = useState();

  const fetchData = async () => {
    setData(await helpers.httpGet(DATA_URL));
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    data &&
      dispatch(
        addDataToMap({
          datasets: {
            info: {
              label: "RECENT EARTHQUAKES IN TURKEY AND ITS ENVIRONMENT",
              id: "EARTHQUAKES",
            },
            data: data,
          },
          option: {
            centerMap: true,
            readOnly: false,
          },
          config: sampleConfig,
        })
      );
  }, [dispatch, data]);
  return (
    <KeplerGl 
      id="map" 
      width={window.innerWidth} 
      height={window.innerHeight} 
      mapboxApiAccessToken="pk.eyJ1Ijoic2FuZGlhOTgiLCJhIjoiY2xvdTZpZW1kMGd5djJsczFramo5dzRpcyJ9.yxs624By4eemQrtjfgakLA" 
    />
    
      );
}

export default Map;
