import numpy as np
import Plotter


class StripPackagingRotations:
    # Attributes
    W = 100
    Pc = 0.65
    Pm = 0.05
    Np = 50
    anchos = []
    alturas = []
    n = 0
    gens = 5000

    show_figure = False

    # Constructor
    def __init__(self, n=10, gens=5000, anchos=None, alturas=None, max_width=100, seed=0, show_figure=True):
        np.random.seed(seed)
        self.W = 100
        self.Pc = 0.65
        self.Pm = 0.05
        self.Np = 50
        self.n = n
        self.gens = gens
        self.W = max_width
        self.show_figure = show_figure
        # Control for empty data
        if alturas is None or anchos is None and n != 0:
            self.anchos = np.random.randint(10, 50, n)
            self.alturas = np.random.randint(10, 75, n)
        else:
            self.anchos = anchos
            self.alturas = alturas

    # Genero la población como permutaciones de n elementos e indicando si está o no rotado el rectángulo
    def _generar_poblacion(self, n):
        poblacion = np.zeros((self.Np, 2, n))
        for i in range(self.Np):
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
    def _fitness(self, individuo):
        i = 0
        ancho_acum = 0
        altura_max = 0
        altura_total = 0

        for rectangulo in individuo[0]:
            rectangulo = int(rectangulo)
            # Chequeo la orientación del rectángulo
            if individuo[1][i] == 0:
                ancho_actual = self.anchos[rectangulo]
                altura_actual = self.alturas[rectangulo]
            else:
                ancho_actual = self.alturas[rectangulo]
                altura_actual = self.anchos[rectangulo]

            if ancho_actual + ancho_acum <= self.W:
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
    def _seleccionar_padre(self, poblacion):
        indice_padre1 = np.random.randint(0, self.Np - 1)
        indice_padre2 = np.random.randint(0, self.Np - 1)
        while indice_padre1 == indice_padre2:
            indice_padre2 = np.random.randint(0, self.Np - 1)
        # Selecciono dos padres al azar
        padre1 = poblacion[indice_padre1]
        padre2 = poblacion[indice_padre2]
        # Elijo al padre con la menor función de fitness
        if self._fitness(padre1) <= self._fitness(padre2):
            return padre1
        else:
            return padre2

    # Operador de crossover PMX
    def _pmx(self, padre1, padre2, n):
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
                index = self._indice(padre1[0], padre2[0][i])
                while punto1 <= index < punto2:
                    index = self._indice(padre1[0], hijo[0][index])
                hijo[0][index] = padre1[0][i]
                hijo[1][index] = padre1[1][i]
        return hijo

    # Mutación mediante intercambio de dos genes al azar
    def _mutacion(self, individuo, n):
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
    def _mejor_individuo(self, poblacion):
        resultado = poblacion[0]
        valor = self._fitness(poblacion[0])

        for i in range(1, self.Np):
            nuevo_valor = self._fitness(poblacion[i])
            if nuevo_valor < valor:
                valor = nuevo_valor
                resultado = poblacion[i]

        return np.copy(resultado)

    # Dado un individuo y un valor me devuelve la posición en la cual se encuentra
    def _indice(self, individuo, valor):
        for i in range(len(individuo)):
            if individuo[i] == valor:
                return i

    # Algoritmo principal
    def run(self):
        n = self.n
        gen = self.gens

        poblacion = self._generar_poblacion(n)
        nueva_poblacion = np.zeros((self.Np, 2, n))

        print("Ancho de los rectángulos: ", end='')
        print(self.anchos)
        print("Altura de los rectángulos: ", end='')
        print(self.alturas)
        print("-----------------------------------------")
        resultado = self._mejor_individuo(poblacion)
        print("Primer mejor resultado: ", end='')
        print(resultado)

        # Plot Individual
        if self.show_figure:
            Plotter.PlotterStrip().plot_individual_with_rotation(individual=resultado, max_width=self.W,
                                                                 heights=self.alturas, widths=self.anchos,
                                                                 title="Strip Packaging Problem - With Rotations \n"
                                                                       "Mejor solución - Inicio")
        print("La altura total es: ", end='')
        print(self._fitness(resultado))
        print("-----------------------------------------")

        for i in range(gen):
            for j in range(self.Np):
                # Realizo crossover
                if np.random.random() <= self.Pc:
                    padre1 = self._seleccionar_padre(poblacion)
                    padre2 = self._seleccionar_padre(poblacion)
                    hijo = self._pmx(padre1, padre2, n)
                else:
                    hijo = poblacion[j]

                # Realizo mutacion
                if np.random.random() <= self.Pm:
                    hijo = self._mutacion(hijo, n)
                # Agrego a la nueva población
                nueva_poblacion[j] = hijo

            poblacion = nueva_poblacion
            mejor_actual = self._mejor_individuo(poblacion)
            if self._fitness(mejor_actual) < self._fitness(resultado):
                resultado = np.copy(mejor_actual)

        print("El orden de rectángulos es: ", end='')
        print(resultado)

        # Plot Individual
        if self.show_figure:
            Plotter.PlotterStrip().plot_individual_with_rotation(individual=resultado, max_width=self.W,
                                                                 heights=self.alturas, widths=self.anchos,
                                                                 title="Strip Packaging Problem - With Rotations \n"
                                                                       "Mejor solución - Final")

        print("La altura total es: ", end='')
        print(self._fitness(resultado))

        # Return best individual and best value
        return resultado, self._fitness(resultado)
