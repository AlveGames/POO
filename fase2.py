# Definimos el molde
class Empleado:
    # El Constructor: inicializa los Atributos (características)
    def __init__(self, nombre_recibido, sueldo_recibido):
        self.nombre = nombre_recibido
        self.sueldo_bruto = sueldo_recibido

    # Un Método (acción): calcula y muestra el recibo
    def mostrar_recibo(self):
        descuento = self.sueldo_bruto * 0.09
        bono = 50
        total_neto = self.sueldo_bruto - descuento + bono
        return f"Empleado: {self.nombre} | Sueldo Neto: ${total_neto}"

# --- AQUÍ CREAMOS LOS OBJETOS ---
empleado1 = Empleado("Sebas", 1500)
empleado2 = Empleado("Maria", 2000)

# Usamos los objetos
print(empleado1.mostrar_recibo())
print(empleado2.mostrar_recibo())