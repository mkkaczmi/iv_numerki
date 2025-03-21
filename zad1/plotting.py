import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List

def plot_function_and_roots(
    f: Callable[[float], float],
    roots: List[float],
    a: float,
    b: float,
    title: str = "Funkcja i jej pierwiastek"
) -> None:
    """
    Rysuje wykres funkcji i zaznacza jej pierwiastek.
    
    Args:
        f: Funkcja do narysowania
        roots: Lista pierwiastków do zaznaczenia
        a: Początek przedziału
        b: Koniec przedziału
        title: Tytuł wykresu
    """
    x = np.linspace(a, b, 1000)
    y = []
    
    # Obliczanie wartości y z zabezpieczeniem przed bardzo dużymi wartościami
    y_min, y_max = float('inf'), float('-inf')
    for xi in x:
        try:
            yi = f(xi)
            # Ograniczenie wartości y do rozsądnego zakresu
            if abs(yi) > 10:
                yi = np.sign(yi) * 10
            y.append(yi)
            y_min = min(y_min, yi)
            y_max = max(y_max, yi)
        except (ValueError, OverflowError):
            y.append(np.nan)  # Użyj NaN dla nieokreślonych punktów
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='Funkcja')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Rysowanie pierwiastków
    for root in roots:
        try:
            root_y = f(root)
            if abs(root_y) > 10:
                root_y = np.sign(root_y) * 10
            plt.plot(root, root_y, 'ro', label=f'Pierwiastek: {root:.6f}')
        except (ValueError, OverflowError):
            continue
    
    # Ustawienie rozsądnych granic osi y
    y_range = y_max - y_min
    plt.ylim([max(y_min - 0.1 * y_range, -10), min(y_max + 0.1 * y_range, 10)])
    
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()