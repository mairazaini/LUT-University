// Fetch GeoJSON data
fetch('https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:kunta4500k&outputFormat=json&srsName=EPSG:4326')
  .then(response => response.json())
  .then(data => {
    // Initialize the map
    const map = L.map('map', {
      minZoom: -3
    }).setView([65, 25], 6);

    // Add OpenStreetMap background layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Fetch migration data
    Promise.all([
      fetch('https://statfin.stat.fi/PxWeb/sq/4bb2c735-1dc3-4c5e-bde7-2165df85e65f').then(response => response.json()),
      fetch('https://statfin.stat.fi/PxWeb/sq/944493ca-ea4d-4fd9-a75c-4975192f7b6e').then(response => response.json())
    ]).then(([positiveDataRaw, negativeDataRaw]) => {
      // Extract necessary data
      const positiveData = positiveDataRaw.dataset.value;
      const negativeData = negativeDataRaw.dataset.value;
      const municipalities = positiveDataRaw.dataset.dimension.Tuloalue.category.label;

      function getColor(positive, negative) {
        const ratio = positive / negative;
        const hue = Math.min(Math.pow(ratio, 3) * 60, 120); // Hue is capped at 120
        return `hsl(${hue}, 75%, 50%)`;
      }

      function onEachFeature(feature, layer) {
        const municipalityName = feature.properties.name;
        const positiveIndex = municipalities[municipalityName] || 0;
        const positiveMigration = positiveData[positiveIndex] || 0;
        const negativeMigration = negativeData[positiveIndex] || 0;

        layer.bindTooltip(municipalityName);

        // Popup on click with positive and negative migration
        layer.bindPopup(`<b>${municipalityName}</b><br>Positive Migration: ${positiveMigration}<br>Negative Migration: ${negativeMigration}`);
      }

      // Add GeoJSON layer with dynamic colors
      const geoJsonLayer = L.geoJson(data, {
        style: function(feature) {
          const municipalityName = feature.properties.name;
          const positiveIndex = municipalities[municipalityName] || 0;
          const positiveMigration = positiveData[positiveIndex] || 0;
          const negativeMigration = negativeData[positiveIndex] || 0;

          return {
            color: getColor(positiveMigration, negativeMigration),
            weight: 2
          };
        },
        onEachFeature: onEachFeature
      }).addTo(map);

      // Fit the map to the GeoJSON data bounds
      map.fitBounds(geoJsonLayer.getBounds());
    });
  });
