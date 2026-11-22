/**
 * Solar & Carbon Savings Calculator with Chart.js Visualizations
 */

let monthlyChart = null;
let projectionChart = null;

document.addEventListener('DOMContentLoaded', function () {
  // Sync Sliders and Number Inputs
  const syncPairs = [
    { slider: 'slider-monthly-bill', input: 'input-monthly-bill' },
    { slider: 'slider-tariff-rate', input: 'input-tariff-rate' },
    { slider: 'slider-roof-area', input: 'input-roof-area' },
    { slider: 'slider-sunlight', input: 'input-sunlight' }
  ];

  syncPairs.forEach(pair => {
    const s = document.getElementById(pair.slider);
    const i = document.getElementById(pair.input);
    if (s && i) {
      s.addEventListener('input', () => {
        i.value = s.value;
        runCalculator();
      });
      i.addEventListener('input', () => {
        s.value = i.value;
        runCalculator();
      });
    }
  });

  const offsetSelect = document.getElementById('select-offset');
  if (offsetSelect) {
    offsetSelect.addEventListener('change', runCalculator);
  }

  // Initial calculation
  runCalculator();

  // Save calculation button
  const saveBtn = document.getElementById('btn-save-calc');
  if (saveBtn) {
    saveBtn.addEventListener('click', saveCalculation);
  }

  // Print button
  const printBtn = document.getElementById('btn-print-calc');
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }
});

let currentCalcData = {};

function runCalculator() {
  const billInput = document.getElementById('input-monthly-bill');
  const tariffInput = document.getElementById('input-tariff-rate');
  const roofInput = document.getElementById('input-roof-area');
  const sunInput = document.getElementById('input-sunlight');
  const offsetSelect = document.getElementById('select-offset');

  if (!billInput || !tariffInput) return;

  const monthlyBill = parseFloat(billInput.value) || 150;
  const tariffRate = parseFloat(tariffInput.value) || 0.16;
  const roofArea = parseFloat(roofInput.value) || 500;
  const sunHours = parseFloat(sunInput.value) || 5.0;
  const offsetPct = (parseFloat(offsetSelect ? offsetSelect.value : 100) || 100) / 100;

  // Consumption calculation
  const monthlyKwh = monthlyBill / tariffRate;
  const annualKwh = monthlyKwh * 12;

  // System sizing: Capacity (kW) = Annual kWh * offset / (sunHours * 365 * 0.78 performance ratio)
  const systemPerformanceRatio = 0.78;
  const recommendedKw = Math.max(1.0, (annualKwh * offsetPct) / (sunHours * 365 * systemPerformanceRatio));
  const roundedKw = Math.round(recommendedKw * 10) / 10;
  const panelsCount = Math.round((roundedKw * 1000) / 400); // 400W modern panels
  const reqRoofArea = Math.round(roundedKw * 75); // ~75 sq ft per kW

  // Generation & Savings
  const annualSolarGenKwh = Math.round(roundedKw * sunHours * 365 * systemPerformanceRatio);
  const monthlySolarGenKwh = Math.round(annualSolarGenKwh / 12);

  const solarValueMonthly = monthlySolarGenKwh * tariffRate;
  const newMonthlyBill = Math.max(12, Math.round((monthlyBill - solarValueMonthly) * 100) / 100); // minimum $12 grid hookup
  const actualMonthlySavings = Math.max(0, Math.round((monthlyBill - newMonthlyBill) * 100) / 100);
  const annualSavings = Math.round(actualMonthlySavings * 12);

  // Financial costs & payback: ~$2.80/W gross, minus 30% clean energy credit
  const grossCost = roundedKw * 1000 * 2.80;
  const netSystemCost = Math.round(grossCost * 0.70);
  const paybackYears = annualSavings > 0 ? (Math.round((netSystemCost / annualSavings) * 10) / 10) : 0;

  // Environmental benefits (EPA standard factor: ~0.709 kg CO2/kWh grid displacement)
  const annualCo2Tons = Math.round((annualSolarGenKwh * 0.000709) * 10) / 10;
  const treesEquiv = Math.round((annualCo2Tons * 1000) / 21.77);
  const carMiles = Math.round(annualCo2Tons * 2480);

  // Store data globally for saving
  currentCalcData = {
    monthly_bill: monthlyBill,
    monthly_kwh: Math.round(monthlyKwh),
    tariff_rate: tariffRate,
    roof_area: roofArea,
    sunlight_hours: sunHours,
    recommended_kw: roundedKw,
    monthly_savings: actualMonthlySavings,
    annual_savings: annualSavings,
    annual_co2_saved_tons: annualCo2Tons,
    trees_equivalent: treesEquiv,
    payback_years: paybackYears,
    new_monthly_bill: newMonthlyBill
  };

  // Update UI Elements
  setText('calc-recommended-kw', `${roundedKw} kW`);
  setText('calc-panels-count', `${panelsCount} Panels`);
  setText('calc-monthly-savings', `$${actualMonthlySavings.toFixed(0)}`);
  setText('calc-annual-savings', `$${annualSavings.toLocaleString()}`);
  setText('calc-new-bill', `$${newMonthlyBill.toFixed(0)}/mo`);
  setText('calc-current-bill-mirror', `$${monthlyBill.toFixed(0)}/mo`);
  setText('calc-payback-years', `${paybackYears} Years`);
  setText('calc-net-cost', `$${netSystemCost.toLocaleString()}`);
  setText('calc-co2-tons', `${annualCo2Tons} Tons`);
  setText('calc-trees-count', `${treesEquiv.toLocaleString()}`);
  setText('calc-car-miles', `${carMiles.toLocaleString()}`);
  setText('calc-monthly-kwh', `${Math.round(monthlyKwh).toLocaleString()} kWh`);
  setText('calc-solar-gen', `${monthlySolarGenKwh.toLocaleString()} kWh/mo`);

  // Roof space badge
  const roofStatusEl = document.getElementById('calc-roof-status');
  if (roofStatusEl) {
    if (roofArea >= reqRoofArea) {
      roofStatusEl.innerHTML = `<span class="badge bg-success-subtle text-success border border-success-subtle"><i class="bi bi-check-circle me-1"></i> Roof space is adequate (Needs ~${reqRoofArea} sq.ft, Available: ${roofArea} sq.ft)</span>`;
    } else {
      roofStatusEl.innerHTML = `<span class="badge bg-warning-subtle text-warning border border-warning-subtle"><i class="bi bi-exclamation-triangle me-1"></i> Space tight: Needs ~${reqRoofArea} sq.ft for 100% offset. Consider high-efficiency 430W panels.</span>`;
    }
  }

  // Update Charts
  updateMonthlyChart(monthlyBill, newMonthlyBill, actualMonthlySavings);
  updateProjectionChart(annualSavings, annualKwh, tariffRate);
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function updateMonthlyChart(currentBill, newBill, savings) {
  const ctx = document.getElementById('monthlyCostChart');
  if (!ctx) return;

  const data = {
    labels: ['Current Electric Bill', 'Bill With Solar Panels', 'Monthly Savings'],
    datasets: [{
      label: 'Monthly Amount ($)',
      data: [currentBill, newBill, savings],
      backgroundColor: [
        'rgba(239, 68, 68, 0.85)',   // Red for old bill
        'rgba(2, 132, 199, 0.85)',   // Ocean Blue for new bill
        'rgba(16, 185, 129, 0.85)'   // Emerald Green for savings
      ],
      borderColor: [
        '#dc2626',
        '#0284c7',
        '#059669'
      ],
      borderWidth: 1.5,
      borderRadius: 8
    }]
  };

  if (monthlyChart) {
    monthlyChart.data = data;
    monthlyChart.update();
  } else {
    monthlyChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => ` $${context.raw.toFixed(2)}`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: val => `$${val}`
            },
            grid: { color: '#f1f5f9' }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }
}

function updateProjectionChart(annualSavings, annualKwh, tariffRate) {
  const ctx = document.getElementById('projectionChart');
  if (!ctx) return;

  const years = [1, 5, 10, 15, 20, 25];
  const cumulativeSavings = [];
  const cumulativeWithoutSolar = [];

  let accumSavings = 0;
  let accumWithoutSolar = 0;
  let rateEscalation = 1.0;

  for (let y = 1; y <= 25; y++) {
    rateEscalation *= 1.03; // 3% annual grid rate hike
    accumSavings += (annualSavings * rateEscalation);
    accumWithoutSolar += (annualKwh * tariffRate * rateEscalation);

    if (years.includes(y)) {
      cumulativeSavings.push(Math.round(accumSavings));
      cumulativeWithoutSolar.push(Math.round(accumWithoutSolar));
    }
  }

  const data = {
    labels: years.map(y => `Year ${y}`),
    datasets: [
      {
        label: 'Cumulative Solar Savings ($)',
        data: cumulativeSavings,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.15)',
        fill: true,
        tension: 0.35,
        borderWidth: 3,
        pointBackgroundColor: '#047857',
        pointRadius: 5
      },
      {
        label: 'Cost If Remaining on 100% Grid ($)',
        data: cumulativeWithoutSolar,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.05)',
        borderDash: [5, 5],
        tension: 0.35,
        borderWidth: 2,
        pointBackgroundColor: '#b91c1c',
        pointRadius: 4
      }
    ]
  };

  if (projectionChart) {
    projectionChart.data = data;
    projectionChart.update();
  } else {
    projectionChart = new Chart(ctx, {
      type: 'line',
      data: data,
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
          },
          tooltip: {
            callbacks: {
              label: context => ` ${context.dataset.label}: $${context.raw.toLocaleString()}`
            }
          }
        },
        scales: {
          y: {
            ticks: {
              callback: val => `$${(val / 1000).toFixed(0)}k`
            },
            grid: { color: '#f1f5f9' }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }
}

function saveCalculation() {
  const saveBtn = document.getElementById('btn-save-calc');
  const alertContainer = document.getElementById('calc-save-status');

  saveBtn.disabled = true;
  saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Saving...';

  fetch('/api/save-calculation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(currentCalcData)
  })
  .then(res => {
    if (res.status === 401 || res.redirected) {
      window.location.href = '/login?next=/calculator';
      return;
    }
    return res.json();
  })
  .then(data => {
    saveBtn.disabled = false;
    saveBtn.innerHTML = '<i class="bi bi-bookmark-check me-1"></i> Save Calculation';

    if (alertContainer) {
      if (data && data.success) {
        alertContainer.innerHTML = `
          <div class="alert alert-success alert-dismissible fade show mt-3" role="alert">
            <i class="bi bi-check-circle-fill me-2"></i> ${data.message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        `;
      } else {
        alertContainer.innerHTML = `
          <div class="alert alert-warning alert-dismissible fade show mt-3" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> ${data ? data.error : 'Please log in to save calculations.'}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        `;
      }
    }
  })
  .catch(err => {
    saveBtn.disabled = false;
    saveBtn.innerHTML = '<i class="bi bi-bookmark-check me-1"></i> Save Calculation';
    console.error('Error saving calculation:', err);
  });
}
