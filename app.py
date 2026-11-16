
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request, jsonify, render_template
from modelo import predecir_enfermedad

app = Flask(__name__)

# Archivo donde se almacenan las predicciones.
# En Docker utilizaremos /data para conservar los registros.
ARCHIVO_PREDICCIONES = os.environ.get(
    "PREDICCIONES_FILE",
    "data/predicciones.json"
)

CATEGORIAS = [
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
    "ENFERMEDAD TERMINAL"
]


# Cargar el historial de predicciones
def cargar_predicciones():

    if not os.path.exists(ARCHIVO_PREDICCIONES):
        return []

    with open(ARCHIVO_PREDICCIONES, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# Guardar una nueva predicción
def guardar_prediccion(num_sintomas, severidad, duracion, resultado):

    predicciones = cargar_predicciones()

    nueva_prediccion = {
        "fecha": datetime.now(ZoneInfo("America/Bogota")).isoformat(timespec="seconds"),
        "num_sintomas": num_sintomas,
        "severidad": severidad,
        "duracion": duracion,
        "prediccion": resultado
    }

    predicciones.append(nueva_prediccion)

    directorio = os.path.dirname(ARCHIVO_PREDICCIONES)

    if directorio:
        os.makedirs(directorio, exist_ok=True)

    with open(ARCHIVO_PREDICCIONES, "w", encoding="utf-8") as archivo:
        json.dump(predicciones, archivo, ensure_ascii=False, indent=4)


# Generar el reporte estadístico
def generar_estadisticas():

    predicciones = cargar_predicciones()

    # Inicializar las cinco categorías en cero
    conteo_categorias = {
        categoria: 0 for categoria in CATEGORIAS
    }

    # Contabilizar las predicciones
    for prediccion in predicciones:
        categoria = prediccion["prediccion"]

        if categoria in conteo_categorias:
            conteo_categorias[categoria] += 1

    # Obtener las últimas cinco predicciones
    ultimas_predicciones = list(reversed(predicciones[-5:]))

    # Fecha de la última predicción
    fecha_ultima = (
        predicciones[-1]["fecha"] if predicciones else None
    )

    return {
        "total_predicciones": len(predicciones),
        "por_categoria": conteo_categorias,
        "ultimas_5_predicciones": ultimas_predicciones,
        "fecha_ultima_prediccion": fecha_ultima
    }


# Página principal
@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")


# Evaluación desde el formulario web
@app.route("/evaluar", methods=["POST"])
def evaluar():

    try:
        num_sintomas = int(request.form["num_sintomas"])
        severidad = int(request.form["severidad"])
        duracion = int(request.form["duracion"])

        resultado = predecir_enfermedad(
            num_sintomas,
            severidad,
            duracion
        )

        # Registrar la predicción
        guardar_prediccion(
            num_sintomas,
            severidad,
            duracion,
            resultado
        )

        return render_template(
            "index.html",
            resultado=resultado
        )

    except (ValueError, KeyError) as e:
        return render_template(
            "index.html",
            error=str(e)
        ), 400


# Endpoint para solicitudes API
@app.route("/predecir", methods=["POST"])
def predecir():

    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "error": "Debe enviar los datos del paciente."
            }), 400

        num_sintomas = int(datos["num_sintomas"])
        severidad = int(datos["severidad"])
        duracion = int(datos["duracion"])

        resultado = predecir_enfermedad(
            num_sintomas,
            severidad,
            duracion
        )

        # Registrar la predicción
        guardar_prediccion(
            num_sintomas,
            severidad,
            duracion,
            resultado
        )

        return jsonify({
            "prediccion": resultado
        })

    except (ValueError, TypeError, KeyError) as e:
        return jsonify({
            "error": str(e)
        }), 400


# Endpoint para consultar las estadísticas
@app.route("/estadisticas", methods=["GET"])
def estadisticas():

    try:
        reporte = generar_estadisticas()

        return render_template(
            "estadisticas.html",
            reporte=reporte
        )

    except (OSError, json.JSONDecodeError, KeyError) as e:
        return jsonify({
            "error": f"No fue posible generar el reporte: {str(e)}"
        }), 500

@app.route("/api/estadisticas", methods=["GET"])
def api_estadisticas():
    try:
        return jsonify(generar_estadisticas())

    except (OSError, json.JSONDecodeError, KeyError) as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

