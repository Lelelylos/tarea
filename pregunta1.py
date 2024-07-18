import numpy as np
from scipy.optimize import linear_sum_assignment

def input_cost_matrix(n):
    cost_matrix = []
    print(f"Ingrese los costos de asignación para {n} centros y {n} rutas:")
    for i in range(n):
        row = list(map(int, input(f"Costo de asignación para el centro {i + 1}: ").split()))
        cost_matrix.append(row)
    return np.array(cost_matrix)

def print_matrix(matrix, step):
    print(f"\nMatriz de costos después del paso {step}:")
    for row in matrix:
        print(" ".join(f"{item:4}" for item in row))

def print_all_matrices(matrix_history):
    print("\nHistórico de cambios en la matriz de costos:")
    for step, matrix in enumerate(matrix_history):
        print_matrix(matrix, step)

def main():
    n = int(input("Ingrese el número de centros de distribución y rutas de entrega: "))
    cost_matrix = input_cost_matrix(n)
    
    print("\nMatriz de costos inicial:")
    print_matrix(cost_matrix, 0)

    matrix_history = [cost_matrix.copy()]

    # Selección de objetivo: maximizar o minimizar
    objetivo = input("¿Desea maximizar o minimizar el costo? (max/min): ").strip().lower()
    if objetivo not in ['max', 'min']:
        print("Opción no válida. Se seleccionará minimizar por defecto.")
        objetivo = 'min'

    if objetivo == 'max':
        # Convertir la matriz para maximizar
        cost_matrix = np.max(cost_matrix) - cost_matrix

    # Paso 1: Restar la mínima de cada fila
    for i in range(n):
        min_value = np.min(cost_matrix[i])
        cost_matrix[i] -= min_value

    matrix_history.append(cost_matrix.copy())
    
    # Paso 2: Restar la mínima de cada columna
    for j in range(n):
        min_value = np.min(cost_matrix[:, j])
        cost_matrix[:, j] -= min_value

    matrix_history.append(cost_matrix.copy())

    # Paso 3: Resolver el problema de asignación
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Calcular el costo total
    if objetivo == 'max':
        total_cost = (np.max(cost_matrix) - cost_matrix[row_ind, col_ind]).sum()
    else:
        total_cost = cost_matrix[row_ind, col_ind].sum()

    # Mostrar resultados
    print("\nAsignación óptima de centros a rutas:")
    for i in range(n):
        print(f"Centro de distribución {row_ind[i] + 1} -> Ruta de entrega {col_ind[i] + 1}")

    if objetivo == 'max':
        print(f"\nCosto total máximo: {-total_cost}")
    else:
        print(f"\nCosto total mínimo: {total_cost}")

    # Mostrar todos los cambios en la matriz
    print_all_matrices(matrix_history)

    # Mostrar el costo total al final
    if objetivo == 'max':
        print(f"\nCosto total máximo final: {-total_cost}")
    else:
        print(f"\nCosto total mínimo final: {total_cost}")

if __name__ == "__main__":
    main()
