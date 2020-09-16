import numpy as np
import Plotter


class StripPackagingNotRotations:
    W = 100
    Pc = 0.65
    Pm = 0.1
    Np = 50
    n = 20
    anchos = []
    alturas = []

    # Constructor
    def __init__(self, n=10, gens=5000, anchos=None, alturas=None, max_width=100):
        np.random.seed(0)
        self.W = 100
        self.Pc = 0.65
        self.Pm = 0.1
        self.Np = 50
        self.n = n
        self.gens = gens
        self.W = max_width

        # Control for empty data
        if alturas is None or anchos is None and n != 0:
            self.anchos = np.random.randint(10, 50, n)
            self.alturas = np.random.randint(10, 75, n)
        else:
            self.anchos = anchos
            self.alturas = alturas

        self._run(self.n, self.gens)

    # Genero la población como permutaciones de n elementos
    def _generar_poblacion(self, n):
        poblacion = np.zeros((self.Np, n))
        for i in range(self.Np):
            individuo = np.random.permutation(n)
            poblacion[i] = individuo
        return poblacion

    # Función de fitness que devuelve la altura total de una distribución de rectángulos
    def _fitness(self, e):
        ancho_acum = 0
        altura_actual = 0
        altura_total = 0

        for i in e:
            i = int(i)
            if self.anchos[i] + ancho_acum <= self.W:
                ancho_acum += self.anchos[i]
                if self.alturas[i] > altura_actual:
                    altura_actual = self.alturas[i]
            else:
                altura_total += altura_actual
                ancho_acum = self.anchos[i]
                altura_actual = self.alturas[i]

        altura_total += altura_actual
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
                index = self._indice(padre1, padre2[i])
                while punto1 <= index < punto2:
                    index = self._indice(padre1, hijo[index])
                hijo[index] = padre1[i]
        return hijo

    # Mutación mediante intercambio de dos genes al azar
    def _mutacion(self, individuo):
        index1 = np.random.randint(0, self.n)
        index2 = np.random.randint(0, self.n)
        while index1 == index2:
            index2 = np.random.randint(0, self.n)
        aux = individuo[index1]
        individuo[index1] = individuo[index2]
        individuo[index2] = aux

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
    def _run(self, n, gen):
        poblacion = self._generar_poblacion(n)
        nueva_poblacion = np.zeros((self.Np, n))

        print("Ancho de los rectángulos: ", end='')
        print(self.anchos)
        print("Altura de los rectángulos: ", end='')
        print(self.alturas)
        print("-----------------------------------------")
        resultado = self._mejor_individuo(poblacion)
        print("Primer mejor resultado: ", end='')
        print(resultado)

        # Plot Individual
        Plotter.PlotterStrip().plot_individual_with_no_rotation(individual=resultado, max_width=self.W,
                                                                heights=self.alturas, widths=self.anchos,
                                                                title="Strip Packaging Problem - No Rotations \n"
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
                    hijo = self._mutacion(hijo)
                # Agrego a la nueva población
                nueva_poblacion[j] = hijo

            poblacion = nueva_poblacion
            mejor_actual = self._mejor_individuo(poblacion)
            if self._fitness(mejor_actual) < self._fitness(resultado):
                resultado = np.copy(mejor_actual)

        print("El orden de rectángulos es: ", end='')
        print(resultado)

        # Plot Individual
        Plotter.PlotterStrip().plot_individual_with_no_rotation(individual=resultado, max_width=self.W,
                                                                heights=self.alturas, widths=self.anchos,
                                                                title = "Strip Packaging Problem - No Rotations \n"
                                                                        "Mejor solución - Final")
        print("La altura total es: ", end='')
        print(self._fitness(resultado))
