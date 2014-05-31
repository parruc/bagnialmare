$(function() {

    $("#rootContainer").on("show.bs.collapse", ".collapse", function () {
        $("#span"+this.id.toString()).removeClass('glyphicon-chevron-right').addClass("glyphicon-chevron-down");
    });

    $("#rootContainer").on("hide.bs.collapse", ".collapse", function () {
        $("#span"+this.id.toString()).removeClass('glyphicon-chevron-down').addClass("glyphicon-chevron-right");
    });

    $("#rootContainer").on('click', '.checkbox input', function(evt){
        showSpinner("#search-results");
        var url = $("#filters").data("base-url") + $(this).data('facet-url');
        var title = $(title).html()

        $.ajax({url:url,
                success:function(response) {
                    hideSpinner("#search-results");
                    $("#rootContainer").html($(response).find("#rootContainer").html());
                    window.scrollTo(0,0);
                    window.history.pushState({}, title, url);
                }
        });
    });

    $("#rootContainer").on("click", "#map-tab-button", function(evt) {
        var map = L.map('bagno_map');
        L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
            attribution: '',
            subdomains: ['otile1','otile2','otile3','otile4'],
            maxZoom: 18
        }).addTo(map);
        var map_markerBounds = new L.LatLngBounds();
        evt.preventDefault();
        $(this).tab('show');

        $("#bagniToBeMapped li").each(function(index, element){
            var p = new L.LatLng(parseFloat($(element).data("y")),
                                 parseFloat($(element).data("x")));
            map_markerBounds.extend(p);
            if($(element).attr('id') == "map_origin"){
                L.circleMarker(p).addTo(map)
                                 .bindPopup('<b class="my-bold">' +
                                            $(element).data("name") +
                                            '</b>');
            }else{
                L.marker(p, {icon: ombrelloneIcon}).addTo(map)
                           .bindPopup('<b class="my-bold"><a href=' +
                                      $(element).data("url") +
                                      '>' +
                                      $(element).data("name") +
                                      '</a></b> <em>' +
                                      $(element).data("address") +
                                      '</em>')
                           .openPopup();
            }
        });
        map.fitBounds(map_markerBounds);
    });
});
