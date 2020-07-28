
var panorama, map;
var markers = [], infoWindows = [];
var mapContainerDiv = document.getElementById("container")
var mapDiv = document.getElementById("map")
var panoDiv = document.getElementById("pano")
var lat, lng;
var pegMovingInSV = false

// const showMenu = () => {
//     // dont show the menu in panorama mode
//     document.querySelector("#menu-modal").style.display = "inline-block"
// }

// const hideMenu = () => {
//     document.querySelector("#menu-modal").style.display = "none"
// }


const showModal = () => {
    if (!panorama.getVisible()) return
    document.querySelector("#floating-modal").style.display = "inline-block"
}

const hideModal = () => {
    if (!panorama.getVisible()) return
    document.querySelector("#floating-modal").style.display = "none"
    document.querySelector("#modal-form-results").innerHTML = ""
}

const markerInfoClick = (marker, infoWindow) => {
    marker.addListener('click', function () {
        infoWindow.open(marker.map, marker);
    });
}

const clear_markers = () => {
    markers.forEach(m => m.setMap(null))
    markers = []
    $('#marker-container').empty()
}

const reset_markers = ms => {
    clear_markers()
    ms.forEach(m => {
        const mapMarker = document.createElement('map-marker')
        mapMarker.setAttribute('hidden', true)
        mapMarker.setAttribute('data-lat', m.lat)
        mapMarker.setAttribute('data-lng', m.lng)
        mapMarker.setAttribute('data-infoText', m.infoText)
        mapMarker.innerText = m.title
        $('#marker-container').append(mapMarker)
    })
    markers = create_markers('map-marker')
}

const changeMaps = (markers, map) => {
    markers.forEach(m => m.setMap(map))
}

const create_markers = query => [...document.querySelectorAll(query)].map(m => {
    const lng = parseFloat(m.getAttribute('data-lng'))
    const lat = parseFloat(m.getAttribute('data-lat'))
    const infoText = m.getAttribute('data-infoText')
    const title = m.innerText
    const label = title.length < 2 ? {
        text: title,
        fontWeight: 'bold',
        fontSize: '1.2em',
    } : ''
    const marker = new google.maps.Marker({
        position: { lat, lng },
        map,
        title,
        label,
    })
    const infoWindow = new google.maps.InfoWindow({
        content: `<p id="info-window">${infoText}</p>`,
        disableAutoPan: true,
    })

    infoWindows = [...infoWindows, infoWindow]
    markerInfoClick(marker, infoWindow)
    return marker
})


function initMap() {
    var tokyo = { lat: 35.689722, lng: 139.692222 };

    $("#menu-modal").dialog({
        autoOpen: false,
        maxWidth: 1200,
        maxHeight: 500,
        width: '50%',
        height: 500,
        modal: true,
    })

    /* create new panoramma to support picture in picture map */
    panorama = new google.maps.StreetViewPanorama(panoDiv, {
        enableCloseButton: true,
        addressControl: true,
        visible: false,
    })

    // Set up the map
    map = new google.maps.Map(mapDiv, {
        center: tokyo,
        zoom: 18,
        mapTypeId: 'satellite',
        streetView: panorama,
        streetViewControl: true,
        zoomControl: true,
        mapTypeControl: true,
        scaleControl: true,
        rotateControl: true,
        fullscreenControl: true,
        overviewMapControl: true,
    });

    // add drawing functionality

    // let drawingManager = new google.maps.drawing.DrawingManager({
    //     drawingControl: true,
    //     drawingControlOptions: {
    //         position: google.maps.ControlPosition.TOP_CENTER,
    //         drawingModes: ['circle', 'polygon', 'rectangle']
    //     },
    // });
    // drawingManager.setMap(map);

    // google.maps.event.addListener(drawingManager, 'overlaycomplete', e => e.overlay.setMap(null))

    // add menu button to map view
    const addMenuDiv = document.createElement("div")
    addMenuDiv.style.margin = "10px"
    addMenuDiv.classList.add('dropdown')
    addMenuDiv.classList.add('d-flex')
    const menuObj = new CreateMenuControl(addMenuDiv, map)
    addMenuDiv.index = 1

    const width = window.innerWidth || document.documentElement.clientWidth ||
        document.body.clientWidth;
    const posRightTop = google.maps.ControlPosition.TOP_CENTER
    const posLeftTop = google.maps.ControlPosition.LEFT_TOP
    const menuPosChangeWidth = 840
    let currentMenuPosition = width < menuPosChangeWidth ? posLeftTop : posRightTop
    const menuWidth = 'w-50'
    const menuHeight = 'h-25'
    addMenuDiv.classList.add(width < menuPosChangeWidth ? 'flex-column' : 'flex-row', 'justify-content-around')
    addMenuDiv.classList.add(width < menuPosChangeWidth ? menuHeight : menuWidth)
    map.controls[currentMenuPosition].push(addMenuDiv);

    const swapControls = (oldPos, newPos, element, map) => {
        const index = map.controls[oldPos].indexOf(element)
        if (index > -1) {
            map.controls[oldPos].removeAt(index)
            map.controls[newPos].push(addMenuDiv)
        }
    }

    // change control position based on screen width
    window.addEventListener('resize', () => {
        const width = window.innerWidth || document.documentElement.clientWidth ||
            document.body.clientWidth;
        const currentMap = panorama.getVisible() ? panorama : map
        if (width < menuPosChangeWidth && currentMenuPosition === posRightTop) {
            swapControls(posRightTop, posLeftTop, addMenuDiv, currentMap)
            currentMenuPosition = posLeftTop
            addMenuDiv.classList.remove('flex-row', menuWidth)
            addMenuDiv.classList.add('flex-column', menuHeight)
        } else if (width >= menuPosChangeWidth && currentMenuPosition == posLeftTop) {
            swapControls(posLeftTop, posRightTop, addMenuDiv, currentMap)
            currentMenuPosition = posRightTop
            addMenuDiv.classList.remove('flex-column', menuHeight)
            addMenuDiv.classList.add('flex-row', menuWidth)
        }
    })

    // add create marker element to panorama view
    const addMarkerDiv = document.createElement("div")
    addMarkerDiv.style.width = "40px"
    addMarkerDiv.style.height = "40px"
    addMarkerDiv.style.margin = "10px"
    const createMarkerObj = new CreateMarkerControl(addMarkerDiv, panorama)
    addMarkerDiv.index = 1
    panorama.controls[google.maps.ControlPosition.TOP_RIGHT].push(addMarkerDiv);

    // add refresh markers element to panorama view
    const refreshMarkersDiv = document.createElement("div")
    refreshMarkersDiv.style.width = "40px"
    refreshMarkersDiv.style.height = "40px"
    refreshMarkersDiv.style.margin = "10px"
    const refreshMarkersObj = new RefreshMarkersControl(refreshMarkersDiv, panorama)
    refreshMarkersDiv.index = 1
    panorama.controls[google.maps.ControlPosition.RIGHT_TOP].push(refreshMarkersDiv);

    infoWindows = [...document.querySelectorAll("info-window")].map(element => new google.maps.InfoWindow({
        content: element.innerHTML,
        disableAutoPan: true,
    }))

    markers = create_markers('map-marker')
    const panoLBControls = panorama.controls[google.maps.ControlPosition.LEFT_BOTTOM]
    let listeners = []
    let sl = new google.maps.StreetViewCoverageLayer()
    //set up panorama for display
    panorama.addListener("visible_changed", function () {
        if (panorama.getVisible() && $("#pano").is(':hidden')) {
            $("#pano").show();
            $("#map").removeClass('big-map');
            $("#map").addClass('pip-map');
            changeMaps(markers, panorama)

            // remove menu controls from map and add to pano
            const index = map.controls[currentMenuPosition].indexOf(addMenuDiv)
            if (index > -1) {
                map.controls[currentMenuPosition].removeAt(index)
                panorama.controls[currentMenuPosition].push(addMenuDiv)
            }

            panoLBControls.push(mapDiv)

            map.setOptions({
                streetViewControl: false,
                zoomControl: true,
                mapTypeControl: false,
                scaleControl: false,
                rotateControl: false,
                fullscreenControl: true,
                overviewMapControl: false,
            })
            mapDiv.style['border-radius'] = "10px"
            mapDiv.style['border'] = "2px solid black"
            let clickListener = map.addListener('click', e => panorama.setPosition(e.latLng))
            //mouse move is used incase pip map is initalized over the mouse
            let mouseOverListener = map.addListener("mousemove", () => {
                if (!sl.getMap()) {
                    sl.setMap(map)
                }
                pegMovingInSV = true
            })
            let mouseOutListener = map.addListener("mouseout", () => {
                sl.setMap(null)
                pegMovingInSV = false
            })
            listeners = [clickListener, mouseOverListener, mouseOutListener]
            //make sure menu modal isn't open
        }
    });

    //set up panorama for closing
    panorama.addListener("closeclick", function () {
        $("#pano").hide();
        $("#map").removeClass('pip-map');
        $("#map").addClass('big-map');
        changeMaps(markers, map)

        // remove menu controls from pano and add to map
        let menuIndex = panorama.controls[currentMenuPosition].indexOf(addMenuDiv)
        if (menuIndex > -1) {
            panorama.controls[currentMenuPosition].removeAt(menuIndex)
            map.controls[currentMenuPosition].push(addMenuDiv)
        }

        // remove pip-map from pano controls and add it back to container
        const mapIndex = panoLBControls.indexOf(mapDiv)
        if (mapIndex > -1) {
            const div = panoLBControls.removeAt(mapIndex)
            mapContainerDiv.append(div)
        }

        mapDiv.style['border-radius'] = "0px"
        mapDiv.style['border'] = "none"

        // reset the map default map controls 
        map.setOptions({
            streetViewControl: true,
            zoomControl: true,
            mapTypeControl: true,
            scaleControl: true,
            rotateControl: true,
            fullscreenControl: true,
            overviewMapControl: true,
        })

        //make sure add marker modal isn't open
        hideModal()

        //remove all pip map only listeners from the map
        listeners.forEach(listener => listener.remove())
    });

    //TODO: might be a better way to store current lat/ lng for use with add marker
    panorama.addListener('position_changed', () => {
        const pos = panorama.getPosition()
        lat = pos.lat()
        lng = pos.lng()

        // dont reposition the map while peg man is being dragged
        if (panorama.getVisible() && !pegMovingInSV) {
            map.setCenter(pos)
        }
    })
}

// add marker to map
const addMarker = (title, infoText) => {
    const marker = new google.maps.Marker({
        position: { lat, lng },
        map: panorama,
        title,
    })
    const infoWindow = new google.maps.InfoWindow({
        content: `<p class="info-window">${infoText}</p>`
    })
    infoWindows = [...infoWindows, infoWindow]
    markers = [...markers, marker]
    markerInfoClick(marker, infoWindow)
}

// add marker to database
function create_marker(title, infoText, palace, path) {
    $.ajax({
        url: "/ajax/create_marker/", // the endpoint
        type: "POST", // http method
        data: { title, infoText, lat, lng, palace, path }, // data sent with the post request

        // handle a successful response
        success: function (json) {
            addMarker(json.title, json.infoText)
            document.querySelector("#floating-modal").style.display = "none"
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#modal-form-results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// load palace paths dynamically
function ajax_load(url, success, errorDivId, method = "GET") {
    $.ajax({
        url: url,
        type: method,
        success: success,
        error: function (xhr, errmsg, err) {
            $(`#${errorDivId}`).html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
};

$("#modal-form").on('submit', event => {
    event.preventDefault()
    const title = $('#id_title').val()
    const infoText = $('#id_infoText').val()
    const palace = currentPalace.pk
    const path = currentPath.pk
    console.log(palace, path)
    create_marker(title, infoText, palace, path)
})

function CreateMarkerControl(controlDiv, map) {
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'rgb(34, 34, 34)';
    controlUI.style.border = '0px';
    controlUI.style.borderRadius = '2px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.style.userSelect = "none"
    controlUI.title = 'Click to add a marker to the map';
    controlDiv.appendChild(controlUI);

    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(221,224,216)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = 'M';
    controlUI.appendChild(controlText);

    controlUI.addEventListener('click', function () {
        if ($("#floating-modal").is(":visible")) {
            hideModal()
        } else {
            showModal()
        }
    });
}

function createDropdown(wrapper, text) {
    const div = document.createElement('div')
    div.classList.add('btn-group')
    const createButton = document.createElement('button')
    createButton.classList.add("btn", "btn-dark")
    createButton.style['width'] = "50px"
    createButton.innerText = "+"
    div.appendChild(createButton)

    const button = document.createElement('button')
    button.style['width'] = "100px"
    button.classList.add("btn", "btn-light", "dropdown-toggle")
    button.type = "button"
    button.setAttribute("data-toggle", "dropdown")
    button.setAttribute("aria-haspopup", "true")
    button.setAttribute("aria-expanded", "false")
    button.setAttribute("id", "dropdownMenu")
    button.innerText = text
    div.appendChild(button);

    const container = document.createElement('div');
    container.classList.add("dropdown-menu")
    container.style['max-height'] = "200px"
    container.style['max-width'] = "400px"
    container.style['overflow-y'] = "auto"
    container.setAttribute("aria-labelledby", "dropdownMenu")
    div.appendChild(container);

    wrapper.appendChild(div)
    return container

}

let currentPalace, currentPath, currentMarker

function CreateMenuControl(container, map) {
    const palaceDrop = createDropdown(container, 'Palaces')
    const pathDrop = createDropdown(container, 'Paths')
    const markerDrop = createDropdown(container, 'Markers')

    const markerSuccess = response => {
        const ms = JSON.parse(response)
        markerDrop.innerHTML = ""
        let newMarkers = []
        ms.forEach((e, i) => {
            const pos = { lat: e.lat, lng: e.lng }
            if (i == 0 && !panorama.getVisible()) {
                map.setCenter(pos)
            }
            newMarkers.push(e)
            console.log(e)
            let menuItem = document.createElement('button');
            menuItem.innerText = e.title.trunc(30)
            menuItem.classList.add("dropdown-item")
            menuItem.setAttribute('type', 'button')
            markerDrop.appendChild(menuItem);
            menuItem.addEventListener('click', () => {
                currentMarker = e
                if (!panorama.getVisible()) {
                    map.setCenter(pos)
                }
            })
        })
        reset_markers(newMarkers)
        console.log("new markers", markers)
    }

    const pathSuccess = response => {
        const ms = JSON.parse(response)
        pathDrop.innerHTML = ""
        ms.forEach((e, i) => {
            if (i == 0) {
                ajax_load(`/ajax/${e.pk}/get_markers`, markerSuccess, errorDivId)
            }
            let menuItem = document.createElement('button');
            menuItem.innerText = e.title.trunc(30)
            menuItem.classList.add("dropdown-item")
            menuItem.setAttribute('type', 'button')
            pathDrop.appendChild(menuItem);
            menuItem.addEventListener('click', () => {
                currentPath = e
                ajax_load(`/ajax/${e.pk}/get_markers`, markerSuccess, errorDivId)
            })
        })
    }

    const success = response => {
        const ms = JSON.parse(response)
        palaceDrop.innerHTML = ""
        ms.forEach((e, i) => {
            if (i == 0) {
                ajax_load(`/ajax/${e.pk}/get_paths`, pathSuccess, errorDivId)
            }
            let menuItem = document.createElement('button');
            menuItem.innerText = e.title.trunc(30)
            menuItem.classList.add("dropdown-item")
            menuItem.setAttribute('type', 'button')
            palaceDrop.appendChild(menuItem);
            menuItem.addEventListener('click', () => {
                currentPalace = e
                ajax_load(`/ajax/${e.pk}/get_paths`, pathSuccess, errorDivId)
            })
        })
    }
    const errorDivId = 'menu-modal-error'
    ajax_load('/ajax/get_palaces', success, errorDivId)
}

function RefreshMarkersControl(controlDiv, map) {
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'rgb(34, 34, 34)';
    controlUI.style.border = '0px';
    controlUI.style.borderRadius = '2px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.style.userSelect = "none"
    controlUI.title = 'Click to reload map markers';
    controlDiv.appendChild(controlUI);

    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(221,224,216)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = 'R';
    controlUI.appendChild(controlText);

    const success = response => {
        const ms = JSON.parse(response)
        reset_markers(ms)
    }
    const errorDivId = 'menu-modal-error'
    controlUI.addEventListener('click', function () {
        ajax_load('/ajax/load_markers', success, errorDivId)
    });
}

$(function () {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

// utility
String.prototype.trunc =
    function (n) {
        return this.substr(0, n - 1) + (this.length > n ? '...' : '');
    };