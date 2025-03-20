def evaluate_polynomial(x: float, coefficients: list[float], length: int) -> float:
    """
    Evaluate polynomial using Horner's scheme.
    
    Args:
        x: Point at which to evaluate the polynomial
        coefficients: List of polynomial coefficients (from highest to lowest degree)
        length: Length of the coefficients array
        
    Returns:
        Value of the polynomial at point x
    """
    result = coefficients[0]
    for i in range(1, length):
        result = result * x + coefficients[i]
    return result