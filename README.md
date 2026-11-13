# Energy Risk Planning: Stochastic Optimization & CVaR

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pyomo](https://img.shields.io/badge/Pyomo-6.10-orange.svg)](https://www.pyomo.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Descripción

Este proyecto implementa un **Modelo de Programación Estocástica de Dos Etapas** para la planificación de recursos en una carpintería, basado en el ejemplo clásico de **Higle (2005)** y las diapositivas del **Prof. David Pozo (Skoltech)**.

El objetivo es demostrar cómo la inclusión de incertidumbre y la gestión de riesgo (**CVaR**) mejoran la toma de decisiones en comparación con los enfoques deterministas. El proyecto incluye desde la formulación matemática hasta una aplicación interactiva para explorar escenarios.

## 🎯 Resultados Clave

| Métrica | Valor | Interpretación |
| :--- | :--- | :--- |
| Beneficio Esperado (RP) | **$1730.00** | Solución estocástica óptima |
| Wait-and-See (WS) | **$4165.00** | Solución con información perfecta |
| **EVPI** | **$2435.00** | Valor máximo a pagar por información perfecta |
| **VSS** | **$185.00** | Valor de modelar la incertidumbre (10.69%) |

*El modelo con aversión al riesgo ($\alpha=0.5$) reduce el beneficio esperado a $1230, pero asegura un CVaR de $1140 (evitando pérdidas en el peor escenario).*

## 🛠️ Stack Tecnológico

* **Optimización:** Pyomo + HiGHS (100% open source).
* **Datos y Análisis:** Pandas, NumPy.
* **Visualización:** Matplotlib, Seaborn.
* **App Interactiva:** Streamlit.
* **Tests:** Pytest.

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone [https://github.com/Joytalcam/energy-risk-carpentry.git](https://github.com/Joytalcam/energy-risk-carpentry.git)
cd energy-risk-carpentry
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Mac/Linux:
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la App Interactiva

```bash
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

### 5. Ejecutar los Tests

```bash
pytest tests/ -v
```

## 📂 Estructura del Proyecto

```text
energy-risk-carpentry/
├── src/                  # Backend (Lógica matemática)
│   ├── data_loader.py    # Carga de datos
│   └── model.py          # Modelo Pyomo + CVaR
├── notebooks/            # Análisis y storytelling
│   └── 01_carpentry_analysis.ipynb
├── tests/                # Red de seguridad
│   └── test_model.py
├── docs/                 # Documentación técnica
│   ├── index.md
│   └── usage.md
├── app.py                # Frontend (Streamlit)
├── requirements.txt      # Dependencias
├── pytest.ini            # Configuración de tests
└── README.md             # Carta de presentación
```

## 📚 Referencias

* Higle, J. L. (2005). *Stochastic Programming: Optimization When Uncertainty Matters*.
* Pozo, D. (2019). *Decision Making Under Uncertainty: Stochastic Programming - Risk*. Skoltech.
* Rockafellar, R. T., & Uryasev, S. (2000). *Optimization of Conditional Value-at-Risk*. Journal of Risk.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

* Al Prof. David Pozo (Skoltech) por sus invaluables materiales docentes sobre planificación energética, programación estocástica y gestión de riesgo, que inspiraron este proyecto.
* A la comunidad Open Source por herramientas como Pyomo, HiGHS, Streamlit y Pandas, que hacen posible este tipo de desarrollos sin costos de licencia.
* A Higle (2005) por el ejemplo clásico de la carpintería, que sigue siendo una referencia fundamental para enseñar programación estocástica.

## 👤 Autor

**Joy Talcam**

* LinkedIn: [tu-linkedin](https://linkedin.com)
* GitHub: [@Joytalcam](https://github.com/Joytalcam)
