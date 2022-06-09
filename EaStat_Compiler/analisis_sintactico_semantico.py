# Antonio Torres Carvajal - A01561769
from ast import Global
from asyncio import constants
from glob import glob
from estructuras_de_compilacion.cubo_sem import cuboSem
from ply.yacc import yacc

import ply.yacc as yacc
import codecs
import os
import sys

from analisis.lexical_analyzer import tokens
from analisis.lexical_analyzer import lexer
from estructuras_de_compilacion.cuadruplos import Arr_Cuadruplos, Cuadruplo
from estructuras_de_compilacion.cubo_sem import cuboSem
from estructuras_de_compilacion.dir_fun import Directorio_Funcs, Funcion
from estructuras_de_compilacion.tab_cons import TablaConst, Constante
from estructuras_de_compilacion.tab_vars import TablaVars, Variable
from estructuras_de_compilacion.cubo_sem import cuboSem
from manejo_de_errores.estaticos import ControladorErrores

# --------------------------------------------------------- CONTROLADOR DE ERRORES ----------------------------------------------------------
# Controlador de errores
llamaError = ControladorErrores()

# ----------------------------------------------------- VARS Y ESTRUCTURAS DE CUADRUPLOS ------------------------------------------------------
# Inicializar cubo semántico
cuboS = cuboSem()

# Inicializamos la lista de cuadruplos
misCuadruplos = Arr_Cuadruplos({})

# Declarar índice de los cuádruplos
indiCuad = 1

# Data Segment: Declarar índice de direcciones GLOBALES (Rango 1,000 -> 9,999, 10k en total)
indicesGlob = [1000, 4000, 7000]

# Stack Segment: Declarar índice de direcciones LOCALES (Rango 10,000 -> 19,999, 10k en total)
indicesLoc = [10000, 13000, 16000]

# Extra Segment: Declarar índice de direcciones TEMPORALES (Rango 20,000 -> 34,999, 15k en total)
indicesTemp = [19000, 22000, 25000, 28000, 31000]

# Declarar índice de direcciones CONSTANTES (Rango 35,000 -> 46,999, 12k en total)
indicesCons = [34000, 37000, 40000, 43000]

# Declaración e inicialización de las pilas de:
stkOperandos = []       # Operandos
stkOperadores = []      # Operadores
stkTipos = []           # Tipos
stkSaltos = []          # Saltos
stkLlamadas = []        # Llamadas de función
stkScope = []           # función en la que se está trabajando
stkArrs = []            # Variable candidata a arreglo
stkDim = []             # Dimensiones

# Tabla general de constantes 
constantes= TablaConst({})

# ----------------------------------------------------------- INICIO GRAMÁTICAS -----------------------------------------------------------

#--------------------------------------------------------------------#
# p_programa1()
#   Regla gramatical para la base de un programa en lenguaje EaStat.
#   
#   - P8: Actualizar contador de temporales globales.
#   - P9: Eliminar tablas de variables.
#   - P10: Generar cuádruplo 'end'.
#   - P11: Exportar cuádruplos, directorio de funciones y constantes.
#--------------------------------------------------------------------#
# PROGRAMA
def p_programa1(p):
    'programa : inicio programa2 principal cuerpo PUCOMA'

    directoriofs.get('Global').updateTemps(indicesTemp)

    #print('Imprimiendo directorio de funciones...\n')
    directoriofs.printDic()

    # Eliminar todas las tablas de variables
    directoriofs.deleteTablasVars()

    # Generar Cuádruplo END
    generaCuadruplo('END', '', '', '')

    #print('\nImprimiendo cuadruplos...\n')
    #misCuadruplos.printCuads()

    # Exportar cuádruplos a un archivo .JSON
    misCuadruplos.exportar()

    # Exportar directorio de funciones a un archivo .JSON
    directoriofs.exportar()

    # Exportar las constantes a un archivo .JSON
    constantes.exportar()

    p[0] = '¡Programa compilado con éxito!'

#--------------------------------------------------------------------#
# p_programa2()
#   Regla gramatical para declaración de variables y de funciones.
#   
#   - P6: Actualizar la cantidad de variables globales
#--------------------------------------------------------------------#
def p_programa2(p):
    '''
    programa2   :  dec_vars programa2
                |  programa3
    '''
    directoriofs.get('Global').updateVars(indicesGlob, 1000)

def p_programa3(p):
    '''
    programa3   : func programa3
                | fin
    '''
#--------------------------------------------------------------------#
# p_inicio()
#   Regla gramatical para el token INICIO
#   
#   - P1: Genera cuadruplo gotoM.
#   - P2: Añadir índice de gotoM al stack de saltos.
#   - P3: Crea el directorio de funciones. 
#   - P4: Registra la función global en el directorio de funciones.
#   - P5: Añadir a la pila currF la función Global.
# Resultado:
#   - Nueva función registrada en el directorio de funciones.
#   - Variable de función añadida a la tabla de variables globales.
#--------------------------------------------------------------------#
def p_inicio(p):
    'inicio : INICIO'

    global indiCuad

    # P1
    generaCuadruplo('gotoM', '', '', '')

    # P2
    stkSaltos.append(indiCuad - 1)
    
    global directoriofs
    # P3
    directoriofs = Directorio_Funcs({})

    # Creación de la tabla de variables globales vacía
    tabla = TablaVars({})

    # Creación de la función global
    fun = Funcion('Global', 'vacio', indiCuad, -1, tabla)

    # P4:
    directoriofs.add(fun)

    # Añadir a la pila la función en la que se está trabajando
    stkScope.append('Global')

#--------------------------------------------------------------------#
# p_principal()
#   Regla gramatical para el token PRINCIPAL.
#   
#   - P7: Actualiza el cuádruplo 'gotoM'
#--------------------------------------------------------------------#
def p_principal(p):
    'principal : PRINCIPAL'
    misCuadruplos.addSalto(str(stkSaltos.pop()), indiCuad)

# VARIABLE
#--------------------------------------------------------------------#
# p_variable1()
#   Regla gramatical para detectar una variable.
#  
#   - V8: Registrar dirección de inicio como constante
#   - V9: Genera cuádruplo de suma de direcciones a pointer
#--------------------------------------------------------------------#
def p_variable1(p):
    'variable : varID variable2'

    # Revisar en cual función me encuentro
    currFunct = stkScope.pop()
    stkScope.append(currFunct)

    # Extraer la función actual del direcitorio
    func = directoriofs.get(currFunct)

    # Extraer la variable en la dimensión
    var = func.tabla.get(stkArrs.pop())

    if var.isArray:
        # Extraer el resultado de la formula
        res = stkOperandos.pop()
        resTipo = stkTipos.pop()

        # Extraer la dimensión
        dimension = stkDim.pop()

        # Extraer la dirección de inicio de la variable
        dirVirtual = var.dir

        # Registrar la dirección como constante
        appendConst('ent', dirVirtual)

        # Extraer constante del stack de operandos
        direccion = stkOperandos.pop()
        dirTipo = stkTipos.pop()
        
        # Obteer la siguiente dirección pointer disponible
        dirPntr = indicesTemp[4] 

        # Generar cuádruplo de suma
        generaCuadruplo('+', res, direccion, dirPntr)

        # Actualizar índices
        indicesTemp[4] = indicesTemp[4] + 1

        # Insertar tipo y dir temporal pntr en el stack de operandos
        stkOperandos.append(dirPntr)
        stkTipos.append(dirTipo)

def p_variable2(p):
    '''
    variable2   : braIzqAccArr expresion_a braDerAccArr variable3
                | braIzqAccArr expresion_a braDerAccArr
                | fin
    '''

def p_variable3(p):
    '''
    variable3   : braIzqAccArr expresion_a braDerAccArr
    '''

#--------------------------------------------------------------------#
# p_varID()
#   Regla gramatical para detectar una variable.
#  
#   - V1: Valida que la variable exista de forma local y luego global.
#   - V2: Agrega la variable al stack de operandos y el tipo al
#         stack de tipos.
#   - V3 Validar que la variable tenga dimensiones y de ser así,
#        intertar el ID en lugar de la dirección.
#--------------------------------------------------------------------#
def p_varID(p):
    'varID : ID'
    varID = p[1]
        
    # Revisar en cual función me encuentro
    currFunct = stkScope.pop()
    stkScope.append(currFunct)

    # Extraer la función actual del direcitorio
    func = directoriofs.get(currFunct)

    # Verificar si la variable existe en la tabla de la función
    if not func.tabla.exists(varID):
       
        # En caso de no existir buscar en la tabla global
        # Si no está, levantamos un error de variable no declarada
        globalFunc = directoriofs.get('Global')
        if not globalFunc.tabla.exists(varID):
            llamaError.varNoDefinida(varID)
        else:
            myVar = globalFunc.tabla.get(varID)
    else: # En caso de estar en la tabla de vars de la función...
       
        # Obtener la variable de la tabla de variables de la función correspondiente
        myVar = func.tabla.get(varID)
        
    # Añadir dirección de la variable al stack de operandos
    stkOperandos.append(myVar.dir)

    # Añadir nombre de variable al stack de arreglos por si la var no está registrada como arreglo
    stkArrs.append(varID)
    
    # Añadir tipo de la variable al stack de operadores
    stkTipos.append(myVar.tipo)

    # En caso de que la variable sea arreglo
    if myVar.isArray:
        DIM = 1
        Dimension = [myVar, DIM]
        stkDim.append(Dimension)
        stkOperadores.append('_FF')
        stkOperandos.pop()
        stkTipos.pop()

#--------------------------------------------------------------------#
# p_braIzqAccArr()
#   Regla gramatical para detectar un '[' de un acceso a un arreglo.
#  
#   - V4: Valida que la variable sea un arreglo.
#--------------------------------------------------------------------#
def p_braIzqAccArr(p):
    'braIzqAccArr : BRAIZQ'

    # Extraer nombre del supuesto arreglo
    arrID = stkArrs.pop()
    stkArrs.append(arrID)
        
    # Revisar en cual función me encuentro
    currFunct = stkScope.pop()
    stkScope.append(currFunct)

    # Extraer la función actual del direcitorio
    func = directoriofs.get(currFunct)
    
    # Extraer variable
    myVar = func.tabla.get(arrID)

    # Validar que la variable es arreglo
    if not myVar.isArray:
        llamaError.indexacionAVarNoArreglo(arrID)

#--------------------------------------------------------------------#
# p_braDerAccArr()
#   Regla gramatical para detectar un ']' de un acceso a un arreglo.
#  
#   - V5: Generar cuadruplo 'verif'
#   - V6: Generar cuadruplo de multiplicación por M
#   - V7: Generar cuadruplo de la suma de las dos dimensiones
#--------------------------------------------------------------------#
def p_braDerAccArr(p):
    'braDerAccArr : BRADER'

    # Extraer resultado de la expresión
    resultado2 = stkOperandos.pop()
    tipoRes2 = stkTipos.pop()

    # Verificar que el tipo de resultado es correcto
    if tipoRes2 != 'ent':
        llamaError.errorDeIndexacion()

    # Extarer dimensión
    dimension = stkDim.pop()

    # Extraer la variable y la DIM del stack de dimensiones
    arrVar = dimension[0]
    dimNum = dimension[1]

    # Extraer el límite superior y convertirlo a constante
    limSup = arrVar.dimensiones[dimNum - 1][0]
    
    # Registrar la dirección como constante
    appendConst('ent', limSup)

    # Extraer constante del stack de operandos
    dirLimSup = stkOperandos.pop()
    dirTipo = stkTipos.pop()

    # Extraer la M
    m = arrVar.dimensiones[dimNum - 1][1]

    # Generar cuadruplo 'verif'
    generaCuadruplo('verif', resultado2, '', dirLimSup)

    # Validar si hay más dimensiones
    if dimNum == 1:
        global indicesTemp

        # Determinar el índice a utilizar indicesTemp[ENT, FLOT, CAR, BOOL, PNTR]
        if tipoRes2 == 'ent':
            indice = 0
        elif tipoRes2 == 'flot':
            indice = 1
        elif tipoRes2 == 'car':
            indice = 2
        elif tipoRes2 == 'bool':
            indice = 3
        else:
            indice = 4

        # Asignar temporal de resultado
        dirTemp = indicesTemp[indice] 

        # Registrar m como constante
        appendConst('ent', m)

        # Extraer constante del stack de operandos
        direccionM = stkOperandos.pop()
        dirTipo = stkTipos.pop()

        # Generar cuadruplo multiplicacióne '*' 
        generaCuadruplo('*', resultado2, direccionM, dirTemp)

        # Actualizar índices
        indicesTemp[indice] = indicesTemp[indice] + 1

        # Quitar Fondo Falso
        stkOperadores.pop()

        # Insertar resultado en el stack de operandos y tipos
        stkOperandos.append(dirTemp)
        stkTipos.append(tipoRes2)
    
    if dimNum == 2:
        # Extraer resultado de la expresión
        resultado1 = stkOperandos.pop()
        tipoRes1 = stkTipos.pop()

        # Determinar el índice a utilizar indicesTemp[ENT, FLOT, CAR, BOOL, PNTR]
        if tipoRes1 == 'ent':
            indice = 0
        elif tipoRes1 == 'flot':
            indice = 1
        elif tipoRes1 == 'car':
            indice = 2
        elif tipoRes1 == 'bool':
            indice = 3
        else:
            indice = 4

        # Asignar temporal de resultado
        dirTemp = indicesTemp[indice] 

        generaCuadruplo('+', resultado1, resultado2, dirTemp)

        # Actualizar índices
        indicesTemp[indice] = indicesTemp[indice] + 1

        # Insertar resultado en el stack de operandos y tipos
        stkOperandos.append(dirTemp)
        stkTipos.append(tipoRes1)
    
    dimension[1] = dimension[1] + 1

    # Regresar nodo dimension al stack de dimensiones
    stkDim.append(dimension)

# DECLARACION DE VARIABLES
#--------------------------------------------------------------------#
# p_dec_vars1()
#   Regla gramatical para detectar una declaración de variable.
#   
#   - DV7: Retirar nombre de variable del stack de potenciales arreglos.
#   - DV8: Verificar si la variable es arreglo.
#   - DV9: Calcular las M's de las dimensiones y actualizar índices
#          glob/loc.
#--------------------------------------------------------------------#
def p_dec_vars1(p):
	
    'dec_vars : registroVar dec_vars2 PUCOMA'
    global R

    # Retirar nombre de variable del stack
    arrNombre = stkArrs.pop()
    
    # Extraer scope actual
    scope = stkScope.pop()
    stkScope.append(scope)
    
    # Extraer la función
    func = directoriofs.get(scope)
    
    # Verificar que la variable tiene dimensiones
    if func.tabla.isArray(arrNombre):
        
        # Calcular las M's
        func.tabla.calculaMs(arrNombre, R)
        tipo = p[1]
        
        # Actualizar índices
        if scope == 'Global':
            if tipo == 'ent':
                indicesGlob[0] = indicesGlob[0] + R - 1
            elif tipo == 'flot':
                indicesGlob[1] = indicesGlob[1] + R - 1
            else:
                indicesGlob[2] = indicesGlob[2] + R - 1
        else:
            if tipo == 'ent':
                indicesLoc[0] = indicesLoc[0] + R - 1
            elif tipo == 'flot':
                indicesLoc[1] = indicesLoc[1] + R - 1
            else:
                indicesLoc[2] = indicesLoc[2] + R - 1

def p_dec_vars2(p):
    '''
    dec_vars2   : braIzqDecArr mandaConst braDerDecArr dec_vars3
                | braIzqDecArr mandaConst braDerDecArr
                | fin
    '''

def p_dec_vars3(p):
    '''
    dec_vars3   : BRAIZQ mandaConst braDerDecArr
    '''

#--------------------------------------------------------------------#
# p_registroVar()
#   Regla gramatical para el tipo y el ID de una declaración de variable
#  
#   - DV1: Manda a registrar la variable con el tipo y el id a tabla de
#     variables de la función corresondiente.
#   - DV2: Inserta nombre de variable al stack de declaración de arreglos.
# Resultado:
#   - La variable queda registrada en su respectiva función.
#--------------------------------------------------------------------#
def p_registroVar(p):
    'registroVar : tipo ID'
    
    # Registro
    tipo = p[1]
    id = p[2]
    addToVarsTab(tipo, id)
    
    # Insertar nombre de variable al stack de declaración de arreglos
    stkArrs.append(id)
    
    # Mandar el tipo de vari
    p[0] = p[1]
#--------------------------------------------------------------------#
# p_braIzqDecArr()
#   Regla gramatical para detectar el token BRAIZQ en la declaración
#   de variables.
#
#   - DV3: Inicializar R (se usa para calcular las M's).
#   - DV4: Marcar variable como arreglo.
#--------------------------------------------------------------------#
def p_braIzqDecArr(p):
    'braIzqDecArr : BRAIZQ'
    
    # Inicializar R
    global R
    R = 1
    
    # Extraer scope actual
    scope = stkScope.pop()
    stkScope.append(scope)
    
    # Extraer el nombre de la variable
    arrNombre = stkArrs.pop()
    stkArrs.append(arrNombre)
    
    # Extraer la función
    func = directoriofs.get(scope)
    
    # Indicar que es de tipo arreglo
    func.tabla.setAsArray(arrNombre)
#--------------------------------------------------------------------#
# p_mandaConst()
#   Regla gramatical para detectar una constante ENT en la diensión
#   1 del arreglo.
#
#   Solo manda el valor de la constante a la regla braDerDecArr
#--------------------------------------------------------------------#
def p_mandaConst(p):
    'mandaConst : C_ENT'
    
    # Mandar constante
    stkOperandos.append(p[1])
#--------------------------------------------------------------------#
# p_braDerDecArr()
#   Regla gramatical para detectar el token BRADER en la declaración
#   de variables.
#
#   - DV5: Generar nodo y re/calcular R.
#   - DV6: Insertar nodo en la variable del scope correspondiente.
#--------------------------------------------------------------------#
def p_braDerDecArr(p):
    'braDerDecArr : BRADER'
    
    # Extraer el nombre de la variable
    arrNombre = stkArrs.pop()
    stkArrs.append(arrNombre)
    
    # Extraer el tamaño de la dimensión
    tamDimension = stkOperandos.pop()
    
    # Generar nodo
    nodo = []
    nodo.append(tamDimension)
    
    # Recalculo R
    global R
    R = R * (tamDimension + 1)
    
    # Extraer scope actual
    scope = stkScope.pop()
    stkScope.append(scope)
    
    # Extraer la función
    func = directoriofs.get(scope)
    
    # Insertar nodo en el stack de la variable
    func.tabla.addNodeToVar(arrNombre, nodo)

# FUNCION
#--------------------------------------------------------------------#
# p_func1()
#   Regla gramatical para una declaración de función.
#   
#   - Valida que la función cuente con retornos si se declaró con 
#     tipo de retorno.
#   - Actualiza los contadores de variables locales y de temporales.
#   - Genera cuádruplo 'endfunc'.
#   - Reinicia los índices locales y temporales.
#--------------------------------------------------------------------#
def p_func1(p):
    'func : tipoFunc PAREIZQ params PAREDER cuerpoFunc PUCOMA'

    # Obtener la función del directorio de funciones
    funcName = stkScope.pop()
    myFunc = directoriofs.get(funcName)

    # Verificar que, si la función no es de tipo 'vacío', cuente con uno o varios 'return' 
    if myFunc.tipo != 'vacio':
        if myFunc.returnCount <= 0:
            llamaError.funcionSinRetorno(myFunc.tipo, funcName)

    global indicesLoc
    global indicesTemp

    # Actualizar contador de locales y temporales necesarios de la función
    myFunc.updateTemps(indicesTemp)
    myFunc.updateVars(indicesLoc, 10000)

    # Generar cuádruplo ENDFUNC
    generaCuadruplo('endfunc', '', '', '')

    # Reiniciar los indices LOCALES y TEMPORALES
    indicesLoc = [10000, 13000, 16000]
    indicesTemp = [19000, 22000, 25000, 28000, 31000]

#--------------------------------------------------------------------#
# p_tipoFunc()
#   Regla gramatical para los tipos de funciones
#   
#   - Registra una función en el directorio de funciones 
#   - Registra su respectiva variable global si la función regresa un
#   valor.
# Resultado:
#   - Nueva función registrada en el directorio de funciones.
#   - Variable de función añadida a la tabla de variables globales.
#--------------------------------------------------------------------#
def p_tipoFunc(p):
    '''
    tipoFunc    : tipo ID
                | VACIO ID
    '''

    # Creación de tabla de variables de una función
    tabla = TablaVars({})

    # Extraer tipo y nombre de la función
    tipo = p[1]
    nombre = p[2]

    # Inicializar la dirección destino de la variable global de la función
    dirDestino = -1

    # Generar variable global de la función si su tipo no es 'vacio'
    if tipo != 'vacio':

        # Determinar el índice a utilizar indicesGlob[ENT, FLOT, CAR]
        if tipo == 'ent':
            indice = 0
        elif tipo == 'flot':
            indice = 1
        else:
            indice = 2

        # Revisar si excedimos el límite de globales
        excedimosGlobales(tipo, indice)

        # Extraer la dirección destino de su var global 
        # para almacenarla en la función
        dirDestino = indicesGlob[indice]

        # Crear variable global
        variable = Variable(tipo, nombre, indicesGlob[indice])
        
        # Actualizar dirección del índice de variables GLOBALES por su tipo
        indicesGlob[indice] = indicesGlob[indice] + 1

        # Buscar función Global y agregar var a su tabla de vars
        directoriofs.get('Global').tabla.add(variable)

    # Creación de la función
    fun = Funcion(nombre, tipo, indiCuad, dirDestino, tabla)

    # Añadir función al directorio (busca si la función ya existe y levanta un error)
    directoriofs.add(fun)

    # Añadir a la pila la función en la que se está trabajando
    stkScope.append(p[2])

# CUERPO FUNCIÓN
def p_cuerpoFunc1(p):
    'cuerpoFunc : LLAIZQ cuerpoFunc2 LLADER'

def p_cuerpoFunc2(p):
    '''
    cuerpoFunc2 : dec_vars cuerpoFunc2
                | cuerpoFunc3
    '''

def p_cuerpoFunc3(p):
    '''
    cuerpoFunc3 : estatuto cuerpoFunc3
                | fin
    '''

# CUERPO
def p_cuerpo1(p):
    'cuerpo : LLAIZQ cuerpo2 LLADER'

def p_cuerpo2(p):
    '''
    cuerpo2 : estatuto cuerpo2
            | fin
    '''

# TIPO
def p_tipo1(p):
    '''
    tipo    : ENT
            | FLOT
            | CAR
    '''
    # Regresar tipo
    p[0] = p[1]

# PARAMS
def p_params1(p):
    '''
    params  : params2
            | fin
    '''
def p_params2(p):
    '''
    params2  : parametro params3
    '''
def p_params3(p):
    '''
    params3 : COMA params2
            | fin
    '''
#--------------------------------------------------------------------#
# p_registroParam()
#   Regla gramatical para parámetros
#   
#   - Registra un prámetro a la tabla de variables de su respectiva función
#   - Actualiza la firma de la función en cuestión.
# Resultado:
#   - Nueva variable en la tabla de variables de la función en cuestión
#   - Firma de la función en cuestión actualizada
#--------------------------------------------------------------------#
def p_registroParam(p):
    'parametro : tipo ID'

    tipoParam = p[1]
    paramID = p[2]

    # Añadir parámetro a la tabla de variables de la función
    addToVarsTab(tipoParam, paramID)
    
    # Actualizar firma de la función
    nombreFunc = stkScope.pop()
    stkScope.append(nombreFunc)

    # Extraer la dirección del parámetro para añadirlo a la firma de la func.
    dirParam = directoriofs.get(nombreFunc).tabla.get(paramID).dir

    # Agregar tipo de dato a la firma de la función
    directoriofs.get(nombreFunc).addParam([tipoParam, dirParam])
    
# ESTATUTO
def p_estatuto1(p):
    'estatuto : estatuto2 PUCOMA'

def p_estatuto2(p):
    '''
    estatuto2   : asignacion
                | regresa
                | llamadaEstat
                | lectura
                | escribir
                | condicion
                | mientras
                | func_esp_s
                | func_esp_c
    '''

# ASIGNACION
#--------------------------------------------------------------------#
# p_asignacion1()
#   Regla gramatical para una asignación.
#   
#   - Valida si hay un '=' en la pila de operadores.
#   - Genera cuádruplo de asignación.
#--------------------------------------------------------------------#
def p_asignacion1(p):
    'asignacion : variable igual expresion_a'

    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un =
            if op == '=':
                # Extraer el operando der con su tipo
                operando_Der = stkOperandos.pop()
                tipo_Der = stkTipos.pop()
                
                # Extraer el operando izq con su tipo
                operando_Izq = stkOperandos.pop()
                tipo_Izq = stkTipos.pop()

                # Revisar si la operación no causa errores y obtener el tipo resultante
                tipoResultado = cuboS.match(tipo_Izq, tipo_Der, op)

                # Verificar si hay un error de tipo
                if tipoResultado == "ERROR":
                    llamaError.tiposIncompatibles(cuboS.traducción[op], tipo_Izq, tipo_Der)
                else: # Si no hay error
                    # Generar cuadruplo
                    generaCuadruplo(op, operando_Der, '', operando_Izq)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else: # En caso de tener fondo falso, lo regresamos a la pila
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_igual()
#   Regla gramatical para detectar un operador '='.
#   
#   - Inserta el operador en el stack de operadores
#--------------------------------------------------------------------#
def p_igual(p):
    'igual : IGUAL'
    stkOperadores.append(p[1])

# REGRESA
#--------------------------------------------------------------------#
# p_regresa()
#   Regla gramatical para el estatuto regresa.
#   
#   - Valida que el resultado de la expresión del retorno sea del mismo
#     tipo que la función.
#   - Genera el cuádruplo 'regresa' con el resultado de la expresión.
#--------------------------------------------------------------------#
def p_regresa(p):
    'regresa : registraRegresa PAREIZQ expresion_a PAREDER'
    # Retirar el nombre de la función
    currFunc = stkScope.pop()
    stkScope.append(currFunc)

    # Obtener la función del directorio de funciones
    func = directoriofs.get(currFunc)
    
    # Extraer el operando de la pila con su tipo
    operandoReturn = stkOperandos.pop()
    tipoReturn = stkTipos.pop()

    # Verificar que la función sí debe de regresar un valor del mismo tipo
    func.matchTipoRegresa(tipoReturn)

    # Generar cuadruplo
    generaCuadruplo('regresa', '', '', operandoReturn)

#--------------------------------------------------------------------#
# p_registraRegresa()
#   Regla gramatical para el token REGRESA.
#   
#   - Valida que la función tiene valor de retorno.
#   - Actualiza el contador de retornos.
#--------------------------------------------------------------------#
def p_registraRegresa(p):
    'registraRegresa : REGRESA'
    # Retirar el nombre de la función
    currFunc = stkScope.pop()
    stkScope.append(currFunc)

    # Obtener la función del directorio de funciones
    func = directoriofs.get(currFunc)

    # Validar que la función debe de tener valor de retorno
    if func.tipo == 'vacio':
        llamaError.funcionVacioConRetorno(func.tipo, func.nombre)

    # Actualizar contador de retornos de la función
    func.addReturn()

# LEER
#--------------------------------------------------------------------#
# p_lectura1()
#   Regla gramatical para el estatuto 'leer'.
#   
#   - Valida si hay un 'leer' en la pila de operadores.
#   - Genera cuádruplo de lectura.
#--------------------------------------------------------------------#
def p_lectura1(p):
    'lectura : leer PAREIZQ variable PAREDER'

    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, extraer el operador a revisar
        op = stkOperadores.pop()

        # Revisar si el operador extraído es un 'leer'
        if op == 'leer':
            # Extraer el operando con su tipo
            operando = stkOperandos.pop()
            stkTipos.pop()

            # Generar cuadruplo
            generaCuadruplo(op, '', '', operando)

#--------------------------------------------------------------------#
# p_leer()
#   Regla gramatical para el token 'LEER'.
#   
#   - Validar si sigue un operador de lectura.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_leer(p):
    'leer : LEER'
    stkOperadores.append(p[1])

# ESCRIBIR
#--------------------------------------------------------------------#
# p_escribir1()
#   Regla gramatical para el estatuto 'escrib'.
#   
#   - Valida si hay un 'escrib' en la pila de operadores.
#   - Genera cuádruplo de escritura.
#--------------------------------------------------------------------#
def p_escribir1(p):
    'escribir : escrib PAREIZQ escribir2 PAREDER'

    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, extraer el operador a revisar
        op = stkOperadores.pop()

        # Revisar si el operador extraído es un =
        if op == 'escrib':
            # Extraer el operando con su tipo
            operando = stkOperandos.pop()
            stkTipos.pop()

            # Generar cuadruplo
            generaCuadruplo(op, '', '', operando)

def p_escribir2(p):
    '''
    escribir2   : expresion_a
                | cadena
    '''

#--------------------------------------------------------------------#
# p_escrib()
#   Regla gramatical para el token 'ESCRIB'.
#   
#   - Validar si sigue un operador de escritura.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_escrib(p):
    'escrib : ESCRIB'
    stkOperadores.append(p[1])

# CONDICION
def p_condicion1(p):
    'condicion : SI PAREIZQ expresion_a pareDerIfWhile cuerpo condicion2'

def p_condicion2(p):
    '''
    condicion2  : condicion3
                | condicion4
    '''

def p_condicion3(p):
    'condicion3  : otro cuerpo condicion4'

#--------------------------------------------------------------------#
# p_condicion4()
#   Regla gramatical para finalizar un estatuto condicional.
#   
#   - Obtener el salto al cuádruplo a actualizar de la pila de saltos.
#   - Actualizar cuádrplo al indice actual.
#--------------------------------------------------------------------#
def p_condicion4(p):
    'condicion4 : fin'
    # Obtener el cuadruplo a modificar
    salto = stkSaltos.pop()

    # Actualizar cuadruplo con el salto al indice actual
    misCuadruplos.addSalto(str(salto), indiCuad)

#--------------------------------------------------------------------#
# p_pareDerIfWhile()
#   Regla gramatical para detectar el paréntesis derecho de un
#   estatuto condicional o cíclico.
#   
#   - Valida que el resultado de la expresión sea de tipo BOOL.
#   - Insertar índice a la pila de saltos
#   - Generar cúadruplo 'gotoF'.
#--------------------------------------------------------------------#
def p_pareDerIfWhile(p):
    'pareDerIfWhile : PAREDER'

    # Extraer operando y su tipo (resultado de la expresión entre paréntesis) 
    expresion = stkOperandos.pop() # Dirección de temporal
    tipo_exp = stkTipos.pop()
    
    # Verificar que sea de tipo bool y desplegar error de no serlo
    if tipo_exp != "bool":
        llamaError.expresionIncompatible(tipo_exp)

    global indiCuad

    # Añadir índice del cuadruplo a la pila de saltos
    stkSaltos.append(indiCuad)
    
    # Generar cuadruplo
    generaCuadruplo('gotoF', expresion, '', 'pendiente')

#--------------------------------------------------------------------#
# p_otro()
#   Regla gramatical para el token OTRO.
#   
#   - Actualiza el salto del cuádruplo 'gotoF'.
#   - Añadir índice actual a la pila de saltos.
#   - Generar cuádruplo 'goto'.
#--------------------------------------------------------------------#
def p_otro(p):
    'otro : OTRO'
    global indiCuad

    # Obtener el cuadruplo a actualizar
    salto = stkSaltos.pop()

    # Actualizar cuadruplo con el salto al indice actual
    misCuadruplos.addSalto(str(salto), indiCuad + 1)

    # Añadir índice del cuadruplo a la pila de saltos
    stkSaltos.append(indiCuad)

    # Generar cuadruplo
    generaCuadruplo('goto', '', '', 'pendiente')

# MIENTRAS
#--------------------------------------------------------------------#
# p_mientras1()
#   Regla gramatical para el estatuto 'mientras'.
#   
#   - Extraer salto para el 'gotoF'.
#   - Extraer salto para el 'goto'.
#   - Generar cuádruplo 'goto'.
#   - Actualizar cuádruplo 'gotoF'.
#--------------------------------------------------------------------#
def p_mientras1(p):
    'mientras : mientrasTkn PAREIZQ expresion_a pareDerIfWhile cuerpo'

    # Extraer los saltos de la pila de saltos
    gotoFalso = stkSaltos.pop()
    retorno = stkSaltos.pop()

    # Generar cuadruplo goto para el retorno
    generaCuadruplo('goto', '', '', retorno)

    # Actualizar cuadruplo gotoF
    misCuadruplos.addSalto(str(gotoFalso), indiCuad)

#--------------------------------------------------------------------#
# p_mientras()
#   Regla gramatical para el token 'MIENTRAS'.
#   
#   - Inserta el índice actual al stack de saltos (lugar previo a la 
#     evaluación de la expresión).
#--------------------------------------------------------------------#
def p_mientras(p):
    'mientrasTkn : MIENTRAS'
    global indiCuad
    stkSaltos.append(indiCuad) 

# LLAMADA
#--------------------------------------------------------------------#
# p_llamada1()
#   Regla gramatical para una llamada a función.
#   
#   - Regresar el ID del nombre de la función para próximas
#     verificaciones semánticas.
#--------------------------------------------------------------------#
def p_llamada1(p):
    'llamada : idFunc pareIzqLlamada llamada2 pareDerLlamada'

    #  para las verificaciones semánticas
    p[0] = p[1]

def p_llamada2(p):
    '''
    llamada2    : llamada3
                | fin
    '''

def p_llamada3(p):
    '''
    llamada3    : paramExpr llamada4
    '''

def p_llamada4(p):
    '''
    llamada4    : comaLlamada paramExpr llamada4
                | fin
    '''

#--------------------------------------------------------------------#
# p_llamadaEstat()
#   Regla gramatical para detectar una llamada de un estatuto.
#   
#   - Valida que la función NO debe retornar un valor.
#   - De lo contrario despliega un error.
#--------------------------------------------------------------------#
def p_llamadaEstat(p):
    'llamadaEstat : llamada'

    # Obtener el nombre de la función
    nombreFunc = p[1]

    # Extraer la función
    func = directoriofs.get(nombreFunc)
    
    # Extraer el tipo de la función
    tipoFunc = func.tipo

    # Validar si es vacío
    if tipoFunc != 'vacio':
        llamaError.LlamadaFuncConRetornoEnExpr(nombreFunc, tipoFunc);

#--------------------------------------------------------------------#
# p_llamadaExp()
#   Regla gramatical para detectar una llamada de una expresión.
#   
#   - Valida que la función debe retornar un valor.
#   - De lo contrario despliega un error.
#--------------------------------------------------------------------#
def p_llamadaExp(p):
    'llamadaExp : llamada'

    # Obtener el nombre de la función
    nombreFunc = p[1]

    # Extraer la función
    func = directoriofs.get(nombreFunc)
    
    # Extraer el tipo de la función
    tipoFunc = func.tipo

    # Validar si es distinto de vacío
    if tipoFunc == 'vacio':
        llamaError.LlamadaFuncSinRetornoEnExpr(nombreFunc, tipoFunc);

#--------------------------------------------------------------------#
# p_idFunc()
#   Regla gramatical para detectar el ID de una función en una llamada.
#   
#   - Valida que la función existe en el directorio de funciones.
#   - Inserta el ID de la llamada al stack de llamadas.
# Resultado:
#   - La variable queda registrada en su respectiva función.
#--------------------------------------------------------------------#
def p_idFunc(p):
    'idFunc : ID'
    id = p[1]
    
    # Verificar que la función existe
    directoriofs.get(id)

    # Enviar el nombre de la función para crear cuadruplo 'ERA'
    stkLlamadas.append(id)

    # Regresar el ID de la llamada
    p[0] = id

#--------------------------------------------------------------------#
# p_pareIzqLlamada()
#   Regla gramatical para detectar el paréntesis izq. de una llamada.
#   
#   - Genera el cuádruplo ERA.
#   - Inicializar indexador de firma.
#   - Valida si la función de la llamada tiene parámetros e inserta un FF.
#--------------------------------------------------------------------#
def p_pareIzqLlamada(p):
    'pareIzqLlamada : PAREIZQ'

    # Extraer el nombre de la función para generar cuadruplo ERA
    nombreFunc = stkLlamadas.pop()
    stkLlamadas.append(nombreFunc)

    # Generar cuadruplo
    generaCuadruplo('era', nombreFunc, '', '')

    # Re/Inicializar indice K (Se usa para indexar la firma de la función)
    global paramCont
    paramCont = 0

    # Verificar si la función tiene params. para añadir un fondo falso
    firma = directoriofs.get(nombreFunc).firma

    # Si la firma no está vacía
    if firma:
        # Insertar fondo falso para la próxima expresión
        stkOperadores.append('_FF')

#--------------------------------------------------------------------#
# p_paramExpr()
#   Regla gramatical para detectar una expresión como parámetro.
#   
#   - Valida el resultado del argumento con el índice K en la firma.
#   - Genera cuádruplo de parámetro con la diección del argumento 
#     y la dir del parámetro.
#--------------------------------------------------------------------#
def p_paramExpr(p):
    'paramExpr : expresion_a'

    global paramCont
    
    # Retirar fondo falso para el resto de la expresión
    stkOperadores.pop()

    # Extraer resultado del parámetro y su tipo
    dirArgumento = stkOperandos.pop()
    tipoArg = stkTipos.pop()

    # Extraer el nombre de la función para obtenerla del directorio de funciones
    nombreFunc = stkLlamadas.pop()
    stkLlamadas.append(nombreFunc)

    # Extraer la función del directorio de funciones
    funcion = directoriofs.get(nombreFunc)

    # Mandar el argumento a verificar con el respectivo índice o # de arg
    funcion.checkFirma(nombreFunc, tipoArg, paramCont)

    # Obtener la dirección de memoria del parámetro
    dirParam = funcion.getDirParam(paramCont)

    # Generar cuadruplo
    generaCuadruplo('param', dirArgumento, '', dirParam)

#--------------------------------------------------------------------#
# p_comaLlamada()
#   Regla gramatical para detectar una coma en los parámetros de una
#   llamada.
#   
#   - Actualiza el índice K.
#   - Inserta un FF para evaluar la siguiente expresión.
#--------------------------------------------------------------------#
def p_comaLlamada(p):
    'comaLlamada : COMA'
    global paramCont

    paramCont = paramCont + 1
    stkOperadores.append('_FF')

#--------------------------------------------------------------------#
# p_pareDerLlamada()
#   Regla gramatical para detectar el paréntesis der. de una llamada.
#   
#   - Verifica la congruencia del número de argumentos.
#   - Genera cuádruplo 'GoSub'.
#   - Valida si la función tiene retornos.
#   - Genera cuádruplo de asignación de la variable global de la
#     función a una temporal.
#   - Mete el temporal al stack de operandos y su tipo al stack de
#     tipos.
#--------------------------------------------------------------------#
def p_pareDerLlamada(p):
    'pareDerLlamada : PAREDER'

    global indiCuad
    global paramCont

    # Extraer el nombre de la función para obtenerla del directorio de funciones
    nombreFunc = stkLlamadas.pop()
    
    # Mandar a verificar congruencia de # de argumentos
    func = directoriofs.get(nombreFunc)
    func.matchFirma(nombreFunc, paramCont)

    # Generar cuadruplo gosub
    generaCuadruplo('gosub', nombreFunc, '', '')

    # Revisar si esta llamada cuenta con uno o más retornos
    if func.tieneRetornos():
        global indicesTemp

        # Extraer el tipo de resultado dado el tipo de la función
        tipoResultado = func.tipo

        # Determinar el índice a utilizar indicesTemp[ENT, FLOT, CAR, BOOL, PNTR]
        if tipoResultado == 'ent':
            indice = 0
        elif tipoResultado == 'flot':
            indice = 1
        elif tipoResultado == 'car':
            indice = 2
        elif tipoResultado == 'bool':
            indice = 3
        else:
            indice = 4
        
        # Obtener dirección del temporal para el resultado
        dirDestino = indicesTemp[indice] 
    
        # Extraer la función global
        globl = directoriofs.get('Global')

        # Extraer la dirección de la variable de la función
        dirVarFunc = globl.tabla.get(nombreFunc).dir

        # Generar cuadruplo
        generaCuadruplo('=', dirVarFunc, '', dirDestino)

        # Actualizar índices
        indicesTemp[indice] = indicesTemp[indice] + 1

        # Insertamos el resultado en la pila de operandos y de tipos
        stkOperandos.append(dirDestino)
        stkTipos.append(tipoResultado)

# FUNCION ESPECIAL SIMPLE
def p_func_esp_s1(p):
    '''
    func_esp_s  : medida_posicion
                | medida_variabilidad
                | puntos_muestrales
                | distribuciones
    '''

# MEDIDAS DE POSICION
def p_medida_posicion1(p):
    '''
    medida_posicion : media
                    | mediana
                    | moda
    '''

# MEDIA
def p_media1(p):
    'media : MEDIA PAREIZQ ID PAREDER'

# MEDIANA
def p_mediana1(p):
    'mediana : MEDIANA PAREIZQ ID PAREDER'

# MODA
def p_moda1(p):
    'moda : MODA PAREIZQ ID PAREDER'

# MEDIDAS DE VARIABILIDAD
def p_medida_variabilidad1(p):
    '''medida_variabilidad  : varianza
                            | desestandar
                            | rango
    '''

# VARIANZA
def p_varianza1(p):
    'varianza : VARIANZA PAREIZQ ID PAREDER'

# DESESTANDAR
def p_desestandar1(p):
    'desestandar : DESESTANDAR PAREIZQ ID PAREDER'

# RANGO
def p_rango1(p):
    'rango : RANGO PAREIZQ ID PAREDER'

# PUNTOS MUESTRALES
def p_puntos_muestrales1(p):
    '''
    puntos_muestrales   : reglamulti
                        | combins
                        | permuts
    '''

# REGLA DE LA MULTIPLICACION
def p_reglamulti1(p):
    'reglamulti  : REGLAMULTI PAREIZQ expresion_a reglamulti2 PAREDER'

def p_reglamulti2(p):
    '''
    reglamulti2 : COMA expresion_a reglamulti2
                | fin
    '''

# COMBINACIONES
def p_combins1(p):
    'combins : COMBINS PAREIZQ expresion_a COMA expresion_a PAREDER'

# PERMUTACIONES
def p_permuts1(p):
    'permuts : PERMUTS PAREIZQ expresion_a COMA expresion_a PAREDER'

# DISTRIBUCIONES
def p_distribuciones1(p):
    '''
    distribuciones  : dstbinom
                    | dstbinomneg
                    | dstgeom
                    | dsthipgeom
                    | dstpoisson
    '''

# DISTRIBUCION BINOMIAL
def p_dstbinom1(p):
    'dstbinom : DSTBINOM PAREIZQ dstbinom2 PAREDER'

def p_dstbinom2(p):
    'dstbinom2 : expresion_a COMA expresion_a COMA expresion_a COMA expresion_a'

# DISTRIBUCION BINOMIAL NEGATIVA
def p_dstbinomneg1(p):
    'dstbinomneg : DSTBINOMNEG PAREIZQ dstbinomneg2 PAREDER'

def p_dstbinomneg2(p):
    'dstbinomneg2 : expresion_a COMA expresion_a COMA expresion_a COMA expresion_a'

# DISTRIBUCION GEOMETRICA
def p_dstgeom1(p):
    'dstgeom : DSTGEOM PAREIZQ dstgeom2 PAREDER'

def p_dstgeom2(p):
    'dstgeom2 : expresion_a COMA expresion_a COMA expresion_a'

# DISTRIBUCION HIPERGEOMETRICA
def p_dsthipgeom1(p):
    'dsthipgeom : DSTHIPGEOM PAREIZQ dsthipgeom2 PAREDER'

def p_dsthipgeom2(p):
    'dsthipgeom2 : expresion_a COMA expresion_a COMA expresion_a COMA expresion_a COMA expresion_a'

# POISSON
def p_dstpoisson1(p):
    'dstpoisson : DSTPOISSON PAREIZQ dstpoisson2 PAREDER'

def p_dstpoisson2(p):
    'dstpoisson2 : expresion_a COMA expresion_a COMA expresion_a'

# FUNNCION ESPECIAL COMPLEJA
def p_func_esp_c1(p):
    'func_esp_c : valores_graficos'

# VALORES GRAFICOS
def p_valores_graficos1(p):
    '''
    valores_graficos    : histograma
                        | grafcaja
    '''

# HISTOGRAMA
def p_histograma1(p):
    'histograma : HISTOGRAMA PAREIZQ ID PAREDER'

# GRAFICA DE CAJA
def p_grafcaja1(p):
    'grafcaja : GRAFCAJA PAREIZQ ID PAREDER'

# EXPRESION A
def p_expresion_a1(p):
    'expresion_a : expresion_b revisaO expresion_a2'

def p_expresion_a2(p):
    '''
    expresion_a2    : o expresion_a
                    | fin
    '''

#--------------------------------------------------------------------#
# p_revisaO()
#   Regla gramatical para revisión de la pila de operadores.
#   
#   - Valida si hay un '||' en la pila de operadores.
#   - Genera cuádruplo de de comparación lógica.
#   - Añade el temporal resultado en la pila de operandos.
#--------------------------------------------------------------------#
def p_revisaO(p):
    'revisaO : fin'
    
    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un ||
            if op == '||':
                generaCuadOperacionBinaria(op)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else:
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_o()
#   Regla gramatical para el token '||'.
#   
#   - Valida si sigue un operador de comparación 'or'.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_o(p):
    'o : O'
    stkOperadores.append(p[1])

# EXPRESION B
def p_expresion_b1(p):
    'expresion_b : expresion_c revisaY expresion_b2'

def p_expresion_b2(p):
    '''
    expresion_b2    : y expresion_b
                    | fin
    '''

#--------------------------------------------------------------------#
# p_revisaY()
#   Regla gramatical para revisión de la pila de operadores.
#   
#   - Valida si hay un '&&' en la pila de operadores.
#   - Genera cuádruplo de de comparación lógica.
#   - Añade el temporal resultado en la pila de operandos.
#--------------------------------------------------------------------#
def p_revisaY(p):
    'revisaY : fin'
        
    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un &&
            if op == '&&':
                generaCuadOperacionBinaria(op)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else: # En caso de tener fondo falso, lo regresamos a la pila
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_y()
#   Regla gramatical para el token '&&'.
#   
#   - Valida si sigue un operador de comparación 'and'.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_y(p):
    'y : Y'
    stkOperadores.append(p[1])

# EXPRESION C
def p_expresion_c1(p):
    '''
    expresion_c : expresion_d revisaMaMeIgDif
                | expresion_d revisaMaMeIgDif compara expresion_d revisaMaMeIgDif
    '''

#--------------------------------------------------------------------#
# p_revisaMaMeIgDif()
#   Regla gramatical para revisión de la pila de operadores.
#   
#   - Valida si hay un '>', '<', '==' o '!=' en la pila de operadores.
#   - Genera cuádruplo de de comparación aritmética.
#   - Añade el temporal resultado en la pila de operandos.
#--------------------------------------------------------------------#
def p_revisaMaMeIgDif(p):
    'revisaMaMeIgDif : fin'

    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un >, <, == o !=
            if op == '>' or op == '<' or op == '==' or op == '!=':
                generaCuadOperacionBinaria(op)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else: # En caso de tener fondo falso, lo regresamos a la pila
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_compara()
#   Regla gramatical para los tokens de '>', '<', '==' o '!='.
#   
#   - Valida si sigue un operador de comparación aritmética.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_compara(p):
    '''
    compara : MAYOR
            | MENOR
            | IGUALQ
            | DIFF
    '''
    stkOperadores.append(p[1])

# EXPRESION D
def p_expresion_d1(p):
    'expresion_d : expresion_e revisaMasMen expresion_d2'

def p_expresion_d2(p):
    '''
    expresion_d2    : masmenos expresion_d
                    | fin
    '''

#--------------------------------------------------------------------#
# p_revisaMasMen()
#   Regla gramatical para revisión de la pila de operadores.
#   
#   - Valida si hay un '+' o '-' en la pila de operadores.
#   - Genera cuádruplo de suma o resta.
#   - Añade el temporal resultado en la pila de operandos.
#--------------------------------------------------------------------#
def p_revisaMasMen(p):
    'revisaMasMen : fin'
    
    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un '+' o '-'
            if op == '+' or op == '-':
                generaCuadOperacionBinaria(op)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else: # En caso de tener fondo falso, lo regresamos a la pila
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_masmenos()
#   Regla gramatical para los tokens de '+' o '-'.
#   
#   - Valida si sigue un operador de suma o resta.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_masmenos(p):
    '''masmenos : MAS
                | MENOS
    '''
    if p[1] == '+' or p[1] == '-':
        stkOperadores.append(p[1])

# EXPRESION E
def p_expresion_e1(p):
    'expresion_e : expresion_f revisaPorDiv expresion_e2'

def p_expresion_e2(p):
    '''
    expresion_e2    : pordiv expresion_e
                    | fin
    '''

#--------------------------------------------------------------------#
# p_revisaPorDiv()
#   Regla gramatical para revisión de la pila de operadores.
#   
#   - Valida si hay un '*' o '/' en la pila de operadores.
#   - Genera cuádruplo de multiplicación o división.
#   - Añade el temporal resultado en la pila de operandos.
#--------------------------------------------------------------------#
def p_revisaPorDiv(p):
    'revisaPorDiv : fin'
    
    # Verificar que el stack no está vacío
    if stkOperadores:
        # Si no está vacío, revisar si no tiene fondo falso
        ff = stkOperadores.pop()
        if ff != '_FF':
            # Si no tiene fondo falso, extraer el operador a revisar
            op = ff

            # Revisar si el operador extraído es un '*' o '/'
            if op == '*' or op == '/':
                generaCuadOperacionBinaria(op)
            else: # De no serlo...
                # Regresar el operador a la pila
                stkOperadores.append(op)
        else: # En caso de tener fondo falso, lo regresamos a la pila
            stkOperadores.append(ff)

#--------------------------------------------------------------------#
# p_pordiv()
#   Regla gramatical para los tokens de '*' o '/'.
#   
#   - Valida si sigue un operador de multiplicación o división.
#   - Inserta el operador en la pila de operadores.
#--------------------------------------------------------------------#
def p_pordiv(p):
    '''pordiv   : POR
                | DIV
    '''
    if p[1] == '*' or p[1] == '/':
        stkOperadores.append(p[1])

# EXPRESION F
def p_expresion_f1(p):
    '''
    expresion_f : pareIzqEx expresion_a pareDerEx
                | c_ent
                | c_flot
                | c_car
                | cadena
                | variable
                | llamadaExp
                | func_esp_s
    '''
#--------------------------------------------------------------------#
# p_pareIzqEx()
#   Regla gramatical para detectar un paréntesis izq de una expresión.
#   
#   - Inserta un fondo falso en el stack de operadores.
#--------------------------------------------------------------------#
def p_pareIzqEx(p):
    'pareIzqEx : PAREIZQ'    
    stkOperadores.append('_FF')

#--------------------------------------------------------------------#
# p_pareDerEx()
#   Regla gramatical para detectar un paréntesis izq de una expresión.
#   
#   - Retira el fondo falso del stack de operadores.
#--------------------------------------------------------------------#
def p_pareDerEx(p):
    'pareDerEx : PAREDER'
    stkOperadores.pop()

#--------------------------------------------------------------------#
# p_c_ent()
#   Regla gramatical para detectar una constante entera.
#   
#   - Inserta una constante 'ent' al stack de operandos.
#--------------------------------------------------------------------#
def p_c_ent(p):
    'c_ent : C_ENT'
    appendConst('ent', p[1])

#--------------------------------------------------------------------#
# p_c_flot()
#   Regla gramatical para detectar una constante flotante.
#   
#   - Inserta una constante 'flot' al stack de operandos.
#--------------------------------------------------------------------#
def p_c_flot(p):
    'c_flot : C_FLOT'
    appendConst('flot', p[1])

#--------------------------------------------------------------------#
# p_c_car()
#   Regla gramatical para detectar una constante entera.
#   
#   - Inserta una constante 'car' al stack de operandos.
#--------------------------------------------------------------------#
def p_c_car(p):
    'c_car : C_CAR'
    appendConst('car', p[1])

#--------------------------------------------------------------------#
# p_cadena()
#   Regla gramatical para detectar una constante entera.
#   
#   - Inserta una constante 'cadena' al stack de operandos.
#--------------------------------------------------------------------#
def p_cadena(p):
    'cadena : CADENA'
    appendConst('cadena', p[1])

# VACIO
def p_fin(p):
    'fin :'
    p[0] = 'fin'

# ----------------------------------------------------------- FIN GRAMÁTICAS -----------------------------------------------------------

# ----------------------------------------------------- INICIO FUNCIONES DE APOYO ------------------------------------------------------

#--------------------------------------------------------------------#
# generaCuadruplo()
#   Función para generar un cuádruplo general.
# Parámetros:
#   operador: String con el operador del cuadruplo.
#   operandoIzq: String con un operando de contenido
#   (no necesariamente una dirección).
# 
#   operandoDer: String con un operando de contenido
#   (no necesariamente una dirección).
# 
#   destino: dirección destino de memoria
#   (no necesariamente es una dirección).
# Resultado:
#   Cuadruplo generado y añadido en la lista de cuádruplos
#--------------------------------------------------------------------#
def generaCuadruplo(operador, operandoIzq, operandoDer, destino):
    global indiCuad

    # Generar cuadruplo
    cuadru = Cuadruplo(str(indiCuad), operador, operandoIzq, operandoDer, destino)

    # Actualizar índice
    indiCuad = indiCuad + 1

    # Insertar cuadruplo a su estructura
    misCuadruplos.add(cuadru)

#--------------------------------------------------------------------#
# generaCuadOperacionBinaria()
#   Función para generar un cuádruplo de operación binaria.
# Parámetros:
#   op: String con el operador del cuadruplo.
# Resultado:
#   Cuadruplo generado y añadido en la lista de cuádruplos
#--------------------------------------------------------------------#
def generaCuadOperacionBinaria(op):
    # Extraer el operando der con su tipo
    operando_Der = stkOperandos.pop()
    tipo_Der = stkTipos.pop()
    
    # Extraer el operando izq con su tipo
    operando_Izq = stkOperandos.pop()
    tipo_Izq = stkTipos.pop()

    # Revisar si la operación no causa errores y obtener el tipo resultante
    tipoResultado = cuboS.match(tipo_Izq, tipo_Der, op)

    # Verificar si hay un error de tipo
    if tipoResultado == "ERROR":
        llamaError.tiposIncompatibles(cuboS.traducción[op], tipo_Izq, tipo_Der)
    else: # Si no hay error

        # Especificar el uso de índices Temporales
        global indicesTemp

        # Determinar el índice a utilizar indicesTemp[ENT, FLOT, CAR, BOOL, PNTR]
        if tipoResultado == 'ent':
            indice = 0
        elif tipoResultado == 'flot':
            indice = 1
        elif tipoResultado == 'car':
            indice = 2
        elif tipoResultado == 'bool':
            indice = 3
        else:
            indice = 4

        # Asignar temporal de resultado
        dirTemp = indicesTemp[indice] 

        # Generar cuadruplo
        generaCuadruplo(op, operando_Izq, operando_Der, dirTemp)

        # Actualizar índices
        indicesTemp[indice] = indicesTemp[indice] + 1

        # Insertamos el resultado en la pila de operandos y de tipos
        stkOperandos.append(dirTemp)
        stkTipos.append(tipoResultado)

#--------------------------------------------------------------------#
# excedimosGlobales()
#   Función validar que los indices GLOBALES no excedan los límites.
# Parámetros:
#   tipo: String con el tipo de variable que puede estar en exceso
#   (su función principal es ser un dato para la generación del error).
#   
#   indice: Indica la indexación a validar.
#--------------------------------------------------------------------#
def excedimosGlobales(tipo, indice):
    if indice == 0 and indicesGlob[indice] > 3999:
        llamaError.excesoGlobales(tipo)
    elif indice == 1 and indicesGlob[indice] > 6999:
        llamaError.excesoGlobales(tipo)
    elif indice == 2 and indicesGlob[indice] > 9999:
        llamaError.excesoGlobales(tipo)

#--------------------------------------------------------------------#
# excedimosLocales()
#   Función validar que los indices LOCALES no excedan los límites.
# Parámetros:
#   tipo: String con el tipo de variable que puede estar en exceso
#   (su función principal es ser un dato para la generación del error).
#   
#   indice: Indica la indexación a validar.
#--------------------------------------------------------------------#
def excedimosLocales(tipo, indice):
    if indice == 0 and indicesLoc[indice] > 12999:
        llamaError.excesoLocales(tipo)
    elif indice == 1 and indicesLoc[indice] > 15999:
        llamaError.excesoLocales(tipo)
    elif indice == 2 and indicesLoc[indice] > 18999:
        llamaError.excesoLocales(tipo)

#--------------------------------------------------------------------#
# excedimosLocales()
#   Función validar que los indices TEMPORALES no excedan los límites.
# Parámetros:
#   tipo: String con el tipo de variable que puede estar en exceso
#   (su función principal es ser un dato para la generación del error).
#   
#   indice: Indica la indexación a validar.
#--------------------------------------------------------------------#
def excedimosTemporales(tipo, indice):
    if indice == 0 and indicesTemp[indice] > 21999:
        llamaError.excesoTemporales(tipo)
    elif indice == 1 and indicesTemp[indice] > 24999:
        llamaError.excesoTemporales(tipo)
    elif indice == 2 and indicesTemp[indice] > 27999:
        llamaError.excesoTemporales(tipo)
    elif indice == 3 and indicesTemp[indice] > 30999:
        llamaError.excesoTemporales(tipo)
    elif indice == 3 and indicesTemp[indice] > 33999:
        llamaError.excesoTemporales(tipo)

#--------------------------------------------------------------------#
# excedimosConstantes()
#   Función validar que los indices CONSTANTES no excedan los límites.
# Parámetros:
#   tipo: String con el tipo de variable que puede estar en exceso
#   (su función principal es ser un dato para la generación del error).
#   
#   indice: Indica la indexación a validar.
#--------------------------------------------------------------------#
def excedimosConstantes(tipo, indice):
    if indice == 0 and indicesCons[indice] > 36999:
        llamaError.excesoConstantes(tipo)
    elif indice == 1 and indicesCons[indice] > 39999:
        llamaError.excesoConstantes(tipo)
    elif indice == 2 and indicesCons[indice] > 42999:
        llamaError.excesoConstantes(tipo)
    elif indice == 3 and indicesCons[indice] > 45999:
        llamaError.excesoConstantes(tipo)

#--------------------------------------------------------------------#
# appendConst()
#   Función para añadir una constante a la tabla de constantes.
# Parámetros:
#   tipo: String con el tipo de constante.
#   valor: Variable con el valor de la constante.
# Resultado:
#   - Inserta la constante y su tipo al stack de operandos y de tipos.
#--------------------------------------------------------------------#
def appendConst(tipo, valor):
    # Verificar si existe la constante
    if not constantes.exists(valor):
        # Determinar el índice a utilizar indicesCons[ENT, FLOT, CAR, CADENA]
        if tipo == 'ent':
            indice = 0
        elif tipo == 'flot':
            indice = 1
        elif tipo == 'car':
            indice = 2
        else:       # cadena
            indice = 3

        # Revisar si excedimos el límite de constantes
        excedimosConstantes(tipo, indice)

        # Crear la constante
        cons = Constante(valor, indicesCons[indice])

        # Actualizar indice de constantes
        indicesCons[indice] = indicesCons[indice] + 1
        
        # Añadir constante en tabla de constantes
        constantes.add(cons)

    # Buscar constante p[1]
    cons = constantes.get(str(valor))

    # Añadir dirección de la constante al Stack de operandos
    stkOperandos.append(cons.dir)

    # Añadir tipo de la constante al stack de operadores
    stkTipos.append(tipo)

#--------------------------------------------------------------------#
# addToVarsTab()
#   Función para añadir una variable a una tabla de variables 
#   de una función global o local
# Parámetros:
#   tipo: String que indica si la variable es 'ent', 'flot' o 'car'
#   id: String con el nombre de la variable a crear
# Resultado:
#   Variable añadida a una tabla de variables globales o locales.
#--------------------------------------------------------------------#
def addToVarsTab(tipo, id):
    # Extraer el nombre de la función a generarle tabla de vars
    currF = stkScope.pop()
    stkScope.append(currF)

    if currF == 'Global':
        global indicesGlob
        indices = indicesGlob
    else:
        global indicesLoc
        indices = indicesLoc

    # Determinar el índice a utilizar indicesGlob/Loc[ENT, FLOT, CAR]
    if tipo == 'ent':
        indice = 0
    elif tipo == 'flot':
        indice = 1
    else:
        indice = 2

    # Revisar si excedimos el límite de Variables Globales/Locales
    if currF == 'Global':
        excedimosGlobales(tipo, indice)
    else: # Local
        excedimosLocales(tipo, indice)

    # Crear variable
    variable = Variable(tipo, id, indices[indice])
    
    # Actualizar dirección del indice de variables Globales/Locales por su tipo
    indices[indice] = indices[indice] + 1

    # Buscar función y agregar var a su tabla de vars
    directoriofs.get(currF).tabla.add(variable)

    # Actualizar indices Globales/Locales
    if currF == 'Global':
        indicesGlob = indices
    else: # Local
        indicesLoc = indices

# ----------------------------------------------------- FIN FUNCIONES DE APOYO ------------------------------------------------------

# Error rule for syntax errors
def p_error(p):
    llamaError.errorDeSintaxis(p, p.lineno)

#--------------------------------------------------------------------#
# buscar()
#   Función para realizar la búsqueda de archivos de prueba para
#   probar.
# Parámetros:
#   dir: String con el directorio base de la carpeta en donde están
#        los archivos de prueba. 
# Retorno:
#   Archivo a probar seleccionado por el usuario.
#--------------------------------------------------------------------#
def buscar(dir):
    archivos = []
    numAr = ''
    resp = False
    cont = 1

    for base, dirs, files in os.walk(dir):
        archivos.append(files)

    archivos = archivos[0]
    archivos.remove(archivos[0])

    print('Selecciona el test a ejecutar: ')

    for file in archivos:
        print (str(cont) + ". " + file)
        cont = cont + 1
    
    while resp == False:
        numAr = input('\nTest número: ')

        for file in archivos:
            if file == archivos[int(numAr) - 1]:
                resp = True
                break
    
    print("Corriendo \"%s\"\n" %archivos[int(numAr) - 1])
    
    return archivos[int(numAr) - 1]

test = False
if test:
    # Test directory
    dir = 'EaStat_Compiler/testing/'
    fileName = '/testing/'
    file = buscar(dir)
    prueba = dir + file
    fp = codecs.open(prueba, "r", "utf-8")
    texto = fp.read()
    fp.close()

    # Costruir el parser
    parser = yacc.yacc('SLR')
    resultado = parser.parse(texto)

    print(resultado)
else:
    parser = yacc.yacc('SLR')