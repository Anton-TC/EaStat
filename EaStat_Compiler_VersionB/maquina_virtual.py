from ast import Pass
from asyncio import constants
from cmath import exp
import codecs
import os
import json
import re
from re import T
import sys
from tkinter import N
from tkinter.messagebox import NO
import numpy

from analisis_sintactico_semantico import parser
from manejo_de_errores.dinamicos import ControladorErrores
from estructuras_de_compilacion.tab_cons import Constante
from estructuras_de_ejecucion.segmento import Segmento
from estructuras_de_ejecucion.controladorMemoria import controladorDeMem

# Esconder el traceback 
sys.tracebacklimit = 1

# Inicializar el controlador de errores
levantaError = ControladorErrores()

#--------------------------------------------------------------------#
# iniciarCompilador()
#   Función que carga la interfaz de selección de archivo a compilar,
#   inicializa la compilación, importa las estructuras base de la
#   compilación y manda a llamar a ejecutar el código objeto.
# Resultado:
#   Inicializa la ejecución del código compilado.
#--------------------------------------------------------------------#
def iniciarCompilador():
    # Inicializamos directorio de pruebas
    dir = './testing/'

    # Prguntamos al usuario cuál archivo desea ejecutar
    file = buscar(dir)

    # Completamos el directorio de pruebas
    prueba = dir + file

    # Tomamos el texto
    fp = codecs.open(prueba, "r", "utf-8")

    # Extraemos el texto
    codigo = fp.read()

    # Cerramos el archivo
    fp.close()

    # Inicio de compilación
    print('Compilando programa...\n')
    respuesta = parser.parse(codigo)
    print(respuesta, '\n')

    # Importación de código objeto
    print('Importando código objeto...\n')
    with open('./estructuras_de_ejecucion/cuadruplos.json') as json_file:
        global misCuadruplos
        misCuadruplos = json.load(json_file)
    print('¡Cuádruplos importados!\n')

    # Importación del directorio de funciones
    print('importando estructuras de ejecución...\n')
    with open('./estructuras_de_ejecucion/directorio.json') as json_file:
        global directoriofs
        directoriofs = json.load(json_file)
    print('¡Directorio importado!\n')

    # Importación de tabla de constantes
    print('Importando constantes identificadas\n')
    with open('./estructuras_de_ejecucion/constantes.json') as json_file:
        misConstantes = json.load(json_file)
    print('¡Constantes importadas!\n')

    # Generar segmentos de memoria
    print('Generando memoria...\n')   

    # Estructurar scope GLOBAL
    memGlob = [] 

    # Generar segmento de memoria de ejecución GLOBAL de variables
    configTipos = [False, False, False]
    configConsts = directoriofs["Global"]['numVars']
    memGlob.append(generarSegmento(1000, configConsts, configTipos))

    # Generar segmento de memoria de ejecución GLOBAL de temporales
    configTipos = [True, False, True]
    configConsts = directoriofs["Global"]['numTemps']
    memGlob.append(generarSegmento(19000, configConsts, configTipos))

    # Generar segmento de memoria de constantes
    memConsts = generarSegmentoConstantes(misConstantes)

    # Estructurar memoria inicial
    memoria = []

    # Instanciar controlador de memoria
    pideAMemoria = controladorDeMem(memoria)
    
    # Insertar segmento de constantes
    pideAMemoria.agregarScope(memConsts)
    # Insertar segmento GLOBAL
    pideAMemoria.agregarScope(memGlob)

    print('¡Memoria generada!\n')

    # Inicializar ejecución
    print('Iniciando ejecución...\n')
    print('|-----------------------------------------------------------|\n')
    ejecutar(pideAMemoria)


#--------------------------------------------------------------------#
# buscar()
#   Función para realizar la búsqueda de archivos de prueba para
#   compilar.
# Parámetros:
#   dir: String con el directorio base de la carpeta en donde están
#        los archivos de prueba. 
# Retorno:
#   Archivo a compilar seleccionado por el usuario.
#--------------------------------------------------------------------#
def buscar(dir):
    archivos = []
    numAr = ''
    resp = False
    cont = 1

    for base, dirs, files in os.walk(dir):
        archivos.append(files)

    #print(archivos)
    archivos = archivos[0]

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

#--------------------------------------------------------------------#
# generarSegmento()
#   Toma las configuraciones del usuario y regresa una nueva
#   instancia de memoria.
# Parámetros:
#   dirInicial: Dato numérico que permite calcular las direcciones
#               límite para el resto de subsegmentos.
# 
#   Tams: Arreglo de valores numéricos con el tamaño destino de cada
#         subsegmento en cada celda.
# 
#   configTipos: Arreglo de booleanos que indican cuáles son los
#                segmentos extras que deben de inicializarse en el
#                objeto.
# Retorno:
#   Objeto Segmento() construido
#--------------------------------------------------------------------#
def generarSegmento(dirInicial, Tams, configTipos):
    return Segmento(dirInicial, Tams, configTipos[0], configTipos[1], configTipos[2])

#--------------------------------------------------------------------#
# generarSegmento()
#   Extrae las constantes de la tabla de constantes y las inserta
#   en un segmento de memoria nueva.
# Parámetros:
#   misConstantes: Diccionario de constantes.
# Retorno:
#   Objeto Segmento() de constantes construido con constantes
#   almacenadas.
#--------------------------------------------------------------------#
def generarSegmentoConstantes(misConstantes):
    configTipos = [False, True, False]
    configConsts = getConfigConsts(misConstantes)
    memConsts = generarSegmento(34000, configConsts, configTipos)
    
    for nombre, constante in misConstantes.items():
        memConsts.set(constante["dir"], constante["valor"])
    
    return memConsts

#--------------------------------------------------------------------#
# getConfigConsts()
#   Extrae la configuración para generar la memoria de constantes.
# Parámetros:
#   misConstantes: Diccionario de constantes.
# Retorno:
#   Arreglo de valores numéricos con el tamaño destino del subsegmento
#   de constantes.
#--------------------------------------------------------------------#
def getConfigConsts(misConstantes):
    config = [0 for i in range(4)] 
    for nombre, const in misConstantes.items():
        if const['tipo'] == 'ent':
            config[0] = config[0] + 1
        elif const['tipo'] == 'flot':
            config[1] = config[1] + 1
        elif const['tipo'] == 'car':
            config[2] = config[2] + 1
        else:
            config[3] = config[3] + 1
    return config

#--------------------------------------------------------------------#
# checkIfNone()
#   Revisa si al menos uno de dos valores son None.
# Parámetros:
#   Operando1: Valor 1.
#   Operando2: Valor 2.
# Resultado:
#   Se levanta un error por intentar hacer una operación entre
#   variables sin asignación.
#--------------------------------------------------------------------#
def checkIfNone(operando1, operando2):
    if operando1 == None or operando2 == None:
        levantaError.variablesSinValor();
        
#--------------------------------------------------------------------#
# ejecutar()
#   Realiza la ejecución de los cuadruplos y avisa si la ejecución
#   fue exitosa.
# Parámetros:
#   pideAMemoria: Controlador de memoria base con segmento de
#                 constantes y par de segmentos de scope global.
# Resultado:
#   Cuadruplos ejecutados.
#--------------------------------------------------------------------#
def ejecutar(pideAMemoria):
    # Inicializar IP
    ip = 1

    # Inicializar stack de scopes y de saltos
    stkScopes = ['Global']
    stkSaltos = []

    # Extraer el primer cuádruplo
    currentCuad = misCuadruplos[str(ip)]
    operacion = currentCuad['operacion']

    # Repetir análisis de cuádruplos hasta encontrar la operación END
    while operacion != "END":

        currScope = stkScopes.pop()
        if operacion == '+':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)

            # Realizar operación
            res = opdo1 + opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '-':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 - opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '*':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 * opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)
            
        elif operacion == '/':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 / opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)
            
        elif operacion == '=':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, '.')
           
            # Guardar valor en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], opdo1, currScope)
            
            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '>':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 > opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '<':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 < opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '!=':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 != opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '==':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 == opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '||':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 or opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == '&&':
            # Extraer operadores del cuádruplo
            opdo1 = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            opdo2 = pideAMemoria.obtenerValor(currentCuad["opdo2"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(opdo1, opdo2)
            
            # Realizar operación
            res = opdo1 and opdo2
            
            # Guardar resultado en memoria
            pideAMemoria.guardarValor(currentCuad["destino"], res, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == 'leer':
            # Solocitar entrada al usuario
            valor = input()
            destino = currentCuad["destino"]

            # Establecer patrones de tipos para type matching
            ptrnFlot = re.compile(r'\d+\.\d*')
            ptrnEnt = re.compile(r'\d+')
            ptrnCad = re.compile(r'(.*)')
            ptrnCar = re.compile(r'(.)')

            # Validar que la asiganación es del tipo adecuado
            if currScope == 'Global':
                if destino >= 1000 and destino < 4000 and not ptrnEnt.match(valor):
                    levantaError.errorEnInput(valor, 'ent')
                elif destino >= 4000 and destino < 7000 and not ptrnFlot.match(valor):
                    levantaError.errorEnInput(valor, 'flot')
                elif destino >= 7000 and destino < 10000 and not ptrnCar.match(valor):
                    levantaError.errorEnInput(valor, 'car')
                elif destino >= 7000 and destino < 10000 and not ptrnCad.match(valor):
                    levantaError.errorEnInput(valor, 'cadena')
            else:
                if destino >= 10000 and destino < 13000 and not ptrnEnt.match(valor):
                    levantaError.errorEnInput(valor, 'ent')
                elif destino >= 13000 and destino < 16000 and not ptrnFlot.match(valor):
                    levantaError.errorEnInput(valor, 'flot')
                elif destino >= 16000 and destino < 19000 and not ptrnCar.match(valor):
                    levantaError.errorEnInput(valor, 'car')
                elif destino >= 7000 and destino < 10000 and not ptrnCad.match(valor):
                    levantaError.errorEnInput(valor, 'cadena')
            
            # Convertir el valor a su tipo adecuado antes de almacenarlo
            if ptrnFlot.match(valor):
                valor = float(valor)
            elif ptrnEnt.match(valor):
                valor = int(valor)
            
            # Guardar el valor
            pideAMemoria.guardarValor(destino, valor, currScope)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)


        elif operacion == 'escrib':
            # Extraer operadores del cuádruplo
            value = pideAMemoria.obtenerValor(currentCuad["destino"], currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(value, '.')
            
            # Imprimir valor
            print(value)

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == 'gotoF':
            # Extraer resultado booleano
            res = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)

            # Actualizar IP en caso de que el resultado sea Verdadero
            ip = ip + 1

            # Verificar si el resultado fue Falso
            if not res:
                # Actualizar el IP al nuevo destino
                ip = currentCuad['destino']

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == 'gotoV':
            # Extraer resultado booleano
            res = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)

            # Verificar si el resultado fue Verdadero
            if res:
                # Actualizar el IP al nuevo destino
                ip = currentCuad['destino']

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        elif operacion == 'gotoM':
            # Actualizar IP
            ip = currentCuad['destino']

            # Reinsertar el scope actual
            stkScopes.append(currScope)
        elif operacion == 'goto':
            # Actualizar IP
            ip = currentCuad['destino']

            # Reinsertar el scope actual
            stkScopes.append(currScope)
        elif operacion == 'era':
            # Extraer el nombre de la función a la que se le va a generar su memoria
            nombreFunc = currentCuad["opdo1"]

            # Estructurar scope LOCAL
            memLoc = [] 

            # Generar segmento de memoria de ejecución LOCAL de variables
            configTipos = [False, False, False]
            configVars = directoriofs[nombreFunc]['numVars']
            memLoc.append(generarSegmento(10000, configVars, configTipos))

            # Generar segmento de memoria de ejecución LOCAL de temporales
            configTipos = [True, False, True]
            configTemps = directoriofs[nombreFunc]['numTemps']
            memLoc.append(generarSegmento(19000, configTemps, configTipos))

            # Insertar scope actual en su stack indicador
            stkScopes.append(currScope)

            # Insertar en el nuevo scope en el stack de scopes
            stkScopes.append(nombreFunc)

            # Actualizar IP
            ip = ip + 1
        elif operacion == 'param':
            # Insertar scope en memoria
            pideAMemoria.agregarScope(memLoc)

            # Extraer la dirección destino
            dirOrigen = currentCuad["opdo1"]
            dirDestino = currentCuad["destino"]

            # Mandar parámetro al nuevo segmento de memoria
            pideAMemoria.mandarParam(dirOrigen, dirDestino)

            # Extraer scope de memoria para un posible próximo parámetro
            memLoc = pideAMemoria.extraerScope()

            # Insertar scope actual en su stack indicador
            stkScopes.append(currScope)

            # Actualizar IP
            ip = ip + 1
        elif operacion == 'gosub':
            # Insertar scope en memoria para ejecutar
            pideAMemoria.agregarScope(memLoc)

            # Extraer el nombre de la función destino y su dir. de inicio
            nombreFunc = currentCuad["opdo1"]
            dirInicio = directoriofs[nombreFunc]["dirInicio"]

            # Guardar IP siguiente
            stkSaltos.append(ip + 1)

            # Actualizar IP
            ip = dirInicio

            # Insertar scope actual en su stack indicador
            stkScopes.append(currScope)
        elif operacion == 'regresa':
            # Extraer dirección del resultado
            dirRes = currentCuad["destino"]
            
            # Extraer dirección de la variable GLOBAL de la función
            dirDestino = directoriofs[currScope]["dirVar"]

            # Asignar resultado a la variable GLOBAL de la función
            res = pideAMemoria.obtenerValor(dirRes, currScope)
            
            # Verificar que las variables tengan valor
            checkIfNone(res, '.')

            pideAMemoria.guardarValor(dirDestino, res, 'Global')

            # Extarer el IP guardado en el stack de saltos
            indexRegreso = stkSaltos.pop()

            # Actualizar IP
            ip = indexRegreso

            # Eliminar memoria LOCAL
            pideAMemoria.eliminarUltimoScope()
        elif operacion == 'endfunc':
            # Extarer el IP guardado en el stack de saltos
            indexRegreso = stkSaltos.pop()

            # Actualizar IP
            ip = indexRegreso

            # Eliminar memoria LOCAL
            pideAMemoria.eliminarUltimoScope()
        elif operacion == 'verif':
            # Extraer expresión de transición del cuádruplo
            expTrans = pideAMemoria.obtenerValor(currentCuad["opdo1"], currScope)
            
            # Extraer límite superior
            limSup = pideAMemoria.obtenerValor(currentCuad["destino"], currScope)
            
            # Realizar verificación de rango
            if expTrans < 0 or expTrans > limSup:
                levantaError.fueraDeLimites()

            # Actualizar IP
            ip = ip + 1

            # Reinsertar el scope actual
            stkScopes.append(currScope)

        # Obtener el siguiente cuádruplo
        currentCuad = misCuadruplos[str(ip)]
        operacion = currentCuad['operacion']
    # Fin del ciclo while

    print('\n|-----------------------------------------------------------|\n')
    print('¡Programa ejecutado con éxito!')
    input()
    
iniciarCompilador()