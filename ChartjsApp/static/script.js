// --- Chart.js Code ---

/**
 * Renders the chart using the data fetched from the backend.
 * @param {object} chartData - The data object for the chart.
 */
function renderChart(chartData) {
    // 1. Get the canvas element from the HTML
    const ctx = document.getElementById('myChart').getContext('2d');

    // 2. Define the configuration and options for the chart
    const chartConfig = {
        type: 'line',
        data: chartData, // Use the data passed into the function
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#000',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 6,
                    displayColors: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#e5e7eb' // Lighter grid lines
                    }
                },
                x: {
                    grid: {
                        display: false // Hide vertical grid lines
                    }
                }
            }
        }
    };

    // 3. Create the new chart instance
    const myChart = new Chart(ctx, chartConfig);
}

/**
 * Fetches data from the backend and then calls the renderChart function.
 */
async function fetchDataAndCreateChart() {
    try {
        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const chartData = await response.json();
        renderChart(chartData);
    } catch (error) {
        console.error("Could not fetch chart data:", error);
    }
}

// Fetch the data and create the chart when the script loads.
fetchDataAndCreateChart();

