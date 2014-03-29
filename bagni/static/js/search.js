$(function() {

    drawMap();
    registerCollapseEvents();

});

function drawMap(){
    var map = L.map('bagno_map');
    L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
        attribution: 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.',
        subdomains: ['otile1','otile2','otile3','otile4'],
        maxZoom: 18
    }).addTo(map);
    var map_markerBounds = new L.LatLngBounds();
    $("#bagniToBeMapped li").each(function(index, element){
            var p = new L.LatLng(parseFloat($(element).data("y").replace(",",".")),
                                 parseFloat($(element).data("x").replace(",",".")));
            var marker = L.marker(p).addTo(map);
            map_markerBounds.extend(p);
            marker.bindPopup('<span class="my-bold"><a href=' +
                             $(element).data("url") +
                             '>' +
                             $(element).data("name") +
                             '</a></span> <em>' +
                             $(element).data("address") +
                             '</em>').openPopup();
            });
    map.fitBounds(map_markerBounds);
    $("#myTab a").click(function (e) {
            e.preventDefault();
            $(this).tab('show');
            //TODO: the following should be done only if tab == map
            map.invalidateSize(false);
            map.fitBounds(map_markerBounds);
        });
};

function checkboxChanged(cb) {
    var bodyTag = $("body");
    var base_url = $("#filters").data("base-url");

    bodyTag.addClass("loading");
    var url = base_url + $(cb).data('facet-url') + " #wrapped";
    $("#rootContainer").load(url, function(response, status, xhr) {
        bodyTag.removeClass("loading");
        window.scrollTo(0,0);
        drawMap();
        registerCollapseEvents();
      }
    );
};

function registerCollapseEvents(){
    $(".collapse").on("shown.bs.collapse", function () {
         $("#span"+this.id.toString()).removeClass('glyphicon-chevron-right').addClass("glyphicon-chevron-down")
    });
    $(".collapse").on('hidden.bs.collapse', function () {
         $("#span"+this.id.toString()).removeClass('glyphicon-chevron-down').addClass("glyphicon-chevron-right")
    });
};