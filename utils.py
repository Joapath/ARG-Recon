from datetime import datetime

def generate_filename(target):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(".", "_").replace("/", "_")
    return f"{safe_target}_{timestamp}.txt"


def save_results(target, result):
    filename = generate_filename(target)
    with open(filename, "w", encoding="utf-8") as archivo:
        if isinstance(result, list):
            for item in result:
                archivo.write(str(item) + "\n")
        else:
            archivo.write(str(result))
    print(f"[+] Resultados guardados en {filename}")


def print_output(result):
    print("\n===== Resultado =====")
    print(result)


def get_target():
    target = input("Ingrese el dominio o IP del objetivo: ")
    return target


def show_menu():
    print("""
    1. Nmap
    2. Whois
    3. DNS (dig + nslookup)
    4. Web (httpx + wafw00f)
    5. Todo
    0. Salir
""")