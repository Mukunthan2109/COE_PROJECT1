/**
 * QA Analytics & Heatmap Chart.js Renderer
 */
function initAnalyticsCharts(diseaseData, gradeData) {
    // 1. Disease Category Distribution Chart
    const ctxDisease = document.getElementById('diseaseChart');
    if (ctxDisease && diseaseData) {
        new Chart(ctxDisease, {
            type: 'doughnut',
            data: {
                labels: Object.keys(diseaseData),
                datasets: [{
                    data: Object.values(diseaseData),
                    backgroundColor: [
                        '#2e7d32', '#f57c00', '#d32f2f', '#0288d1', '#7b1fa2',
                        '#388e3c', '#fbc02d', '#c2185b', '#0097a7', '#512da8'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' }
                }
            }
        });
    }

    // 2. Batch Quality Intake Breakdown Chart
    const ctxGrade = document.getElementById('gradeChart');
    if (ctxGrade && gradeData) {
        new Chart(ctxGrade, {
            type: 'bar',
            data: {
                labels: Object.keys(gradeData),
                datasets: [{
                    label: 'Number of Crop Batches',
                    data: Object.values(gradeData),
                    backgroundColor: ['#2e7d32', '#f57c00', '#fbc02d', '#d32f2f']
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, precision: 0 }
                }
            }
        });
    }
}
