import json

datos = {"producto": "camisa", "stock": 7}

# Para guardar (Write):
with open("inventario.json", "w") as archivo:
    json.dump(datos, archivo)


# Para leer (Read):
with open("inventario.json", "r") as archivo:
    datos_leidos = json.load(archivo)
    
print(f"Recuperado stock: {datos_leidos['stock']}")

print("-----------------------------------------------------------------------")

input 