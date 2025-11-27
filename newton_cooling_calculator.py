"""
Módulo de cálculos para la Ley de Enfriamiento de Newton
Implementa las soluciones explícita e implícita de la ecuación diferencial
"""

import numpy as np
from scipy.optimize import fsolve


class NewtonCoolingCalculator:
    """
    Calculadora para la Ley de Enfriamiento de Newton
    
    La ecuación diferencial es: dT/dt = -k(T - Ta)
    Donde:
    - T(t): temperatura del objeto en el instante t
    - Ta: temperatura ambiente (constante)
    - k: constante de enfriamiento (k > 0)
    """
    
    def __init__(self, T0, Ta, k):
        """
        Inicializa la calculadora con los parámetros del problema
        
        Args:
            T0: Temperatura inicial del objeto (°C)
            Ta: Temperatura ambiente (°C)
            k: Constante de enfriamiento (min^-1)
        """
        self.T0 = T0
        self.Ta = Ta
        self.k = k
        self.C = self._calculate_constant()
    
    def _calculate_constant(self):
        """
        Calcula la constante C de la solución implícita
        C = ln|T0 - Ta|
        """
        return np.ln(abs(self.T0 - self.Ta))
    
    def temperature_explicit(self, t):
        """
        Solución explícita de la ecuación diferencial
        T(t) = Ta + (T0 - Ta) * exp(-k*t)
        
        Args:
            t: Tiempo en minutos
            
        Returns:
            Temperatura en °C
        """
        return self.Ta + (self.T0 - self.Ta) * np.exp(-self.k * t)
    
    def temperature_implicit(self, t):
        """
        Verifica la solución implícita: ln|T - Ta| + k*t = C
        
        Args:
            t: Tiempo en minutos
            
        Returns:
            Valor de la expresión ln|T - Ta| + k*t (debe ser igual a C)
        """
        T = self.temperature_explicit(t)
        return np.ln(abs(T - self.Ta)) + self.k * t
    
    def cooling_rate(self, t):
        """
        Calcula la razón de enfriamiento dT/dt en el tiempo t
        dT/dt = -k(T - Ta)
        
        Args:
            t: Tiempo en minutos
            
        Returns:
            Razón de enfriamiento en °C/min
        """
        T = self.temperature_explicit(t)
        return -self.k * (T - self.Ta)
    
    def time_to_reach_temperature(self, target_temp, tolerance=0.01):
        """
        Calcula el tiempo necesario para alcanzar una temperatura objetivo
        
        Args:
            target_temp: Temperatura objetivo (°C)
            tolerance: Tolerancia para la convergencia
            
        Returns:
            Tiempo en minutos, o None si no es alcanzable
        """
        if abs(target_temp - self.Ta) < tolerance:
            return None  # Nunca alcanzará exactamente la temperatura ambiente
        
        if (target_temp > self.T0 > self.Ta) or (target_temp < self.T0 < self.Ta):
            return None  # La temperatura objetivo está en dirección opuesta
        
        # De la solución explícita: t = (1/k) * ln((T0 - Ta)/(T - Ta))
        try:
            t = (1 / self.k) * np.ln(abs((self.T0 - self.Ta) / (target_temp - self.Ta)))
            return max(0, t)  # Asegurar tiempo no negativo
        except:
            return None
    
    def generate_time_series(self, t_max, num_points=100):
        """
        Genera una serie temporal de temperaturas
        
        Args:
            t_max: Tiempo máximo en minutos
            num_points: Número de puntos a generar
            
        Returns:
            Tupla (tiempos, temperaturas)
        """
        times = np.linspace(0, t_max, num_points)
        temperatures = [self.temperature_explicit(t) for t in times]
        return times, np.array(temperatures)
    
    def verify_implicit_solution(self, times):
        """
        Verifica que la solución implícita se mantiene constante
        
        Args:
            times: Array de tiempos para verificar
            
        Returns:
            Array de valores de la expresión implícita (deben ser ~C)
        """
        return [self.temperature_implicit(t) for t in times]
    
    @staticmethod
    def calculate_k_from_data(T0, Ta, T_measured, t_measured):
        """
        Calcula la constante k a partir de datos experimentales
        
        Args:
            T0: Temperatura inicial (°C)
            Ta: Temperatura ambiente (°C)
            T_measured: Temperatura medida en tiempo t_measured (°C)
            t_measured: Tiempo de la medición (min)
            
        Returns:
            Constante k (min^-1)
        """
        # De T(t) = Ta + (T0 - Ta) * exp(-k*t)
        # Despejando k: k = (1/t) * ln((T0 - Ta)/(T - Ta))
        if abs(T_measured - Ta) < 1e-10:
            raise ValueError("La temperatura medida es muy cercana a la temperatura ambiente")
        
        k = (1 / t_measured) * np.ln(abs((T0 - Ta) / (T_measured - Ta)))
        return k