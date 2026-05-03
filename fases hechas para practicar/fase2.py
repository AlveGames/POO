#ejercicio 1:
#----------------------------------------------------------------------------------
#ejercicio dado por gemini:
# 1. Definición de la Clase (El Molde)
# class Guerrero:
    
#     # 2. El Constructor (__init__): Se ejecuta CADA VEZ que creas un guerrero.
#     # El 'self' es como decir "este guerrero específico".
#     def __init__(self, nombre, fuerza):
#         self.nombre = nombre  # Atributo: guarda el nombre
#         self.fuerza = fuerza  # Atributo: guarda la fuerza
#         self.vida = 100       # Atributo: todos empiezan con 100 de vida

#     # 3. Un Método: Es una función que solo los Guerreros saben hacer.
#     def atacar(self):
#         return f"{self.nombre} ataca con una fuerza de {self.fuerza}!"

# # 4. Instanciación: Aquí creamos el objeto real
# mi_guerrero = Guerrero("Ragnar", 50)

# # 5. Acceso: Usamos el punto (.) para entrar a sus habilidades
# print(mi_guerrero.atacar())
#---------------------------------------------------------------------------------
#problema 1:
# Reto 1: El Objeto Simple (Nivel Fácil) 🟢
# Crea una clase llamada Mascota.
# Su constructor debe recibir nombre y tipo (ej. "Perro", "Gato").
# Crea un método llamado hacer_sonido que retorne un mensaje como: "Fido es un Perro y está ladrando".
# Instancia (crea) dos mascotas diferentes y muestra sus sonidos en la terminal.
#------------------------------------------------------------------------------------------
class mascota():
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    
    def sonido(self):
        return f"{self.nombre} es un gato de raza {self.tipo} y esta maullando"
    
mi_mascota = mascota("michifus", "angora turco")
print(mi_mascota.sonido())

print("--------------------------------------------------------------------------")

#------------------------------------------------------------------------------------------
#problema 2:
# Reto 2: Atributos y Cálculos (Nivel Medio) 🟡
# Crea una clase llamada Rectangulo.
# Su constructor debe recibir base y altura.
# Crea un método llamado calcular_area que retorne el resultado de base * altura.
# Crea otro método llamado mostrar_datos que imprima: "Rectángulo de [base]x[altura] - Área: [resultado]".
# Pista: Recuerda usar self.base y self.altura dentro de los métodos.
#-----------------------------------------------------------------------------------------------------------------
class Rectangulo():

    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def crear_area(self):
         resultado = self.base * self.altura
         return resultado


    def mostrar_datos(self):
        area_final = self.crear_area()
        return f"rectangulo de {self.base} x {self.altura} es = {area_final}"


datos_de_la_mondaa = Rectangulo(10,5)
print(datos_de_la_mondaa.mostrar_datos())


print("----------------------------------------------------------------------------------------------")
#problema 3 :
# Reto 3: El Sistema Bancario 🏦
# Tu misión es crear la clase CuentaBancaria.
# El Constructor (__init__): debe recibir dos datos: titular y saldo_inicial. Guárdalos en el objeto usando self.
# Método depositar(monto):
# Este método debe recibir un número (el monto a depositar).
# Debe sumar ese monto al saldo que ya tiene el objeto (self.saldo).
# Tip: No necesitas retornar nada aquí, solo actualizar el valor.
# Método ver_balance():
# Debe retornar (usando return) una frase con una f-string que diga: "El titular [nombre] tiene un saldo de $[saldo]".


class CuentaBancaria():
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.saldo = saldo_inicial

    def depositar(self, monto):
        self.monto =self.saldo + monto
        print(f"--- El Depósito exitoso de ${monto} ---")

    def ver_balance(self):

        return f"el titular {self.titular} tiene un saldo de $ {self.saldo}"



# 1. Creamos la cuenta con 100 dólares
mi_cuenta = CuentaBancaria("Sebas", 100)

# 2. Depositamos 50 dólares más
mi_cuenta.depositar(50)

# 3. Vemos el resultado final
print(mi_cuenta.ver_balance())


print("----------------------------------------------------------------------------------------------------")
#-----------------------------------------------------------------------------------------------------------------
# Reto Final de Fase 2: El Sistema de Inventario 📦
# Imagina que tienes una tienda. Necesitas un molde para los Productos.
# Tu misión es crear la clase Producto.
# El Constructor (__init__): debe recibir nombre, precio y cantidad_stock.
# Método vender(unidades): * Este método debe recibir cuántas unidades se están vendiendo.
# Debe restar esas unidades del self.cantidad_stock.
# No necesita retornar nada, solo actualizar el stock.
# Método ver_info():
# Debe retornar una f-string que diga: "Producto: [nombre] | Precio: $[precio] | Stock: [cantidad_stock] unidades".
#-------------------------------------------------------------------------------------------------------------------
class inventario():
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self,unidades):
        self.stock =  self.stock - unidades 

    def ver_info(self):
        
        return f"producto {self.nombre} | precio:{self.precio} | stock:{self.stock} "

mi_item = inventario("camisa", 25 , 3)

mi_item.vender(1)

print(mi_item.ver_info())