# Sistema de Gestión - Ley de Enfriamiento de Newton

Sistema interactivo para la gestión y análisis de la Ley de Enfriamiento de Newton, específicamente diseñado para modelar el enfriamiento de un bloque de acero.

## Caso de Estudio

Este sistema está centrado en el siguiente problema de la industria manufacturera:

**Problema:** Un bloque de acero con dimensiones de **10 cm × 10 cm × 2 cm** es retirado de un horno industrial a una temperatura de **300°C**. Inmediatamente se coloca en un ambiente con temperatura constante de **20°C** para su enfriamiento. Después de **5 minutos**, se mide que la temperatura del bloque ha descendido a **200°C**.

**Contexto Industrial:** Este tipo de situación es común en procesos de manufactura como el tratamiento térmico de metales, donde es fundamental controlar la velocidad de enfriamiento para garantizar propiedades mecánicas específicas.

**Parámetros del Caso de Estudio:**
- Temperatura inicial: $T_0 = 300°C$
- Temperatura ambiente: $T_a = 20°C$
- Temperatura medida a los 5 minutos: $T(5) = 200°C$
- Constante de enfriamiento calculada: $k \approx 0.088367$ min⁻¹

> **Nota:** Aunque el sistema está diseñado alrededor de este caso específico, puede adaptarse a cualquier problema de enfriamiento cambiando los parámetros.

## Modelo Matemático

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

$$\ln|T - T_a| + kt = C$$

Donde $C = \ln|T_0 - T_a|$ es una constante determinada por las condiciones iniciales.

## Parámetros del Sistema

- **Temperatura Inicial (T₀)**: Temperatura inicial del objeto metálico (°C)
- **Temperatura Ambiente (Tₐ)**: Temperatura constante del medio ambiente (°C)
- **Constante de Enfriamiento (k)**: Constante de proporcionalidad (min⁻¹)

### Valores por Defecto (Caso de Estudio)

Los valores por defecto corresponden al caso de estudio del bloque de acero:

- **T₀ = 300°C**: Temperatura inicial del bloque al salir del horno
- **Tₐ = 20°C**: Temperatura constante del ambiente de enfriamiento
- **k = 0.088367 min⁻¹**: Constante calculada a partir de la medición experimental (T(5min) = 200°C)

La constante $k$ se calcula usando la fórmula:
$$k = \frac{1}{t} \ln\left(\frac{T_0 - T_a}{T - T_a}\right) = \frac{1}{5} \ln\left(\frac{300 - 20}{200 - 20}\right) \approx 0.088367 \text{ min}^{-1}$$

## Verificación Matemática

El sistema verifica que la solución implícita satisface la ecuación diferencial mediante:

1. Cálculo de la expresión $\ln|T - T_a| + kt$ para múltiples valores de tiempo
2. Verificación de que esta expresión permanece constante (igual a C)
3. Derivación implícita para confirmar que se recupera la ecuación diferencial original

## Autores

Desarrollado para el análisis de ecuaciones diferenciales aplicadas a problemas de ingeniería.

---

**Nota**: Este sistema es una herramienta educativa para el análisis y visualización de la Ley de Enfriamiento de Newton.
