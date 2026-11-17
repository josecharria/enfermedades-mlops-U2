
import pytest
from modelo import predecir_enfermedad


def test_clasificacion_no_enfermo():
    resultado = predecir_enfermedad(0, 0, 0)
    assert resultado == "NO ENFERMO"


def test_clasificacion_enfermedad_aguda():
    resultado = predecir_enfermedad(5, 9, 3)
    assert resultado == "ENFERMEDAD AGUDA"


def test_clasificacion_enfermedad_terminal():
    resultado = predecir_enfermedad(5, 9, 365)
    assert resultado == "ENFERMEDAD TERMINAL"


def test_validacion_numero_sintomas():
    with pytest.raises(ValueError):
        predecir_enfermedad(11, 5, 10)
