// Revenue and Earnings Chart using Chartjs
async function fetchData() {
    const response = await fetch('/financials'); // Fetch data from server
    const data = await response.json();

    const labels = data.map(entry => entry.year); // Dates
    const valuesRevenue = data.map(entry => entry.revenue); // Revenue 
    const valuesEarnings = data.map(entry => entry.earnings); // Earnings
    const valuesShares = data.map(entry => entry.shares); // Shares 
    const valuesDebt = data.map(entry => entry.debt); // Long term debt
    const valuesFCF = data.map(entry => entry.fcf); // Free Cash Flow

    let currentChartType = 'line';  // Default chart type

    // Get canvas context
    const ctx = document.getElementById('financialsChart').getContext('2d');

    // Function to create the chart
    function createChart(chartType) {
        return new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: [
                // {
                //     label: 'Apple Revenue',
                //     data: valuesRevenue,    // Revenue
                //     backgroundColor: 'rgb(48, 146, 231, 0.3)',
                //     borderColor: 'rgb(48, 146, 231)',
                //     borderWidth: 2,
                //     pointStyle: 'circle',
                //     pointRadius: 5,
                //     pointHoverRadius: 10,
                //     fill: false,
                //     tension: 0.2
                // },
                {
                    label: 'Apple Earnings',
                    data: valuesEarnings,   // Earnings
                    backgroundColor: 'rgb(16, 206, 64, 0.3)',
                    borderColor: 'rgb(16, 206, 64)',
                    borderWidth: 2,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    fill: false,
                    tension: 0.2
                },
                {
                    label: 'Apple Debt',
                    data: valuesDebt,   // Debt
                    backgroundColor: 'rgb(146, 16, 206, 0.3)',
                    borderColor: 'rgb(146, 16, 206)',
                    borderWidth: 2,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    fill: false,
                    tension: 0.2
                },
                {
                    label: 'Apple Cash Flow',
                    data: valuesFCF,   // FCF
                    backgroundColor: 'rgb(206, 16, 165, 0.3)',
                    borderColor: 'rgb(206, 16, 165)',
                    borderWidth: 2,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    fill: false,
                    tension: 0.2
                }, 
                {
                    label: 'Shares',
                    data: valuesShares,   // Shares
                    backgroundColor: 'rgb(206, 124, 16, 0.3)',
                    borderColor: 'rgb(206, 124, 16)',
                    borderWidth: 2,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    fill: false,
                    tension: 0.2
                }               
            ]
            },
            options: {
                responsive: true,
                plugins: { 
                    // Title
                    title: { 
                    display: true,
                    text: 'Financial and Shares Trends',  
                    font: {
                        size: 24,  
                        weight: 'bold' 
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }, // Legend
                    legend: { position: 'bottom',
                        align: 'center',
                        labels: { font : { size: 18 } } 
                },
                    // Tooltip
                    tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            let value = context.raw;
                            let index = context.dataIndex;
                            let date = labels[index];  // Get corresponding date
    
                            const formattedNumber = new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD'
                              }).format(value);
                            
                            return `${label}: ${formattedNumber}`;  // Custom tooltip format
                        },
                    }
                } 
                },
                scales: { // Axis
                //     x: { title: { display: true, text: 'Date', font: { size: 16} }, 
                //         ticks: { font: { size: 14 } } 
                // },
                    y: { title: { display: true, text: 'Financials and Shares', font: { size: 16} },
                    ticks: { font: { size: 14 },
                            callback: function(value, index, values) {
                                return `$${(value/1000000000).toFixed(0)}B`; // Convert Y-axis labels to currency format in billions
                            }
                        } 
                    }
                }
            }
        });
    }

    // Create initial chart
    let revEarningsChart = createChart(currentChartType);

    // Button click event to toggle chart type
    document.getElementById('toggleChart').addEventListener('click', function () {
        revEarningsChart.destroy();  // Destroy current chart
        currentChartType = (currentChartType === 'line') ? 'bar' : 'line';  // Toggle type
        revEarningsChart = createChart(currentChartType);  // Create new chart

        // Update button text
        this.textContent = (currentChartType === 'line') ? 'Switch to Bar Chart' : 'Switch to Line Chart';
    });
}

fetchData();