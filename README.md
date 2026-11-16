# Sistema de Clasificación de Enfermedades – MLOps

## 1. Finalidad de la solución

El proyecto consiste en desarrollar un servicio de clasificación de pacientes a partir de información relacionada con sus síntomas, utilizando una arquitectura basada en Python, Flask y Docker.

La solución recibe tres variables de entrada:

- **Cantidad de síntomas:** número de síntomas reportados por el paciente (entre 0 y 10).
- **Severidad:** intensidad de los síntomas en una escala de 0 a 10.
- **Duración:** tiempo de permanencia de los síntomas, expresado en días.

A partir de estos datos, el servicio genera una de las siguientes cuatro categorías:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA

Para este ejercicio académico se implementó una lógica de clasificación simulada mediante reglas condicionales. No se realizó entrenamiento de un modelo de Machine Learning.

La solución dispone de dos mecanismos de entrada: una interfaz web sencilla para el ingreso de información y un endpoint API que permite recibir solicitudes en formato JSON.

**Nota:** Esta herramienta es una simulación académica y no constituye un diagnóstico médico ni reemplaza la valoración de un profesional de la salud.

## 2. Tecnologías utilizadas

- Python 3.12
- Flask 3.1.1
- Docker
- HTML y CSS
- API REST con respuestas JSON

## 3. Estructura del proyecto

```text
servicio_enfermedades/
│
├── app.py
├── modelo.py
├── requirements.txt
├── Dockerfile
├── README.md
│
└── templates/
    └── index.html
```

Descripción de los archivos:

- `app.py`: aplicación Flask, encargada de gestionar las solicitudes web y API.
- `modelo.py`: contiene la función de clasificación de enfermedades.
- `requirements.txt`: especifica las dependencias de Python.
- `Dockerfile`: define las instrucciones para construir la imagen Docker.
- `templates/index.html`: contiene la interfaz web del sistema.
- `README.md`: documentación e instrucciones de ejecución.

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

Este comando utiliza las instrucciones del Dockerfile para crear una imagen que contiene Python, Flask y los archivos de la aplicación.

Para verificar que la imagen se haya construido correctamente:

```bash
docker images
```

## 6. Ejecución del contenedor

Ejecutar el siguiente comando:

```bash
docker run -d -p 5000:5000 --name servicio-enfermedades servicio-enfermedades
```

El servicio quedará ejecutándose en segundo plano y el puerto 5000 del contenedor estará disponible desde el equipo local.

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

### 7.2. Mediante el endpoint API

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

Estos resultados corresponden a las reglas de clasificación implementadas en `modelo.py`.

## 8. Detener y eliminar el contenedor

Para detener el servicio:

```bash
docker stop servicio-enfermedades
```

Para eliminar el contenedor:

```bash
docker rm servicio-enfermedades
```

La imagen permanece disponible y puede utilizarse nuevamente para crear otro contenedor.

## 9. Consideraciones finales

La solución demuestra la contenerización y puesta en funcionamiento de un servicio de clasificación mediante Docker. La separación entre la lógica de clasificación (`modelo.py`) y la aplicación de servicio (`app.py`) facilita su mantenimiento y actualización.

La arquitectura permite reemplazar en el futuro las reglas simuladas por un modelo de Machine Learning entrenado, manteniendo los mecanismos de acceso mediante la interfaz web y el endpoint API.