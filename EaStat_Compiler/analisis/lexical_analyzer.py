# Antonio Torres Carvajal - A01561769
import codecs
import os

import ply.lex as lex

# Lista de tokens
# Palabras reservadas
reserved = {
    'inicio' : 'INICIO',
    'principal' : 'PRINCIPAL',
    'ent' : 'ENT',
    'flot' : 'FLOT',
    'car' : 'CAR',
    'leer' : 'LEER',
    'escrib' : 'ESCRIB',
    'si' : 'SI',
    'otro' : 'OTRO',
    'mientras' : 'MIENTRAS',
    'vacio' : 'VACIO',
    'regresa' : 'REGRESA',
    
    # Funciones especiales
    'media' : 'MEDIA',
    'mediana' : 'MEDIANA',
    'moda' : 'MODA',
    'varianza' : 'VARIANZA',
    'desestandar' : 'DESESTANDAR',
    'rango' : 'RANGO',
    'reglamulti' : 'REGLAMULTI',
    'combins' : 'COMBINS',
    'permuts' : 'PERMUTS',
    'histograma' : 'HISTOGRAMA',
    'grafcaja' : 'GRAFCAJA',
    'dstbinom' : 'DSTBINOM',
    'dstbinomneg' : 'DSTBINOMNEG',
    'dstgeom' : 'DSTGEOM',
    'dsthipgeom' : 'DSTHIPGEOM',
    'dstpoisson' : 'DSTPOISSON'
}

tokens = list(reserved.values()) + [

    # Operadores lógicos
    'MAYOR',
    'MENOR',
    'DIFF',
    'IGUALQ',
    'O',
    'Y',

    # Símbolos
    'PUCOMA',
    'COMA',
    'BRAIZQ',
    'BRADER',
    'PAREIZQ',
    'PAREDER',
    'LLAIZQ',
    'LLADER',

    # Operadores aritméticos
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIV',

    # Nombres y constantes
    'ID',
    'C_ENT',
    'C_FLOT',
    'C_CAR',
    'CADENA'
]

# Expresiones regulares

# Operadores lógicos
t_MAYOR = r'>'
t_MENOR = r'<'
t_DIFF = r'!='
t_IGUALQ = r'=='
t_O = r'\|\|'
t_Y = r'&&'

# Símbolos
t_PUCOMA = r';'
t_COMA = r','
t_BRAIZQ = r'\['
t_BRADER = r'\]'
t_PAREIZQ = r'\('
t_PAREDER = r'\)'
t_LLAIZQ = r'{'
t_LLADER = r'}'

# Operadores aritméticos
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'\-'
t_POR = r'\*'
t_DIV  = r'/'

# Tokens con acciones
def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'

    t.type = reserved.get(t.value,'ID')
    
    return t

def t_C_FLOT(t):
    r'-?\d+\.\d*'
    
    # Convertir valor en flotante
    t.value = float(t.value)
    return t

def t_C_ENT(t):
    r'-?\d+'
    
    # Convertir valor en entero
    t.value = int(t.value)
    return t

def t_C_CAR(t):
    r'(\'.\')'

    # Retirar las '' del caracter
    tamCadena = len(t.value)
    t.value = t.value[1 : tamCadena - 1]
    return t

def t_CADENA(t):
    r'(“.*” | ".*")'

    # Retirar las "" o “” del String
    tamCadena = len(t.value)
    if tamCadena <= 2:
        t.value = ''
    else:
        t.value = t.value[1 : tamCadena - 1]
    return t

# Regla para lineas nuevas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# String que contiene los caracteres a ignorar (espacios y tabs)
t_ignore  = ' \t' + chr(13)

# Manejo de errores
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    #print("código ASCII: '%s'" % ord(t.value[0]))
    t.lexer.skip(1)

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

test = False
if test:
    # Test directory
    dir = './testing/'
    file = buscar(dir)
    prueba = dir + file
    fp = codecs.open(prueba, "r", "utf-8")
    texto = fp.read()
    fp.close()

    # Costruir el lexer
    lexer = lex.lex()
    lexer.input(texto)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

else:
    # Costruir el lexer
    lexer = lex.lex()
