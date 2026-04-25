import subprocess
import os

# ============================================================
#  UTILIDADES
# ============================================================

def save_results(target, results): # REGALA ORO: si es string → write() si es lista → for + write()
    
    
    filename = f"{target}_results.txt"

    with open(filename, "w") as archivo:
        archivo.write(results)

    print(f" Resultados guardados en {filename}")

   

def print_output(results):
    print("===== Resultado =====")
    print(results)


def get_target(): # Como solo pide input no necesita parametros
    
    target = input("Ingrese el dominio o IP del objetivo: ")
    return target

def valid_target(target):
    
    
        results = subprocess.run(["ping", "-c", "2", target],
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
        return f"Error: {' '.join(command)} tardo demasiado en responder" #lista → join → string legible
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
    return run_tool(["httpx", "-u", target, "-title", "-tech-detect", "-sc"], timeout=60)

def run_wafw00f(target):
    return run_tool(["waffw00f", target], timeout=60)       

# ============================================================
#   MAIN
# ============================================================

if __name__ == "__main__":
    target = get_target()

    if valid_target(target):

        nmap_resp = run_nmap(target)
        whois_resp = run_whois(target)
        dig_resp = run_dig(target)
        nslookup_resp = run_nslookup(target)
        httpx_resp = run_httpx(target)
        wafw00f_resp = run_wafw00f(target)

        # Ejecutar las tool
        final_result = (
            "==== NMAP ====\n" +
            nmap_resp +
            "\n\n==== WHOIS ====\n" +   
            whois_resp +
            "\n\n==== DIG ====" +
            dig_resp +
            "\n\n==== NSLOOKUP ====" +
            nslookup_resp +
            "\n\n==== HTTPX ====" +
            httpx_resp +
            "\n\n==== WAFW00F ====" +
            wafw00f_resp 
         )
        save_results(target, final_result)
        print_output(final_result)
    
    else:
        print("Objetivo no valido")
