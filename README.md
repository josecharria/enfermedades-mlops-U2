# Enfermedades MLOps - Unidad 2

## Descripción del problema

Se busca desarrollar una solución para apoyar a los profesionales de la salud en la clasificación de pacientes a partir de información relacionada con sus síntomas.

La solución inicial utiliza una función de clasificación simulada, desplegada mediante una aplicación web desarrollada con Flask y contenerizada con Docker.

## Propósito del repositorio

Este repositorio tiene como propósito mantener el control de versiones del proyecto, gestionar la evolución de la solución y automatizar las pruebas y el despliegue mediante GitHub Actions.

Durante esta unidad se incorporarán nuevas categorías de predicción, funcionalidades de consulta de estadísticas y un pipeline de integración y despliegue continuo (CI/CD).

## Estructura del repositorio

La estructura prevista del proyecto es:

- `app.py`: aplicación Flask y gestión de solicitudes.
- `modelo.py`: función de clasificación de enfermedades.
- `requirements.txt`: dependencias del proyecto.
- `Dockerfile`: instrucciones para construir la imagen Docker.
- `templates/`: interfaz web del sistema.
- `README.md`: documentación del proyecto.
- `tests/`: pruebas unitarias.
- `.github/workflows/`: automatización mediante GitHub Actions.

## Tecnologías

- Python
- Flask
- Docker
- Git y GitHub
- GitHub Actions
- Pytest

## Consideraciones

La clasificación implementada es una simulación académica. No constituye un diagnóstico médico ni reemplaza la valoración de un profesional de la salud.
