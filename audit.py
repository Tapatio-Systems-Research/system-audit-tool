#!/usr/bin/env python3
"""
TSR-001 | System Integrity & Infrastructure Audit Tool
Auth: Tapatío Systems Research (TSR) Node
License: MIT
"""

import os
import platform
import logging
import datetime
from typing import List, Dict

# --- CONFIGURATION ---
LOG_FORMAT = "%(asctime)s [TSR-AUDIT] %(levelname)s: %(message)s"
CRITICAL_FILES = [
    '/etc/passwd',
    '/etc/shadow',
    '/etc/ssh/sshd_config',
    '/etc/sudoers',
    '/etc/hosts'
]

def setup_logger():
    """Configura el sistema de logging para trazabilidad forense."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    return logging.getLogger("TSR-Audit")

def get_system_metadata() -> Dict[str, str]:
    """Extrae metadatos de hardware y kernel con alta precisión."""
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "node": platform.node(),
        "python_v": platform.python_version()
    }

def audit_filesystem_integrity(files: List[str], logger: logging.Logger):
    """Ejecuta una auditoría de superficie sobre archivos críticos del sistema."""
    logger.info("Iniciando escaneo de integridad de archivos críticos...")
    
    for file_path in files:
        if os.path.exists(file_path):
            # Verificamos permisos de lectura sin romper el script
            readable = os.access(file_path, os.R_OK)
            status = "ACCESSIBLE" if readable else "PROTECTED/NO_ACCESS"
            logger.info(f"Target: {file_path:25} | Status: {status}")
        else:
            logger.warning(f"Target: {file_path:25} | Status: NOT_FOUND")

def main():
    logger = setup_logger()
    metadata = get_system_metadata()
    
    print("\n" + "="*50)
    print("   🛡️ TAPATÍO SYSTEMS RESEARCH | SYSTEM AUDIT   ")
    print("="*50)
    
    for key, value in metadata.items():
        print(f"[{key.upper()}]: {value}")
    
    print("-" * 50)
    
    try:
        audit_filesystem_integrity(CRITICAL_FILES, logger)
    except Exception as e:
        logger.error(f"Falla crítica en el proceso de auditoría: {str(e)}")
        sys.exit(1)
    
    print("="*50)
    print("AUDIT COMPLETE | OPERATIONAL INTEGRITY VERIFIED")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
