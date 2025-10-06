// --- Interactive Dashboard Chart Code ---

// --- Global Variables ---
let priceChart = null;
let inventoryChart = null;
let allCities = [];
let selectedCities = [];
const MAX_CITIES = 8;
let highlightedIndex = -1;
let chartUpdateTimeout;

// Data stores
let fullPriceData = null;
let fullInventoryData = null;

// State for time ranges
let activePriceTimeRange = 'max';
let activeInventoryTimeRange = 'max';

// --- DOM Element References ---
const searchInput = document.getElementById('city-search-input');
const cityDropdown = document.getElementById('city-dropdown');
const tagsContainer = document.getElementById('city-tags-container');
const selectorContainer = document.getElementById('city-selector-container');
const selectionError = document.getElementById('selection-error');
const priceTimeRangeContainer = document.getElementById('price-time-range-container');
const inventoryTimeRangeContainer = document.getElementById('inventory-time-range-container');


// --- Charting Functions ---

/**
 * Applies a time filter to a given dataset.
 * @param {object} fullData - The complete, unfiltered dataset.
 * @param {string} timeRange - The active time range ('max', '5y', '2y', '1y').
 * @returns {object} The filtered data object.
 */
function applyTimeFilter(fullData, timeRange) {
    if (!fullData) return null;

    const filteredData = JSON.parse(JSON.stringify(fullData)); // Deep copy
    const { labels } = filteredData;
    
    let startIndex = 0;
    if (timeRange !== 'max') {
        const startDate = new Date();
        let yearsToSubtract = 0;
        switch(timeRange) {
            case '5y': yearsToSubtract = 5; break;
            case '2y': yearsToSubtract = 2; break;
            case '1y': yearsToSubtract = 1; break;
        }
        startDate.setFullYear(startDate.getFullYear() - yearsToSubtract);
        
        startIndex = labels.findIndex(label => new Date(label) >= startDate);
        if(startIndex === -1) startIndex = 0;
    }

    filteredData.labels = labels.slice(startIndex);
    filteredData.datasets.forEach(dataset => {
        dataset.data = dataset.data.slice(startIndex);
    });
    
    return filteredData;
}

/**
 * Creates a generic Chart.js configuration object.
 * @param {boolean} isCurrency - Whether to format the y-axis and tooltips as currency.
 * @returns {object} A Chart.js options object.
 */
function createChartOptions(isCurrency = false) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            tooltip: {
                enabled: true,
                mode: 'nearest',
                intersect: false,
                callbacks: {
                    title: (tooltipItems) => {
                        const date = new Date(tooltipItems[0].label);
                        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
                    },
                    label: (context) => {
                        let label = context.dataset.label || '';
                        if (label) { label += ': '; }
                        if (context.parsed.y !== null) {
                            if (isCurrency) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(context.parsed.y);
                            } else {
                                label += new Intl.NumberFormat('en-US').format(context.parsed.y);
                            }
                        }
                        return label;
                    }
                }
            },
        },
        scales: {
            y: {
                beginAtZero: false,
                ticks: { 
                    callback: (value) => isCurrency 
                        ? '$' + new Intl.NumberFormat('en-US').format(value) 
                        : new Intl.NumberFormat('en-US').format(value) 
                }
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
    };
}

/**
 * Renders or updates a specific chart.
 * @param {Chart} chartInstance - The chart instance to update (e.g., priceChart).
 * @param {string} canvasId - The ID of the canvas element.
 * @param {object} chartData - The data to render.
 * @param {object} options - The chart options.
 * @returns {Chart} The new or updated Chart instance.
 */
function renderChart(chartInstance, canvasId, chartData, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    if (chartInstance) {
        chartInstance.destroy();
    }
    return new Chart(ctx, { type: 'line', data: chartData, options: options });
}

/**
 * Fetches data for all charts and triggers rendering.
 */
function updateAllCharts() {
    clearTimeout(chartUpdateTimeout);
    chartUpdateTimeout = setTimeout(async () => {
        if (selectedCities.length === 0) {
            if (priceChart) { priceChart.destroy(); priceChart = null; }
            if (inventoryChart) { inventoryChart.destroy(); inventoryChart = null; }
            fullPriceData = null;
            fullInventoryData = null;
            return;
        }
        
        try {
            // Fetch both datasets in parallel
            const [priceResponse, inventoryResponse] = await Promise.all([
                fetch(`/api/pricedata?cities=${selectedCities.join(',')}`),
                fetch(`/api/inventorydata?cities=${selectedCities.join(',')}`)
            ]);

            if (!priceResponse.ok) throw new Error('Price data fetch failed');
            if (!inventoryResponse.ok) throw new Error('Inventory data fetch failed');

            fullPriceData = await priceResponse.json();
            fullInventoryData = await inventoryResponse.json();

            // Filter and render both charts
            const filteredPriceData = applyTimeFilter(fullPriceData, activePriceTimeRange);
            priceChart = renderChart(priceChart, 'priceChart', filteredPriceData, createChartOptions(true));

            const filteredInventoryData = applyTimeFilter(fullInventoryData, activeInventoryTimeRange);
            inventoryChart = renderChart(inventoryChart, 'inventoryChart', filteredInventoryData, createChartOptions(false));

        } catch (error) {
            console.error("Could not fetch chart data:", error);
            selectionError.textContent = "Failed to load chart data.";
        } finally {
            validateSelection();
        }
    }, 300);
}


// --- City Selection UI Functions ---

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

function selectCity(city) {
    if (selectedCities.length < MAX_CITIES) {
        selectedCities.push(city);
        addCityTag(city);
        searchInput.value = '';
        cityDropdown.classList.add('hidden');
        searchInput.focus();
        updateAllCharts();
    }
    validateSelection();
}

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

function removeCity(city, tagElement) {
    selectedCities = selectedCities.filter(c => c !== city);
    tagsContainer.removeChild(tagElement);
    updateAllCharts();
    validateSelection();
}

function validateSelection() {
    const count = selectedCities.length;
    searchInput.disabled = count >= MAX_CITIES;
    selectionError.textContent = count >= MAX_CITIES ? `Maximum of ${MAX_CITIES} cities allowed.` : '';
}

function handleKeyboardNavigation(e) {
    const items = cityDropdown.querySelectorAll('div');
    if (items.length === 0) return;

    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault();
            highlightedIndex = (highlightedIndex + 1) % items.length;
            break;
        case 'ArrowUp':
            e.preventDefault();
            highlightedIndex = (highlightedIndex - 1 + items.length) % items.length;
            break;
        case 'Enter':
            e.preventDefault();
            if (highlightedIndex > -1) selectCity(items[highlightedIndex].textContent);
            return; 
        case 'Escape':
            cityDropdown.classList.add('hidden');
            return;
        default:
            return;
    }
    updateDropdownHighlight(items);
}

function updateDropdownHighlight(items) {
    items.forEach((item, index) => {
        item.classList.toggle('highlighted', index === highlightedIndex);
        if (index === highlightedIndex) item.scrollIntoView({ block: 'nearest' });
    });
}


// --- Sidebar Navigation ---
function setupSidebarNavigation() {
    const sidebarNav = document.getElementById('sidebar-nav');
    if (!sidebarNav) return;

    const sections = [
        document.getElementById('price-chart-card'),
        document.getElementById('inventory-chart-card')
    ];
    const navLinks = sidebarNav.querySelectorAll('a');

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50% 0px', // Trigger when section is in top half of screen
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const targetId = entry.target.getAttribute('id');
            const link = sidebarNav.querySelector(`a[href="#${targetId}"]`);
            if (entry.isIntersecting) {
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        if (section) observer.observe(section);
    });
}


// --- Initialization ---

async function initialize() {
    try {
        const response = await fetch('/api/cities');
        if (!response.ok) throw new Error('Failed to fetch city list.');
        allCities = await response.json();
        
        if (allCities.includes('Los Angeles, CA')) selectCity('Los Angeles, CA'); 
        if (allCities.includes('New York, NY')) selectCity('New York, NY');

        if (selectedCities.length === 0) updateAllCharts();

    } catch (error) {
        console.error("Initialization failed:", error);
        selectionError.textContent = "Could not load city data.";
    }
}


// --- Event Listeners ---

document.addEventListener('DOMContentLoaded', () => {
    initialize();
    setupSidebarNavigation();
});

searchInput.addEventListener('input', renderDropdown);
searchInput.addEventListener('keydown', handleKeyboardNavigation);

document.addEventListener('click', (e) => {
    if (!selectorContainer.contains(e.target)) {
        cityDropdown.classList.add('hidden');
    }
});

priceTimeRangeContainer.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        const newRange = e.target.dataset.range;
        if (newRange !== activePriceTimeRange) {
            activePriceTimeRange = newRange;
            priceTimeRangeContainer.querySelector('.active').classList.remove('active');
            e.target.classList.add('active');
            const filteredData = applyTimeFilter(fullPriceData, activePriceTimeRange);
            priceChart = renderChart(priceChart, 'priceChart', filteredData, createChartOptions(true));
        }
    }
});

inventoryTimeRangeContainer.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        const newRange = e.target.dataset.range;
        if (newRange !== activeInventoryTimeRange) {
            activeInventoryTimeRange = newRange;
            inventoryTimeRangeContainer.querySelector('.active').classList.remove('active');
            e.target.classList.add('active');
            const filteredData = applyTimeFilter(fullInventoryData, activeInventoryTimeRange);
            inventoryChart = renderChart(inventoryChart, 'inventoryChart', filteredData, createChartOptions(false));
        }
    }
});

