// Initialize map for attraction detail page
function initMap(lat, lng, title) {
    // Check if the coordinates are provided
    if (!lat || !lng) {
        console.error('No coordinates provided for the map');
        return;
    }
    
    // Create map centered at the attraction
    const attractionCoords = { lat: parseFloat(lat), lng: parseFloat(lng) };
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: attractionCoords,
        mapTypeId: 'roadmap'
    });
    
    // Add marker for the attraction
    const marker = new google.maps.Marker({
        position: attractionCoords,
        map: map,
        title: title,
        animation: google.maps.Animation.DROP
    });
    
    // Add info window
    const infoWindow = new google.maps.InfoWindow({
        content: `<strong>${title}</strong>`
    });
    
    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });
    
    // Load nearby restaurants and activities if available
    loadNearbyPlaces(map, attractionCoords);
}

// Load nearby restaurants and activities
function loadNearbyPlaces(map, attractionCoords) {
    // Get nearby restaurants
    const restaurants = document.querySelectorAll('.restaurant-data');
    restaurants.forEach(restaurant => {
        const lat = parseFloat(restaurant.getAttribute('data-lat'));
        const lng = parseFloat(restaurant.getAttribute('data-lng'));
        const name = restaurant.getAttribute('data-name');
        
        if (lat && lng) {
            addMarker(map, { lat, lng }, name, 'restaurant');
        }
    });
    
    // Add restaurants and activities to the map
    function addMarker(map, position, title, type) {
        let icon;
        
        // Set marker icon based on type
        if (type === 'restaurant') {
            icon = {
                url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            };
        } else {
            icon = {
                url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            };
        }
        
        // Create marker
        const marker = new google.maps.Marker({
            position: position,
            map: map,
            title: title,
            icon: icon
        });
        
        // Add info window
        const infoWindow = new google.maps.InfoWindow({
            content: `<strong>${title}</strong><br>${type}`
        });
        
        marker.addListener('click', function() {
            infoWindow.open(map, marker);
        });
    }
}

// Initialize map for all attractions page
function initAttractionsMap() {
    // Create map centered at Egypt
    const egyptCoords = { lat: 26.8206, lng: 30.8025 };
    const map = new google.maps.Map(document.getElementById('attractions-map'), {
        zoom: 6,
        center: egyptCoords,
        mapTypeId: 'roadmap'
    });
    
    // Fetch attractions data from API
    fetch('/api/attractions')
        .then(response => response.json())
        .then(attractions => {
            // Add markers for each attraction
            attractions.forEach(attraction => {
                if (attraction.latitude && attraction.longitude) {
                    const marker = new google.maps.Marker({
                        position: { lat: attraction.latitude, lng: attraction.longitude },
                        map: map,
                        title: attraction.name,
                        animation: google.maps.Animation.DROP
                    });
                    
                    // Add info window with link to attraction
                    const infoWindow = new google.maps.InfoWindow({
                        content: `
                            <strong>${attraction.name}</strong><br>
                            <a href="/attraction/${attraction.id}">View details</a>
                        `
                    });
                    
                    marker.addListener('click', function() {
                        infoWindow.open(map, marker);
                    });
                }
            });
        })
        .catch(error => console.error('Error loading attractions data:', error));
}
