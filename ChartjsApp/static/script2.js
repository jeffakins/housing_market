let chartInstance = null;

async function loadData() {
  const response = await fetch("/citydata");   // updated endpoint
  const dataset = await response.json();

  const citySelect = document.getElementById("citySelect");

  // Populate dropdown
  Object.keys(dataset.cities).forEach(city => {
    const option = document.createElement("option");
    option.value = city;
    option.textContent = city;
    citySelect.appendChild(option);
  });

  // Initial chart render
  renderChart(dataset, Object.keys(dataset.cities)[0]);

  // Update chart when dropdown changes
  citySelect.addEventListener("change", (e) => {
    renderChart(dataset, e.target.value);
  });
}

function renderChart(dataset, selectedCity) {
  const ctx = document.getElementById("cityChart").getContext("2d");

  if (chartInstance) chartInstance.destroy();

  // Build [{x, y}, ...] points
  const points = dataset.dates.map((d, i) => ({
    x: d,
    y: dataset.cities[selectedCity][i]
  }));

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {
          label: selectedCity,
          data: points,
          borderColor: "blue",
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          type: "time",
          time: {
            unit: "month"
          }
        },
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

loadData();

