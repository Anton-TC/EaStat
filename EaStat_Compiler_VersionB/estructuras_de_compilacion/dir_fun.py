import json

from manejo_de_errores.estaticos import ControladorErrores

# Controlador de errores
llamaError = ControladorErrores()

class Funcion():
    def __init__(self, nombre, tipo, dirInicio, dirVar, tabla):
        self.nombre = nombre
        self.tipo = tipo
        self.returnCount = 0
        self.dirInicio = dirInicio
        self.dirVar = dirVar
        self.firma = []
        # Contadores de cantidades de variables [ENT, FLOT, CAR]
        self.numVars = [0, 0, 0]
        # Contadores de cantidades de temporales [ENT, FLOT, CAR, BOOL, CADENA]
        self.numTemps= [0, 0, 0, 0, 0]
        self.tabla = tabla
    
    #--------------------------------------------------------------------#
    # addReturn()
    #   Método para actualizar el número de retornos.
    # Resultado:
    #   contador de retornos actualizado.
    #--------------------------------------------------------------------#
    def addReturn(self):
        self.returnCount = self.returnCount + 1
    
    #--------------------------------------------------------------------#
    # tieneRetornos()
    #   Método para confirmar si la función cuenta con retornos.
    # Retorno:
    #   Bool que indica si existen retornos.
    #--------------------------------------------------------------------#
    def tieneRetornos(self):
        if self.returnCount > 0:
            return True
        return False

    #--------------------------------------------------------------------#
    # checkFirma()
    #   Método para verificar que un tipo de parámetro enviado, coincide
    #   con el tipo del argumento de la firma de la función, además de
    #   verificar que no se manden parámetros de más.
    # Parámetros:
    #   nombreFunc: String con el nombre de la función para usar en caso
    #               de tener que levantar un error.
    #   tipo: String con el tipo del parámetro a enviar.
    #   k: Indice en la firma de la función.
    # Resultado:
    #   Verificación de firma realizada correctamente
    #--------------------------------------------------------------------#
    def checkFirma(self, nombreFunc, tipo, k):
        length = len(self.firma)

        if k > length:
            llamaError.noIncorrectoParametros(nombreFunc, self.firma)
        
        if tipo != self.firma[k][0]:
            llamaError.secuenciaParamétricaIncorrecta(nombreFunc, self.firma)
    
    #--------------------------------------------------------------------#
    # matchFirma()
    #   Método para verificar que se llama con la misma cantidad de
    #   parametros.
    # Parámetros:
    #   nombreFunc: String con el nombre de la función para usar en caso
    #               de tener que levantar un error.
    #   k: Indice en la firma de la función.
    # Resultado:
    #   Validación de cantidad de parámetros realizada correctamente
    #--------------------------------------------------------------------#
    def matchFirma(self, nombreFunc, k):
        if len(self.firma) == 0:
            length = len(self.firma)
        else:
            length = len(self.firma) - 1

        if k != length:
            llamaError.noIncorrectoParametros(nombreFunc, self.firma)
    
    #--------------------------------------------------------------------#
    # matchTipoRegresa()
    #   Método para verificar el tipo del valor en el retorno con el tipo
    #   de la función.
    # Parámetros:
    #   tipoRes: Tipo del valor a retornar.
    # Resultado:
    #   Tipo de retorno validado correctamente.
    #--------------------------------------------------------------------#
    def matchTipoRegresa(self, tipoRes):
        if tipoRes != self.tipo:
            llamaError.tipoRetornoIncorrecto(self.nombre, tipoRes, self.tipo) 

    #--------------------------------------------------------------------#
    # addParam()
    #   Método para añadir un parámetro a la firma de la función.
    # Parámetros:
    #   param: Arreglo con el tipo y dirección del parámetro. 
    # Resultado:
    #   Parámetro añadido correctamente en la firma de la función.
    #--------------------------------------------------------------------#
    def addParam(self, param):
        self.firma.append(param)

        # PNF 3: Actualizar contador de variables LOCALES
        if param[0] == 'ent':
            self.numVars[0] = self.numVars[0] + 1
        elif param[0] == 'flot':
            self.numVars[1] = self.numVars[1] + 1
        else:
            self.numVars[2] = self.numVars[2] + 1

    #--------------------------------------------------------------------#
    # getDirParam()
    #   Método que extrae la dirección de un parámetro dado su índice
    #   para la firma de la función.
    # Parámetros:
    #   posParam: Índice del parámetro en la firma de la función. 
    # Retorno:
    #   Dirección del parámetro en la memoria del scope.
    #--------------------------------------------------------------------#
    def getDirParam(self, posParam):
        return self.firma[posParam][1]

    #--------------------------------------------------------------------#
    # updateVars()
    #   Método para actualizar la cantidad de VARIABLES de una función al
    #   restar los offsets de cada subsegmento.
    # Parámetros:
    #   nuevosIndices: Arreglo con el acumulado de indices del segmento. 
    #   offset: dirección base del segmento. 
    # Resultado:
    #   Cantidad de variables actualizadas.
    #--------------------------------------------------------------------#
    def updateVars(self, nuevosIndices, offset):
        # Conteo de variables ENT
        self.numVars[0] = nuevosIndices[0] - offset
        offset = offset + 3000
        # Conteo de variables FLOT
        self.numVars[1] = nuevosIndices[1] - offset
        offset = offset + 3000
        # Conteo de variables CAR
        self.numVars[2] = nuevosIndices[2] - offset

    #--------------------------------------------------------------------#
    # updateTemps()
    #   Método para actualizar la cantidad de TEMPORALES de una función.
    # Parámetros:
    #   nuevosIndices: Arreglo con el acumulado de indices del segmento. 
    # Resultado:
    #   Cantidad de temporales actualizadas.
    #--------------------------------------------------------------------#
    def updateTemps(self, nuevosIndices):
        # Conteo de temporales ENT
        self.numTemps[0] = nuevosIndices[0] - 19000
        # Conteo de temporales FLOT
        self.numTemps[1] = nuevosIndices[1] - 22000
        # Conteo de temporales CAR
        self.numTemps[2] = nuevosIndices[2] - 25000
        # Conteo de temporales BOOL
        self.numTemps[3] = nuevosIndices[3] - 28000
        # Conteo de temporales CADENA
        self.numTemps[4] = nuevosIndices[4] - 31000

    #--------------------------------------------------------------------#
    # emptyTablaVars()
    #   Método para vaciar la propia tabla de variables.
    # Resultado:
    #   Tabla de variables de la función queda sin variables.
    #--------------------------------------------------------------------#
    def emptyTablaVars(self):
        del self.tabla
        self.tabla = None

    #--------------------------------------------------------------------#
    # deleteTablaVars()
    #   Método para eliminar la propia tabla de variables.
    # Resultado:
    #   Tabla de variables de la función queda eliminada.
    #--------------------------------------------------------------------#
    def deleteTablaVars(self):
        del self.tabla

    #--------------------------------------------------------------------#
    # printFunc()
    #   Método para imprimir una función.
    # Resultado:
    #   Datos de la función impresos en consola en un formato más amigable.
    #--------------------------------------------------------------------#
    def printFunc(self):
        print(  'Función: ',            self.nombre,
                ', Tipo: ',             self.tipo,
                ', #Return: ',          self.returnCount,
                ', Dirección Inicio: ', self.dirInicio,
                ', Dirección Variable', self.dirVar,
                ', Firma: ',            self.firma,
                ', #Vars: ',            self.numVars,
                ', #Temporales: ',      self.numTemps)
        if self.tabla != None:
            print('\tTabla: ')
            self.tabla.printT()
        else:
            print('\tTabla: Eliminada')

class Directorio_Funcs():
    def __init__(self, funciones = {}):
        self.funciones = funciones
    
    #--------------------------------------------------------------------#
    # add()
    #   Método para añadir una nueva función al diccionario.
    # Parámetros:
    #   función: Objeto Funcion() a agregar al diccionario.
    # Resultado:
    #   Función añadida en el diccionario.
    #--------------------------------------------------------------------#
    def add(self, funcion):
        if not funcion.nombre in self.funciones:
            self.funciones[funcion.nombre] = funcion
            # Borrar
            #print('Función de nombre ' + funcion.nombre + ' añadida')
        else:
            llamaError.funcionYaDefinida(funcion.nombre)
         
    #--------------------------------------------------------------------#
    # get()
    #   Método para obtener una función del diccionario.
    # Parámetros:
    #   nombre: String con el nombre de la función a encontrar. 
    # Retorno:
    #   Función deseada.
    #--------------------------------------------------------------------#
    def get(self, nombre):
        if not nombre in self.funciones:
            llamaError.funcionNoDefinida(nombre)

        return self.funciones[nombre]

    #--------------------------------------------------------------------#
    # exportar()
    #   Método que genera un string en formato JSON y lo exporta a un
    #   archivo .JSON.
    # Resultado:
    #   Diccionario de funciones exportado en formato JSON.
    #--------------------------------------------------------------------#
    def exportar(self):
        jsonString = '{'
        ultimo = len(self.funciones)
        indx = 1
        for nombre, func in self.funciones.items():
            if indx < ultimo:
                jsonString = jsonString + '\n\t"' + func.nombre + '": ' + json.dumps(func.__dict__) + ','
            else:
                jsonString = jsonString + '\n\t"' + func.nombre + '": ' + json.dumps(func.__dict__)
            indx = indx + 1
        jsonString = jsonString + '\n}'
    
        with open('.//estructuras_de_ejecucion/directorio.json', 'w') as outfile:
            outfile.write(jsonString)

    #--------------------------------------------------------------------#
    # deleteTablasVars()
    #   Método para eliminar todas las tablas de variables de todas las
    #   funciones.
    # Resultado:
    #   Funciones sin tablas de variables
    #--------------------------------------------------------------------#
    def deleteTablasVars(self):
        for nombre, func in self.funciones.items():
            func.deleteTablaVars()
    
    #--------------------------------------------------------------------#
    # printDic()
    #   Método para imprimir el diccionario completo.
    # Resultado:
    #   Directorio de funciones impreso en consola en un formato amigable.
    #--------------------------------------------------------------------#
    def printDic(self):
        for nombre, valor in self.funciones.items():
            valor.printFunc()

