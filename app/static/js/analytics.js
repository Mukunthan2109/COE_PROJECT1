/**
 * AgriShield Analytics Engine & Chart.js Visualizer
 * Renders real database-driven analytics across crop health, disease, risk, and review SLAs.
 */
function initAnalyticsCharts(payload) {
    if (!payload) return;

    // 1. Disease Distribution Chart (Doughnut)
    const ctxDisease = document.getElementById('diseaseChart');
    if (ctxDisease && payload.disease_counts && Object.keys(payload.disease_counts).length > 0) {
        new Chart(ctxDisease, {
            type: 'doughnut',
            data: {
                labels: Object.keys(payload.disease_counts),
                datasets: [{
                    data: Object.values(payload.disease_counts),
                    backgroundColor: ['#2a9d8f', '#e76f51', '#f4a261', '#264653', '#e9c46a', '#457b9d', '#8d99ae']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
                }
            }
        });
    }

    // 2. Observations by Crop Chart (Horizontal Bar)
    const ctxCrop = document.getElementById('cropChart');
    if (ctxCrop && payload.crop_counts && Object.keys(payload.crop_counts).length > 0) {
        new Chart(ctxCrop, {
            type: 'bar',
            data: {
                labels: Object.keys(payload.crop_counts),
                datasets: [{
                    label: 'Observations',
                    data: Object.values(payload.crop_counts),
                    backgroundColor: '#2d6a4f',
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { beginAtZero: true, ticks: { precision: 0 } }
                }
            }
        });
    }

    // 3. Risk Distribution Chart (Pie)
    const ctxRisk = document.getElementById('riskChart');
    if (ctxRisk && payload.risk_counts && Object.keys(payload.risk_counts).length > 0) {
        new Chart(ctxRisk, {
            type: 'pie',
            data: {
                labels: Object.keys(payload.risk_counts),
                datasets: [{
                    data: Object.values(payload.risk_counts),
                    backgroundColor: ['#2e7d32', '#f57c00', '#d32f2f']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
                }
            }
        });
    }

    // 4. Observation Trend Chart (Line / Bar)
    const ctxTrend = document.getElementById('trendChart');
    if (ctxTrend && payload.trend_data && Object.keys(payload.trend_data).length > 0) {
        new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: Object.keys(payload.trend_data),
                datasets: [{
                    label: 'Daily Observations',
                    data: Object.values(payload.trend_data),
                    borderColor: '#1b5e20',
                    backgroundColor: 'rgba(46, 125, 50, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 } }
                }
            }
        });
    }
}
