import subprocess   # ← acá estaba el bug, faltaba este import
import platform

def valid_target(target):
    try:                                    # ← try/except que faltaba antes
        flag = "-n" if platform.system() == "Windows" else "-c"
        results = subprocess.run(
            ["ping", flag, "2", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return results.returncode == 0
    except Exception:
        return False                        # Si algo falla, el target no es válido