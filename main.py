from utils import get_target, show_menu, save_results, print_output
from validator import valid_target
from tools import run_nmap, run_whois, run_dig, run_nslookup, run_httpx, run_wafw00f

# ↑ Cada import le dice a Python "busca ese archivo en la misma carpeta"

if __name__ == "__main__":
    target = get_target()

    if not valid_target(target):
        print("[-] Objetivo no válido o inaccesible.")
        exit()

    show_menu()
    option = input("Seleccione una opcion: ")

    match option:
        case "1":
            result = run_nmap(target)
            save_results(target, result)
            print_output(result)

        case "2":
            result = run_whois(target)
            save_results(target, result)
            print_output(result)

        case "3":
            result = (
                "\n\n==== DIG ====\n\n" + run_dig(target) +
                "\n\n==== NSLOOKUP ====\n\n" + run_nslookup(target)
            )
            save_results(target, result)
            print_output(result)

        case "4":
            result = (
                "\n\n==== HTTPX ====\n\n" + run_httpx(target) +
                "\n\n==== WAFW00F ====\n\n" + run_wafw00f(target)
            )
            save_results(target, result)
            print_output(result)

        case "5":
            result = (
                "==== NMAP ====\n" + run_nmap(target) +
                "\n\n==== WHOIS ====\n" + run_whois(target) +
                "\n\n==== DIG ====\n" + run_dig(target) +
                "\n\n==== NSLOOKUP ====\n" + run_nslookup(target) +
                "\n\n==== HTTPX ====\n" + run_httpx(target) +
                "\n\n==== WAFW00F ====\n" + run_wafw00f(target)
            )
            save_results(target, result)
            print_output(result)

        case "0":
            print("Saliendo...")
            exit()

        case _:
            print("Opcion invalida")