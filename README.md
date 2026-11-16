# Sistema de Clasificación de Enfermedades – MLOps

## 1. Finalidad de la solución

El proyecto consiste en desarrollar un servicio de clasificación de pacientes a partir de información relacionada con sus síntomas, utilizando una arquitectura basada en Python, Flask y Docker.

La solución recibe tres variables de entrada:

- **Cantidad de síntomas:** número de síntomas reportados por el paciente (entre 0 y 10).
- **Severidad:** intensidad de los síntomas en una escala de 0 a 10.
- **Duración:** tiempo de permanencia de los síntomas, expresado en días.

A partir de estos datos, el servicio genera una de las siguientes cinco categorías:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA
- ENFERMEDAD TERMINAL

Para este ejercicio académico se implementó una lógica de clasificación simulada mediante reglas condicionales. No se realizó entrenamiento de un modelo de Machine Learning.

La solución dispone de dos mecanismos de entrada: una interfaz web para el ingreso de información y un endpoint API que permite recibir solicitudes en formato JSON.

Adicionalmente, se implementó un mecanismo de registro persistente de las predicciones realizadas, junto con un módulo de estadísticas que permite consultar el total de predicciones, su distribución por categoría y las cinco predicciones más recientes.

**Nota:** Esta herramienta es una simulación académica y no constituye un diagnóstico médico ni reemplaza la valoración de un profesional de la salud.

## 2. Tecnologías utilizadas

- Python 3.12
- Flask 3.1.1
- tzdata
- Docker
- HTML y CSS
- API REST con respuestas JSON
- Almacenamiento de información mediante archivos JSON

## 3. Estructura del proyecto

```text
servicio_enfermedades/
│
├── app.py
├── modelo.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
│
├── data/
│   └── predicciones.json
│
└── templates/
    ├── index.html
    └── estadisticas.html
```

Descripción de los archivos:

- `app.py`: aplicación Flask, encargada de gestionar las solicitudes web, API, registro de predicciones y generación de estadísticas.
- `modelo.py`: contiene la función de clasificación de enfermedades.
- `requirements.txt`: especifica las dependencias de Python.
- `Dockerfile`: define las instrucciones para construir la imagen Docker.
- `templates/index.html`: contiene la interfaz web de evaluación.
- `templates/estadisticas.html`: presenta el reporte visual de estadísticas.
- `data/predicciones.json`: almacena el historial de predicciones realizadas. Se genera automáticamente durante la ejecución.
- `.gitignore`: excluye del control de versiones los registros generados y archivos temporales.

## 4. Requisitos previos

Para ejecutar la solución se requiere:

- Docker Desktop instalado y funcionando.
- Git Bash o una terminal compatible.
- Navegador web.

No es necesario instalar Python ni Flask directamente en el equipo, dado que las dependencias se instalan dentro de la imagen Docker.

## 5. Construcción de la imagen Docker

Abrir Git Bash y ubicarse en el directorio principal del proyecto:

```bash
cd ruta/servicio_enfermedades
```

Construir la imagen ejecutando:

```bash
docker build -t servicio-enfermedades .
```

Este comando utiliza las instrucciones del Dockerfile para crear una imagen que contiene Python, las dependencias y los archivos de la aplicación.

Para verificar que la imagen se haya construido correctamente:

```bash
docker images
```

## 6. Ejecución del contenedor

Crear la carpeta local para almacenar las predicciones:

```bash
mkdir -p data
```

Ejecutar el siguiente comando desde Git Bash:

```bash
MSYS_NO_PATHCONV=1 docker run -d \
  -p 5000:5000 \
  --name servicio-enfermedades \
  -v "$(pwd -W)/data:/data" \
  -e PREDICCIONES_FILE=/data/predicciones.json \
  servicio-enfermedades
```

El servicio quedará ejecutándose en segundo plano y el puerto 5000 del contenedor estará disponible desde el equipo local.

El volumen Docker permite mantener el historial de predicciones en la carpeta `data` del equipo, evitando que los registros se pierdan al reiniciar o eliminar el contenedor.

Para verificar su funcionamiento:

```bash
docker ps
```

Para consultar los registros de ejecución:

```bash
docker logs servicio-enfermedades
```

## 7. Obtener respuestas del servicio

### 7.1. Mediante la interfaz web

Abrir un navegador y acceder a:

http://localhost:5000

La página presenta un formulario en el que se ingresan los siguientes datos:

1. Cantidad de síntomas.
2. Severidad de los síntomas.
3. Duración de los síntomas en días.

Al seleccionar el botón **Evaluar paciente**, la aplicación procesa la información y presenta la categoría obtenida.

### 7.2. Mediante el endpoint API de predicción

También es posible consultar el servicio mediante solicitudes HTTP POST al endpoint:

`http://localhost:5000/predecir`

La solicitud debe enviarse en formato JSON, incluyendo los tres campos requeridos.

**Ejemplo de solicitud:**

```bash
curl -X POST http://localhost:5000/predecir \
-H "Content-Type: application/json" \
-d '{"num_sintomas":5,"severidad":9,"duracion":3}'
```

**Respuesta esperada:**

```json
{
  "prediccion": "ENFERMEDAD AGUDA"
}
```

### 7.3. Ejemplos de clasificación

| Síntomas | Severidad | Duración (días) | Resultado |
|---:|---:|---:|---|
| 0 | 0 | 0 | NO ENFERMO |
| 2 | 3 | 5 | ENFERMEDAD LEVE |
| 5 | 9 | 3 | ENFERMEDAD AGUDA |
| 4 | 5 | 120 | ENFERMEDAD CRÓNICA |
| 5 | 9 | 365 | ENFERMEDAD TERMINAL |

Estos resultados corresponden a las reglas de clasificación implementadas en `modelo.py`.

## 8. Registro y consulta de estadísticas

Cada predicción realizada, tanto desde la interfaz web como desde el endpoint API, se almacena en el archivo `data/predicciones.json`.

El registro contiene:

- Fecha y hora de la predicción.
- Cantidad de síntomas.
- Severidad.
- Duración.
- Categoría obtenida.

El sistema dispone de un módulo de estadísticas que presenta:

- Total de predicciones realizadas.
- Cantidad de predicciones por cada una de las cinco categorías.
- Las últimas cinco predicciones registradas.
- Fecha y hora de la última predicción.

### 8.1. Reporte visual

Acceder desde el navegador a:

http://localhost:5000/estadisticas

Esta ruta presenta la información mediante una interfaz web.

### 8.2. Reporte mediante API

También es posible consultar las estadísticas mediante una solicitud HTTP GET al endpoint:

`http://localhost:5000/api/estadisticas`

Ejemplo:

```bash
curl http://localhost:5000/api/estadisticas
```

El servicio devuelve la información estadística en formato JSON.

## 9. Detener y eliminar el contenedor

Para detener el servicio:

```bash
docker stop servicio-enfermedades
```

Para eliminar el contenedor:

```bash
docker rm servicio-enfermedades
```

La imagen permanece disponible y puede utilizarse nuevamente para crear otro contenedor.

Los registros de predicciones permanecen almacenados en la carpeta local `data`, gracias al volumen configurado durante la ejecución del contenedor.

## 10. Consideraciones finales

La solución demuestra la contenerización y puesta en funcionamiento de un servicio de clasificación mediante Docker. La separación entre la lógica de clasificación (`modelo.py`) y la aplicación de servicio (`app.py`) facilita su mantenimiento y actualización.

La incorporación del registro persistente y del módulo de estadísticas permite realizar seguimiento a las predicciones generadas por el servicio.

La arquitectura permite reemplazar en el futuro las reglas simuladas por un modelo de Machine Learning entrenado, manteniendo los mecanismos de acceso mediante la interfaz web y los endpoints API.