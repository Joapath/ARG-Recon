from runner import run_tool   # ← importa la lavadora desde runner.py

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