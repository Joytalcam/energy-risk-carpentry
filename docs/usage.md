# Guía de Instalación y Uso

## Requisitos Previos

* Python 3.10 o superior.
* Git (opcional, para clonar el repo).

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/energy-risk-carpentry.git](https://github.com/tu-usuario/energy-risk-carpentry.git)
   cd energy-risk-carpentry
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Mac/Linux:
   source .venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Análisis en Notebook**  
   Ejecuta Jupyter para ver el análisis completo de EVPI, VSS y la Frontera Eficiente:
   ```bash
   python -m notebook
   ```
   Abre `notebooks/01_carpentry_analysis.ipynb`.

2. **Aplicación Interactiva (Streamlit)**  
   Para explorar los escenarios y el nivel de riesgo de forma visual:
   ```bash
   streamlit run app.py
   ```
   Se abrirá en `http://localhost:8501`.

3. **Tests Automáticos**  
   Para verificar que el modelo funciona correctamente:
   ```bash
   pytest tests/ -v
   ```

## Estructura del Proyecto

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
└── README.md             # Carta de presentación
```