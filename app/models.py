from pydantic import BaseModel, Field
from typing import List, Dict


class Stage(BaseModel):
    name: str
    mean_minutes: float = Field(gt=0, description="Tiempo promedio por etapa")
    std_minutes: float = Field(ge=0, description="Desviacion estandar")
    sla_minutes: float = Field(gt=0, description="SLA meta por etapa")


class FlowConfig(BaseModel):
    stages: List[Stage]


class SimulationInput(BaseModel):
    cases: int = Field(ge=1, le=5000, default=300)
    # mezcla de casos: debe sumar ~1.0 (se normaliza)
    mix: Dict[str, float] = Field(
        default={"vivo": 0.6, "remision": 0.25, "voluntario": 0.15}
    )
    flows: Dict[str, FlowConfig]
