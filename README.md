# HUN: Alertas inteligentes

Este proyecto implementa un **prototipo digital** para simular y analizar el proceso de egreso hospitalario en el Hospital Universitario Nacional (HUN).  
El sistema permite detectar cuellos de botella, medir tiempos, evaluar cumplimiento de SLAs y probar escenarios de mejora sin intervenir el proceso real.

---

## 🧩 Contexto del problema

El HUN tiene una meta mensual de **880 egresos**, pero el desempeño reciente ronda los **722 egresos/mes**, cerca de un **20% por debajo de la meta**.

La causa crítica identificada es:

> Falta de estandarizacion, comunicación fragmentada y baja trazabilidad entre áreas involucradas en el proceso.

Esto produce:
- Tiempos muertos  
- Retrasos administrativos  
- Cuellos de botella invisibles  
- Baja rotación de cama  
- Ausencia de métricas claras  

---

## 🎯 Objetivo del prototipo

Desarrollar un simulador interactivo que permita:

- Medir tiempos promedio del egreso  
- Estimar variabilidad (desviación estándar)  
- Evaluar cumplimiento de SLAs  
- Identificar cuellos de botella  
- Probar escenarios “qué pasaría si…”  
- Construir evidencia para rediseñar el proceso de egreso  

El simulador está alineado al flujo real del HUN y considera **tres tipos de egreso**:

1. Egreso hospitalario (vivo)  
2. Egreso por remisión  
3. Egreso voluntario  

---

## 🏗️ Arquitectura general

### Backend
- Python 3.12  
- FastAPI  
- NumPy (simulación estadística)  
- Pydantic  

### Frontend
- HTML + CSS sencillo  
- JavaScript nativo  
- Tablas editables  
- Comunicación con el backend vía `fetch()` (JSON)  

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
```

---

## ⚙️ Requisitos

Debes tener instalado:

- **Python 3.10+**  
- **Git**  
- **Navegador moderno** (Edge, Chrome, Firefox)

---

## 🚀 Instalación y puesta en marcha

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/prototipo-egreso-hun.git
cd prototipo-egreso-hun
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv .venv
```

### 3️⃣ Activarlo (Windows)

```bash
.venv\Scripts\activate
```

### 4️⃣ Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5️⃣ Ejecutar el servidor

```bash
python -m uvicorn app.main:app --reload
```

Deberías ver:

```
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

---

## 🌐 Uso del prototipo

Con el servidor corriendo, abrir:

```
http://127.0.0.1:8000/
```

La interfaz permite:

### ✔️ Configuración general
- Número de pacientes  
- Mezcla vivo/remisión/voluntario  

### ✔️ Edición de etapas
Cada etapa permite editar:
- Media (min)  
- Desviación estándar  
- SLA (tiempo máximo esperado)

### ✔️ Ejecutar simulación
El sistema calcula:
- Tiempo total promedio  
- P90  
- Cumplimiento de SLAs  
- Cuellos de botella  
- KPIs por flujo  

### ✔️ Resultados
El panel muestra:
- Distribución efectiva de casos  
- KPIs globales  
- KPIs por tipo de egreso  
- Rendimiento por etapa  

---

## 🧮 Cómo funciona la simulación

Para cada paciente:

1. Se asigna aleatoriamente a un flujo según la mezcla.  
2. Para cada etapa:
   - Se genera un tiempo aleatorio  
     `t ~ N(media, desviacion)`  
   - Se trunca a positivo  
   - Se evalúa SLA  
3. Se calcula tiempo total  
4. Se generan KPIs:  
   - Promedio  
   - P90  
   - Cumplimiento  
   - Cuellos de botella  

---

## 🔍 API del sistema

### `GET /`
Devuelve la interfaz del prototipo.

### `POST /simulate`
**Entrada:**
```json
{
  "cases": 300,
  "mix": { "vivo": 0.6, "remision": 0.25, "voluntario": 0.15 },
  "flows": {
    "vivo": { "stages": [...] },
    "remision": { "stages": [...] },
    "voluntario": { "stages": [...] }
  }
}
```

**Salida:**
- Casos por flujo  
- Tiempo promedio  
- P90  
- Cumplimiento  
- Cuellos de botella  
- KPIs por etapa  

---

## 📈 Mejoras planificadas

- Cargar CSV con datos reales del HUN  
- Gráficos con Chart.js  
- Escenarios preconfigurados  
- Rediseño visual (TailwindCSS)  
- Diagrama interactivo con Mermaid  

---

## 👥 Autores

Proyecto desarrollado para la asignatura **TPI – HUN: Alertas Inteligentes**  
Universidad Nacional de Colombia – 2025-II  

---

## 📄 Licencia

Pendiente según directrices académicas y del HUN.
