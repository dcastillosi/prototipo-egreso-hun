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

⚙️ Requisitos

Debes tener instalado:

Python 3.10+

Git

Navegador moderno (Edge, Chrome, Firefox)

🚀 Instalación y puesta en marcha
1️⃣ Clonar el repositorio
git clone https://github.com/TU-USUARIO/prototipo-egreso-hun.git
cd prototipo-egreso-hun

2️⃣ Crear entorno virtual
python -m venv .venv

3️⃣ Activarlo (Windows)
.venv\Scripts\activate

4️⃣ Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

5️⃣ Ejecutar el servidor
python -m uvicorn app.main:app --reload


Deberías ver:

Uvicorn running on http://127.0.0.1:8000
Application startup complete.

🌐 Uso del prototipo

Con el servidor corriendo, abrir:

http://127.0.0.1:8000/


La interfaz permite:

✔️ Configuración general

Número de pacientes

Mezcla vivo/remisión/voluntario

✔️ Edición de etapas

Cada etapa permite editar:

Media (min)

Desviación estándar

SLA (tiempo máximo esperado)

✔️ Ejecutar simulación

El sistema calcula:

Tiempo total promedio

P90

Cumplimiento de SLAs

Cuellos de botella

KPIs por flujo

✔️ Resultados

El panel muestra:

Distribución efectiva de casos

KPIs globales

KPIs por tipo de egreso

Rendimiento por etapa

🧮 Cómo funciona la simulación

Para cada paciente:

Se asigna aleatoriamente a un flujo según la mezcla.

Para cada etapa:

Se genera un tiempo aleatorio
t ~ N(media, desviacion)

Se trunca a positivo

Se evalúa SLA

Se calcula tiempo total

Se generan KPIs:

Promedio

P90

Cumplimiento

Cuellos de botella

🔍 API del sistema
GET /

Devuelve la interfaz del prototipo.

POST /simulate

Entrada:

{
  "cases": 300,
  "mix": { "vivo": 0.6, "remision": 0.25, "voluntario": 0.15 },
  "flows": {
    "vivo": { "stages": [...] },
    "remision": { "stages": [...] },
    "voluntario": { "stages": [...] }
  }
}


Salida:

Casos por flujo

Tiempo promedio

P90

Cumplimiento

Cuellos de botella

KPIs por etapa

📈 Mejoras planificadas

Cargar CSV con datos reales del HUN

Gráficos con Chart.js

Escenarios preconfigurados

Rediseño visual (TailwindCSS)

Diagrama interactivo con Mermaid

👥 Autores

Proyecto desarrollado para la asignatura TPI – HUN: Alertas Inteligentes
Universidad Nacional de Colombia – 2025-I

📄 Licencia

Pendiente según directrices académicas y del HUN.


---

# 🎯 **INSTRUCCIONES FINALES**
✔️ **Copia TODO el bloque de arriba (completo).**  
✔️ Pégalo en `README.md` EN VEZ del contenido actual.  
✔️ Guarda → Commit → Push.




