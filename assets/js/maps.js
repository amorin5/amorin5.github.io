import { getData } from "./firebase.js"

let map;

async function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.073051, lng: -89.401230 },
    zoom: 14,
  });

  const d2 = await getData();

  d2.forEach((doc) => {
    //db debug
    const latlong = doc.data();
    console.log(doc.id, " => ", latlong);
    new google.maps.Marker({
      position: { lat: latlong.lat, lng: latlong.long},
      map: map,
    });
  });

}

window.initMap = initMap;
