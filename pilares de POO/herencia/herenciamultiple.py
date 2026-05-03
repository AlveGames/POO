# 🛠️ Tu Reto de Inicio en este Chat: "La Herencia de Empleados"
# Basado en el video de Dalto y lo que ya sabes, intenta esto en tu VS Code:

# Crea una clase padre llamada Persona que reciba nombre y edad.

# Crea una clase hija llamada Empleado que herede de Persona.

# Usa la función super().__init__(nombre, edad) dentro del constructor de Empleado para pasarle esos datos a la clase padre.

# Añade el atributo sueldo solo a Empleado.

class Persona():
    def __init__(self,nombre,edad):
        self.nombre = nombre
        self.edad  = edad

class gamer():
    def __init__(self,computador):
        self.computador = computador
        
    def tipo_de_computador(self):
        print(f"tengo un computador tipo {self.computador}")

class empleado(Persona):
    def __init__(self, nombre, edad,sueldo):
        super().__init__(nombre, edad)
        self.sueldo = sueldo
    
    def hablar(self):
        print(f"soy {self.nombre} tengo {self.edad} y gano un aprox de {self.sueldo} mensual")

class streamer(Persona,gamer):
    def __init__(self, nombre, edad,computador,platamensual,plataforma):
        Persona.__init__(self,nombre,edad)
        gamer.__init__(self,computador)
        self.platamensual = platamensual
        self.plataforma = plataforma 

    def presentarse(self):
        print(f"klk mamawevos me llamo {self.nombre} tengo un computador {self.computador} y strimeo en {self.plataforma}")



humano1 = empleado("alve",21,1500,)

humano1.hablar()
print("----------------------------------------------------------------------")
humano2 = streamer("alve",21,"gamer",1500,"tiktok")

humano2.presentarse()
print("----------------------------------------------------------------------")
# herencia = issubclass(empleado,Persona)
# instancia = isinstance(humano1, empleado)
# print(herencia)

#--------------------------------------------------------------------------------------
# El Reto: "El Murciélago" 🦇
# Dalto usa este ejemplo porque un murciélago tiene habilidades de dos mundos: es un Mamífero (amamanta)
#  y se comporta como un Ave (vuela).
# Instrucciones para tu VS Code:
# Crea una clase Mamifero con un método amamantar() que imprima "Amamantando a las crías...".
# Crea una clase Ave con un método volar() que imprima "Volando por el cielo...".
# Crea la clase Murcielago que herede de ambas: class Murcielago(Mamifero, Ave):.
# Usa pass en su interior si no quieres agregarle atributos nuevos por ahora.
# Crea un objeto batman = Murcielago() y haz que use ambos métodos.
# Dato Pro del video de Dalto: Cuando hagas esto, habrás creado un objeto que
#  tiene acceso a los "superpoderes" de dos planos distintos.

class mamifero():
    def amamantar(self):
        print("amamantando las crias...")

class ave():
    def volar(self):
        print("volando por el cielo...")

class murcielago(mamifero,ave):
    pass
#ESTO ES UNA PORQUERIA, CREO QUE GEMINI ME ESTA TOMANDO EL PELO (ME PONE WEVADAS PARA HACER :/)
batman = murcielago()

batman.amamantar()
batman.volar()
print("_________________________________________________________________________")
print("")
print("")
# 🎮 Reto: "El Guerrero Tecnológico"
# Imagina que estás desarrollando un juego donde existen Guerreros y Científicos.
#  Ahora quieres crear una clase especial llamada Cyborg que herede las habilidades de ambos.
# Instrucciones para tu VS Code:
# Clase Guerrero:
# Constructor: Recibe fuerza.
# Método atacar(): Imprime "Atacando con una fuerza de [fuerza]...".
# Clase Cientifico:
# Constructor: Recibe habilidad_ia.
# Método analizar(): Imprime "Analizando datos con nivel de IA: [habilidad_ia]...".
# Clase Cyborg:
# Debe heredar de Guerrero y Cientifico.
# Constructor: Debe recibir nombre, fuerza y habilidad_ia.
# Crucial: Llama manualmente a los constructores de los padres:
# Guerrero.__init__(self, fuerza)
# Cientifico.__init__(self, habilidad_ia)
# Método presentarse(): Usa una f-string que diga:
#  "Hola, soy el Cyborg [nombre]. Mi fuerza es [fuerza] y mi IA es de nivel [habilidad_ia]".

class guerrero():
    def __init__(self,fuerza):
        self.fuerza = fuerza


    def atacar(self):
        print(f"Atacando con una fuerza de{self.fuerza}...")
    def defensa(self):
        print(f"defiendo con {self.resistencia} de resistencia")

class cientifico():
    def __init__(self,habilidad_ia):
        self.habilidad_ia = habilidad_ia

    def analizar(self):
        print(f"Analizando datos con nivel de IA: {self.habilidad_ia}")

class ciborg():
    def __init__(self, fuerza, habilidad_ia,nombre):
        guerrero.__init__(self,fuerza)
        cientifico.__init__(self,habilidad_ia)
        self.nombre = nombre
    def presentarse(self):
        print(f"Hola, soy el Cyborg {self.nombre}. Mi fuerza es {self.fuerza} y mi IA es de nivel {self.habilidad_ia}")


ciborg1 = ciborg("paladino",100,500)

ciborg1.presentarse()
print("")