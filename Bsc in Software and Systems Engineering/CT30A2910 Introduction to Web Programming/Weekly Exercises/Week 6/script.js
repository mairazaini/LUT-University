async function fetchPopulationData(areaCode) {
    try {
      const response = await fetch('https://statfin.stat.fi/PxWeb/api/v1/en/StatFin/synt/statfin_synt_pxt_12dy.px', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "query": [
            { "code": "Vuosi", "selection": { "filter": "item", "values": Array.from({length: 22}, (v, k) => (2000 + k).toString()) }},
            { "code": "Alue", "selection": { "filter": "item", "values": [areaCode] }},
            { "code": "Tiedot", "selection": { "filter": "item", "values": ["vaesto"] }}
          ],
          "response": { "format": "json-stat2" }
        })
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching population data:", error);
    }
  }
  function renderPopulationChart(labels, values) {
    const chart = new frappe.Chart("#chart", {
      title: "Population Growth in Whole Country",
      data: {
        labels: labels,
        datasets: [
          {
            name: "Population",
            values: values
          }
        ]
      },
      type: 'line',
      height: 450,
      colors: ['#eb5146']
    });
  }
  if (window.location.pathname.includes("index.html")) {
    window.onload = async function() {
      const data = await fetchPopulationData("SSS");
      const labels = data.dataset.dimension.Vuosi.category.label;
      const values = data.dataset.value;
      renderPopulationChart(Object.values(labels), values);
    };
    document.getElementById("submit-data").addEventListener("click", async function() {
      const areaCode = document.getElementById("input-area").value.toUpperCase();
      const data = await fetchPopulationData(areaCode);
      if (data) {
        const labels = data.dataset.dimension.Vuosi.category.label;
        const values = data.dataset.value;
        renderPopulationChart(Object.values(labels), values);
      }
    });
    document.getElementById("add-data").addEventListener("click", function() {
      const chart = document.querySelector('#chart').__chartist__.data;
      const values = chart.datasets[0].values;
      const diffs = values.slice(1).map((v, i) => v - values[i]);
      const meanDelta = diffs.reduce((acc, v) => acc + v, 0) / diffs.length;
      const nextValue = values[values.length - 1] + meanDelta;
      values.push(nextValue);
      renderPopulationChart(chart.labels, values);
    });
  
    document.getElementById("navigation").addEventListener("click", function() {
      window.location.href = "newchart.html";
    });
  }
  async function fetchBirthDeathData(areaCode) {
    const birthResponse = await fetch('https://statfin.stat.fi/PxWeb/api/v1/en/StatFin/synt/statfin_synt_pxt_12dy.px', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "query": [
          { "code": "Vuosi", "selection": { "filter": "item", "values": Array.from({length: 22}, (v, k) => (2000 + k).toString()) }},
          { "code": "Alue", "selection": { "filter": "item", "values": [areaCode] }},
          { "code": "Tiedot", "selection": { "filter": "item", "values": ["vm01"] }}
        ],
        "response": { "format": "json-stat2" }
      })
    });
  
    const deathResponse = await fetch('https://statfin.stat.fi/PxWeb/api/v1/en/StatFin/synt/statfin_synt_pxt_12dy.px', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "query": [
          { "code": "Vuosi", "selection": { "filter": "item", "values": Array.from({length: 22}, (v, k) => (2000 + k).toString()) }},
          { "code": "Alue", "selection": { "filter": "item", "values": [areaCode] }},
          { "code": "Tiedot", "selection": { "filter": "item", "values": ["vm11"] }}
        ],
        "response": { "format": "json-stat2" }
      })
    });
    const birthData = await birthResponse.json();
    const deathData = await deathResponse.json();
    return {
      years: Object.values(birthData.dataset.dimension.Vuosi.category.label),
      births: birthData.dataset.value,
      deaths: deathData.dataset.value
    };
  }
  function renderBirthDeathChart(years, births, deaths) {
    const chart = new frappe.Chart("#chart", {
      title: "Births and Deaths in Whole Country",
      data: {
        labels: years,
        datasets: [
          {
            name: "Births",
            values: births,
            chartType: 'bar',
            colors: ['#63d0ff']
          },
          {
            name: "Deaths",
            values: deaths,
            chartType: 'bar',
            colors: ['#363636']
          }
        ]
      },
      type: 'bar',
      height: 450
    });
  }
  if (window.location.pathname.includes("newchart.html")) {
    window.onload = async function() {
      const data = await fetchBirthDeathData("SSS");
      renderBirthDeathChart(data.years, data.births, data.deaths);
    };
    document.getElementById("navigation").addEventListener("click", function() {
      window.location.href = "index.html";
    });
  }
  