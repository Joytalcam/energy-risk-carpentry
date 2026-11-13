# test_quick.py
from src.data_loader import get_carpentry_data
from src.model import build_stochastic_model, solve_model
import pyomo.environ as pyo

# 1. Cargar datos
scenarios, probs = get_carpentry_data()

# 2. Construir el modelo Risk Neutral (Estrategia E)
print("--- Resolviendo Estrategia E (Risk Neutral) ---")
m = build_stochastic_model(scenarios, probs, alpha=None)

# 3. Resolver
results = solve_model(m)

# 4. Mostrar resultados
print(f"Estado del solver: {results.solver.termination_condition}")
print(f"Beneficio Esperado (Objetivo): ${pyo.value(m.obj):.2f}")
print(f"Madera comprada (x_l): {pyo.value(m.x_l):.1f}")
print(f"Acabado comprado (x_f): {pyo.value(m.x_f):.1f}")
print(f"Carpintería comprada (x_p): {pyo.value(m.x_p):.1f}")

# Mostrar producción por escenario
for w in m.W:
    print(f"Escenario {w}:")
    print(f"  Escritorios: {pyo.value(m.y_d[w]):.1f}")
    print(f"  Mesas:      {pyo.value(m.y_t[w]):.1f}")
    print(f"  Sillas:     {pyo.value(m.y_c[w]):.1f}")
    print(f"  Beneficio:  ${pyo.value(m.profit_w[w]):.2f}")