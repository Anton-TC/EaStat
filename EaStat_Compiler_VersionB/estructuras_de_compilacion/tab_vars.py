from manejo_de_errores.estaticos import ControladorErrores

# Controlador de errores
llamaError = ControladorErrores()

class Variable():
    def __init__(self, tipo, nombre, dir):
        self.tipo = tipo
        self.nombre = nombre
        self.dir = dir
        self.tam = 1
        self.esArreglo = False
        self.dimensiones = []
        
    #--------------------------------------------------------------------#
    # printVar()
    #   Método para imprimir la variable.
    # Resultado:
    #   Datos de las variable impresos en consola en un formato más
    #   amigable.
    #--------------------------------------------------------------------#
    def printVar(self):
        print(  '\tVariable: '  , self.nombre,
                ', Tipo: '      , self.tipo,
                ', Dir: '       , self.dir, 
                ', Tam: '       , self.tam,
                ', ¿Arr?: '     , self.esArreglo,
                ', Dims: '      , self.dimensiones, '\n')

class TablaVars():
    def __init__(self, variables = {}):
        self.variables = variables
    
    #--------------------------------------------------------------------#
    # add()
    #   Método para añadir una nueva variable al diccionario “variables”.
    # Parámetros:
    #   variable: Objeto Variable() a agregar al diccionario.
    # Resultado:
    #   Variable añadida en el diccionario.
    #--------------------------------------------------------------------#
    def add(self, variable):
        if variable.nombre not in self.variables:
            self.variables[variable.nombre] = variable
        else:
            llamaError.variableYaDefinida(variable.nombre)

    #--------------------------------------------------------------------#
    # exists()
    #   Método para verificar que la variable existe en el diccionario
    #   "variables".
    # Parámetros:
    #   nombre: Nombre de la variable a verificar si está registrada.
    # Retorno:
    #   Bool que indica si existe o no en el diccionario.
    #--------------------------------------------------------------------#
    def exists(self, nombre):
        if nombre in self.variables:
            return True
        else:
            return False

    #--------------------------------------------------------------------#
    # get()
    #   Método para obtener una variable del diccionario dado su nombre.
    # Parámetros:
    #   nombre: Nombre de la variable.
    # Retorno:
    #   Variable deseada.
    #--------------------------------------------------------------------# 
    def get(self, nombre):
        if not nombre in self.variables:
            llamaError.variableNoDefinida(nombre)
        
        return self.variables[nombre]

    #--------------------------------------------------------------------#
    # update()
    #   Método que actualiza una variable al añadirla con el mismo nombre
    #   con el que estaba registrada.
    # Parámetros:
    #   variable: Variable a actualizar.
    # Resultado:
    #   Variable actualizada.
    #--------------------------------------------------------------------# 
    def update(self, variable):
        if not variable.nombre in self.variables:
            llamaError.variableNoDefinida(variable.nombre)

        self.variables[variable.nombre] = variable

    #--------------------------------------------------------------------#
        # addNodeToVar()
    #   Método que agrega un nuevo nodo a la estructura de un arreglo
    # Parámetros:
    #   nombreVar: Nombre del arreglo.
    #   nodo: Nodo para el arreglo.
    # Resultado:
    #   Arreglo actualizado.
    #--------------------------------------------------------------------#
    def addNodeToVar(self, nombreVar, nodo):
        self.get(nombreVar).dimensiones.append(nodo)
    #--------------------------------------------------------------------#
    # setAsArray()
    #   Método para indicar que una variable es arreglo
    #--------------------------------------------------------------------#
    def setAsArray(self, nombreVar):
        var = self.get(nombreVar)
        var.esArreglo = True
    #--------------------------------------------------------------------#
    # esArreglo()
    #   Método para verificar si una variable es arreglo
    #--------------------------------------------------------------------#
    def esArreglo(self, nombreVar):
        return self.get(nombreVar).esArreglo
    
    #--------------------------------------------------------------------#
    # calculaMs()
    #   Método para calcular las M´s de los arreglos.
    #--------------------------------------------------------------------#
    def calculaMs(self, arrNombre, R):
        # Extraer la variable a calcularle las Ms
        var = self.get(arrNombre)
        
        # Actualizar el tamaño total
        var.tam = R
        # Extraer la pila/arreglo de nodos
        nodos = var.dimensiones
        # Calcular Ms
        for nodo in nodos:
            m = R / (nodo[0] + 1)
            R = m
            
            # Si la M es 1, estoy en el nodo final
            nodo.append(int(m))


    #--------------------------------------------------------------------#
    # printT()
    #   Método para imprimir todas las variables.
    # Resultado:
    #   Tabla de variables impresa en consola en un formato más amigable.
    #--------------------------------------------------------------------#
    def printT(self):
        for nombre, valor in self.variables.items():
            valor.printVar()
