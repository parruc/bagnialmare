var map
$(function() {
    var bagno_x = $("#bagno_map").data("x")
    var bagno_y = $("#bagno_map").data("y")
    var bagno_name = $("#bagno_map").data("name")
    var bagno_address = $("#bagno_map").data("address")
    map = L.map('bagno_map').setView([bagno_y, bagno_x], 13);
    L.tileLayer('http://b.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '',
        subdomains:'1234',
        maxZoom: 18
    }).addTo(map);
    var marker = L.marker([bagno_y, bagno_x], {icon: ombrelloneIcon}).addTo(map);
    marker.bindPopup('<b class="my-bold">'+ bagno_name +'</b><br /><em>' + bagno_address + '</em>').openPopup();
});
