# Sistema de Gestión - Ley de Enfriamiento de Newton

Sistema interactivo para la gestión y análisis de la Ley de Enfriamiento de Newton, específicamente diseñado para modelar el enfriamiento de un bloque de acero.

## 🔬 Modelo Matemático

### Ecuación Diferencial

La Ley de Enfriamiento de Newton establece:

$$\frac{dT}{dt} = -k(T - T_a)$$

Donde:

- $T(t)$: temperatura del objeto en el instante $t$ (°C)
- $T_a$: temperatura ambiente (constante) (°C)
- $k > 0$: constante de enfriamiento (min⁻¹)

### Solución Explícita

$$T(t) = T_a + (T_0 - T_a) e^{-kt}$$

### Solución Implícita

$$\log|T - T_a| + kt = C$$

Donde $C = \log|T_0 - T_a|$ es una constante determinada por las condiciones iniciales.

## 🔧 Parámetros del Sistema

- **Temperatura Inicial (T₀)**: Temperatura inicial del objeto metálico (°C)
- **Temperatura Ambiente (Tₐ)**: Temperatura constante del medio ambiente (°C)
- **Constante de Enfriamiento (k)**: Constante de proporcionalidad (min⁻¹)

### Valores por Defecto (del PDF de referencia)

- T₀ = 300°C
- Tₐ = 20°C
- k = 0.088367 min⁻¹

## 🧮 Verificación Matemática

El sistema verifica que la solución implícita satisface la ecuación diferencial mediante:

1. Cálculo de la expresión $\log|T - T_a| + kt$ para múltiples valores de tiempo
2. Verificación de que esta expresión permanece constante (igual a C)
3. Derivación implícita para confirmar que se recupera la ecuación diferencial original

## 👥 Autores

Desarrollado para el análisis de ecuaciones diferenciales aplicadas a problemas de ingeniería.

---

**Nota**: Este sistema es una herramienta educativa para el análisis y visualización de la Ley de Enfriamiento de Newton.
