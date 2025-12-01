import src.interpreter as interpreter

def test_evaluar_entero():
    # Limpiamos variables globales antes de probar
    interpreter.variables.clear()
    interpreter.variables['x'] = 5
    result = interpreter.evaluar('x + 3')
    assert result == 8

