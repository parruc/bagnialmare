var map
$(function() {
    var bagno_x = $("#bagno_map").data("x")
    var bagno_y = $("#bagno_map").data("y")
    var bagno_name = $("#bagno_map").data("name")
    var bagno_address = $("#bagno_map").data("address")
    map = L.map('bagno_map').setView([bagno_y, bagno_x], 13);
    L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
        attribution: 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.',
        subdomains: ['otile1','otile2','otile3','otile4'],
        maxZoom: 18
    }).addTo(map);
    var marker = L.marker([bagno_y, bagno_x]).addTo(map);
    marker.bindPopup('<b class="my-bold">'+ bagno_name +'</b><br /><em>' + bagno_address + '</em>').openPopup();
});
