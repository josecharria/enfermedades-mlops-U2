
from flask import Flask, request, jsonify, render_template
from modelo import predecir_enfermedad

app = Flask(__name__)


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

        return jsonify({
            "prediccion": resultado
        })

    except (ValueError, TypeError, KeyError) as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

