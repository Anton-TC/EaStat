class cuboSem():
    def __init__(self):
        self.cubo = {
            # Valores enteros con...
            "ent" : {
                # Valores enteros y operadores...
                "ent" : {
                    # Aritméticos
                    "+"     : "ent",
                    "-"     : "ent",
                    "*"     : "ent",
                    "/"     : "flot",
                    # Asignación
                    "="     : "ent",
                    # Lógicos
                    ">"     : "bool",
                    "<"     : "bool",
                    "!="    : "bool",
                    "=="    : "bool",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Valores flotantes y operadores...
                "flot" : {
                    # Aritméticos
                    "+"     : "flot",
                    "-"     : "flot",
                    "*"     : "flot",
                    "/"     : "flot",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "bool",
                    "<"     : "bool",
                    "!="    : "bool",
                    "=="    : "bool",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Caracteres y operadores...
                "car" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Booleanos y operadores...
                "bool" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                }
            },

            # Valores flotantes con...
            "flot" : {
                # Valores enteros y operadores...
                "ent" : {
                    # Aritméticos
                    "+"     : "flot",
                    "-"     : "flot",
                    "*"     : "flot",
                    "/"     : "flot",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "bool",
                    "<"     : "bool",
                    "!="    : "bool",
                    "=="    : "bool",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Valores flotantes y operadores...
                "flot" : {
                    # Aritméticos
                    "+"     : "flot",
                    "-"     : "flot",
                    "*"     : "flot",
                    "/"     : "flot",
                    # Asignación
                    "="     : "flot",
                    # Lógicos
                    ">"     : "bool",
                    "<"     : "bool",
                    "!="    : "bool",
                    "=="    : "bool",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Caracteres y operadores...
                "car" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Booleanos y operadores...
                "bool" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                }
            },

            # Caracteres con...
            "car" : {
                # Valores enteros y operadores...
                "ent" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Valores flotantes y operadores...
                "flot" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Caracteres y operadores...
                "car" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "car",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "bool",
                    "=="    : "bool",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Booleanos y operadores...
                "bool" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                }
            },

            # Booleanos con...
            "bool" : {
                # Valores enteros y operadores...
                "ent" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Valores flotantes y operadores...
                "flot" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Caracteres y operadores...
                "car" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "ERROR",
                    "&&"    : "ERROR"
                },
                # Booleanos y operadores...
                "bool" : {
                    # Aritméticos
                    "+"     : "ERROR",
                    "-"     : "ERROR",
                    "*"     : "ERROR",
                    "/"     : "ERROR",
                    # Asignación
                    "="     : "ERROR",
                    # Lógicos
                    ">"     : "ERROR",
                    "<"     : "ERROR",
                    "!="    : "ERROR",
                    "=="    : "ERROR",
                    "||"    : "bool",
                    "&&"    : "bool"
                }
            }
        }

        self.traducción = {
            # Operadores Aritméticos
                    "+"     : "suma",
                    "-"     : "resta",
                    "*"     : "multiplicación",
                    "/"     : "divisón",
                    # Asignación
                    "="     : "asignación",
                    # Lógicos
                    ">"     : "comparación tipo '>'",
                    "<"     : "comparación tipo '<'",
                    "!="    : "comparación tipo '!='",
                    "=="    : "comparación tipo '=='",
                    "||"    : "comparación tipo '||'",
                    "&&"    : "comparación tipo '&&'"
        }

    #--------------------------------------------------------------------#
    # match()
    #   Método para consultar el cubo semántico
    # Parámetros:
    #   operando1: Tipo de valor 1.
    #   operando2: Tipo de valor 2.
    #   operador: Operador con el que se van a evaluar los operandos.
    # Resultado:
    #   Resultado del cubo semántico.
    #--------------------------------------------------------------------#
    def match(self, operando1, operando2, operador):
        #print("\nBuscando : " + operando1 + ' ' + operador + ' ' + operando2)
        res = self.cubo[operando1][operando2][operador]
        return res