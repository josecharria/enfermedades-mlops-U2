
def predecir_enfermedad(num_sintomas, severidad, duracion):

    # Validación de los datos
    if not (0 <= num_sintomas <= 10):
        raise ValueError("La cantidad de síntomas debe estar entre 0 y 10.")

    if not (0 <= severidad <= 10):
        raise ValueError("La severidad debe estar entre 0 y 10.")

    if duracion < 0:
        raise ValueError("La duración no puede ser negativa.")

    # Reglas simuladas para el ejercicio
    if num_sintomas == 0 or severidad == 0:
        resultado = "NO ENFERMO"

    elif severidad >= 8 and duracion >= 365:
        resultado = "ENFERMEDAD TERMINAL"

    elif duracion >= 90:
        resultado = "ENFERMEDAD CRÓNICA"

    elif severidad >= 8 and duracion < 14:
        resultado = "ENFERMEDAD AGUDA"

    else:
        resultado = "ENFERMEDAD LEVE"

    return resultado

