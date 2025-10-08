import L from 'leaflet';

export function initMap() {
  const map = L.map('app').setView([1.3521, 103.8198], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);
  return map;
}
