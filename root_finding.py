from typing import Tuple, Callable
import numpy as np

def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float,
    iterations: int,
    use_epsilon_condition: bool
) -> Tuple[float | None, int]:
    """
    Znajduje pierwiastek używając metody bisekcji.
    
    Args:
        f: Funkcja do znalezienia pierwiastka
        a: Lewy koniec przedziału
        b: Prawy koniec przedziału
        epsilon: Tolerancja zbieżności
        iterations: Liczba iteracji do wykonania (używane tylko gdy use_epsilon_condition=False)
        use_epsilon_condition: Jeśli True, użyj warunku |x_i - x_(i-1)| < ε
        
    Returns:
        Krotka zawierająca (pierwiastek lub None, liczba wykonanych iteracji)
    """
    try:
        fa = f(a)
        fb = f(b)
    except (ValueError, OverflowError):
        # Obsługa przypadku gdy funkcja jest nieokreślona na końcach
        return None, 0
        
    if fa * fb >= 0:
        return None, 0
    
    i = 0
    x_prev = a
    
    if use_epsilon_condition:
        # Używaj tylko warunku |x_i - x_(i-1)| < ε
        while True:
            c = (a + b) / 2
            try:
                fc = f(c)
            except (ValueError, OverflowError):
                # Jeśli funkcja jest nieokreślona w punkcie środkowym, spróbuj punktu nieco na lewo
                try:
                    c = c - epsilon
                    fc = f(c)
                except (ValueError, OverflowError):
                    return None, i
            
            if abs(c - x_prev) < epsilon:
                return c, i + 1
                
            try:
                if f(a) * fc < 0:
                    b = c
                else:
                    a = c
            except (ValueError, OverflowError):
                return None, i
                
            x_prev = c
            i += 1
    else:
        # Wykonaj dokładnie zadaną liczbę iteracji
        while i < iterations:
            c = (a + b) / 2
            try:
                fc = f(c)
            except (ValueError, OverflowError):
                # Jeśli funkcja jest nieokreślona w punkcie środkowym, spróbuj punktu nieco na lewo
                try:
                    c = c - epsilon
                    fc = f(c)
                except (ValueError, OverflowError):
                    return None, i
                    
            try:
                if f(a) * fc < 0:
                    b = c
                else:
                    a = c
            except (ValueError, OverflowError):
                return None, i
                
            x_prev = c
            i += 1
        
        return c, iterations

def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    epsilon: float,
    iterations: int,
    use_epsilon_condition: bool
) -> Tuple[float | None, int]:
    """
    Znajduje pierwiastek używając metody siecznych.
    
    Args:
        f: Funkcja do znalezienia pierwiastka
        x0: Pierwszy punkt początkowy
        x1: Drugi punkt początkowy
        epsilon: Tolerancja zbieżności
        iterations: Liczba iteracji do wykonania (używane tylko gdy use_epsilon_condition=False)
        use_epsilon_condition: Jeśli True, użyj warunku |x_i - x_(i-1)| < ε
        
    Returns:
        Krotka zawierająca (pierwiastek lub None, liczba wykonanych iteracji)
    """
    i = 0
    x_prev = x0
    x_curr = x1
    
    try:
        f_prev = f(x_prev)
        f_curr = f(x_curr)
    except (ValueError, OverflowError):
        return None, 0
    
    if use_epsilon_condition:
        while True:
            try:
                f_prev = f(x_prev)
                f_curr = f(x_curr)
                
                # Sprawdź czy mianownik nie jest zbyt bliski zeru
                denominator = f_curr - f_prev
                if abs(denominator) < 1e-10:  # Zabezpieczenie przed dzieleniem przez zero
                    # Użyj kroku bisekcji
                    x_next = (x_curr + x_prev) / 2
                else:
                    x_next = x_curr - f_curr * (x_curr - x_prev) / denominator
                    
                    # Sprawdź czy następny punkt nie jest zbyt daleko
                    if abs(x_next - x_curr) > abs(x1 - x0):
                        x_next = (x_curr + x_prev) / 2
                
            except (ValueError, OverflowError):
                # W przypadku błędu użyj kroku bisekcji
                x_next = (x_curr + x_prev) / 2
            
            # Utrzymuj x_next w granicach przedziału
            x_next = max(min(x_next, max(x0, x1)), min(x0, x1))
            
            # Sprawdź warunek stopu
            if abs(x_next - x_curr) < epsilon:
                try:
                    f_next = f(x_next)
                    if not np.isnan(f_next):  # Sprawdź czy wynik jest poprawny
                        return x_next, i + 1
                except (ValueError, OverflowError):
                    pass
                # Jeśli wynik jest niepoprawny, kontynuuj
            
            x_prev = x_curr
            x_curr = x_next
            i += 1
    else:
        # Wykonaj dokładnie zadaną liczbę iteracji
        for i in range(iterations):
            try:
                f_prev = f(x_prev)
                f_curr = f(x_curr)
                
                # Sprawdź czy mianownik nie jest zbyt bliski zeru
                denominator = f_curr - f_prev
                if abs(denominator) < 1e-10:
                    x_next = (x_curr + x_prev) / 2
                else:
                    x_next = x_curr - f_curr * (x_curr - x_prev) / denominator
                    
                    if abs(x_next - x_curr) > abs(x1 - x0):
                        x_next = (x_curr + x_prev) / 2
                
            except (ValueError, OverflowError):
                x_next = (x_curr + x_prev) / 2
            
            x_next = max(min(x_next, max(x0, x1)), min(x0, x1))
            
            x_prev = x_curr
            x_curr = x_next
        
        # Sprawdź czy końcowy wynik jest poprawny
        try:
            f_final = f(x_curr)
            if not np.isnan(f_final):
                return x_curr, iterations
        except (ValueError, OverflowError):
            pass
        
        return None, iterations