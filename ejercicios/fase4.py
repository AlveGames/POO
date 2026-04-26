import json
#inicio para decoradores y mas
# 1. Definimos el Decorador (La envoltura)
# def decorador_mensaje(funcion_original):
#     def envoltura():
#         print(">>> Iniciando proceso...")
#         funcion_original() # Aquí se ejecuta la función que "envolvemos"
#         print(">>> Proceso finalizado con éxito.")
#     return envoltura

# # 2. Usamos el decorador con el símbolo @
# @decorador_mensaje
# def saludar():
#     print("Hola, estoy aprendiendo Decoradores.")

# # 3. Ejecutamos
# saludar()

#----------------------------------------------------------------------------------------
# Tu Reto Final: El Decorador "Vigilante de Ventas" ⚡
# Vamos a crear un decorador que, cada vez que llames al método vender, imprima automáticamente un mensaje de aviso.
# Instrucciones para tu VS Code:
# Define el decorador: Crea una función llamada aviso_venta(func). Adentro debe tener la envoltura(*args, **kwargs)--- 
# que imprima "--- Verificando salida de inventario ---", ejecute la función y luego imprima "--- Venta registrada en el sistema ---".
# Aplica el decorador: Pon @aviso_venta justo arriba de tu método vender dentro de la clase.
# Ejecuta: Llama a mi_item.vender(1) y mira la magia en la terminal.
#------------------------------------------------------------------------------------------
#aqui ira el decorador

def aviso_venta(funcion_original):
    def envoltura(*args, **kwargs):
        print("--- Verificando salida de inventario ---")
        resultado = funcion_original(*args, **kwargs) 
        print("--- Venta registrada en el sistema ---")
        return resultado
    return envoltura

# def aviso_guardar_datos(funcionpepa):     #(intente hacer otro aviso pero no tenia funcion asi que no funcionó)
#     def  envolx1(*args, **kwargs):
#         print("--- Procesando datos para recuperar ---")
#         resul = funcionpepa(*args, **kwargs)
#         print("--- Validando constancia de datos ---")
#         return resul
#     return envolx1
#---------------------------------------------------------------------------------------

class inventario():
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    @aviso_venta
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
#creo que quedo perfecto