# src/model.py
import pyomo.environ as pyo

def build_stochastic_model(scenarios, probs, alpha=None):
    """
    Construye el modelo estocástico de dos etapas para la carpintería.
    
    Si alpha es None -> Modelo Risk Neutral (Estrategia E)
    Si alpha es float -> Modelo Risk Averse con CVaR (Estrategia F)
    """
    m = pyo.ConcreteModel()
    
    # Conjuntos
    m.W = pyo.Set(initialize=scenarios.keys())
    
    # --- Variables de Primera Etapa (Recursos - Aquí y Ahora) ---
    m.x_l = pyo.Var(domain=pyo.NonNegativeReals) # Madera (lumber)
    m.x_f = pyo.Var(domain=pyo.NonNegativeReals) # Acabado (finishing)
    m.x_p = pyo.Var(domain=pyo.NonNegativeReals) # Carpintería (carpentry)
    
    # --- Variables de Segunda Etapa (Producción - Esperar y Ver) ---
    m.y_d = pyo.Var(m.W, domain=pyo.NonNegativeReals) # Escritorios (desks)
    m.y_t = pyo.Var(m.W, domain=pyo.NonNegativeReals) # Mesas (tables)
    m.y_c = pyo.Var(m.W, domain=pyo.NonNegativeReals) # Sillas (chairs)
    
    # Expresión de beneficio por escenario
    def profit_rule(m, w):
        return (60 * m.y_d[w] + 40 * m.y_t[w] + 10 * m.y_c[w] - 
                2 * m.x_l - 4 * m.x_f - 5.2 * m.x_p)
    m.profit_w = pyo.Expression(m.W, rule=profit_rule)
    
    # --- Restricciones ---
    # 1. Límites de Demanda por escenario
    m.demand_d = pyo.Constraint(m.W, rule=lambda m, w: m.y_d[w] <= scenarios[w]['d'])
    m.demand_t = pyo.Constraint(m.W, rule=lambda m, w: m.y_t[w] <= scenarios[w]['t'])
    m.demand_c = pyo.Constraint(m.W, rule=lambda m, w: m.y_c[w] <= scenarios[w]['c'])
    
    # 2. Uso de Recursos (Acoplamiento entre etapas)
    m.res_lumber = pyo.Constraint(m.W, rule=lambda m, w: 8*m.y_d[w] + 6*m.y_t[w] + 1*m.y_c[w] - m.x_l <= 0)
    m.res_finish = pyo.Constraint(m.W, rule=lambda m, w: 4*m.y_d[w] + 2*m.y_t[w] + 1.5*m.y_c[w] - m.x_f <= 0)
    m.res_carp   = pyo.Constraint(m.W, rule=lambda m, w: 2*m.y_d[w] + 1.5*m.y_t[w] + 0.5*m.y_c[w] - m.x_p <= 0)
    
    # --- Función Objetivo ---
    if alpha is None:
        # Estrategia E: Risk Neutral (Maximizar Beneficio Esperado)
        m.obj = pyo.Objective(
            expr=sum(probs[w] * m.profit_w[w] for w in m.W),
            sense=pyo.maximize
        )
        m.is_risk_averse = False
    else:
        # Estrategia F: Risk Averse (Maximizar CVaR)
        m.eta = pyo.Var() # Value at Risk (VaR)
        m.u = pyo.Var(m.W, domain=pyo.NonNegativeReals) # Exceso de pérdida
        
        # Restricciones del CVaR
        m.cvar_con = pyo.Constraint(m.W, rule=lambda m, w: m.eta - m.profit_w[w] <= m.u[w])
        
        # Objetivo CVaR (Rockafellar & Uryasev)
        m.obj = pyo.Objective(
            expr=m.eta - (1/(1-alpha)) * sum(probs[w] * m.u[w] for w in m.W),
            sense=pyo.maximize
        )
        m.is_risk_averse = True
        
    return m


def solve_model(m):
    """Resuelve el modelo usando HiGHS y retorna el estado."""
    solver = pyo.SolverFactory('appsi_highs')
    results = solver.solve(m)
    return results

def calculate_ws(scenarios, probs):
    """
    Wait-and-See (WS): Resuelve el problema perfectamente para cada escenario 
    y promedia los resultados. (Asume que sabemos el futuro).
    """
    ws_profits = {}
    for w, demand in scenarios.items():
        # Creamos un escenario "falso" donde solo existe w con prob 1
        single_scenario = {w: demand}
        single_prob = {w: 1.0}
        m = build_stochastic_model(single_scenario, single_prob, alpha=None)
        solve_model(m)
        ws_profits[w] = pyo.value(m.profit_w[w])
    
    ws_expected = sum(probs[w] * ws_profits[w] for w in scenarios)
    return ws_expected

def calculate_eev(scenarios, probs):
    """
    Expected result of using the Expected Value solution (EEV).
    Resuelve el problema con la demanda promedio y luego evalúa ese plan
    en los escenarios reales.
    """
    # 1. Calcular demanda promedio
    avg_scenario = {
        'Avg': {
            'd': sum(probs[w] * scenarios[w]['d'] for w in scenarios),
            't': sum(probs[w] * scenarios[w]['t'] for w in scenarios),
            'c': sum(probs[w] * scenarios[w]['c'] for w in scenarios)
        }
    }
    # 2. Resolver con el promedio
    m_avg = build_stochastic_model(avg_scenario, {'Avg': 1.0}, alpha=None)
    solve_model(m_avg)
    
    # Extraer las decisiones de primera etapa (el plan de recursos)
    x_l_fix = pyo.value(m_avg.x_l)
    x_f_fix = pyo.value(m_avg.x_f)
    x_p_fix = pyo.value(m_avg.x_p)
    
    # 3. Evaluar ese plan fijo en los escenarios reales
    eev_profits = {}
    for w, demand in scenarios.items():
        m_eval = build_stochastic_model({w: demand}, {w: 1.0}, alpha=None)
        # Fijamos los recursos calculados en el paso 2
        m_eval.x_l.fix(x_l_fix)
        m_eval.x_f.fix(x_f_fix)
        m_eval.x_p.fix(x_p_fix)
        solve_model(m_eval)
        eev_profits[w] = pyo.value(m_eval.profit_w[w])
        
    eev_expected = sum(probs[w] * eev_profits[w] for w in scenarios)
    return eev_expected