# Prototipo de Estandarizacion del Proceso de Egreso – HUN

Prototipo digital para **simular y analizar el proceso de egreso hospitalario** del Hospital Universitario Nacional (HUN).  
Permite evaluar tiempos, SLAs y cuellos de botella en **tres tipos de egreso**:

- Egreso hospitalario (vivo)  
- Egreso por remision  
- Egreso voluntario  

---

## 🧩 Contexto del problema

El HUN tiene una meta mensual de **880 egresos**, pero el desempeño reciente ronda los **722 egresos/mes**, es decir, cerca de un **20% por debajo de la meta**.

Durante las visitas y entrevistas al hospital se identifico que una de las causas criticas es la:

> Falta de estandarizacion y trazabilidad en la comunicacion entre las areas que intervienen en el egreso.

Esto genera:
- Tiempos muertos
- Retrasos administrativos
- Cuellos de botella invisibles
- Baja rotacion de cama

---

## 🎯 Objetivo del prototipo

Construir un **simulador digital del proceso de egreso**, alineado con la realidad del HUN, que permita:

- Medir tiempos promedio y variabilidad por etapa  
- Calcular cumplimiento de SLAs (tiempos objetivo)  
- Identificar cuellos de botella por tipo de egreso  
- Probar escenarios “que pasaria si” sin intervenir el proceso real  

El prototipo funciona como una herramienta de **apoyo a la decision** para jefaturas, coordinaciones y equipos de mejora de procesos.

---

## 🏗️ Arquitectura general

**Backend**
- Python 3.12
- FastAPI (API REST)
- NumPy (simulacion estadistica)
- Pydantic (modelos de datos)

**Frontend**
- HTML + CSS sencillo (sin frameworks pesados)
- JavaScript nativo
- Tablas editables para tiempos y SLAs
- Comunicacion con el backend via `fetch` (JSON)

---

## 📁 Estructura del proyecto

```text
egreso_prototipo/
├── app/
│   ├── main.py          # Rutas, FastAPI, templates
│   ├── models.py        # Modelos Pydantic de entrada
│   ├── simulation.py    # Logica de simulacion de tiempos
│   ├── templates/
│   │   └── index.html   # Interfaz web principal
│   └── static/
│       └── script.js    # Logica de interfaz y llamadas a la API
├── requirements.txt     # Dependencias de Python
├── .gitignore
└── README.md
