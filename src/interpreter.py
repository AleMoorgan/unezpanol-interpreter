# --- INTERPRETE SIMPLE: UNEZPAÑOL (v1.1) ---
import re

# Tabla de símbolos global
variables = {}

def evaluar(expr):
    expr_sustituida = expr
    for nombre, valor in variables.items():
        expr_sustituida = re.sub(rf'\b{nombre}\b', repr(valor), expr_sustituida)
    try:
        return eval(expr_sustituida)
    except Exception as e:
        raise ValueError(f"Error al evaluar '{expr}' (transformada a '{expr_sustituida}'): {e}")

def interpretar(codigo):
    i = 0
    while i < len(codigo):
        linea = codigo[i].strip()

        if linea == "" or linea.startswith("#"):
            i += 1
            continue

        m = re.match(r'(entero|cadena)\s+(\w+)\s*=\s*(.+);', linea)
        if m:
            tipo, nombre, valor_expr = m.groups()
            valor_expr = valor_expr.strip()

            if tipo == "cadena":
                variables[nombre] = valor_expr.strip('"')
            elif tipo == "entero":
                variables[nombre] = int(evaluar(valor_expr))

            i += 1
            continue

        m = re.match(r'Imprimir\((.+)\);', linea)
        if m:
            print(evaluar(m.group(1).strip()))
            i += 1
            continue

        if re.match(r'Pausar\(\);', linea):
            input("\n[Ejecución pausada] Presiona ENTER para continuar...\n")
            i += 1
            continue

        if linea.startswith("Si") and "Entonces" in linea:
            condicion = re.findall(r'Si\s+(.+)\s+Entonces', linea)[0].strip()
            bloque = []
            i += 1
            nivel = 1

            while i < len(codigo) and nivel > 0:
                l = codigo[i].strip()
                if l.startswith("Si") and "Entonces" in l:
                    nivel += 1
                elif l == "FinSi":
                    nivel -= 1
                    if nivel == 0:
                        i += 1
                        break
                if nivel > 0:
                    bloque.append(codigo[i])
                i += 1

            if evaluar(condicion):
                interpretar(bloque)
            continue

        if linea.startswith("Mientras") and "Hacer" in linea:
            condicion = re.findall(r'Mientras\s+(.+)\s+Hacer', linea)[0].strip()
            bloque = []
            i += 1
            nivel = 1

            while i < len(codigo) and nivel > 0:
                l = codigo[i].strip()
                if l.startswith("Mientras") and "Hacer" in l:
                    nivel += 1
                elif l == "FinMientras":
                    nivel -= 1
                    if nivel == 0:
                        i += 1
                        break
                if nivel > 0:
                    bloque.append(codigo[i])
                i += 1

            contador_seguridad = 0
            while evaluar(condicion):
                interpretar(bloque)
                contador_seguridad += 1
                if contador_seguridad > 10000:
                    raise RuntimeError("Bucle infinito detectado.")
            continue

        raise SyntaxError(f"Línea no reconocida: {linea}")
