/*
* Javascript functions to set up the map menu options
*/


/**
 * Function returning the right click position coordinates
 * @param {Object} currentLatLng: latlng obbject of the right click event  
 * @param {Object} map: the Map 
 * @return {Object} Maps Point 
 */
var getCanvasXY = function (currentLatLng, map) {
    var scale = Math.pow(2, map.getZoom());
    var nw = new google.maps.LatLng(
        map.getBounds().getNorthEast().lat(),
        map.getBounds().getSouthWest().lng()
    );
    var worldCoordinateNW = map.getProjection().fromLatLngToPoint(nw);
    var worldCoordinate = map.getProjection().fromLatLngToPoint(currentLatLng);
    var currentLatLngOffset = new google.maps.Point(
        Math.floor((worldCoordinate.x - worldCoordinateNW.x) * scale),
        Math.floor((worldCoordinate.y - worldCoordinateNW.y) * scale)
    );
    return currentLatLngOffset;
    
}


/**
 * Set the menu CSS options close to where the user clicked 
 * and the size of the map
 * @param {Object} currentLatLng: latlng of the right click event  
 * @param {Object} map: The map 
 */
var setMenuXY = function (currentLatLng, map) {
    var mapWidth = $('#map_container').width();
    var mapHeight = $('#map_container').height();
    var menuWidth = $('.contextmenu').width();
    var menuHeight = $('.contextmenu').height();
    var clickedPosition = getCanvasXY(currentLatLng, map);

    var x = clickedPosition.x ;
    var y = clickedPosition.y ;
    
    if((mapWidth - x ) < menuWidth)
        x = x - menuWidth;
    if((mapHeight - y ) < menuHeight)
        y = y - menuHeight;
    
    $('.contextmenu').css('left',x  );
    $('.contextmenu').css('top',y );
};


/**
 * This function updates the map from the new latitude and
 * longitude chosen by the user right click.
 * It will get the hidden latitude and longitude values and
 * render the new truck view that will center the map to this
 * new position as well as fetching the correct trucks based 
 * on the current category and distance values.
 * @param {Object} latitude: latitude of the right click event
 * @param {Object} longitude: longitude of the right click event
 * @param {Object} trucksView: The truck collection view
 */
var updateLatLongitude = function (latitude, longitude, trucksView) {
    
    var latInput = trucksView.$el.find('#getTrucks #latitude'),
        lngInput = trucksView.$el.find('#getTrucks #longitude'),
        button = document.getElementById('addingLocation');

    button.addEventListener("click", function (event) {
        latInput.val(latitude);
        lngInput.val(longitude);
        trucksView.renderList();
    }, latitude, longitude, latInput, lngInput, trucksView);
};


/**
 * Function that shows the right click menu of the map to
 * allow the user to change the central location and find
 * the new trucks close to this new location.
 * @param {Object} currentLatLng: latlng of the right click event
 * @param {Object} trucksView: The truck collection view 
*/
var showContextMenu = function (currentLatLng, trucksView) {

    var contextmenuDir;

    // Clean the previous context menu and add the new one
    $('.contextmenu').remove();
    contextmenuDir = document.createElement("div");
    contextmenuDir.className  = 'contextmenu';
    contextmenuDir.innerHTML = "<div id='addingLocation'><div class=context>Check at this location<\/div><\/div>";

    $(trucksView.map.getDiv()).append(contextmenuDir);
    setMenuXY(currentLatLng, trucksView.map);
    contextmenuDir.style.visibility = "visible";

    // Adding the event on clicking to the addingLocation link
    var latitude = currentLatLng.lat(), 
        longitude = currentLatLng.lng();
    
    // Update the map with this new location center
    updateLatLongitude(latitude, longitude, trucksView);

};



/**
 * Function that cleans any remaining contextmenu div left behind
*/
var clearSetMenu = function () {
    $('.contextmenu').remove();
};
