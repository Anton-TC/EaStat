from tkinter import N
from tkinter.messagebox import NO
import numpy


class Segmento():
    def __init__(self, dirBase, tamanos, bool, cadena, pntr):
        # Inicializar atributos de configuración
        self.cBool = bool
        self.cCad = cadena
        self.cPntr = pntr

        # BORRAR: es posible que no sean necesarios
        self.bool = self.cadena = self.pntr = None
        self.dirBB = self.dirBS = self.DirBP = None
        
        # Inicializar indice de tamaños de los segmentos de tipos
        extra = len(tamanos) - 3

        # Inicializar índice de indexación para la lista de tamaños
        indice = 3

        # Inicializar espacio de ENTEROS
        self.dirBE = dirBase
        self.ent = numpy.empty(tamanos[0], dtype=object)
        
        # Inicializar espacio de FLOTANTES
        self.dirBF = self.dirBE + 3000
        self.flot = numpy.empty(tamanos[1], dtype=object) 

        # Inicializar espacio de CAREACTARES
        self.dirBC = aux = self.dirBF + 3000
        self.car = numpy.empty(tamanos[2], dtype=object)
        
        # Verificar si tiene e inicializar espacio de BOOLEANOS
        if bool and extra > 0:
            self.dirBB = aux = aux + 3000
            self.bool = numpy.empty(tamanos[indice], dtype=object)
            extra = extra - 1
            indice = indice + 1
        
        # Verificar si tiene e inicializar espacio de CADENAS
        if cadena and extra > 0:
            self.dirBS = aux = aux + 3000
            self.cadena = numpy.empty(tamanos[indice], dtype=object)
            extra = extra - 1
            indice = indice + 1
        
        # Verificar si tiene e inicializar espacio de PUNTEROS
        if pntr and extra > 0:
            self.dirBP = aux = aux + 3000
            self.pntr = numpy.empty(tamanos[indice], dtype=object)
            extra = extra - 1
            indice = indice + 1

    # Método que obtiene el valor de cualquiera de los sub_segmentos de tipos
    def get(self, direccion):
        # Buscar si la dirección forma parte de los valores enteros, flotantes o caracteres
        if direccion >= self.dirBE and direccion < self.dirBF:
            return self.ent[direccion - self.dirBE]

        elif direccion >= self.dirBF and direccion < self.dirBC:
            return self.flot[direccion - self.dirBF]

        elif direccion >= self.dirBC and direccion < self.dirBC + 3000:
            return self.car[direccion - self.dirBC]

        # Buscar si la dirección forma parte de los valores booleanos, cadena o pointer
        elif self.cBool:
            if direccion >= self.dirBB and direccion < self.dirBB + 3000:
                return self.bool[direccion - self.dirBB]
        
        elif self.cCad:
            if direccion >= self.dirBS and direccion < self.dirBS + 3000:
                return self.cadena[direccion - self.dirBS]
        
        elif self.cPntr:
            if direccion >= self.dirBP and direccion < self.dirBP + 3000:
                return self.pntr[direccion - self.dirBP]

    # Método que asigna un valor en cualquiera de los sub_segmentos de tipos
    def set(self, direccion, valor):
        # Buscar si la dirección forma parte de los valores enteros, flotantes o caracteres
        if direccion >= self.dirBE and direccion < self.dirBF:
            self.ent[direccion - self.dirBE] = valor

        elif direccion >= self.dirBF and direccion < self.dirBC:
            self.flot[direccion - self.dirBF] = valor

        elif direccion >= self.dirBC and direccion < self.dirBC + 3000:
            self.car[direccion - self.dirBC] = valor

        # Buscar si la dirección forma parte de los valores booleanos, cadena o pointer
        elif self.cBool:
            if direccion >= self.dirBB and direccion < self.dirBB + 3000:
                self.bool[direccion - self.dirBB] = valor
        
        elif self.cCad:
            if direccion >= self.dirBS and direccion < self.dirBS + 3000:
                self.cadena[direccion - self.dirBS] = valor
        
        elif self.cPntr:
            if direccion >= self.dirBP and direccion < self.dirBP + 3000:
                self.pntr[direccion - self.dirBP] = valor

    def printMem(self):
        print()