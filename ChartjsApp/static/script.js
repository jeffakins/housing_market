// --- Interactive Dashboard Chart Code ---

// Global variables
let myChart = null;
let allCities = [];
let selectedCities = [];

// DOM element references
const searchInput = document.getElementById('city-search-input');
const cityDropdown = document.getElementById('city-dropdown');
const tagsContainer = document.getElementById('city-tags-container');
const selectorContainer = document.getElementById('city-selector-container');
const updateBtn = document.getElementById('update-chart-btn');
const selectionError = document.getElementById('selection-error');

/**
 * Renders or updates the chart with new data.
 * @param {object} chartData - Data object for the chart from the backend.
 */
function renderChart(chartData) {
    const ctx = document.getElementById('myChart').getContext('2d');
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                },
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + new Intl.NumberFormat('en-US').format(value);
                        }
                    }
                },
                x: { 
                    grid: { display: false },
                    ticks: {
                        // --- NEW: Custom X-Axis Label Formatting ---
                        callback: function(value) {
                            // 'value' is the index of the label in the data.labels array.
                            // this.getLabelForValue(value) retrieves the actual label (e.g., "2023-01-31").
                            const label = this.getLabelForValue(value);
                            
                            // Create a date object, ensuring it's treated as local time to avoid timezone shifts.
                            const date = new Date(label);

                            // If the month is January (month index 0), show month and year.
                            if (date.getMonth() === 0) {
                                return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
                            }
                            
                            // Otherwise, just show the three-letter month name.
                            return date.toLocaleDateString('en-US', { month: 'short' });
                        }
                    }
                }
            }
        }
    });
}

/**
 * Fetches data for the selected cities and triggers chart rendering.
 */
async function updateChart() {
    if (selectedCities.length === 0) {
        selectionError.textContent = 'Please select at least one city.';
        return;
    }

    updateBtn.textContent = 'Loading...';
    updateBtn.disabled = true;

    try {
        const response = await fetch(`/api/citydata?cities=${selectedCities.join(',')}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const chartData = await response.json();
        renderChart(chartData);
    } catch (error) {
        console.error("Could not fetch chart data:", error);
    } finally {
        updateBtn.textContent = 'Update Chart';
        validateSelection();
    }
}

/**
 * Populates the dropdown with filtered, unselected cities.
 */
function renderDropdown() {
    cityDropdown.innerHTML = '';
    const searchTerm = searchInput.value.toLowerCase();
    
    const availableCities = allCities
        .filter(city => !selectedCities.includes(city))
        .filter(city => city.toLowerCase().includes(searchTerm));

    if (availableCities.length === 0) {
        cityDropdown.innerHTML = `<div class="px-4 py-2 text-gray-500">No cities found</div>`;
    } else {
        availableCities.forEach(city => {
            const item = document.createElement('div');
            item.className = 'px-4 py-2 cursor-pointer hover:bg-gray-100';
            item.textContent = city;
            item.addEventListener('click', () => selectCity(city));
            cityDropdown.appendChild(item);
        });
    }
}

/**
 * Handles the selection of a city from the dropdown.
 * @param {string} city - The city name to select.
 */
function selectCity(city) {
    if (selectedCities.length < 5) {
        selectedCities.push(city);
        addCityTag(city);
        searchInput.value = '';
        renderDropdown();
        searchInput.focus();
    }
    validateSelection();
}

/**
 * Creates and displays a tag for a selected city.
 * @param {string} city - The city name for the tag.
 */
function addCityTag(city) {
    const tag = document.createElement('div');
    tag.className = 'bg-indigo-100 text-indigo-700 text-sm font-medium px-2 py-1 rounded-full flex items-center gap-2';
    tag.innerHTML = `
        <span>${city}</span>
        <button class="text-indigo-500 hover:text-indigo-700 focus:outline-none">&times;</button>
    `;
    tag.querySelector('button').addEventListener('click', () => removeCity(city, tag));
    tagsContainer.appendChild(tag);
}

/**
 * Removes a city from the selection and its corresponding tag.
 * @param {string} city - The city name to remove.
 * @param {HTMLElement} tagElement - The tag element to remove.
 */
function removeCity(city, tagElement) {
    selectedCities = selectedCities.filter(c => c !== city);
    tagsContainer.removeChild(tagElement);
    renderDropdown();
    validateSelection();
}

/**
 * Validates the number of selected cities and updates UI state.
 */
function validateSelection() {
    const count = selectedCities.length;
    if (count > 5) {
        selectionError.textContent = 'Maximum of 5 cities allowed.';
        updateBtn.disabled = true;
    } else if (count === 0) {
        selectionError.textContent = 'Please select at least one city.';
        updateBtn.disabled = true;
    } else {
        selectionError.textContent = '';
        updateBtn.disabled = false;
    }
}

/**
 * Fetches the initial list of all cities to populate the selector.
 */
async function initialize() {
    try {
        const response = await fetch('/api/cities');
        allCities = await response.json();
        
        // Pre-select the first two cities for the initial view
        if (allCities.length >= 2) {
            selectCity('Los Angeles, CA'); //allCities[0]
            selectCity('New York, NY'); //allCities[1]
        }
        
        updateChart();
    } catch (error) {
        console.error("Could not fetch city list:", error);
    }
}

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', initialize);
updateBtn.addEventListener('click', updateChart);
searchInput.addEventListener('input', renderDropdown);
searchInput.addEventListener('focus', () => {
    renderDropdown();
    cityDropdown.classList.remove('hidden');
});

// Hide dropdown when clicking outside of the selector
document.addEventListener('click', (e) => {
    if (!selectorContainer.contains(e.target)) {
        cityDropdown.classList.add('hidden');
    }
});

