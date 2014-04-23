$(function() {

    drawMap();
    $("body").on("shown.bs.collapse", ".collapse", function () {
        $("#span"+this.id.toString()).removeClass('glyphicon-chevron-right').addClass("glyphicon-chevron-down")
    });
    $("body").on('hidden.bs.collapse', ".collapse", function () {
        $("#span"+this.id.toString()).removeClass('glyphicon-chevron-down').addClass("glyphicon-chevron-right")
    });

    $("body").on('click', '.checkbox input', function(evt){
        $("body").addClass("loading");
        var url = $("#filters").data("base-url") + $(this).data('facet-url');
        var title = $(title).html()

        $.ajax({url:url, 
                success:function(response) {
                    $("body").removeClass("loading");
                    $("#rootContainer").html($(response).find("#rootContainer").html());
                    window.scrollTo(0,0);
                    window.history.pushState({}, title, url)
                }
        });
    });
});

function drawMap(){
    L.Icon.Default.imagePath = '/static/js/images/';
    var map = L.map('bagno_map');
    L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
        attribution: 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.',
        subdomains: ['otile1','otile2','otile3','otile4'],
        maxZoom: 18
    }).addTo(map);
    var map_markerBounds = new L.LatLngBounds();
    $("#bagniToBeMapped li").each(function(index, element){
            var p = new L.LatLng(parseFloat($(element).data("y")),
                                 parseFloat($(element).data("x")));
            var marker = L.marker(p).addTo(map);
            map_markerBounds.extend(p);
            marker.bindPopup('<b class="my-bold"><a href=' +
                             $(element).data("url") +
                             '>' +
                             $(element).data("name") +
                             '</a></b> <em>' +
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
