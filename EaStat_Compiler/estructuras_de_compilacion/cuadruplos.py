from ast import Str
import json

class Cuadruplo():
    def __init__(self, indice, operacion, opdo1, opdo2, destino):
        self.indice = indice
        self.operacion = operacion
        self.opdo1 = opdo1
        self.opdo2 = opdo2
        self.destino = destino
    
    #--------------------------------------------------------------------#
    # printCuad()
    #   Método para imprimir el cuadruplo.
    # Resultado:
    #   Datos del cuádruplo impresos en consola en un formato más
    #   amigable.
    #--------------------------------------------------------------------#
    def printCuad(self):
        print(  '#' + self.indice + ' - ' +
                ' Opcn: \'' + str(self.operacion) + '\'' +
                ' \tOpdo1: \''   + str(self.opdo1)  + '\'' +
                ' \tOpdo2: \''   + str(self.opdo2) + '\'' +
                ' \tDestino: \'' + str(self.destino) + '\'')

class Arr_Cuadruplos():
    def __init__(self, cuadruplos = {}):
        self.cuadruplos = cuadruplos

    #--------------------------------------------------------------------#
    # addSalto()
    #   Método para añadir un salto a un cuadruplo tipo goto.
    # Parámetros:
    #   indice: Índice del cuádruplo a actualizar.
    #   salto: Salgo a añadir en el cuádruplo.
    # Resultado:
    #   Cuádruplo actualizado con el salto.
    #--------------------------------------------------------------------#
    def addSalto(self, indice, salto):
        cuadru = self.cuadruplos[indice]
        cuadru = Cuadruplo(str(indice), cuadru.operacion, cuadru.opdo1, cuadru.opdo2, salto)
        self.add(cuadru)

    #--------------------------------------------------------------------#
    # add()
    #   Método que añade un cuadruplo al diccionario.
    # Parámetros:
    #   cuadruplo: Objeto Cuadruplo() a agregar al diccionario.
    # Resultado:
    #   Cuádruplo añadido en el diccionario.
    #--------------------------------------------------------------------#
    def add(self, cuadruplo):
        self.cuadruplos[cuadruplo.indice] = cuadruplo

    #--------------------------------------------------------------------#
    # exportar()
    #   Método que genera un string en formato JSON y lo exporta a un archivo .JSON
    # Resultado:
    #   Lista de cuádruplos exportada en formato JSON.
    #--------------------------------------------------------------------#
    def exportar(self):
        jsonString = '{'
        indx = 1
        for nombre, cuad in self.cuadruplos.items():
            if cuad.operacion != 'END':
                jsonString = jsonString + '\n\t"' + str(indx) + '": ' + json.dumps(cuad.__dict__) + ','
            else:
                jsonString = jsonString + '\n\t"' + str(indx) + '": ' + json.dumps(cuad.__dict__)
            indx = indx + 1
        jsonString = jsonString + '\n}'
    
        with open('./EaStat_Compiler/estructuras_de_ejecucion/cuadruplos.json', 'w') as outfile:
            outfile.write(jsonString)

    #--------------------------------------------------------------------#
    # printCuads()
    #   Método para imprimir todos los cuádruplos.
    # Resultado:
    #   Lista de cuádruplos impresa en consola en un formato más amigable.
    #--------------------------------------------------------------------#
    def printCuads(self):
        for nombre, valor in self.cuadruplos.items():
            valor.printCuad()
