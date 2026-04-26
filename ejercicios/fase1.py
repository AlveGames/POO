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
print ("---------------------------ejercicio final----------------------------------------")
print ("----------------------------------------------------------------------------------")
#codigo dado por gemini:
# # Función 1: Solo calcula el impuesto
# def calcular_iva(precio):
#     iva = precio * 0.15  # <--- Usamos 0.15 para el 15%
#     return iva           # <--- El "jugo" sale de la licuadora

# # Función 2: Usa la anterior para mostrar el total
# def imprimir_factura(producto, precio):
#     # Llamamos a la función de arriba y guardamos su "return"
#     impuesto_calculado = calcular_iva(precio) 
    
#     total = precio + impuesto_calculado
    
#     # Usamos la 'f' para que aparezcan los resultados [cite: 122, 124]
#     print(f"--- FACTURA ---")
#     print(f"Producto: {producto}")
#     print(f"Precio base: ${precio}")
#     print(f"IVA (15%): ${impuesto_calculado}")
#     print(f"Total a pagar: ${total}")

# # Prueba tu código así:
# imprimir_factura("Laptop", 1000)
#-------------------------------------------------------------------------------------------
#ejercicio final:
#El Reto: El Consultor de Sueldos
#Imagina que vas a trabajar como programador. Tu contrato dice un sueldo bruto, pero te descuentan salud y te dan un bono por transporte.
#Tu misión es crear una función llamada generar_recibo(nombre, sueldo_bruto) que:
#Tenga una función interna llamada calcular_descuentos() que:
# Calcule el 9% del sueldo_bruto (por salud y pensiones).
# Retorne ese valor de descuento.
# Tenga otra función interna llamada calcular_bono() que:
# Retorne un valor fijo de $50 por bono de alimentación.
# Calcule el total final: sueldo_bruto - descuentos + bono.
# Use una F-string para imprimir un recibo profesional.
#------------------------------------------------------------------------------------------
def generar_recibo(nombre, sueldo_bruto):
    def calcular_descuentos():
        descuento = sueldo_bruto * 0.09
        return descuento
    
    def calcular_bono():
        bono= 50
        return bono
    
    total_finalfinal = sueldo_bruto - calcular_descuentos() + calcular_bono()
    
    return f"estimado/a {nombre} su sueldo neto es de {total_finalfinal}"
print(generar_recibo("sebas", 1500))