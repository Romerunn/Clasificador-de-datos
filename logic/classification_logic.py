import json

def cargar_diccionario(ruta='palabras_ponderadas.json'):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def puntaje(p_nota, p_clave_ponderada):
    result = 0
    for palabra in p_nota:
        result += p_clave_ponderada.get(palabra, 0)
    return result

def curso_mayor(p_nota, dicti):
    max_puntaje = 0
    result = ""
    for i in dicti:
        palabras_del_curso = dicti[i]["palabras_clave"]
        temp = puntaje(p_nota, palabras_del_curso)
        if max_puntaje < temp:
            max_puntaje = temp
            result = i
    return result

def limpiar_nota(nota):
    actual = ['á', 'é', 'í', 'ó', 'ú', '.', ',', ':', ';', '"', '(', ')', '?', '¿', '!', '¡', '\'']
    nuevo = ['a', 'e', 'i', 'o', 'u', '', '', '', '', '', '', '', '', '', '', '', '']
    for i in range(len(actual)):
        nota = nota.replace(actual[i], nuevo[i])
    return nota

def clasificar_nota(nota, diccionario):
    nota_limpia = limpiar_nota(nota.lower())
    palabras_nota = nota_limpia.split()
    curso = curso_mayor(palabras_nota, diccionario)
    return curso
