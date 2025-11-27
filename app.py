"""
Sistema de Gestión de Ley de Enfriamiento de Newton
Aplicación web interactiva usando Streamlit
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from newton_cooling_calculator import NewtonCoolingCalculator

# Configuración de la página
st.set_page_config(
    page_title="Ley de Enfriamiento de Newton",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌡️ Sistema de Gestión - Ley de Enfriamiento de Newton")
st.markdown("### Enfriamiento de un Bloque de Acero")
st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #4ECDC4; margin-bottom: 20px;'>
<h4 style='color: #2c3e50; margin-top: 0;'>📋 Caso de Estudio</h4>
<p style='color: #34495e; margin-bottom: 10px;'>
Un <strong>bloque de acero</strong> con dimensiones de <strong>10 cm × 10 cm × 2 cm</strong> es retirado de un horno industrial 
a una temperatura de <strong>300°C</strong>. Inmediatamente se coloca en un ambiente con temperatura constante de <strong>20°C</strong> 
para su enfriamiento. Después de <strong>5 minutos</strong>, se mide que la temperatura del bloque ha descendido a <strong>200°C</strong>.
</p>
<p style='color: #34495e; margin: 0;'>
<strong>Contexto Industrial:</strong> Este tipo de situación es común en procesos de manufactura como el tratamiento térmico de metales, 
donde es fundamental controlar la velocidad de enfriamiento para garantizar propiedades mecánicas específicas.
</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Sidebar para parámetros de entrada
st.sidebar.header("⚙️ Parámetros del Sistema")

# Parámetros principales
T0 = st.sidebar.number_input(
    "Temperatura Inicial (°C)",
    min_value=-50.0,
    max_value=1000.0,
    value=300.0,
    step=1.0,
    help="Temperatura inicial del bloque de acero al salir del horno (caso de estudio: 300°C)"
)

Ta = st.sidebar.number_input(
    "Temperatura Ambiente (°C)",
    min_value=-50.0,
    max_value=100.0,
    value=20.0,
    step=1.0,
    help="Temperatura constante del ambiente de enfriamiento (caso de estudio: 20°C)"
)

k = st.sidebar.number_input(
    "Constante de Enfriamiento k (min⁻¹)",
    min_value=0.001,
    max_value=1.0,
    value=0.088367,
    step=0.001,
    format="%.6f",
    help="Constante de proporcionalidad del enfriamiento. Para el caso de estudio (T0=300°C, Ta=20°C, T(5min)=200°C), k ≈ 0.088367 min⁻¹"
)

# Opción para calcular k desde datos experimentales
st.sidebar.markdown("---")
st.sidebar.subheader("🔬 Calcular k desde Datos")
use_experimental = st.sidebar.checkbox("Usar datos experimentales para calcular k")

if use_experimental:
    T_measured = st.sidebar.number_input(
        "Temperatura Medida (°C)",
        min_value=-50.0,
        max_value=1000.0,
        value=200.0,
        step=1.0,
        help="Temperatura medida del bloque después de cierto tiempo (caso de estudio: 200°C a los 5 minutos)"
    )
    t_measured = st.sidebar.number_input(
        "Tiempo de Medición (min)",
        min_value=0.1,
        max_value=1000.0,
        value=5.0,
        step=0.1,
        help="Tiempo transcurrido desde que se retiró del horno (caso de estudio: 5 minutos)"
    )
    
    try:
        k = NewtonCoolingCalculator.calculate_k_from_data(T0, Ta, T_measured, t_measured)
        st.sidebar.success(f"k calculado: {k:.6f} min⁻¹")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Inicializar calculadora
try:
    calculator = NewtonCoolingCalculator(T0, Ta, k)
    
    # Mostrar información del modelo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperatura Inicial", f"{T0:.2f} °C")
    with col2:
        st.metric("Temperatura Ambiente", f"{Ta:.2f} °C")
    with col3:
        st.metric("Constante k", f"{k:.6f} min⁻¹")
    with col4:
        st.metric("Constante C", f"{calculator.C:.6f}")
    
    st.markdown("---")
    
    # Tabs para diferentes secciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visualización", 
        "📋 Tabla de Resultados", 
        "🔍 Análisis Detallado",
        "✅ Verificación de Solución",
        "📖 Información del Modelo"
    ])
    
    with tab1:
        st.header("Gráfica del Proceso de Enfriamiento")
        
        t_max = st.slider(
            "Tiempo máximo (minutos)",
            min_value=10,
            max_value=200,
            value=60,
            step=5
        )
        
        times, temperatures = calculator.generate_time_series(t_max, 200)
        cooling_rates = [calculator.cooling_rate(t) for t in times]
        
        # Crear gráfica con subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Temperatura vs Tiempo", "Razón de Enfriamiento vs Tiempo"),
            vertical_spacing=0.1,
            row_heights=[0.6, 0.4]
        )
        
        # Gráfica de temperatura
        fig.add_trace(
            go.Scatter(
                x=times,
                y=temperatures,
                mode='lines',
                name='Temperatura',
                line=dict(color='#FF6B6B', width=2),
                hovertemplate='Tiempo: %{x:.2f} min<br>Temperatura: %{y:.2f} °C<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Línea de temperatura ambiente
        fig.add_hline(
            y=Ta,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"Temperatura Ambiente ({Ta}°C)",
            row=1, col=1
        )
        
        # Gráfica de razón de enfriamiento
        fig.add_trace(
            go.Scatter(
                x=times,
                y=cooling_rates,
                mode='lines',
                name='dT/dt',
                line=dict(color='#4ECDC4', width=2),
                hovertemplate='Tiempo: %{x:.2f} min<br>Razón: %{y:.2f} °C/min<extra></extra>'
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Tiempo (min)", row=2, col=1)
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
        fig.update_yaxes(title_text="dT/dt (°C/min)", row=2, col=1)
        fig.update_layout(height=700, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Información adicional
        st.info(f"""
        **Información del modelo:**
        - Ecuación diferencial: dT/dt = -k(T - Ta)
        - Solución explícita: T(t) = {Ta:.2f} + ({T0:.2f} - {Ta:.2f}) × e^(-{k:.6f}×t)
        - La temperatura tiende asintóticamente a {Ta:.2f}°C
        """)
    
    with tab2:
        st.header("Tabla de Resultados")
        
        num_points_table = st.slider(
            "Número de puntos en la tabla",
            min_value=5,
            max_value=50,
            value=15,
            step=1
        )
        
        t_max_table = st.slider(
            "Tiempo máximo para la tabla (minutos)",
            min_value=10,
            max_value=200,
            value=30,
            step=5
        )
        
        times_table = np.linspace(0, t_max_table, num_points_table)
        temperatures_table = [calculator.temperature_explicit(t) for t in times_table]
        cooling_rates_table = [calculator.cooling_rate(t) for t in times_table]
        implicit_values = calculator.verify_implicit_solution(times_table)
        
        # Explicación simple e intuitiva antes de la tabla
        st.markdown("### 📊 Tabla de Resultados del Enfriamiento")
        
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #4ECDC4; margin-bottom: 20px;'>
        <h4 style='color: #2c3e50; margin-top: 0;'>💡 ¿Qué muestra esta tabla?</h4>
        <p style='color: #34495e; margin-bottom: 10px;'>
        Esta tabla muestra cómo cambia la temperatura del objeto a medida que pasa el tiempo. 
        <strong>Observa cómo la temperatura disminuye gradualmente</strong> desde {:.1f}°C hacia {:.1f}°C (temperatura ambiente).
        </p>
        <p style='color: #34495e; margin-bottom: 10px;'>
        <strong>Columna importante:</strong> La última columna muestra la expresión <strong>ln|T - Ta| + kt</strong>. 
        Esta es una forma matemática de verificar que nuestro modelo es correcto. 
        <span style='background-color: #fff3cd; padding: 2px 5px; border-radius: 3px;'>
        <strong>¡Mira cómo todos los valores son prácticamente iguales!</strong>
        </span>
        </p>
        <p style='color: #34495e; margin: 0;'>
        Si todos los valores de esta columna son iguales (o muy cercanos), significa que nuestra solución matemática 
        es correcta y el modelo funciona bien.
        </p>
        </div>
        """.format(T0, Ta), unsafe_allow_html=True)
        
        st.info("""
        **🔍 Explicación simple de la última columna:**
        
        La expresión **ln|T - Ta| + kt** es como una "firma matemática" que debe mantenerse constante. 
        Imagínalo como una balanza: aunque la temperatura cambia con el tiempo, esta expresión siempre suma el mismo valor.
        
        - Cuando el objeto está muy caliente (t=0), la diferencia |T - Ta| es grande
        - A medida que pasa el tiempo, la temperatura baja y la diferencia |T - Ta| se hace más pequeña
        - Pero el término **kt** aumenta con el tiempo
        - **La suma de ambos siempre da el mismo resultado** = {:.6f}
        
        Esto confirma que nuestro modelo matemático es correcto ✅
        """.format(calculator.C))
        
        df = pd.DataFrame({
            'Tiempo (min)': [f"{t:.2f}" for t in times_table],
            'Temperatura (°C)': [f"{T:.2f}" for T in temperatures_table],
            'Razón de Enfriamiento (°C/min)': [f"{rate:.2f}" for rate in cooling_rates_table],
            'Solución Implícita: ln|T-Ta| + kt (debe ser constante = C)': [f"{val:.6f}" for val in implicit_values]
        })
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Explicación después de la tabla
        st.markdown("""
        <div style='background-color: #d4edda; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin-top: 20px;'>
        <h4 style='color: #155724; margin-top: 0;'>✅ ¿Qué observamos en la tabla?</h4>
        <ul style='color: #155724; margin-bottom: 0;'>
        <li><strong>Temperatura:</strong> Empieza en {:.1f}°C y va disminuyendo hacia {:.1f}°C</li>
        <li><strong>Razón de Enfriamiento:</strong> Es más rápida al inicio (cuando hay más diferencia de temperatura) y se hace más lenta con el tiempo</li>
        <li><strong>Solución Implícita:</strong> Todos los valores son aproximadamente <strong>{:.6f}</strong> - ¡esto confirma que el modelo es correcto!</li>
        </ul>
        </div>
        """.format(T0, Ta, calculator.C), unsafe_allow_html=True)
        
        # Botón para descargar
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar tabla como CSV",
            data=csv,
            file_name=f"newton_cooling_results_T0_{T0}_Ta_{Ta}_k_{k:.6f}.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.header("Análisis Detallado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temperatura en Tiempo Específico")
            t_specific = st.number_input(
                "Tiempo (minutos)",
                min_value=0.0,
                max_value=500.0,
                value=10.0,
                step=0.5
            )
            
            T_at_t = calculator.temperature_explicit(t_specific)
            rate_at_t = calculator.cooling_rate(t_specific)
            
            st.metric("Temperatura", f"{T_at_t:.2f} °C")
            st.metric("Razón de Enfriamiento", f"{rate_at_t:.2f} °C/min")
            
            # Diferencia con temperatura ambiente
            diff = abs(T_at_t - Ta)
            st.metric("Diferencia con Ambiente", f"{diff:.2f} °C")
        
        with col2:
            st.subheader("Tiempo para Alcanzar Temperatura")
            target_temp = st.number_input(
                "Temperatura Objetivo (°C)",
                min_value=float(Ta + 0.1) if T0 > Ta else -100.0,
                max_value=float(T0 - 0.1) if T0 > Ta else 1000.0,
                value=(T0 + Ta) / 2,
                step=1.0
            )
            
            time_to_target = calculator.time_to_reach_temperature(target_temp)
            
            if time_to_target is not None:
                st.metric("Tiempo Requerido", f"{time_to_target:.2f} minutos")
                st.metric("Tiempo Requerido", f"{time_to_target/60:.2f} horas")
                
                # Verificación
                T_verify = calculator.temperature_explicit(time_to_target)
                st.info(f"Verificación: T({time_to_target:.2f}) = {T_verify:.2f}°C")
            else:
                st.warning("La temperatura objetivo no es alcanzable con los parámetros dados.")
        
        # Análisis de tiempos característicos
        st.subheader("Tiempos Característicos")
        
        # Tiempo para reducir a la mitad la diferencia inicial
        half_diff_temp = Ta + (T0 - Ta) / 2
        t_half = calculator.time_to_reach_temperature(half_diff_temp)
        
        # Tiempo para alcanzar 90% de la diferencia inicial
        ninety_percent_temp = Ta + 0.1 * (T0 - Ta)
        t_90 = calculator.time_to_reach_temperature(ninety_percent_temp)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tiempo para reducir diferencia a la mitad", 
                     f"{t_half:.2f} min" if t_half else "N/A")
        with col2:
            st.metric("Tiempo para alcanzar 90% del equilibrio", 
                     f"{t_90:.2f} min" if t_90 else "N/A")
        with col3:
            # Tiempo de vida media térmica (similar a decaimiento exponencial)
            t_half_life = np.log(2) / k
            st.metric("Vida Media Térmica (ln(2)/k)", f"{t_half_life:.2f} min")
    
    with tab4:
        st.header("Verificación de la Solución Implícita")
        
        st.markdown("""
        ### ¿Qué es la Solución Implícita?
        
        Al resolver la ecuación diferencial $\frac{dT}{dt} = -k(T - T_a)$ por el método de separación de variables, 
        obtenemos una relación matemática que puede expresarse en forma **implícita**:
        
        $$
        \\ln|T - T_a| + kt = C
        $$
        
        ### ¿Qué significa esta expresión?
        
        Esta expresión combina dos términos:
        
        1. **$\\ln|T - T_a|$**: El lnaritmo natural del valor absoluto de la diferencia entre la temperatura del objeto 
           y la temperatura ambiente. Este término disminuye a medida que el objeto se acerca a la temperatura ambiente.
        
        2. **$kt$**: El producto de la constante de enfriamiento por el tiempo transcurrido. Este término aumenta linealmente con el tiempo.
        
        ### ¿Por qué es importante verificar esto?
        
        La suma de estos dos términos debe resultar en una **constante C** para todos los valores de tiempo. 
        Esta constante se determina a partir de las condiciones iniciales: $C = \\ln|T_0 - T_a|$.
        
        Si esta expresión se mantiene constante, confirma matemáticamente que nuestra solución satisface correctamente 
        la ecuación diferencial original. Esta es una forma rigurosa de verificar la validez del modelo.
        
        ### Interpretación Física
        
        La solución implícita nos dice que a medida que pasa el tiempo, la diferencia de temperatura disminuye exponencialmente, 
        pero la combinación lnarítmica de esta diferencia más el tiempo escalado por la constante k siempre suma el mismo valor constante.
        """)
        
        # Generar datos para verificación
        times_verify = np.linspace(0, 60, 20)
        implicit_values_verify = calculator.verify_implicit_solution(times_verify)
        
        # Crear gráfica de verificación
        fig_verify = go.Figure()
        
        fig_verify.add_trace(
            go.Scatter(
                x=times_verify,
                y=implicit_values_verify,
                mode='lines+markers',
                name='Solución Implícita: ln|T - Ta| + kt',
                line=dict(color='#95E1D3', width=2),
                marker=dict(size=8),
                hovertemplate='Tiempo: %{x:.2f} min<br>Valor de ln|T-Ta| + kt: %{y:.6f}<br>Constante esperada C: ' + f'{calculator.C:.6f}<extra></extra>'
            )
        )
        
        # Línea de referencia para la constante C
        fig_verify.add_hline(
            y=calculator.C,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Constante C = {calculator.C:.6f}",
            annotation_position="right"
        )
        
        fig_verify.update_layout(
            title="Verificación de la Solución Implícita: La expresión debe mantenerse constante",
            xaxis_title="Tiempo (min)",
            yaxis_title="Valor de ln|T - Ta| + kt (debe ser constante = C)",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_verify, use_container_width=True)
        
        # Tabla de verificación con explicación simple
        st.markdown("### 📋 Tabla de Verificación Detallada")
        
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 20px;'>
        <h4 style='color: #856404; margin-top: 0;'>🎯 ¿Cómo leer esta tabla?</h4>
        <p style='color: #856404; margin-bottom: 15px;'>
        Esta tabla demuestra paso a paso que nuestro modelo matemático funciona correctamente. 
        Veamos qué significa cada columna:
        </p>
        <table style='width: 100%; border-collapse: collapse; color: #856404;'>
        <tr style='background-color: #ffeaa7;'>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>Tiempo</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'>Momentos diferentes durante el enfriamiento</td>
        </tr>
        <tr>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>Temperatura T</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'>La temperatura del objeto en ese momento</td>
        </tr>
        <tr style='background-color: #ffeaa7;'>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>Diferencia |T - Ta|</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'>Cuánto más caliente está el objeto comparado con el ambiente</td>
        </tr>
        <tr>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>ln|T - Ta| + kt</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><span style='background-color: #fff; padding: 3px 6px; border-radius: 3px;'>
        <strong>¡Esta debe ser siempre la misma!</strong></span> Si cambia mucho, hay un error</td>
        </tr>
        <tr style='background-color: #ffeaa7;'>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>Constante C esperada</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'>El valor que deberíamos obtener siempre: {:.6f}</td>
        </tr>
        <tr>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'><strong>Diferencia con C</strong></td>
        <td style='padding: 8px; border: 1px solid #fdcb6e;'>Qué tan cerca estamos del valor esperado (mientras más pequeño, mejor)</td>
        </tr>
        </table>
        <p style='color: #856404; margin-top: 15px; margin-bottom: 0;'>
        <strong>💡 Consejo:</strong> Observa la columna "ln|T - Ta| + kt". Si todos los números son muy parecidos 
        (diferencia menor a 0.000001), ¡nuestro modelo es correcto! ✅
        </p>
        </div>
        """.format(calculator.C), unsafe_allow_html=True)
        
        df_verify = pd.DataFrame({
            'Tiempo (min)': [f"{t:.2f}" for t in times_verify],
            'Temperatura T (°C)': [f"{calculator.temperature_explicit(t):.2f}" for t in times_verify],
            'Diferencia |T - Ta| (°C)': [f"{abs(calculator.temperature_explicit(t) - Ta):.2f}" for t in times_verify],
            'ln|T - Ta| + kt (debe ser constante)': [f"{val:.6f}" for val in implicit_values_verify],
            'Constante C esperada': [f"{calculator.C:.6f}" for _ in times_verify],
            'Diferencia con C': [f"{abs(val - calculator.C):.2e}" for val in implicit_values_verify]
        })
        
        st.dataframe(df_verify, use_container_width=True, hide_index=True)
        
        # Explicación visual después de la tabla
        st.markdown("""
        <div style='background-color: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 5px solid #0c5460; margin-top: 20px;'>
        <h4 style='color: #0c5460; margin-top: 0;'>🔬 Análisis de los Resultados</h4>
        <p style='color: #0c5460; margin-bottom: 10px;'>
        <strong>Observaciones importantes:</strong>
        </p>
        <ol style='color: #0c5460; margin-bottom: 10px;'>
        <li><strong>La temperatura baja:</strong> Empieza en {:.1f}°C y va disminuyendo hacia {:.1f}°C</li>
        <li><strong>La diferencia se reduce:</strong> La columna "Diferencia |T - Ta|" muestra cómo la brecha entre 
        el objeto y el ambiente se hace cada vez más pequeña</li>
        <li><strong>La expresión se mantiene constante:</strong> Mira la columna "ln|T - Ta| + kt". 
        Todos los valores deberían ser aproximadamente <strong>{:.6f}</strong></li>
        <li><strong>La diferencia con C es muy pequeña:</strong> Los valores en la última columna son extremadamente pequeños 
        (como 0.000000), lo que significa que nuestro cálculo es muy preciso</li>
        </ol>
        <p style='color: #0c5460; margin: 0; font-weight: bold;'>
        ✅ <strong>Conclusión:</strong> Si la "Diferencia con C" es muy pequeña en todas las filas, 
        significa que nuestro modelo matemático funciona perfectamente y describe correctamente el proceso de enfriamiento.
        </p>
        </div>
        """.format(T0, Ta, calculator.C), unsafe_allow_html=True)
        
        # Estadísticas de verificación
        max_diff = max([abs(val - calculator.C) for val in implicit_values_verify])
        mean_diff = np.mean([abs(val - calculator.C) for val in implicit_values_verify])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Diferencia Máxima con C", f"{max_diff:.2e}")
        with col2:
            st.metric("Diferencia Promedio con C", f"{mean_diff:.2e}")
        
        if max_diff < 1e-6:
            st.success("✅ La solución implícita se verifica correctamente (diferencia < 1e-6)")
        else:
            st.warning(f"⚠️ La diferencia es mayor a 1e-6. Esto puede deberse a errores numéricos.")
    
    with tab5:
        st.header("Información del Modelo Matemático")
        
        st.markdown("""
        ### Ecuación Diferencial
        
        La Ley de Enfriamiento de Newton establece que la velocidad de cambio de la temperatura 
        de un objeto es directamente proporcional a la diferencia entre su temperatura instantánea 
        y la temperatura del medio ambiente:
        
        $$
        \\frac{dT}{dt} = -k(T - T_a)
        $$
        
        Donde:
        - $T(t)$: temperatura del objeto en el instante $t$ (°C)
        - $T_a$: temperatura ambiente (constante) (°C)
        - $k > 0$: constante de enfriamiento (min⁻¹)
        - El signo negativo indica que la temperatura disminuye cuando $T > T_a$
        
        ### Solución Explícita
        
        Resolviendo la ecuación diferencial por separación de variables, se obtiene:
        
        $$
        T(t) = T_a + (T_0 - T_a) e^{-kt}
        $$
        
        Donde $T_0$ es la temperatura inicial del objeto.
        
        ### Solución Implícita
        
        La solución también puede expresarse en forma **implícita**, donde la relación entre temperatura y tiempo 
        se expresa mediante una ecuación que no está resuelta explícitamente para $T$:
        
        $$
        \\ln|T - T_a| + kt = C
        $$
        
        **¿Qué significa esta expresión?**
        
        - **$\\ln|T - T_a|$**: lnaritmo natural del valor absoluto de la diferencia entre la temperatura del objeto 
          y la temperatura ambiente. Este término representa cómo la diferencia de temperatura disminuye con el tiempo.
        
        - **$kt$**: Producto de la constante de enfriamiento por el tiempo. Este término aumenta linealmente con el tiempo.
        
        - **$C$**: Constante de integración que se determina a partir de las condiciones iniciales: 
          $C = \\ln|T_0 - T_a|$, donde $T_0$ es la temperatura inicial.
        
        **Importancia de la solución implícita:**
        
        La suma $\\ln|T - T_a| + kt$ debe mantenerse **constante** (igual a $C$) para todos los valores de tiempo. 
        Esta propiedad permite verificar matemáticamente que la solución satisface la ecuación diferencial original. 
        Si derivamos implícitamente esta expresión respecto al tiempo, recuperamos la ecuación diferencial original, 
        confirmando así la validez del modelo.
        
        ### Propiedades del Modelo
        
        1. **Comportamiento Asintótico**: La temperatura tiende exponencialmente hacia $T_a$ cuando $t \\to \\infty$
        
        2. **Razón de Enfriamiento**: La velocidad de cambio de temperatura es:
           $$
           \\frac{dT}{dt} = -k(T - T_a)
           $$
           Esta razón es máxima al inicio y disminuye a medida que el objeto se acerca a la temperatura ambiente.
        
        3. **Vida Media Térmica**: El tiempo necesario para reducir la diferencia de temperatura a la mitad es:
           $$
           t_{1/2} = \\frac{\\ln(2)}{k}
           $$
        
        ### Aplicaciones
        
        Este modelo es útil para:
        - Tratamiento térmico de metales
        - Diseño de sistemas de refrigeración
        - Control de procesos térmicos industriales
        - Análisis de transferencia de calor
        
        ### Limitaciones
        
        El modelo es válido cuando:
        - La diferencia de temperatura no es excesivamente grande
        - Los mecanismos de transferencia de calor (conducción, convección, radiación) pueden aproximarse como proporcionales a la diferencia de temperatura
        - La temperatura ambiente permanece constante
        """)
        
        # Mostrar ecuación con valores actuales
        st.subheader("Ecuación con Valores Actuales")
        st.latex(f"\\frac{{dT}}{{dt}} = -{k:.6f}(T - {Ta:.2f})")
        st.latex(f"T(t) = {Ta:.2f} + ({T0:.2f} - {Ta:.2f}) e^{{-{k:.6f}t}}")
        st.latex(f"\\ln|T - {Ta:.2f}| + {k:.6f}t = {calculator.C:.6f}")

except Exception as e:
    st.error(f"Error al inicializar el calculador: {e}")
    st.info("Por favor, verifica que los parámetros sean válidos.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Sistema de Gestión de Ley de Enfriamiento de Newton</p>
    <p>Desarrollado para el análisis de ecuaciones diferenciales</p>
</div>
""", unsafe_allow_html=True)

