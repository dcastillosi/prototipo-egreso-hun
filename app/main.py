from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import SimulationInput
from .simulation import run_simulation_global

app = FastAPI(title="Prototipo Egreso HUN (3 flujos)")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "vivo": [
        {"name": "Orden de egreso + resumen clinico", "mean_minutes": 60, "std_minutes": 15, "sla_minutes": 90},
        {"name": "Epicrisis + inventario habitacion", "mean_minutes": 45, "std_minutes": 10, "sla_minutes": 60},
        {"name": "Devolucion medicamentos", "mean_minutes": 15, "std_minutes": 5, "sla_minutes": 30},
        {"name": "Alta temprana (pendientes admin)", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 40},
        {"name": "Facturacion / copagos", "mean_minutes": 50, "std_minutes": 20, "sla_minutes": 90},
        {"name": "TICs: depuracion pendientes HC", "mean_minutes": 30, "std_minutes": 10, "sla_minutes": 60},
        {"name": "TICs: cierre facturacion", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "TICs: cierre historia clinica", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "Limpieza y alistamiento de cama", "mean_minutes": 40, "std_minutes": 15, "sla_minutes": 60},
    ],
    "remision": [
        {"name": "Diligenciar formatos de remision", "mean_minutes": 40, "std_minutes": 15, "sla_minutes": 60},
        {"name": "Generar remision en sistema", "mean_minutes": 30, "std_minutes": 10, "sla_minutes": 45},
        {"name": "Referencia valida y abre tramite", "mean_minutes": 60, "std_minutes": 20, "sla_minutes": 120},
        {"name": "Coordina movil y comunica llegada", "mean_minutes": 60, "std_minutes": 20, "sla_minutes": 120},
        {"name": "Devolucion medicamentos", "mean_minutes": 15, "std_minutes": 5, "sla_minutes": 30},
        {"name": "Facturacion / copagos", "mean_minutes": 50, "std_minutes": 20, "sla_minutes": 90},
        {"name": "TICs: depuracion pendientes HC", "mean_minutes": 30, "std_minutes": 10, "sla_minutes": 60},
        {"name": "TICs: cierre facturacion", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "TICs: cierre historia clinica", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "Limpieza y alistamiento de cama", "mean_minutes": 40, "std_minutes": 15, "sla_minutes": 60},
    ],
    "voluntario": [
        {"name": "Explicacion condicion y consecuencias", "mean_minutes": 30, "std_minutes": 10, "sla_minutes": 45},
        {"name": "Registro en HC + firma voluntaria", "mean_minutes": 35, "std_minutes": 10, "sla_minutes": 60},
        {"name": "Devolucion medicamentos", "mean_minutes": 15, "std_minutes": 5, "sla_minutes": 30},
        {"name": "Facturacion / copagos", "mean_minutes": 50, "std_minutes": 20, "sla_minutes": 90},
        {"name": "TICs: depuracion pendientes HC", "mean_minutes": 30, "std_minutes": 10, "sla_minutes": 60},
        {"name": "TICs: cierre facturacion", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "TICs: cierre historia clinica", "mean_minutes": 20, "std_minutes": 10, "sla_minutes": 45},
        {"name": "Limpieza y alistamiento de cama", "mean_minutes": 40, "std_minutes": 15, "sla_minutes": 60},
    ],
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "defaults": DEFAULTS})


@app.post("/simulate", response_class=JSONResponse)
async def simulate(payload: SimulationInput):
    flows = {k: [s.model_dump() for s in v.stages] for k, v in payload.flows.items()}
    result = run_simulation_global(payload.cases, payload.mix, flows)
    return result
