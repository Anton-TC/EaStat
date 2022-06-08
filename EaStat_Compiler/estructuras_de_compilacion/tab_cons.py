import json

class Constante():
    def __init__(self, valor, dir):
        self.valor = valor
        self.dir = dir

        if self.dir >= 34000 and self.dir < 37000:
            self.tipo = 'ent'
        elif self.dir >= 37000 and self.dir < 40000:
            self.tipo = 'flot'
        elif self.dir >= 40000 and self.dir < 43000:
            self.tipo = 'car'
        else:
            self.tipo = 'cadena'

    #--------------------------------------------------------------------#
    # printCons()
    #   Método para imprimir la constante.
    # Resultado:
    #   Datos de la constante impresos en consola en un formato más
    #   amigable.
    #--------------------------------------------------------------------#
    def printCons(self):
        print(  '\tTipo: '  + str(self.valor) +
                ', Dir: '   + str(self.dir) + 
                ', tipo: '  + '\n')

class TablaConst():
    def __init__(self, constantes = {}):
        self.constantes = constantes
    
    #--------------------------------------------------------------------#
    # add()
    #   Método para añadir una nueva constante al diccionario "constantes".
    # Parámetros:
    #   constante: Objeto Constante() a agregar al diccionario.
    # Resultado:
    #   Constante añadida en el diccionario.
    #--------------------------------------------------------------------#
    def add(self, constante):
        self.constantes[str(constante.valor)] = constante

    #--------------------------------------------------------------------#
    # exists()
    #   Método para verificar que la constante existe en el diccionario
    #   "constantes".
    # Parámetros:
    #   valor: Valor de tipo variado a verificar si está registrado.
    # Retorno:
    #   Bool que indica si existe o no en el diccionario.
    #--------------------------------------------------------------------#
    def exists(self, valor):
        if str(valor) in self.constantes:
            return True
        else:
            return False

    #--------------------------------------------------------------------#
    # get()
    #   Método para obtener una constante del diccionario dado su valor.
    # Parámetros:
    #   valor: Valor de la constante.
    # Retorno:
    #   Constante deseada.
    #--------------------------------------------------------------------#
    def get(self, valor):
        return self.constantes[str(valor)]

    #--------------------------------------------------------------------#
    # exportar()
    #   Método que genera un string en formato JSON y lo exporta a un
    #   archivo .JSON.
    # Resultado:
    #   Tabla de constantes exportada en formato JSON.
    #--------------------------------------------------------------------#
    def exportar(self):
        jsonString = '{'
        ultimo = len(self.constantes)
        indx = 1
        for nombre, const in self.constantes.items():
            if indx < ultimo:
                jsonString = jsonString + '\n\t"' + str(const.valor) + '": ' + json.dumps(const.__dict__) + ','
            else:
                jsonString = jsonString + '\n\t"' + str(const.valor) + '": ' + json.dumps(const.__dict__)
            indx = indx + 1
        jsonString = jsonString + '\n}'
    
        with open('./EaStat_Compiler/estructuras_de_ejecucion/constantes.json', 'w') as outfile:
            outfile.write(jsonString)

    #--------------------------------------------------------------------#
    # printT()
    #   Método para imprimir todas las constantes.
    # Resultado:
    #   Tabla de constantes impresa en consola en un formato más amigable.
    #--------------------------------------------------------------------#
    def printT(self):
        for nombre, valor in self.constantes.items():
            valor.printCons()