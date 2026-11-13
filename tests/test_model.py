# tests/test_model.py
import pytest
import pyomo.environ as pyo
from src.data_loader import get_carpentry_data
from src.model import build_stochastic_model, solve_model, calculate_ws, calculate_eev

def test_stochastic_model_expected_profit():
    """
    Verifica que el modelo estocástico (Risk Neutral) devuelva el beneficio esperado
    de $1730, tal como en la teoría de Pozo (Higle, 2005).
    """
    scenarios, probs = get_carpentry_data()
    m = build_stochastic_model(scenarios, probs, alpha=None)
    solve_model(m)
    
    expected_profit = pyo.value(m.obj)
    assert pytest.approx(expected_profit, rel=1e-3) == 1730.0

def test_evpi():
    """
    Verifica que el EVPI sea $2435.
    """
    scenarios, probs = get_carpentry_data()
    
    m_rp = build_stochastic_model(scenarios, probs, alpha=None)
    solve_model(m_rp)
    rp_value = pyo.value(m_rp.obj)
    
    ws_value = calculate_ws(scenarios, probs)
    evpi = ws_value - rp_value
    
    assert pytest.approx(evpi, rel=1e-3) == 2435.0

def test_vss():
    """
    Verifica que el VSS sea $185.
    """
    scenarios, probs = get_carpentry_data()
    
    m_rp = build_stochastic_model(scenarios, probs, alpha=None)
    solve_model(m_rp)
    rp_value = pyo.value(m_rp.obj)
    
    eev_value = calculate_eev(scenarios, probs)
    vss = rp_value - eev_value
    
    assert pytest.approx(vss, rel=1e-3) == 185.0

def test_cvar_strategy():
    """
    Verifica que la Estrategia F (CVaR con alpha=0.5) devuelva
    el beneficio esperado de $1230, tal como en Pozo (diapositiva 65).
    """
    scenarios, probs = get_carpentry_data()
    m = build_stochastic_model(scenarios, probs, alpha=0.5)
    solve_model(m)
    
    expected_profit = sum(probs[w] * pyo.value(m.profit_w[w]) for w in m.W)
    assert pytest.approx(expected_profit, rel=1e-3) == 1230.0