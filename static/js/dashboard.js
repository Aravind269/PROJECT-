/**
 * Dashboard Visualizations with Chart.js
 */

document.addEventListener('DOMContentLoaded', function () {
  const mixCanvas = document.getElementById('generationMixChart');
  const trendCanvas = document.getElementById('monthlyTrendChart');

  if (!mixCanvas || !trendCanvas) return;

  fetch('/api/dashboard/stats')
    .then(res => res.json())
    .then(data => {
      renderGenerationMixChart(mixCanvas, data);
      renderMonthlyTrendChart(trendCanvas, data);
    })
    .catch(err => {
      console.error('Failed to load dashboard statistics:', err);
    });
});

function renderGenerationMixChart(canvas, data) {
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: data.sources,
      datasets: [{
        data: data.generation_by_source,
        backgroundColor: [
          '#f59e0b', // Solar Amber
          '#0284c7', // Wind Sky Blue
          '#6366f1', // Hydro Indigo
          '#10b981'  // Biomass Emerald
        ],
        borderWidth: 2,
        borderColor: '#ffffff',
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 14,
            font: { weight: 600 }
          }
        },
        tooltip: {
          callbacks: {
            label: function (ctx) {
              const val = ctx.raw;
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
              const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
              return ` ${ctx.label}: ${val.toLocaleString()} MWh (${pct}%)`;
            }
          }
        }
      },
      cutout: '68%'
    }
  });
}

function renderMonthlyTrendChart(canvas, data) {
  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: data.months,
      datasets: [
        {
          type: 'line',
          label: 'Estimated Savings ($ Thousands)',
          data: data.monthly_savings_k,
          borderColor: '#10b981',
          backgroundColor: '#10b981',
          borderWidth: 3,
          tension: 0.35,
          yAxisID: 'y1',
          pointRadius: 4,
          pointBackgroundColor: '#047857'
        },
        {
          type: 'bar',
          label: 'Clean Energy Generated (MWh)',
          data: data.monthly_generation_mwh,
          backgroundColor: 'rgba(2, 132, 199, 0.75)',
          borderRadius: 6,
          yAxisID: 'y'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          position: 'top',
          labels: { font: { weight: 600 } }
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Generation (MWh)',
            font: { weight: 600 }
          },
          grid: { color: '#f1f5f9' }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Savings ($k)',
            font: { weight: 600 }
          },
          grid: { drawOnChartArea: false }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}
