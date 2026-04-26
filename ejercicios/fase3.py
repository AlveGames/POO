# nombre = input("ingrese su nombre: ")


# # Para guardar (Write):
# with open("usuario.txt", "w") as archivo:
#     archivo.write(nombre)


# print(f"datos guardados perfectamente, se guardo el dato: {nombre}")


# with open("usuario.txt", "r") as archivo:
#     contenido = archivo.read() # Esto saca el texto del archivo
#     print(f"Leído del archivo: {contenido}")

#---------------------------------------------------------------------------------
# contenido = input("ingrese el contenido que desea guardar: ")

# with open ("usuario.txt", "w") as creararchivo:
#     creararchivo.write(contenido)

# print(f"El contenido que usted metio fue: {contenido}")

# print("-------------------------------------------------------------------")


# with open("usuario.txt", "r") as creararchivo:
#     Leercontenido = creararchivo.read()
#     print(f"El contenido recuperado es: {Leercontenido}")
#------------------------------------------------------------------------------------
# import json # Importamos la librería para manejar datos estructurados

# usuario = {
#     "nombre": "Sebas",
#     "nivel": 5,
#     "puntos": 150
# }

# # Guardar en JSON (Estructurado)
# with open("perfil.json", "w") as archivo:
#     json.dump(usuario, archivo) # dump "vuelca" el diccionario al archivo
#---------------------------------------------------------------------------------------
# Tu Reto Final de Fase 3: "La Persistencia del Objeto" 💾
# Este reto une la Fase 2 (Clases) con la Fase 3 (Archivos).
# Usa tu clase inventario (la que tiene nombre, precio y stock).
# Crea un objeto: item = inventario("Camisa", 25, 10).
# Reto: Crea un diccionario con los datos de ese objeto y guárdalo en un archivo llamado stock.json.
# Prueba definitiva: Intenta leer ese archivo JSON y crear un nuevo objeto con esos datos.
#---------------------------------------------------------------------------------------------
import json
class inventario():
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self,unidades):
        self.stock =  self.stock - unidades 

    def ver_info(self):
        
        return f"producto:{self.nombre} | precio:{self.precio} | stock:{self.stock} "

item1 = inventario("camisa", 25 , 10)
item2 = inventario("sueter", 15, 5 )

item2.vender(1)

print(item2.ver_info())

usuario = {
    "nombre": item1.nombre,
    "precio": item1.precio,
    "stock": item1.stock
}

with open("perfil.json", "w") as creararchivo:
    json.dump(usuario,creararchivo)

print("se guardo el perfil")

print("--------------------------------------------------------------------------------")

with open("perfil.json", "r") as creararchivo:
    datos = json.load(creararchivo)
    datos_recuperados = inventario(datos["nombre"], datos["precio"], datos["stock"])

    print("datos recuperados existosamente...")
    print(datos_recuperados.ver_info())