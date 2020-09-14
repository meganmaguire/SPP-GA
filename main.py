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
        individuo = np.zeros((2,n))
        individuo[0] = np.random.permutation(n)
        # El valor 0 indica que no está rotado mientras que el 1 indica que si está rotado
        individuo[1] = np.random.randint(0,2,n)
        poblacion[i] = individuo
    return poblacion


# Función de fitness que devuelve la altura total de una distribución de rectángulos
def f(e):
    ancho_acum = 0
    altura_actual = 0
    altura_total = 0

    for i in e:
        i = int(i)
        if anchos[i] + ancho_acum <= W:
            ancho_acum += anchos[i]
            if alturas[i] > altura_actual:
                altura_actual = alturas[i]
        else:
            altura_total += altura_actual
            ancho_acum = anchos[i]
            altura_actual = alturas[i]

    altura_total += altura_actual
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
    hijo = np.zeros(n)
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
    hijo[:punto1] = padre1[:punto1]
    hijo[punto1:punto2] = padre2[punto1:punto2]
    hijo[punto2:] = padre1[punto2:]
    # Busco aquellos valores que no fueron copiados
    for i in range(punto1, punto2):
        if not (padre1[i] in padre2[punto1:punto2]):
            index = indice(padre1, padre2[i])
            while punto1 <= index < punto2:
                index = indice(padre1, hijo[index])
            hijo[index] = padre1[i]
    return hijo


# Mutación mediante intercambio de dos genes al azar
def mutacion(individuo):
    index1 = np.random.randint(0, n)
    index2 = np.random.randint(0, n)
    while index1 == index2:
        index2 = np.random.randint(0, n)
    aux = individuo[index1]
    individuo[index1] = individuo[index2]
    individuo[index2] = aux

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

ga(n, 10000)