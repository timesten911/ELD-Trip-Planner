import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons
const createCustomIcon = (color) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background-color: ${color}; width: 25px; height: 25px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
    iconSize: [25, 25],
    iconAnchor: [12, 12],
  });
};

const FitBounds = ({ bounds }) => {
  const map = useMap();
  
  useEffect(() => {
    if (bounds && bounds.length > 0) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [bounds, map]);
  
  return null;
};

const RouteMap = ({ routeData }) => {
  if (!routeData) {
    return (
      <div className="w-full h-[500px] bg-muted rounded-lg flex items-center justify-center">
        <p className="text-muted-foreground">Enter trip details to see route</p>
      </div>
    );
  }

  const { current_location, pickup_location, dropoff_location, route_to_pickup, route_to_dropoff } = routeData;

  // Extract coordinates
  const currentCoords = current_location.coordinates;
  const pickupCoords = pickup_location.coordinates;
  const dropoffCoords = dropoff_location.coordinates;

  // Decode polyline for route visualization
  const decodePolyline = (geometry) => {
    if (!geometry) return [];
    
    // Check if geometry is GeoJSON
    if (geometry.coordinates) {
      return geometry.coordinates.map(coord => [coord[1], coord[0]]);
    }
    
    // Otherwise assume it's encoded polyline string
    const coords = [];
    let index = 0, len = geometry.length;
    let lat = 0, lng = 0;

    while (index < len) {
      let b, shift = 0, result = 0;
      do {
        b = geometry.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      const dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
      lat += dlat;

      shift = 0;
      result = 0;
      do {
        b = geometry.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      const dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
      lng += dlng;

      coords.push([lat / 1e5, lng / 1e5]);
    }

    return coords;
  };

  const routeToPickupCoords = route_to_pickup.geometry ? decodePolyline(route_to_pickup.geometry) : [];
  const routeToDropoffCoords = route_to_dropoff.geometry ? decodePolyline(route_to_dropoff.geometry) : [];

  // Calculate bounds for all points
  const allPoints = [
    currentCoords,
    pickupCoords,
    dropoffCoords,
    ...routeToPickupCoords,
    ...routeToDropoffCoords
  ];

  const center = pickupCoords;

  return (
    <div className="w-full h-[500px] rounded-lg overflow-hidden border shadow-sm">
      <MapContainer
        center={center}
        zoom={6}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <FitBounds bounds={allPoints} />

        {/* Current Location Marker */}
        <Marker position={currentCoords} icon={createCustomIcon('#3b82f6')}>
          <Popup>
            <strong>Current Location</strong><br />
            {current_location.address}
          </Popup>
        </Marker>

        {/* Pickup Location Marker */}
        <Marker position={pickupCoords} icon={createCustomIcon('#10b981')}>
          <Popup>
            <strong>Pickup Location</strong><br />
            {pickup_location.address}
          </Popup>
        </Marker>

        {/* Dropoff Location Marker */}
        <Marker position={dropoffCoords} icon={createCustomIcon('#ef4444')}>
          <Popup>
            <strong>Dropoff Location</strong><br />
            {dropoff_location.address}
          </Popup>
        </Marker>

        {/* Route to Pickup */}
        {routeToPickupCoords.length > 0 && (
          <Polyline
            positions={routeToPickupCoords}
            color="#3b82f6"
            weight={4}
            opacity={0.7}
          />
        )}

        {/* Route to Dropoff */}
        {routeToDropoffCoords.length > 0 && (
          <Polyline
            positions={routeToDropoffCoords}
            color="#10b981"
            weight={4}
            opacity={0.7}
          />
        )}
      </MapContainer>
    </div>
  );
};

export default RouteMap;
