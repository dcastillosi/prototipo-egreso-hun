function readTable(id) {
  const rows = Array.from(document.querySelectorAll(`#${id} tbody tr`));
  return rows.map((tr) => {
    const tds = tr.querySelectorAll("td");
    return {
      name: tds[0].innerText.trim(),
      mean_minutes: parseFloat(tds[1].querySelector("input").value),
      std_minutes: parseFloat(tds[2].querySelector("input").value),
      sla_minutes: parseFloat(tds[3].querySelector("input").value),
    };
  });
}

function formatFlow(name, data, includeStages = true) {
  const lines = [];
  lines.push(`== ${name.toUpperCase()} ==`);
  lines.push(`Casos: ${data.cases}`);
  lines.push(`Tiempo total promedio: ${data.avg_total_minutes} min`);
  lines.push(`P90 tiempo total: ${data.p90_total_minutes} min`);
  lines.push(`Cumplimiento total (todas las etapas dentro de SLA): ${data.compliance_total_pct}%`);
  lines.push(`Cuellos de botella: ${data.bottlenecks && data.bottlenecks.length ? data.bottlenecks.join(", ") : "-"}`);

  if (includeStages && Array.isArray(data.stages)) {
    lines.push(`Por etapa:`);
    data.stages.forEach(s => {
      lines.push(
        `  - ${s.name}: avg ${s.avg.toFixed(1)} | P90 ${s.p90.toFixed(1)} | SLA ${s.sla} | Cumple ${s.compliance_pct}%`
      );
    });
  }

  lines.push("");
  return lines.join("\n");
}

async function runSimulation() {
  const resultEl = document.getElementById("result");
  resultEl.textContent = "Ejecutando simulacion...";

  try {
    const cases = parseInt(document.getElementById("cases").value || "300", 10);
    const mix_vivo = parseFloat(document.getElementById("mix_vivo").value);
    const mix_rem = parseFloat(document.getElementById("mix_remision").value);
    const mix_vol = parseFloat(document.getElementById("mix_voluntario").value);

    const payload = {
      cases,
      mix: { vivo: mix_vivo, remision: mix_rem, voluntario: mix_vol },
      flows: {
        vivo: { stages: readTable("tbl_vivo") },
        remision: { stages: readTable("tbl_remision") },
        voluntario: { stages: readTable("tbl_voluntario") },
      }
    };

    const resp = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const text = await resp.text();

    if (!resp.ok) {
      resultEl.textContent = `Error ${resp.status} al llamar /simulate:\n\n${text}`;
      return;
    }

    const data = JSON.parse(text);

    const out = [];
    out.push("MIX EFECTIVO (casos por flujo):");
    Object.entries(data.counts).forEach(([k, v]) => out.push(`- ${k}: ${v}`));
    out.push("");

    // Global sin detalle por etapa
    out.push(formatFlow("Global", data.overall, false));

    // Flujos con detalle de etapas
    out.push(formatFlow("Vivo", data.per_flow.vivo, true));
    out.push(formatFlow("Remision", data.per_flow.remision, true));
    out.push(formatFlow("Voluntario", data.per_flow.voluntario, true));

    resultEl.textContent = out.join("\n");
  } catch (e) {
    resultEl.textContent = "Error en el JavaScript de la simulacion:\n" + e;
  }
}

document.getElementById("runBtn").addEventListener("click", runSimulation);
