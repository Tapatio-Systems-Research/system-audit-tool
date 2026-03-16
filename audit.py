import os, platform, socket, hashlib, logging

# Configuración y Detección de OS
logging.basicConfig(format="%(asctime)s [TSR] %(message)s", level=logging.INFO)
FILES = [r'C:\Windows\System32\drivers\etc\hosts', r'C:\Windows\System32\config\SAM'] if os.name == 'nt' else ['/etc/shadow', '/etc/hosts', '/etc/passwd']

def get_hash(path):
    """Genera SHA-256. Retorna 'DENIED' si no hay permisos."""
    try:
        with open(path, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
    except: return "DENIED"

def run_audit():
    print(f"\n[TSR AUDIT] NODE: {socket.gethostname()} | OS: {platform.system()}\n" + "-"*55)
    for f in FILES:
        status = get_hash(f) if os.path.exists(f) else "NOT_FOUND"
        logging.info(f"{f:35} | {status[:15]}...")

if __name__ == "__main__": 
    run_audit()
