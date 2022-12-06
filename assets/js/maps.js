import { getData } from "./firebase.js"

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.073051, lng: -89.401230 },
    zoom: 8,
  });

  let d2 = getData();

  
}

window.initMap = initMap;
