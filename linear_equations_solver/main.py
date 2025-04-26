import numpy as np
import os
import glob

def print_system(A, b):
    n = len(b)
    print("\nUkład równań:")
    print("A * x = B")
    print("\nMacierz A:")
    for row in A:
        print(" ".join(f"{x:8.4f}" for x in row))
    print("\nWektor B:")
    print(" ".join(f"{x:8.4f}" for x in b))
    print()

def read_system_from_file(filename):
    try:
        with open(filename, 'r') as file:
            n = int(file.readline().strip())
            if n < 1 or n > 10:
                raise ValueError("Liczba równań musi być z przedziału od 1 do 10")
            
            A = np.zeros((n, n))
            b = np.zeros(n)
            
            for i in range(n):
                line = file.readline().strip()
                coefficients = list(map(float, line.split()))
                if len(coefficients) != n + 1:
                    raise ValueError(f"Nieprawidłowa liczba współczynników w równaniu {i+1}")
                A[i] = coefficients[:-1]
                b[i] = coefficients[-1]
            
            return A, b
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return None, None
    except ValueError as e:
        print(f"Błąd: {e}")
        return None, None

def read_system_from_terminal():
    try:
        n = int(input("Podaj liczbę równań (1-10): "))
        if n < 1 or n > 10:
            raise ValueError("Liczba równań musi być z przedziału od 1 do 10")
        
        A = np.zeros((n, n))
        b = np.zeros(n)
        
        print(f"Podaj {n} równań, każde z {n+1} współczynnikami (oddzielone spacjami):")
        for i in range(n):
            line = input(f"Równanie {i+1}: ")
            coefficients = list(map(float, line.split()))
            if len(coefficients) != n + 1:
                raise ValueError(f"Nieprawidłowa liczba współczynników w równaniu {i+1}")
            A[i] = coefficients[:-1]
            b[i] = coefficients[-1]
        
        return A, b
    except ValueError as e:
        print(f"Błąd: {e}")
        return None, None

def gaussian_elimination(A, b):
    n = len(b)
    #Tworzenie macierzy rozszerzonej
    Ab = np.column_stack((A, b))
    
    #Redukcja do postaci trójkątnej
    for i in range(n):
        #Wybór elementu podstawowego
        max_row = i
        for k in range(i+1, n):
            if abs(Ab[k, i]) > abs(Ab[max_row, i]):
                max_row = k
        
        #Zamiana wierszy jeśli konieczna
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        #Sprawdzenie czy układ jest sprzeczny lub nieoznaczony
        if abs(Ab[i, i]) < 1e-10:
            if abs(Ab[i, n]) > 1e-10:
                return None, "Układ jest sprzeczny - nie istnieje rozwiązanie"
            return None, "Układ jest nieoznaczony - istnieje nieskończenie wiele rozwiązań"
        
        #Eliminacja poniżej
        for k in range(i+1, n):
            factor = Ab[k, i] / Ab[i, i]
            Ab[k, i:] -= factor * Ab[i, i:]
    
    #Podstawienie
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        if abs(Ab[i, i]) < 1e-10:
            if abs(Ab[i, n]) > 1e-10:
                return None, "Układ jest sprzeczny - nie istnieje rozwiązanie"
            return None, "Układ jest nieoznaczony - istnieje nieskończenie wiele rozwiązań"
        x[i] = (Ab[i, n] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x, None

def solve_and_print_results(A, b, system_name=""):
    if system_name:
        print(f"\n{'='*50}")
        print(f"Rozwiązywanie układu z pliku: {system_name}")
        print(f"{'='*50}")
    
    print_system(A, b)
    print("Rozwiązywanie układu...")
    solution, error = gaussian_elimination(A, b)
    
    if error:
        print(f"Wynik: {error}")
    else:
        print("Rozwiązanie:")
        for i, x in enumerate(solution):
            print(f"x{i+1} = {x:.6f}")

def solve_all_from_dataset():
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    if not os.path.exists(dataset_path):
        print("\nBłąd: Katalog 'dataset' nie istnieje!")
        return
    
    test_files = glob.glob(os.path.join(dataset_path, "*.txt"))
    if not test_files:
        print("\nBrak plików testowych w katalogu 'dataset'!")
        return
    
    for file_path in sorted(test_files):
        A, b = read_system_from_file(file_path)
        if A is not None and b is not None:
            solve_and_print_results(A, b, os.path.basename(file_path))

def main():
    while True:
        print("\nRozwiązywanie układu równań liniowych")
        print("1. Wczytaj z pliku")
        print("2. Wprowadź równania ręcznie")
        print("3. Rozwiąż wszystkie układy z katalogu dataset")
        print("4. Zakończ program")
        choice = input("\nWybierz opcję (1-4): ")
        
        if choice == '4':
            print("\nDo widzenia!")
            break
        
        if choice == '3':
            solve_all_from_dataset()
        elif choice in ['1', '2']:
            A = None
            b = None
            
            if choice == '1':
                filename = input("\nPodaj nazwę pliku: ")
                A, b = read_system_from_file(filename)
            elif choice == '2':
                A, b = read_system_from_terminal()
            
            if A is not None and b is not None:
                solve_and_print_results(A, b)
        else:
            print("\nNieprawidłowy wybór. Wybierz 1, 2, 3 lub 4.")
            continue
        
        input("\nNaciśnij Enter, aby kontynuować...")

if __name__ == "__main__":
    main()
