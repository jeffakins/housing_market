// --- Interactive Dashboard Chart Code ---

// Global variables
let myChart = null;
let allCities = [];
let selectedCities = [];
const MAX_CITIES = 8;
let highlightedIndex = -1;
let chartUpdateTimeout;
let fullChartData = null; // To store the complete data from API
let activeTimeRange = 'max'; // Default time range

// DOM element references
const searchInput = document.getElementById('city-search-input');
const cityDropdown = document.getElementById('city-dropdown');
const tagsContainer = document.getElementById('city-tags-container');
const selectorContainer = document.getElementById('city-selector-container');
const selectionError = document.getElementById('selection-error');
const timeRangeContainer = document.getElementById('time-range-container');

/**
 * Applies the active time range filter to the full dataset.
 */
function applyTimeFilter() {
    if (!fullChartData) return;

    const filteredData = JSON.parse(JSON.stringify(fullChartData)); // Deep copy
    const { labels } = filteredData;
    
    let startIndex = 0;
    if (activeTimeRange !== 'max') {
        const startDate = new Date(); // Create a new date object for calculation
        let yearsToSubtract = 0;
        switch(activeTimeRange) {
            case '5y': yearsToSubtract = 5; break;
            case '2y': yearsToSubtract = 2; break;
            case '1y': yearsToSubtract = 1; break;
        }
        // This safely modifies the new startDate object
        startDate.setFullYear(startDate.getFullYear() - yearsToSubtract);
        
        startIndex = labels.findIndex(label => new Date(label) >= startDate);
        if(startIndex === -1) startIndex = 0; // If no data in range, show from beginning
    }

    // Slice the data based on the start index
    filteredData.labels = labels.slice(startIndex);
    filteredData.datasets.forEach(dataset => {
        dataset.data = dataset.data.slice(startIndex);
    });
    
    renderChart(filteredData);
}


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
                    mode: 'nearest',
                    intersect: true,
                    callbacks: {
                        title: function(tooltipItems) {
                            const date = new Date(tooltipItems[0].label);
                            return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
                        },
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) { label += ': '; }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                },
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: { callback: value => '$' + new Intl.NumberFormat('en-US').format(value) }
                },
                x: { 
                    grid: { display: false },
                    ticks: {
                        callback: function(value) {
                            const label = this.getLabelForValue(value);
                            const date = new Date(label);
                            return date.getMonth() === 0 
                                ? date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
                                : date.toLocaleDateString('en-US', { month: 'short' });
                        }
                    }
                }
            }
        }
    });
}

/**
 * Fetches data for the selected cities, stores it, and triggers filtering/rendering.
 */
function updateChart() {
    clearTimeout(chartUpdateTimeout);
    chartUpdateTimeout = setTimeout(async () => {
        if (selectedCities.length === 0) {
            if (myChart) { myChart.destroy(); myChart = null; }
            fullChartData = null;
            return;
        }
        
        try {
            const response = await fetch(`/api/citydata?cities=${selectedCities.join(',')}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            fullChartData = await response.json(); // Store full data
            applyTimeFilter(); // Apply filter and render
        } catch (error) {
            console.error("Could not fetch chart data:", error);
            selectionError.textContent = "Failed to load chart data.";
        } finally {
            validateSelection();
        }
    }, 300);
}

/**
 * Populates the dropdown with filtered, unselected cities.
 */
function renderDropdown() {
    cityDropdown.innerHTML = '';
    highlightedIndex = -1;
    const searchTerm = searchInput.value.toLowerCase();
    
    const availableCities = allCities
        .filter(city => !selectedCities.includes(city))
        .filter(city => city.toLowerCase().includes(searchTerm));

    if (availableCities.length > 0 && searchTerm.length > 0) {
        cityDropdown.classList.remove('hidden');
        availableCities.forEach(city => {
            const item = document.createElement('div');
            item.className = 'px-4 py-2 cursor-pointer hover:bg-gray-100';
            item.textContent = city;
            item.addEventListener('click', () => selectCity(city));
            cityDropdown.appendChild(item);
        });
    } else {
        cityDropdown.classList.add('hidden');
    }
}

/**
 * Handles the selection of a city from the dropdown.
 * @param {string} city - The city name to select.
 */
function selectCity(city) {
    if (selectedCities.length < MAX_CITIES) {
        selectedCities.push(city);
        addCityTag(city);
        searchInput.value = '';
        cityDropdown.classList.add('hidden');
        searchInput.focus();
        updateChart();
    }
    validateSelection();
}

/**
 * Creates and displays a tag for a selected city.
 * @param {string} city - The city name for the tag.
 */
function addCityTag(city) {
    const tag = document.createElement('div');
    tag.className = 'bg-blue-100 text-[#246D9E] text-sm font-medium px-2 py-1 rounded-full flex items-center gap-2';
    tag.innerHTML = `
        <span>${city}</span>
        <button class="text-[#1D567C] hover:text-blue-700 focus:outline-none" aria-label="Remove ${city}">&times;</button>
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
    updateChart();
    validateSelection();
}

/**
 * Validates the number of selected cities and updates UI state.
 */
function validateSelection() {
    const count = selectedCities.length;
    if (count >= MAX_CITIES) {
        selectionError.textContent = `Maximum of ${MAX_CITIES} cities allowed.`;
        searchInput.disabled = true;
    } else {
        selectionError.textContent = '';
        searchInput.disabled = false;
    }
}

/**
 * Manages keyboard navigation for the city dropdown.
 * @param {KeyboardEvent} e - The keyboard event.
 */
function handleKeyboardNavigation(e) {
    const items = cityDropdown.querySelectorAll('div');
    if (items.length === 0) return;

    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault();
            highlightedIndex = (highlightedIndex + 1) % items.length;
            updateDropdownHighlight(items);
            break;
        case 'ArrowUp':
            e.preventDefault();
            highlightedIndex = (highlightedIndex - 1 + items.length) % items.length;
            updateDropdownHighlight(items);
            break;
        case 'Enter':
            e.preventDefault();
            if (highlightedIndex > -1) {
                selectCity(items[highlightedIndex].textContent);
            }
            break;
        case 'Escape':
            cityDropdown.classList.add('hidden');
            break;
    }
}

/**
 * Updates the visual highlight on dropdown items.
 * @param {NodeListOf<HTMLDivElement>} items - The list of dropdown items.
 */
function updateDropdownHighlight(items) {
    items.forEach((item, index) => {
        if (index === highlightedIndex) {
            item.classList.add('highlighted');
            item.scrollIntoView({ block: 'nearest' });
        } else {
            item.classList.remove('highlighted');
        }
    });
}

/**
 * Fetches the initial list of all cities to populate the selector.
 */
async function initialize() {
    try {
        const response = await fetch('/api/cities');
        if (!response.ok) throw new Error('Failed to fetch city list.');
        allCities = await response.json();
        
        if (allCities.includes('Los Angeles, CA')) {
            selectCity('Los Angeles, CA'); 
        } else {
            updateChart();
        }
    } catch (error) {
        console.error("Initialization failed:", error);
        selectionError.textContent = "Could not load city data.";
    }
}

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', initialize);
searchInput.addEventListener('input', renderDropdown);
searchInput.addEventListener('keydown', handleKeyboardNavigation);

document.addEventListener('click', (e) => {
    if (!selectorContainer.contains(e.target)) {
        cityDropdown.classList.add('hidden');
    }
});

timeRangeContainer.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        const newRange = e.target.dataset.range;
        if (newRange !== activeTimeRange) {
            activeTimeRange = newRange;
            // Update active button style
            timeRangeContainer.querySelector('.active').classList.remove('active');
            e.target.classList.add('active');
            // Re-filter and render the chart
            applyTimeFilter();
        }
    }
});

