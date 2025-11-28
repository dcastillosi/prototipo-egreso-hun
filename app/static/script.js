// script.js

let chartVivoTimes = null;

function getNumber(el) {
  const v = parseFloat(el.value);
  return isNaN(v) ? 0 : v;
}

// Lee las tablas y construye el objeto de configuracion para la API
function buildConfigFromDom() {
  const cases = parseInt(document.getElementById("casesInput").value) || 0;
  const mixVivo = parseFloat(document.getElementById("mixVivoInput").value) || 0;
  const mixRem = parseFloat(document.getElementById("mixRemisionInput").value) || 0;
  const mixVol = parseFloat(document.getElementById("mixVoluntarioInput").value) || 0;

  const flows = {
    vivo: { stages: [] },
    remision: { stages: [] },
    voluntario: { stages: [] },
  };

  // Recorre todas las tablas con data-flow
  document.querySelectorAll("table.flow-table").forEach((table) => {
    const flowKey = table.dataset.flow;
    const stages = [];
    table.querySelectorAll("tbody tr").forEach((row) => {
      const cells = row.querySelectorAll("td");
      if (cells.length < 4) return;

      const name = cells[0].innerText.trim();
      const mean = getNumber(cells[1].querySelector("input"));
      const std = getNumber(cells[2].querySelector("input"));
      const sla = getNumber(cells[3].querySelector("input"));

      stages.push({ name, mean, std, sla });
    });

    if (flows[flowKey]) {
      flows[flowKey].stages = stages;
    }
  });

  return {
    cases: cases,
    mix: {
      vivo: mixVivo,
      remision: mixRem,
      voluntario: mixVol,
    },
    flows: flows,
  };
}

// Llama al backend para ejecutar la simulacion
async function runSimulation() {
  const cfg = buildConfigFromDom();

  try {
    const resp = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cfg),
    });

    if (!resp.ok) {
      const txt = await resp.text();
      document.getElementById("resultsBox").innerText =
        "Error en la API de simulacion:\n" + txt;
      return;
    }

    const data = await resp.json();
    renderResults(data);
  } catch (err) {
    console.error(err);
    document.getElementById("resultsBox").innerText =
      "Error en la llamada a la API:\n" + err;
  }
}

// Muestra los resultados en texto (por ahora generico)
function renderResults(data) {
  // Aqui puedes adaptar al formato real que retorna tu backend.
  // Por ahora mostramos el JSON "bonito".
  document.getElementById("resultsBox").innerText = JSON.stringify(
    data,
    null,
    2
  );
}

// Construye o actualiza la grafica de tiempos para el flujo vivo
function updateVivoChart() {
  const table = document.querySelector('table.flow-table[data-flow="vivo"]');
  if (!table) return;

  const labels = [];
  const values = [];

  table.querySelectorAll("tbody tr").forEach((row) => {
    const cells = row.querySelectorAll("td");
    if (cells.length < 4) return;

    const name = cells[0].innerText.trim();
    const mean = getNumber(cells[1].querySelector("input"));

    labels.push(name);
    values.push(mean);
  });

  const ctx = document.getElementById("chartVivoTimes").getContext("2d");

  if (chartVivoTimes) {
    chartVivoTimes.destroy();
  }

  chartVivoTimes = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Media por etapa (minutos)",
          data: values,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { autoSkip: false, maxRotation: 60, minRotation: 45 } },
        y: { beginAtZero: true },
      },
    },
  });
}

// Eventos
document.addEventListener("DOMContentLoaded", () => {
  const btnRun = document.getElementById("runSimulationBtn");
  const btnCharts = document.getElementById("updateChartsBtn");

  if (btnRun) {
    btnRun.addEventListener("click", (e) => {
      e.preventDefault();
      runSimulation();
      updateVivoChart();
    });
  }

  if (btnCharts) {
    btnCharts.addEventListener("click", (e) => {
      e.preventDefault();
      updateVivoChart();
    });
  }

  // Dibuja la grafica inicial con los valores por defecto
  updateVivoChart();
});
