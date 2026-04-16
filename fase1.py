import math
#ejercicio 1
# funciones sin parametros y sin retorno
#-----------------------------------------------------------------------
#codigo que dio Gemini:
# def saludar_estudiante():
#     print("¡Bienvenido a tu clase de POO!")
#     print("Preparando el entorno...")

# # Para que funcione, debes "llamarla":
# saludar_estudiante()
#-----------------------------------------------------------------------
#mi codigo:
def saludando_gente():
    print("klk mi gente")
    print("aqui andamo comiendono un mangito classic")

saludando_gente()

# --------------------------------------------------------------------
#lo unico que hace es hablar cuando se le llama a una funcion
# --------------------------------------------------------------------
print("--------------------------------------------------------------------")
#ejercicio 2
#Funciones con parámetros y retorno
#----------------------------------------------------------------------
#codigo dado por Gemini:
# def calcular_area_rectangulo(base, altura):
#     area = base * altura
#     return area  # Aquí entregas el producto terminado

# # Guardamos el resultado en una variable
# resultado = calcular_area_rectangulo(10, 5)
# print(f"El área es: {resultado}")
#----------------------------------------------------------------------
#mi codigo:
def calcular_hipotenuza(cateto1,cateto2):
    hipotenuza = math.sqrt(cateto1**2 + cateto2**2)
    return hipotenuza

resultado = calcular_hipotenuza(5,5)
print(f"la medida de la hipotenuza es {resultado}")

print("--------------------------------------------------------------------")
#---------------------------------------------------------------------------------
#ejercicio 3
#Funciones dentro de funciones
#---------------------------------------------------------------------------------
#codigo dado por Gemini:
# def procesar_pago(monto):
#     def aplicar_descuento(valor):
#         return valor * 0.90  # Aplica un 10% de descuento
    
#     total = aplicar_descuento(monto)
#     return f"El total a pagar con descuento es: {total}"

# print(procesar_pago(100))
#-------------------------------------------------------------------------------
#mi codigo:
def calcularpago(valor):
    def porcentajeiva():
        return valor * 0.15
    
    totalfinal = valor + porcentajeiva()

    return f"lo que tenes que pagar con todo es {totalfinal}"

print(calcularpago(100))
print ("----------------------------------------------------------------------------------")
