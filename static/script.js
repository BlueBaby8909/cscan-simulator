// Register the DataLabels plugin
Chart.register(ChartDataLabels);

function initChart(sequenceData, diskSize) {
    const ctx = document.getElementById('diskGraph').getContext('2d');

    // Map Sequence to {x: track, y: step}
    const scatterData = sequenceData.map((track, index) => ({
        x: track,
        y: index
    }));

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Disk Head Path',
                data: scatterData,
                showLine: true,
                borderColor: '#03DAC6',
                borderWidth: 2,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#03DAC6',
                pointBorderWidth: 2,
                pointRadius: 5,
                tension: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: { top: 20, bottom: 20, left: 20, right: 40 }
            },
            scales: {
                x: {
                    position: 'top',
                    min: 0,
                    max: diskSize,
                    grid: {
                        color: '#404040',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        color: '#E0E0E0',
                        font: { size: 12, family: 'Inter' }
                    },
                    title: { display: false }
                },
                y: {
                    reverse: true, // 0 at TOP, increasing DOWNWARDS
                    grid: {
                        color: '#404040',
                        borderDash: [5, 5]
                    },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#1E1E1E',
                    titleColor: '#03DAC6',
                    bodyColor: '#E0E0E0',
                    borderColor: '#333',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) { return `Track: ${context.parsed.x}`; }
                    }
                },
                datalabels: {
                    align: 'right',
                    anchor: 'center',
                    color: '#E0E0E0',
                    font: { size: 11, weight: 'bold', family: 'Inter' },
                    formatter: function(value) { return value.x; }
                }
            }
        }
    });
}