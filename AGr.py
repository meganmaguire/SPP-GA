import numpy as np

np.random.seed(0)

W = 100
Pc = 0.65
Pm = 0.1
Np = 50


# Genero la población como permutaciones de n elementos e indicando si está o no rotado el rectángulo
def generar_poblacion(n):
    poblacion = np.zeros((Np, 2, n))
    for i in range(Np):
        # Matriz de individuo donde la primera fila indica el orden de rectángulos y la segunda fila indica rotación
        # [0] = rectángulos
        # [1] = orientaciones
        individuo = np.zeros((2, n))
        individuo[0] = np.random.permutation(n)
        # El valor 0 indica que no está rotado mientras que el 1 indica que si está rotado
        individuo[1] = np.random.randint(0, 2, n)
        poblacion[i] = individuo
    return poblacion


# Función de fitness que devuelve la altura total de una distribución de rectángulos
def f(individuo):
    i = 0
    ancho_acum = 0
    altura_max = 0
    altura_total = 0

    for rectangulo in individuo[0]:
        rectangulo = int(rectangulo)
        # Chequeo la orientación del rectángulo
        if individuo[1][i] == 0:
            ancho_actual = anchos[rectangulo]
            altura_actual = alturas[rectangulo]
        else:
            ancho_actual = alturas[rectangulo]
            altura_actual = anchos[rectangulo]

        if ancho_actual + ancho_acum <= W:
            ancho_acum += ancho_actual
            if altura_actual > altura_max:
                altura_max = altura_actual
        else:
            altura_total += altura_max
            ancho_acum = ancho_actual
            altura_max = altura_actual
        i += 1

    altura_total += altura_max
    return altura_total


# Selecciona dos individuos al azar y elige el mejor
def seleccionar_padre(poblacion):
    indice_padre1 = np.random.randint(0, Np - 1)
    indice_padre2 = np.random.randint(0, Np - 1)
    while indice_padre1 == indice_padre2:
        indice_padre2 = np.random.randint(0, Np - 1)
    # Selecciono dos padres al azar
    padre1 = poblacion[indice_padre1]
    padre2 = poblacion[indice_padre2]
    # Elijo al padre con la menor función de fitness
    if f(padre1) <= f(padre2):
        return padre1
    else:
        return padre2


# Operador de crossover PMX
def pmx(padre1, padre2, n):
    hijo = np.zeros((2, n))
    punto1 = np.random.randint(1, n - 1)
    punto2 = np.random.randint(1, n - 1)
    while (punto1 == punto2):
        punto2 = np.random.randint(1, n - 1)
    # Acomodo los índices si están cruzados
    if punto1 > punto2:
        aux = punto2
        punto2 = punto1
        punto1 = aux
    # Reparto los segmentos
    # Copio los rectángulos
    hijo[0][:punto1] = padre1[0][:punto1]
    hijo[0][punto1:punto2] = padre2[0][punto1:punto2]
    hijo[0][punto2:] = padre1[0][punto2:]
    # Copio las orientaciones
    hijo[1][:punto1] = padre1[1][:punto1]
    hijo[1][punto1:punto2] = padre2[1][punto1:punto2]
    hijo[1][punto2:] = padre1[1][punto2:]
    # Busco aquellos valores que no fueron copiados
    for i in range(punto1, punto2):
        if not (padre1[0][i] in padre2[0][punto1:punto2]):
            index = indice(padre1[0], padre2[0][i])
            while punto1 <= index < punto2:
                index = indice(padre1[0], hijo[0][index])
            hijo[0][index] = padre1[0][i]
            hijo[1][index] = padre1[1][i]
    return hijo


# Mutación mediante intercambio de dos genes al azar
def mutacion(individuo):
    index1 = np.random.randint(0, n)
    index2 = np.random.randint(0, n)
    while index1 == index2:
        index2 = np.random.randint(0, n)
    # Intercambio el rectángulo y su orientación al mismo tiempo
    aux0 = individuo[0][index1]
    aux1 = individuo[1][index1]
    individuo[0][index1] = individuo[0][index2]
    individuo[1][index1] = individuo[1][index2]
    individuo[0][index2] = aux0
    individuo[1][index2] = aux1

    return individuo


# Retorna el mejor individuo de su población
def mejor_individuo(poblacion):
    resultado = poblacion[0]
    valor = f(poblacion[0])

    for i in range(1, Np):
        nuevo_valor = f(poblacion[i])
        if nuevo_valor < valor:
            valor = nuevo_valor
            resultado = poblacion[i]

    return np.copy(resultado)


# Dado un individuo y un valor me devuelve la posición en la cual se encuentra
def indice(individuo, valor):
    for i in range(len(individuo)):
        if individuo[i] == valor:
            return i


# Algoritmo principal
def ga(n, gen):
    poblacion = generar_poblacion(n)
    nueva_poblacion = np.zeros((Np, 2, n))

    print("Ancho de los rectángulos: ", end='')
    print(anchos)
    print("Altura de los rectángulos: ", end='')
    print(alturas)
    print("-----------------------------------------")
    resultado = poblacion[0]
    print("Primer mejor resultado: ", end='')
    print(resultado)
    print("La altura total es: ", end='')
    print(f(resultado))
    print("-----------------------------------------")

    for i in range(gen):
        for j in range(Np):
            # Realizo crossover
            if np.random.random() <= Pc:
                padre1 = seleccionar_padre(poblacion)
                padre2 = seleccionar_padre(poblacion)
                hijo = pmx(padre1, padre2, n)
            else:
                hijo = poblacion[j]

            # Realizo mutacion
            if np.random.random() <= Pm:
                hijo = mutacion(hijo)
            # Agrego a la nueva población
            nueva_poblacion[j] = hijo

        poblacion = nueva_poblacion
        mejor_actual = mejor_individuo(poblacion)
        if f(mejor_actual) < f(resultado):
            resultado = np.copy(mejor_actual)

    print("El orden de rectángulos es: ", end='')
    print(resultado)
    print("La altura total es: ", end='')
    print(f(resultado))


n = 20
anchos = np.random.randint(10, 50, n)
alturas = np.random.randint(10, 75, n)

ga(n, 5000)
