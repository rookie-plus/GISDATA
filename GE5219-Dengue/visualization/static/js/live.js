import { initMap } from '../../app.js';

const map = initMap();

async function refreshClusters() {
  try {
    const response = await fetch('/api/dengue/latest');
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }
    const geojson = await response.json();
    // TODO: Visualise clusters
    console.debug('Fetched clusters', geojson);
  } catch (error) {
    console.error('Cluster refresh error', error);
  }
}

refreshClusters();
setInterval(refreshClusters, 5 * 60 * 1000);
