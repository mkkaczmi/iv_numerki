from typing import Tuple, Callable
import numpy as np

def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float,
    max_iterations: int,
    use_epsilon_condition: bool
) -> Tuple[float | None, int]:
    """
    Znajduje pierwiastek używając metody bisekcji.
    
    Args:
        f: Funkcja do znalezienia pierwiastka
        a: Lewy koniec przedziału
        b: Prawy koniec przedziału
        epsilon: Tolerancja zbieżności
        max_iterations: Maksymalna liczba iteracji
        use_epsilon_condition: Jeśli True, użyj warunku |x_i - x_(i-1)| < ε
        
    Returns:
        Krotka zawierająca (pierwiastek lub None, liczba iteracji)
    """
    try:
        fa = f(a)
        fb = f(b)
    except (ValueError, OverflowError):
        # Obsługa przypadku gdy funkcja jest nieokreślona na końcach
        return None, 0
        
    if fa * fb >= 0:
        return None, 0
    
    iterations = 0
    x_prev = a
    
    while iterations < max_iterations:
        c = (a + b) / 2
        try:
            fc = f(c)
        except (ValueError, OverflowError):
            # Jeśli funkcja jest nieokreślona w punkcie środkowym, spróbuj punktu nieco na lewo
            try:
                c = c - epsilon
                fc = f(c)
            except (ValueError, OverflowError):
                return None, iterations
        
        if use_epsilon_condition:
            if abs(c - x_prev) < epsilon:
                if abs(fc) < epsilon:
                    return c, iterations + 1
                else:
                    return None, iterations + 1
        
        if abs(fc) < epsilon:
            return c, iterations + 1
            
        try:
            if f(a) * fc < 0:
                b = c
            else:
                a = c
        except (ValueError, OverflowError):
            return None, iterations
            
        x_prev = c
        iterations += 1
    
    return (a + b) / 2, iterations

def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    epsilon: float,
    max_iterations: int,
    use_epsilon_condition: bool
) -> Tuple[float | None, int]:
    """
    Znajduje pierwiastek używając metody siecznych.
    
    Args:
        f: Funkcja do znalezienia pierwiastka
        x0: Pierwszy punkt początkowy
        x1: Drugi punkt początkowy
        epsilon: Tolerancja zbieżności
        max_iterations: Maksymalna liczba iteracji
        use_epsilon_condition: Jeśli True, użyj warunku |x_i - x_(i-1)| < ε
        
    Returns:
        Krotka zawierająca (pierwiastek lub None, liczba iteracji)
    """
    iterations = 0
    x_prev = x0
    x_curr = x1
    
    try:
        f_x0 = f(x0)
        f_x1 = f(x1)
    except (ValueError, OverflowError):
        return None, 0
    
    while iterations < max_iterations:
        try:
            f_prev = f(x_prev)
            f_curr = f(x_curr)
        except (ValueError, OverflowError):
            return None, iterations
        
        if abs(f_curr) < epsilon:
            return x_curr, iterations + 1
            
        if abs(f_curr - f_prev) < epsilon * epsilon:  # Użyj mniejszego epsilon dla mianownika
            if abs(f_curr) < epsilon:
                return x_curr, iterations + 1
            return None, iterations + 1
            
        try:
            x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
            
            # Sprawdź czy następny punkt nie jest zbyt daleko (możliwa asymptota)
            if abs(x_next - x_curr) > (x1 - x0):
                x_next = (x_curr + x_prev) / 2  # Użyj kroku bisekcji zamiast tego
                
        except (ValueError, OverflowError, ZeroDivisionError):
            # Jeśli dzielenie się nie powiedzie, spróbuj mniejszego kroku
            x_next = (x_curr + x_prev) / 2
        
        if use_epsilon_condition:
            if abs(x_next - x_curr) < epsilon:
                if abs(f(x_next)) < epsilon:
                    return x_next, iterations + 1
                else:
                    return None, iterations + 1
        
        # Utrzymuj x_next w oryginalnym przedziale
        x_next = max(min(x_next, max(x0, x1)), min(x0, x1))
        
        x_prev = x_curr
        x_curr = x_next
        iterations += 1
    
    # Końcowe sprawdzenie czy znaleziono pierwiastek
    try:
        if abs(f(x_curr)) < epsilon:
            return x_curr, iterations
    except (ValueError, OverflowError):
        pass
        
    return None, iterations