import subprocess

# La "lavadora" - todas las herramientas pasan por acá

def run_tool(command, timeout=50):
    try:
        results = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if results.returncode == 0:
            return results.stdout
        else:
            return f"Error: \n{results.stderr}"

    except subprocess.TimeoutExpired:
        return f"Error: {' '.join(command)} tardó demasiado en responder"
    except FileNotFoundError:
        return f"Error: {' '.join(command)} no está instalado"
    except Exception as e:
        return f"Error inesperado: {e}"