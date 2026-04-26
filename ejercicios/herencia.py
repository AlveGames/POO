# 🛠️ Tu Reto de Inicio en este Chat: "La Herencia de Empleados"
# Basado en el video de Dalto y lo que ya sabes, intenta esto en tu VS Code:

# Crea una clase padre llamada Persona que reciba nombre y edad.

# Crea una clase hija llamada Empleado que herede de Persona.

# Usa la función super().__init__(nombre, edad) dentro del constructor de Empleado para pasarle esos datos a la clase padre.

# Añade el atributo sueldo solo a Empleado.

class Persona():
    def __init__(self,nombre,edad,nacionalidad):
        self.nombre = nombre
        self.edad  = edad
        self.nacionalidad = nacionalidad


class empleado(Persona):
    def __init__(self, nombre, edad,nacionalidad,sueldo,rango):
        super().__init__(nombre, edad,nacionalidad)
        self.sueldo = sueldo
        self.rango = rango
    def hablar(self):
        print(f"soy {self.nombre} tengo {self.edad} soy de {self.nacionalidad} y gano un aprox de {self.sueldo} mensual y tengo el rango de {self.rango}")

print("----------------------------------------------------------------------")
humano1 = empleado("alve",21,"ecuatoriana",1500,"programador senior")

humano1.hablar()

print("__________________________________________________________________")
# Reto de Herencia Simple: "El Concesionario"
# Imagina que tienes un plano general para todos los vehículos, pero luego quieres especificar características únicas para un coche.
# Instrucciones para tu VS Code:
# Crea una clase padre llamada Vehiculo:
# Su constructor (__init__) debe recibir marca y modelo.
# Crea una clase hija llamada Auto que herede de Vehiculo:
# Su constructor debe recibir marca, modelo y un atributo nuevo: puertas.
# Crucial: Usa super().__init__(marca, modelo) para inicializar los datos en la clase padre.
# Agrega un método en Auto llamado detalles() que imprima un mensaje elegante usando una f-string con todos los datos (marca, modelo y número de puertas).
class vehiculos():
    def __init__(self,marca, modelo):
        self.marca = marca
        self.modelo = modelo

class auto(vehiculos):
    def __init__(self, marca, modelo,puertas,asientos):
        super().__init__(marca, modelo)
        self.puertas = puertas
        self.asientos = asientos
    def detalles(self):
        print(f"el coche es de la marca {self.marca}, su modelo es:{self.modelo} con puertas de: {self.puertas} y asientos: {self.asientos}")


carro = auto("toyota", "highlux","blindadas","reclinables")
carro.detalles()