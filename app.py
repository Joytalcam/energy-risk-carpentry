# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pyomo.environ as pyo
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import get_carpentry_data
from src.model import build_stochastic_model, solve_model, calculate_ws, calculate_eev

# Configuración de página
st.set_page_config(page_title="Energy Risk Planning", layout="wide")

st.title("🪚 Planificación de Carpintería bajo Incertidumbre")
st.markdown("""
Esta herramienta interactiva replica el modelo de **Programación Estocástica de Dos Etapas** 
de David Pozo (basado en Higle, 2005). Ajusta los escenarios y el nivel de riesgo para ver 
cómo cambian las decisiones óptimas de compra de recursos.
""")

# --- Sidebar: Controles ---
st.sidebar.header("⚙️ Configuración de Escenarios")

# Slider para probabilidades
st.sidebar.subheader("Probabilidades")
p_low = st.sidebar.slider("Probabilidad Escenario Low", 0.0, 1.0, 0.3, 0.05)
p_med = st.sidebar.slider("Probabilidad Escenario Medium", 0.0, 1.0, 0.4, 0.05)
p_high = st.sidebar.slider("Probabilidad Escenario High", 0.0, 1.0, 0.3, 0.05)

# Normalizar probabilidades (para que sumen 1)
total_prob = p_low + p_med + p_high
if total_prob > 0:
    probs = {'Low': p_low/total_prob, 'Medium': p_med/total_prob, 'High': p_high/total_prob}
else:
    probs = {'Low': 0.33, 'Medium': 0.34, 'High': 0.33}

st.sidebar.subheader("Demanda (Escritorios, Mesas, Sillas)")
# Slider para escenario Low
st.sidebar.markdown("**Escenario Low**")
d_low = st.sidebar.slider("Escritorios Low", 0, 300, 50)
t_low = st.sidebar.slider("Mesas Low", 0, 300, 20)
c_low = st.sidebar.slider("Sillas Low", 0, 500, 200)

# Slider para escenario Medium
st.sidebar.markdown("**Escenario Medium**")
d_med = st.sidebar.slider("Escritorios Med", 0, 300, 150)
t_med = st.sidebar.slider("Mesas Med", 0, 300, 110)
c_med = st.sidebar.slider("Sillas Med", 0, 500, 225)

# Slider para escenario High
st.sidebar.markdown("**Escenario High**")
d_high = st.sidebar.slider("Escritorios High", 0, 300, 250)
t_high = st.sidebar.slider("Mesas High", 0, 300, 250)
c_high = st.sidebar.slider("Sillas High", 0, 500, 500)

scenarios = {
    'Low': {'d': d_low, 't': t_low, 'c': c_low},
    'Medium': {'d': d_med, 't': t_med, 'c': c_med},
    'High': {'d': d_high, 't': t_high, 'c': c_high}
}

st.sidebar.subheader("Nivel de Riesgo (Alpha)")
alpha_slider = st.sidebar.slider("Alpha (0 = Risk Neutral, 1 = Súper Conservador)", 0.0, 1.0, 0.5, 0.05)

# --- Main: Optimización ---
if st.sidebar.button("🚀 Calcular Solución"):
    with st.spinner("Resolviendo modelo estocástico..."):
        
        # 1. Resolver modelo con el alpha seleccionado
        m = build_stochastic_model(scenarios, probs, alpha=alpha_slider)
        solve_model(m)
        
        # 2. Extraer métricas
        expected_profit = sum(probs[w] * pyo.value(m.profit_w[w]) for w in m.W)
        cvar_value = pyo.value(m.obj)
        
        # 3. Mostrar métricas principales
        col1, col2, col3 = st.columns(3)
        col1.metric("Beneficio Esperado", f"${expected_profit:,.2f}")
        col2.metric("CVaR (Peor Escenario)", f"${cvar_value:,.2f}")
        col3.metric("Alpha Seleccionado", f"{alpha_slider:.2f}")
        
        st.divider()
        
        # 4. Mostrar decisiones de primera etapa
        st.subheader("📦 Decisiones de Compra de Recursos (Primera Etapa)")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Madera (Lumber)", f"{pyo.value(m.x_l):.1f} unidades")
        col_b.metric("Acabado (Finishing)", f"{pyo.value(m.x_f):.1f} horas")
        col_c.metric("Carpintería (Carpentry)", f"{pyo.value(m.x_p):.1f} horas")
        
        st.divider()
        
        # 5. Mostrar producción por escenario
        st.subheader("🏭 Producción por Escenario")
        prod_data = []
        for w in m.W:
            prod_data.append({
                'Escenario': w,
                'Escritorios': pyo.value(m.y_d[w]),
                'Mesas': pyo.value(m.y_t[w]),
                'Sillas': pyo.value(m.y_c[w]),
                'Beneficio ($)': pyo.value(m.profit_w[w])
            })
        st.dataframe(pd.DataFrame(prod_data), use_container_width=True)
        
        st.divider()
        
        # 6. Gráfica de beneficios por escenario
        st.subheader("📊 Distribución de Beneficios")
        fig, ax = plt.subplots(figsize=(10, 5))
        profits = [pyo.value(m.profit_w[w]) for w in m.W]
        colors = ['#ff6b6b' if p < 0 else '#51cf66' for p in profits]
        bars = ax.bar(scenarios.keys(), profits, color=colors)
        ax.axhline(0, color='black', linewidth=0.8)
        ax.set_ylabel('Beneficio ($)')
        ax.set_title(f'Beneficios por Escenario (α = {alpha_slider:.2f})')
        
        # Añadir etiquetas de valor
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'${height:,.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        
        st.pyplot(fig)
        
else:
    st.info("👈 Ajusta los parámetros en la barra lateral y presiona 'Calcular Solución'.")