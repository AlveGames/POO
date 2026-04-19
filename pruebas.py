import json
usuario = {
    "nom" : "sebas",
}

with open("perfil.json", "w") as creararchivo:
    json.dump(usuario,creararchivo)

print("se guardo el perfil")
