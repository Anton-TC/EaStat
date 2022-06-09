class ControladorErrores():
    def __init__(self):
        self.separadorA = '---------------------------------------------------- ERROR ----------------------------------------------------\n'
        self.separadorB = '\n---------------------------------------------------- ERROR ----------------------------------------------------'

    # Levanta un error si hubo un error de sintáxis
    def errorDeSintaxis(self, entrada, noLinea):
        print("Error de sintaxis en tu entrada!", entrada)
        print("Error line: ", noLinea)
        raise Exception('Error de sintaxis')

    # Levanta un error si se intentó hacer una operación entre tipos incompatibles
    def tiposIncompatibles(self, operador, tipo_Izq, tipo_Der):
        print(self.separadorA)
        print('Mi compa... ¿cómo se te ocurre una ', operador,
                ' entre un ', tipo_Izq, ' y un ', tipo_Der, '?')
        print(self.separadorB)
        raise Exception('Tipos incompatibles')

    # Levanta un error si se intenta utilizar una variable no definida
    def varNoDefinida(self, id):
        print(self.separadorA)
        print('¿Y la declaración de "', id, '" dónde anda? ¿en Acapulco?')
        print(self.separadorB)
        raise Exception("Variable no definida")

    # Levanta un error si ya no existen espacios de memoria para constantes
    def excesoConstantes(self, tipo):
        print(self.separadorA)
        print('Hijole... no gracias mano, ya me llené de constantes tipo "',
                tipo, '"')
        print(self.separadorB)
        raise Exception("Exceso de constantes")

    # Levanta un error si ya no existen espacios de memoria para GLOBALES
    def excesoGlobales(self, tipo):
        print(self.separadorA)
        print('Hijole... no gracias mano, ya me llené de variables globales tipo "',
                tipo, '"')
        print(self.separadorB)
        raise Exception("Exceso de variables globales")

    # Levanta un error si ya no existen espacios de memoria para LOCALES
    def excesoLocales(self, tipo):
        print(self.separadorA)
        print('Hijole... no gracias mano, ya me llené de variables locales tipo "',
                tipo, '"')
        print(self.separadorB)
        raise Exception("Exceso de variables locales")

    # Levanta un error si ya no existen espacios de memoria para TEMPORALES
    def excesoTemporales(self, tipo):
        print(self.separadorA)
        print('Hijole... no gracias mano, ya me llené de temporales tipo "',
                tipo, '"')
        print(self.separadorB)
        raise Exception("Exceso de temporales")

    # Levanta un error si se utiliza una expresión incompatible en estatutos if o while
    def expresionIncompatible(self, tipo_exp):
        print(self.separadorA)
        print('Mmm... sí sabes que los "si" y los "mientras" ',
                'necesitan una expresión booleana y no una de tipo "',
                tipo_exp, '" ¿verdad?')
        print(self.separadorB)
        raise Exception('Expresión incompatible')
        
    # Levanta un error si la función sin tipo de retorno cuenta con un 'return'
    def funcionVacioConRetorno(self, tipo, nombre):
        print(self.separadorA)
        print('¡¿QUÉ ES ESTO?! ¡¿Un estatuto "regresa();" en la función ',
                nombre, ' de tipo ', tipo, '?!', '\n *Se muere de ver tal barbaridad*')
        print(self.separadorB)
        raise Exception('Declaración de función "vacio" con estatuto "regresa();"')

    # Levanta un error si tu función con tipo de retorno no cuenta con un 'return'
    def funcionSinRetorno(self, tipo, nombre):
        print(self.separadorA)
        print('O regresas un valor de tipo "', tipo, '" en tu función "',
                nombre , '" o regresas a programación nivel -1')
        print(self.separadorB)
        raise Exception('Declaración de función sin estatuto "regresa();"')

    # Levanta un error si se define una función más de una vez
    def funcionYaDefinida(self, nombre):
        print(self.separadorA)
        print('Hay mijo... ya definiste la función "', nombre,
                '()" ¿no te acuerdas?')
        print(self.separadorB)
        raise Exception("Función ya definida")
    
    # Levanta un error si se realiza una llamada a una función no definida
    def funcionNoDefinida(self, nombre):
        print(self.separadorA)
        print('¿A quién tratas de llamar? ¿a Dios? porque la función "',
                nombre , '()" ni existe')
        print(self.separadorB)
        raise Exception("Función no definida")
    
    # Levanta un error si se manda una cantidad incompatible de parámetros
    def noIncorrectoParametros(self, nombreFunc, firma):
        firmaTipos = []

        for par in firma:
            firmaTipos.append[par[0]]
        
        print(self.separadorA)
        print('¿Qué onda carnal? me dijiste que la función "', nombreFunc, 
                '" necesita la secuencia ', firmaTipos, 
                ' no esa locura que andas intentando')
        print(self.separadorB)
        raise Exception("Cantidad de parámetros incorrectos")
    
    # Levanta un error si la secuencia paramétirca no es respetada
    def secuenciaParamétricaIncorrecta(self, nombreFunc, firma):
        firmaTipos = []

        for par in firma:
            firmaTipos.append[par[0]]

        print(self.separadorA)
        print('Ah caray... no sabía que "', nombreFunc, 
                '" necesitaba la secuencia ', firmaTipos, 
                ' o leí mal o estás muy... ajam...')
        print(self.separadorB)
        raise Exception("Secuencia paramétrica incorrecta")
    
    # Levanta un error si el tipo de valor de retorno no coincide con el tipo de la función
    def tipoRetornoIncorrecto(self, nombre, tipoRes, tipo):
        print(self.separadorA)
        print('¡Aquí te voy a regresar pero un guamazo! tu función "',
                nombre, '" intenta regresar un valor de tipo "', tipoRes,
                '" siendo una función de tipo "', tipo, '"')
        print(self.separadorB)
        raise Exception("Tipo de retorno inválido")

    # Levanta un error si se intenta llamar una función sin retorno en una expresión
    def LlamadaFuncSinRetornoEnExpr(self, nombre, tipo):
        print(self.separadorA)
        print('Ta\' loco mi chato, me llamaste a la función ', nombre,
                ' de tipo ', tipo, ' ¡dentro de una expresión!')
        print(self.separadorB)
        raise Exception("Llamada a función sin retorno dentro de una expresión")
    
    # Levanta un error si se intenta llamar una función con retorno fuera de una expresión
    def LlamadaFuncConRetornoEnExpr(self, nombre, tipo):
        print(self.separadorA)
        print('Bueno bueno... ya tengo el resultado tipo ', tipo ,
                ' de ', nombre, '... ¿pero ahora qué hago con eso?')
        print(self.separadorB)
        raise Exception("Llamada a función con retorno fuera de una expresión, función, llamada, etc.")

    # Levanta un error si se intenta declarar una variable una 2da vez
    def variableYaDefinida(self, nombre):
        print(self.separadorA)
        print('JAJAJAJA muy buena esa... doble declaración de "', nombre, 
                '" JAJAJA...\n', 'Momento... ¿era en serio?')
        print(self.separadorB)
        raise Exception("Variable ya definida")

    # Levanta un error si se intenta usar una variable no declarada
    def variableNoDefinida(self, nombre):
        print(self.separadorA)
        print('¿Y la declaración de "', nombre, '" dónde anda? ¿en Acapulco?')
        print(self.separadorB)
        raise Exception("Variable no definida")

    # Levanta un error si se intenta indexar una variable normal
    def indexacionAVarNoArreglo(self, nombreVar):
        print(self.separadorA)
        print("No recuerdo que me dijeras que ", nombreVar, " es un arreglo")
        print(self.separadorB)
        raise Exception('Intento de indexación a variable normal')    
