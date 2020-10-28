function addMarker (map,myLatLng)
{
		 var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: 'THIS YOUR FUCKING LOCATION',
		  animation:google.maps.Animation.BOUNCE,

        });
      }

function loaddata (map,link){
	map.data.loadGeoJson(link);
}

