import subprocess

# ============================================================
#  UTILIDADES
# ============================================================

def save_results(target, results):
    filename = f"{target}_results.txt"
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
    results = subprocess.run(             # CAMBIO: indentación corregida, estaba indentado de más
        ["ping", "-c", "2", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return results.returncode == 0

# ============================================================
#  FUNCIÓN GENÉRICA (la lavadora)
# ============================================================

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
        return f"Error: {' '.join(command)} tardo demasiado en responder"
    except FileNotFoundError:
        return f"Error: {' '.join(command)} no esta instalado"

# ============================================================
#  HERRAMIENTAS (cada una arma su comando y llama run_tool)
# ============================================================

def run_nmap(target):
    return run_tool(["nmap", "-sV", "--top-ports", "1000", target], timeout=120)

def run_whois(target):
    return run_tool(["whois", target, "-H"], timeout=30)

def run_nslookup(target):
    return run_tool(["nslookup", target], timeout=30)

def run_dig(target):
    return run_tool(["dig", target, "ANY", "+noall", "+answer"], timeout=30)

def run_httpx(target):
    return run_tool(["httpx", "-d", target, "-title", "-tech-detect", "-sc"], timeout=60)

def run_wafw00f(target):
    return run_tool(["wafw00f", target], timeout=60)

# ============================================================
#  MENU
# ============================================================

def show_menu():
    print("""
    1. Nmap
    2. Whois
    3. DNS (dig + nslookup)
    4. Web (httpx + wafw00f)
    5. Todo
    0. Salir
""")

# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    target = get_target()

    if not valid_target(target):                        # CAMBIO: if not + exit temprano, evita anidar todo en un if
        print("[-] Objetivo no válido o inaccesible.")
        exit()

    show_menu()
    option = input("Seleccione una opcion: ")           # CAMBIO: agregué ": " al final para que se vea bien

    match option:
        case "1":
            result =(
            "\n\n==== NMAP ====\n\n" +
            run_nmap(target)
                )
        case "2":
            result = (
                 "\n\n==== WHOIS ====\n\n" +
                 run_whois(target)
                )
        case "3":
            result = (
                "\n\n==== DIG ====\n\n" +
                run_dig(target) +
                "\n\n==== NSLOOKUP ====\n\n" +
                run_nslookup(target)
            )

        case "4":
            result = (
                "\n\n==== HTTPX ====\n\n" +               # CAMBIO: saqué el ==== TECNOLOGIAS WEB ==== que era redundante
                run_httpx(target) +
                "\n\n==== WAFW00F ====\n\n" +             # CAMBIO: corregí "WAFW00f" → "WAFW00F" para consistencia
                run_wafw00f(target)
            )

        case "5":
            result = (
                "==== NMAP ====\n" + run_nmap(target) +
                "\n\n==== WHOIS ====\n" + run_whois(target) +
                "\n\n==== DIG ====\n" + run_dig(target) +
                "\n\n==== NSLOOKUP ====\n" + run_nslookup(target) +
                "\n\n==== HTTPX ====\n" + run_httpx(target) +
                "\n\n==== WAFW00F ====\n" + run_wafw00f(target)
            )

        case "0":                                         # CAMBIO: era print() + exit() lo cual rompe Python
            print("Saliendo...")                          # print() devuelve None, None + exit() es error
            exit()

        case _:                                           # CAMBIO: era case "_": con comillas, eso nunca matchea
            print("Opcion invalida")                      # el default de match es case _: sin comillas
            exit()

    save_results(target, result)                          # CAMBIO: moví save y print fuera del match,
    print_output(result)                                  # estaban dentro de algunos cases y en otros no, inconsistente
