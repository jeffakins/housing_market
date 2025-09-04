let chartInstance = null;
let datasetCache = null;

async function loadData() {
  const response = await fetch("/citydata");
  datasetCache = await response.json();

  const citySelect = $("#citySelect");

  // Populate dropdown
  Object.keys(datasetCache.cities).forEach(city => {
    const option = new Option(city, city, false, false);
    citySelect.append(option);
  });

  // Initialize Select2
  citySelect.select2({
    placeholder: "Choose cities...",
    allowClear: true
  });

  // Render chart when selection changes
  citySelect.on("change", () => {
    const selectedCities = citySelect.val();
    renderChart(selectedCities);
  });

  // Render with first city pre-selected
  citySelect.val([Object.keys(datasetCache.cities)[0]]).trigger("change");
}

function renderChart(selectedCities) {
  const ctx = document.getElementById("cityChart").getContext("2d");

  if (chartInstance) chartInstance.destroy();

  const datasets = selectedCities.map(city => {
    const points = datasetCache.dates.map((d, i) => ({
      x: d,
      y: datasetCache.cities[city][i]
    }));

    return {
      label: city,
      data: points,
      borderColor: getRandomColor(),
      fill: false
    };
  });

  chartInstance = new Chart(ctx, {
    type: "line",
    data: { datasets },
    options: {
      responsive: true,
      scales: {
        x: {
          type: "time",
          time: { unit: "month" }
        },
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Utility: generate random colors for lines
function getRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

loadData();
