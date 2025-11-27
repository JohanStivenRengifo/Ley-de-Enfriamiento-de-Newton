import numpy as np
from scipy.optimize import fsolve

class NewtonCoolingCalculator:
    def __init__(self, T0, Ta, k):
        """
        T0: Temperatura inicial del objeto (°C)
        Ta: Temperatura ambiente (°C)
        k: Constante de enfriamiento (min^-1)
        T(t): temperatura del objeto en el instante t
        Ta: temperatura ambiente (constante)
        k: constante de enfriamiento (k > 0)
        """
        
        self.T0 = T0
        self.Ta = Ta
        self.k = k
        self.C = self._calculate_constant()
    
    def _calculate_constant(self):
        # Calcula la constante C de la solución implícita ==>  C = ln|T0 - Ta|
        return np.log(abs(self.T0 - self.Ta))
    
    def temperature_explicit(self, t):
        # Solución explícita de la ecuación diferencial T(t) = Ta + (T0 - Ta) * exp(-k*t)
        return self.Ta + (self.T0 - self.Ta) * np.exp(-self.k * t)
    
    def temperature_implicit(self, t):
        # Verifica la solución implícita: ln|T - Ta| + k*t = C
        T = self.temperature_explicit(t)
        return np.log(abs(T - self.Ta)) + self.k * t
    
    def cooling_rate(self, t):
        # Calcula la razón de enfriamiento dT/dt en el tiempo t dT/dt = -k(T - Ta)
        T = self.temperature_explicit(t)
        return -self.k * (T - self.Ta)
    
    def time_to_reach_temperature(self, target_temp, tolerance=0.01):
        # Tiempo necesario para temperatura objetivo
        if abs(target_temp - self.Ta) < tolerance:
            return None  # No alcanza la temperatura ambiente
        
        if (target_temp > self.T0 > self.Ta) or (target_temp < self.T0 < self.Ta):
            return None  # La temperatura objetivo está en dirección opuesta
        
        # De la solución explícita: t = (1/k) * ln((T0 - Ta)/(T - Ta))
        try:
            t = (1 / self.k) * np.log(abs((self.T0 - self.Ta) / (target_temp - self.Ta)))
            return max(0, t)  # Asegurar tiempo no negativo
        except:
            return None
    
    def generate_time_series(self, t_max, num_points=100):
        # Genera una serie temporal de temperaturas
        times = np.linspace(0, t_max, num_points)
        temperatures = [self.temperature_explicit(t) for t in times]
        return times, np.array(temperatures)
    
    def verify_implicit_solution(self, times):
        # Verifica que la solución implícita se mantiene constante, devuelve ~C
        return [self.temperature_implicit(t) for t in times]
    
    @staticmethod
    def calculate_k_from_data(T0, Ta, T_measured, t_measured):
        # Calcula la constante k a partir de datos experimentales
        if abs(T_measured - Ta) < 1e-10:
            raise ValueError("La temperatura medida es muy cercana a la temperatura ambiente")
        
        k = (1 / t_measured) * np.log(abs((T0 - Ta) / (T_measured - Ta)))
        return k
        # De T(t) = Ta + (T0 - Ta) * exp(-k*t)
        # Despejando k: k = (1/t) * ln((T0 - Ta)/(T - Ta))
        if abs(T_measured - Ta) < 1e-10:
            raise ValueError("La temperatura medida es muy cercana a la temperatura ambiente")
        
        k = (1 / t_measured) * np.log(abs((T0 - Ta) / (T_measured - Ta)))
        return k