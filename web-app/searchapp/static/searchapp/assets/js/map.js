$(document).ready(function() {
    var latlng = new google.maps.LatLng("{{ res.location.lat }}", "{{ res.location.lon }}");
    var mapOptions = {
        zoom: 15,
        center: latlng,
        mapTypeControl: false,
        navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map($('.map')[0], mapOptions);

    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title:"{{ res.name }}"
    });
});