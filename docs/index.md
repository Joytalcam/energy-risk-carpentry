# Planificación Energética bajo Incertidumbre: Modelo de Carpintería

## 1. Introducción

Este proyecto implementa un **Modelo de Programación Estocástica de Dos Etapas** para la planificación de recursos en una carpintería, basado en el ejemplo clásico de Higle (2005) y las diapositivas del Prof. David Pozo (Skoltech). El objetivo es demostrar cómo la inclusión de incertidumbre y la gestión de riesgo (CVaR) mejoran la toma de decisiones en comparación con los enfoques deterministas.

## 2. Formulación Matemática

### 2.1 Conjuntos y Parámetros

| Símbolo | Descripción |
|---------|-------------|
| $W$ | Conjunto de escenarios (Low, Medium, High) |
| $\pi_w$ | Probabilidad del escenario $w$ |
| $d_{dw}, d_{tw}, d_{cw}$ | Demanda de escritorios, mesas y sillas en el escenario $w$ |
| $c_l, c_f, c_p$ | Costos unitarios de madera, acabado y carpintería |
| $p_d, p_t, p_c$ | Precios de venta de escritorios, mesas y sillas |

### 2.2 Variables de Decisión

**Primera Etapa (Aquí y Ahora):**
*   $x_l$: Cantidad de madera a comprar.
*   $x_f$: Horas de acabado a contratar.
*   $x_p$: Horas de carpintería a contratar.

**Segunda Etapa (Esperar y Ver, por escenario $w$):**
*   $y_{dw}, y_{tw}, y_{cw}$: Producción de escritorios, mesas y sillas en el escenario $w$.

### 2.3 Modelo Estocástico (Risk Neutral)

$$
\max \sum_{w \in W} \pi_w (60 y_{dw} + 40 y_{tw} + 10 y_{cw}) - 2x_l - 4x_f - 5.2x_p
$$

**Sujeto a:**

*   **Restricciones de Demanda (Segunda Etapa):**
    $$y_{dw} \le d_{dw}, \quad y_{tw} \le d_{tw}, \quad y_{cw} \le d_{cw} \quad \forall w \in W$$

*   **Restricciones de Recursos (Acoplamiento):**
    $$8y_{dw} + 6y_{tw} + 1y_{cw} \le x_l \quad \forall w \in W$$
    $$4y_{dw} + 2y_{tw} + 1.5y_{cw} \le x_f \quad \forall w \in W$$
    $$2y_{dw} + 1.5y_{tw} + 0.5y_{cw} \le x_p \quad \forall w \in W$$

### 2.4 Modelo con Aversión al Riesgo (CVaR)

Para gestionar el riesgo, se maximiza el **Conditional Value at Risk (CVaR)** en lugar del beneficio esperado. Siguiendo a Rockafellar y Uryasev (2000), introducimos la variable $\eta$ (VaR) y las variables de exceso $u_w$:

$$
\max \eta - \frac{1}{1-\alpha} \sum_{w \in W} \pi_w u_w
$$

**Sujeto a:**
$$\eta - \text{Profit}_w \le u_w \quad \forall w \in W$$
$$u_w \ge 0 \quad \forall w \in W$$
*(Más las restricciones del modelo original)*

Donde $\alpha \in [0, 1]$ es el nivel de aversión al riesgo. $\alpha = 0.5$ maximiza el 50% de los peores escenarios.

## 3. Métricas de Valor de la Información

*   **EVPI (Expected Value of Perfect Information):** Mide cuánto estaríamos dispuestos a pagar por conocer el futuro con certeza. $EVPI = WS - RP$.
*   **VSS (Value of Stochastic Solution):** Mide el valor de modelar la incertidumbre en lugar de usar solo el promedio. $VSS = RP - EEV$.

## 4. Resultados Clave

| Métrica | Valor |
|---------|-------|
| Beneficio Esperado (RP) | $1730.00 |
| Wait-and-See (WS) | $4165.00 |
| EEV (Plan con Promedio) | $1545.00 |
| **EVPI** | **$2435.00** |
| **VSS** | **$185.00** |

## 5. Referencias

*   Higle, J. L. (2005). *Stochastic Programming: Optimization When Uncertainty Matters*.
*   Pozo, D. (2019). *Decision Making Under Uncertainty: Stochastic Programming - Risk*. Skoltech.
*   Rockafellar, R. T., & Uryasev, S. (2000). *Optimization of Conditional Value-at-Risk*. Journal of Risk.