def recorrer(elemento):
    for item in elemento:
        print(f"el elemento es: {item}")

lista1 = [1,2,3,4]
lista2 = ["mamawevo", "ff y desinstala"]
deletrea1 = "7w7"
recorrer(lista1)
recorrer(lista2)
recorrer(deletrea1)

print("_________________________________________________")

class Perro():
        def sonido(self):
                return "guau"

class Gato():
        def sonido(self):
            return "miau"

gato = Gato()
perro = Perro()

print(gato.sonido())