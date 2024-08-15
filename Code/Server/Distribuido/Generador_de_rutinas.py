import numpy as np


def crea_rutina(num_bailes=0):

    """
    primero se establece la cantidad de pasos y la matriz de probabilidades, el formato será P = [pij]
    donde i es el estado final y j es el estado inicial
    """
    transition_matrix = np.array([[0,  0.5,  0,    0.4,     0],
                                  [0.4, 0,    0,    0,    0.4],
                                  [0.6, 0,    0.4,  0.3,    0],
                                  [0,   0.5,  0.3,  0,    0.2],
                                  [0,   0,    0.3,  0.3,  0.4]])

    "Se trata de 5 bailes diferentes, con los siguientes nombres: "
    state = {
         0: "baile_1",
         1: "baile_2",
         2: "baile_3",
         3: "baile_4",
         4: "baile_5"
        }

    " Se establece una lista para guardar los pasos de baile"
    rutina_gen = []

    "Establecidos los estados, se inicializa la rutina en el primer estado"
    n = num_bailes  # este es el número de pasos en la rutina de baile
    start_state = 0  # estado inicial de la rutina de baile
    prev_state = start_state
    rutina_gen.append(state[prev_state])

    " Una vez establecido el inicio de la rutina, inicia el random walk "
    while n-1:
        curr_state = np.random.choice([0, 1, 2, 3, 4], p=transition_matrix[:, prev_state])  # escoge nuevo state
        prev_state = curr_state
        rutina_gen.append(state[prev_state])  # actualiza la lista de pasos
        n -= 1

    return rutina_gen


"""
Pn = np.linalg.matrix_power(P,100)
print(Pn)
"""

if __name__ == "__main__":
    k = 6

    rutina = crea_rutina(k)
    print(rutina)
