import subprocess
import os

# ============================================================
#  UTILIDADES
# ============================================================

def save_results(target, tool_name, results):
    filename = f"{target}_{tool_name}_results.txt"
    with open(filename, "w") as archivo:
        archivo.write(results)
    print(f"[+] Resultados guardados en {filename}")


def print_output(results):
    print("===== Resultado =====")
    print(results)


def get_target():
    target = input("Ingrese el dominio o IP del objetivo: ")
    return target


def valid_target(target):
    result = subprocess.run(
        ["ping", "-c", "2", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


# ============================================================
#  FUNCIÓN GENÉRICA (la lavadora)
# ============================================================

def run_tool(command, timeout=60):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return f"Error: {command[0]} tardó demasiado"
    except FileNotFoundError:
        return f"Error: {command[0]} no está instalado o no está en el PATH"


# ============================================================
#  HERRAMIENTAS (cada una arma su comando y llama run_tool)
# ============================================================

def run_nmap(target):
    return run_tool(["nmap", "-Pn", "-sV", "--top-ports", "1000", target], timeout=120)

def run_whois(target):
    return run_tool(["whois", "-H", target], timeout=30)

def run_nslookup(target):
    return run_tool(["nslookup", target], timeout=30)

def run_dig(target):
    # ANY pide todos los registros DNS disponibles
    return run_tool(["dig", target, "ANY", "+noall", "+answer"], timeout=30)

def run_httpx(target):
    # -title muestra el título de la página, -tech-detect detecta tecnologías
    return run_tool(["httpx", "-u", target, "-title", "-tech-detect", "-status-code"], timeout=60)

def run_whatweb(target):
    return run_tool(["whatweb", target], timeout=60)

def run_wafw00f(target):
    return run_tool(["wafw00f", target], timeout=60)

def run_sslscan(target):
    return run_tool(["sslscan", "--no-colour", target], timeout=60)


# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":

    target = get_target()

    if not valid_target(target):
        print("[-] Objetivo no válido o inaccesible.")
        exit()

    # Diccionario: nombre legible → función
    herramientas = {
        "nmap":     run_nmap,
        "whois":    run_whois,
        "nslookup": run_nslookup,
        "dig":      run_dig,
        "httpx":    run_httpx,
        "whatweb":  run_whatweb,
        "wafw00f":  run_wafw00f,
        "sslscan":  run_sslscan,
    }

    print("\nHerramientas disponibles:")
    for i, nombre in enumerate(herramientas, start=1):
        print(f"  {i}. {nombre}")

    print(f"  {len(herramientas) + 1}. Correr TODAS")

    eleccion = input("\nElegí una opción: ")

    # Correr todas
    if eleccion == str(len(herramientas) + 1):
        for nombre, funcion in herramientas.items():
            print(f"\n[*] Corriendo {nombre}...")
            resultado = funcion(target)
            save_results(target, nombre, resultado)
            print_output(resultado)

    # Correr una sola
    elif eleccion.isdigit() and 1 <= int(eleccion) <= len(herramientas):
        nombre = list(herramientas.keys())[int(eleccion) - 1]
        funcion = herramientas[nombre]
        print(f"\n[*] Corriendo {nombre}...")
        resultado = funcion(target)
        save_results(target, nombre, resultado)
        print_output(resultado)

    else:
        print("[-] Opción inválida.")