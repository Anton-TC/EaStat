from hashlib import new


class controladorDeMem():
    def __init__(self, memoria):
        self.memoria = memoria

    #--------------------------------------------------------------------#
    # obtenerValor()
    #   Método para obtener un valor de una dirección específica de
    #   memoria.
    # Parámetros:
    #   dir: String con la dirección de memoria.
    #   scope: String que ayuda a identificar qué segmento de memoria tomar. 
    # Retorno:
    #   Valor solicitado.
    #--------------------------------------------------------------------#
    def obtenerValor(self, dir, scope):
        # Revisar si voy a buscar constantes
        if dir >= 34000 and dir < 46000:
            return self.memoria[0].get(dir)

        # Revisar si vestoy buscando variables GLOBALES
        if dir >= 1000 and dir < 10000:
            return self.memoria[1][0].get(dir)

        # Revisar si estoy buscando memoria temporal GLOBAL
        elif scope == 'Global':
            # Revisar si la dirección es de tipo pointer
            if dir >= 31000 and dir < 34000:
                # Obtener el valor de la dirección puntero
                newDir = self.memoria[1][1].get(dir)
                # Llamar recursivamente
                return self.obtenerValor(newDir, 'Global')
            # Regresar valor temporal
            return self.memoria[1][1].get(dir)

        # De otra forma, estoy buscando mmemoria LOCAL
        else:
            # Extraer y regresar la memoria del scope actual
            scopeActual = self.memoria.pop()
            self.memoria.append(scopeActual)

            # Revisar si la dirección es de variables o de temporales
            if dir >= 10000 and dir < 19000: # Variables
                return scopeActual[0].get(dir)
            else:   # Temporales
                
                # Revisar si la dirección es de tipo pointer
                if dir >= 31000 and dir < 34000:
                    # Obtener el valor de la dirección puntero
                    newDir = scopeActual[1].get(dir)

                    # Llamar recursivamente
                    return self.obtenerValor(newDir, scope)

                return scopeActual[1].get(dir)

    #--------------------------------------------------------------------#
    # guardarValor()
    #   Método para guardar un valor de una dirección específica de
    #   memoria.
    # Parámetros:
    #   dir: String con la dirección de memoria.
    #   valor: Dato a guardar.
    #   scope: String que ayuda a identificar qué segmento de memoria tomar. 
    # Resultado:
    #   Valor guardado.
    #--------------------------------------------------------------------#
    def guardarValor(self, dir, valor, scope):
        # Revisar si voy a buscar constantes
        if dir >= 34000 and dir < 46000:
            self.memoria[0].set(dir, valor)

        # Revisar si vestoy buscando variables GLOBALES
        elif dir >= 1000 and dir < 10000: # Variables
            self.memoria[1][0].set(dir, valor)

        # Revisar si estoy buscando memoria temporal GLOBAL
        elif scope == 'Global':
            # Revisar si la dirección es de tipo pointer
            if dir >= 31000 and dir < 34000:
                # Obtener el valor de la dirección puntero
                newDir = self.memoria[1][1].get(dir)
                # Llamar recursivamente
                self.guardarValor(newDir, valor, 'Global')
            else:
                # Temporales
                self.memoria[1][1].set(dir, valor)
        # De otra forma, estoy buscando mmemoria LOCAL
        else:
            # Extraer la memoria local más reciente
            memLocal = self.memoria.pop()

            # Revisar si la dirección es de variables o de temporales
            if dir >= 10000 and dir < 19000: # Variables
                memLocal[0].set(dir, valor)
            else:
                # Revisar si la dirección es de tipo pointer
                if dir >= 31000 and dir < 34000:
                    # Obtener el valor de la dirección puntero
                    newDir = memLocal[1].get(dir)

                    # Llamar recursivamente
                    self.guardarValor(newDir, valor, scope)
                else:
                    # Temporales
                    memLocal[1].set(dir, valor)
            
            # Regresar memoria local al stack
            self.memoria.append(memLocal)

    #--------------------------------------------------------------------#
    # reescribirApuntador()
    #   Método para reescribir la memoria a la que apunta un apuntador.
    # Parámetros:
    #   dirDestino: String con la dirección de memoria a modificar.
    #   dirNueva: Nueva dirección a colocar.
    #   scope: String que ayuda a identificar qué segmento de memoria tomar.
    # Resultado:
    #   Dirección guardada.
    #--------------------------------------------------------------------#
    def reescribirApuntador(self, dirDestino, dirNueva, scope):
        if scope == 'Global':
            self.memoria[1][1].set(dirDestino, dirNueva)
        else:
            # Extraer la memoria local más reciente
            memLocal = self.memoria.pop()
            memLocal[1].set(dirDestino, dirNueva)
            
            # Regresar memoria local al stack
            self.memoria.append(memLocal)

    #--------------------------------------------------------------------#
    # mandarParam()
    #   Método que permite mandar parámetros entre distintos scopes.
    # Parámetros:
    #   dirOrigen: String con la dirección de memoria origen.
    #   dirDestino: Direcición a la cual pasar parámetro.
    # Resultado:
    #   Parámetros mandados al nuevo segmento de memoria.
    #--------------------------------------------------------------------#
    def mandarParam(self, dirOrigen, dirDestino):
        # Extraer el scope actual
        scopeActual = self.memoria.pop()

        # Revisar si voy a mandar una constante y mandarla al scope actual
        if dirOrigen >= 34000 and dirOrigen < 46000:
            param = self.memoria[0].get(dirOrigen)
            scopeActual[0].set(dirDestino, param)

            self.memoria.append(scopeActual)
        else:
            # Extraer el scope anterior
            scopeAnterior = self.memoria.pop()
            
            # Quitar direcciones tipo pointer
            while dirOrigen >= 31000 and dirOrigen < 34000:
                dirOrigen = scopeAnterior[1].get(dirOrigen)

            # Revisar si la dirección es de variables o de temporales
            # y extraer el dato de la dirección origen del scope anterior 
            if dirOrigen >= 1000 and dirOrigen < 10000: # Variables Globales
                param = scopeAnterior[0].get(dirOrigen)
            elif dirOrigen >= 10000 and dirOrigen < 19000: # Variables Locales
                param = scopeAnterior[0].get(dirOrigen)
            else:   # Temporales

                param = scopeAnterior[1].get(dirOrigen)

            # Mandar el dato a la dirección destino del scope actual
            # (Siempre es a las variables, no se puede asignar un parámetro
            # a una temporal)
            scopeActual[0].set(dirDestino, param)

            # Regresar los scopes a como estaban
            self.memoria.append(scopeAnterior)
            self.memoria.append(scopeActual)

    #--------------------------------------------------------------------#
    # agregarScope()
    #   Método que agrega un nuevo scope al final de la pila.
    # Parámetros:
    #   scope: Segmento de memoria a agregar al stack de memoria.
    # Resultado:
    #   Segmento de memoria insertado.
    #--------------------------------------------------------------------#
    def agregarScope(self, scope):
        self.memoria.append(scope)

    #--------------------------------------------------------------------#
    # extraerScope()
    #   Método que regresa el último scope de la pila.
    # Retorno:
    #   Segmento al final de memoria.
    #--------------------------------------------------------------------#
    def extraerScope(self):
        return self.memoria.pop()

    #--------------------------------------------------------------------#
    # eliminarUltimoScope()
    #   Método que elimina el último scope de la pila.
    # Retorno:
    #   Último segmento eliminado de memoria.
    #--------------------------------------------------------------------#
    def eliminarUltimoScope(self):
        self.memoria.pop()

