import numpy as np
from typing import Dict, Any, List, Tuple


def _clamp_pos(x: float) -> float:
    return x if x > 0 else 0.0


def _draw_path(mix: Dict[str, float]) -> str:
    items = list(mix.items())
    keys, probs = zip(*items)
    choice = np.random.choice(len(keys), p=probs)
    return keys[choice]


def _normalize_mix(mix: Dict[str, float]) -> Dict[str, float]:
    total = sum(max(v, 0.0) for v in mix.values()) or 1.0
    return {k: max(v, 0.0) / total for k, v in mix.items()}


def _simulate_path(cases: int, stages: List[Dict[str, float]]) -> Dict[str, Any]:
    per_stage_times: Dict[str, List[float]] = {s["name"]: [] for s in stages}
    per_stage_hit: Dict[str, int] = {s["name"]: 0 for s in stages}
    totals: List[float] = []
    hit_all = 0

    for _ in range(cases):
        total = 0.0
        all_ok = True
        for s in stages:
            t = np.random.normal(s["mean_minutes"], s["std_minutes"])
            t = _clamp_pos(t)
            total += t
            per_stage_times[s["name"]].append(t)
            if t <= s["sla_minutes"]:
                per_stage_hit[s["name"]] += 1
            else:
                all_ok = False
        totals.append(total)
        if all_ok:
            hit_all += 1

    # KPIs del camino
    avg_total = float(np.mean(totals)) if totals else 0.0
    p90_total = float(np.percentile(totals, 90)) if totals else 0.0
    compliance_total = round(100 * hit_all / cases, 1) if cases else 0.0

    # estadisticos por etapa
    stage_stats = []
    contrib = []
    for s in stages:
        name = s["name"]
        arr = np.array(per_stage_times[name]) if per_stage_times[name] else np.array([0])
        avg = float(np.mean(arr))
        p90 = float(np.percentile(arr, 90))
        sla = s["sla_minutes"]
        comp = round(100 * per_stage_hit[name] / cases, 1) if cases else 0.0
        stage_stats.append({"name": name, "avg": avg, "p90": p90, "sla": sla, "compliance_pct": comp})
        contrib.append((name, avg))

    contrib.sort(key=lambda x: x[1], reverse=True)
    bottlenecks = [name for name, _ in contrib[:2]]

    return {
        "cases": cases,
        "avg_total_minutes": round(avg_total, 1),
        "p90_total_minutes": round(p90_total, 1),
        "compliance_total_pct": compliance_total,
        "stages": stage_stats,
        "bottlenecks": bottlenecks,
    }


def run_simulation_global(total_cases: int, mix: Dict[str, float], flows: Dict[str, List[Dict[str, float]]]) -> Dict[str, Any]:
    """
    Simula total_cases asignando cada caso a un camino segun mix normalizado.
    Retorna KPIs por camino y globales.
    """
    mix_n = _normalize_mix(mix)
    keys = list(mix_n.keys())
    probs = list(mix_n.values())

    # conteo por camino
    counts = {k: 0 for k in keys}
    choices = np.random.choice(keys, size=total_cases, p=probs)
    for k in choices:
        counts[k] += 1

    per_flow_results: Dict[str, Dict[str, Any]] = {}
    global_totals: List[float] = []
    global_hit_all = 0
    global_cases = 0

    # simulacion por camino
    for k in keys:
        n = counts[k]
        if n <= 0:
            per_flow_results[k] = {"cases": 0, "avg_total_minutes": 0, "p90_total_minutes": 0,
                                   "compliance_total_pct": 0, "stages": [], "bottlenecks": []}
            continue

        res = _simulate_path(n, flows[k])
        per_flow_results[k] = res

    # Agregar globales (promedios ponderados)
    if total_cases > 0:
        # mezclar sumando promedios ponderados por cantidad
        overall_avg = 0.0
        overall_p90_approx = 0.0  # aproximacion por ponderacion
        overall_comp = 0.0
        contrib_global: List[Tuple[str, float]] = []

        for k in keys:
            n = per_flow_results[k]["cases"]
            if n == 0:
                continue
            frac = n / total_cases
            overall_avg += per_flow_results[k]["avg_total_minutes"] * frac
            overall_p90_approx += per_flow_results[k]["p90_total_minutes"] * frac
            overall_comp += per_flow_results[k]["compliance_total_pct"] * frac
            # contribuciones promedio por etapa (agregadas por nombre)
            for st in per_flow_results[k]["stages"]:
                contrib_global.append((st["name"], st["avg"] * frac))

        # top 3 "bottlenecks" globales por contribucion ponderada
        agg: Dict[str, float] = {}
        for name, val in contrib_global:
            agg[name] = agg.get(name, 0.0) + val
        bottlenecks_global = sorted(agg.items(), key=lambda x: x[1], reverse=True)[:3]
        bottlenecks_global = [n for n, _ in bottlenecks_global]

        overall = {
            "cases": total_cases,
            "avg_total_minutes": round(overall_avg, 1),
            "p90_total_minutes": round(overall_p90_approx, 1),
            "compliance_total_pct": round(overall_comp, 1),
            "bottlenecks": bottlenecks_global,
        }
    else:
        overall = {"cases": 0, "avg_total_minutes": 0, "p90_total_minutes": 0, "compliance_total_pct": 0, "bottlenecks": []}

    return {
        "counts": counts,
        "per_flow": per_flow_results,
        "overall": overall,
    }
