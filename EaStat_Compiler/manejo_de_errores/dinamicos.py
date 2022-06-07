class ControladorErrores():
    def __init__(self):
        self.separadorA = '---------------------------------------------------- ERROR ----------------------------------------------------\n'
        self.separadorB = '\n---------------------------------------------------- ERROR ----------------------------------------------------'

    # Levanta un error si se intenta ingresar un dato incompatible con su destino
    def errorEnInput(self, valor, tipo):
        print(self.separadorA)
        print('*Se va pa\' tras de ver cómo intentan asignar un "' + str(valor) + '" en una var tipo "' + tipo + '"')
        print(self.separadorB)

        raise Exception("Tipo de input incompatible")
