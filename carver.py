#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         LOST DATA RETRIEVAL — FILE CARVER           ║
║         Análisis Forense Digital | kaleth4          ║
╚══════════════════════════════════════════════════════╝
Recupera archivos eliminados/corruptos desde imágenes
de disco raw usando detección por Magic Numbers.
"""

import os
import sys
import json
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────────
# FIRMAS DE ARCHIVOS (Magic Numbers)
# ─────────────────────────────────────────────────────
SIGNATURES = {
    "jpg": {
        "ext":    ".jpg",
        "header": b'\xff\xd8\xff',
        "footer": b'\xff\xd9',
        "max_size": 10 * 1024 * 1024,  # 10 MB
    },
    "png": {
        "ext":    ".png",
        "header": b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
        "footer": b'\x49\x45\x4e\x44\xae\x42\x60\x82',
        "max_size": 20 * 1024 * 1024,  # 20 MB
    },
    "pdf": {
        "ext":    ".pdf",
        "header": b'\x25\x50\x44\x46',
        "footer": b'\x25\x25\x45\x4f\x46',
        "max_size": 50 * 1024 * 1024,  # 50 MB
    },
    "zip": {
        "ext":    ".zip",
        "header": b'\x50\x4b\x03\x04',
        "footer": b'\x50\x4b\x05\x06',
        "max_size": 100 * 1024 * 1024, # 100 MB
    },
    "gif": {
        "ext":    ".gif",
        "header": b'\x47\x49\x46\x38',
        "footer": b'\x00\x3b',
        "max_size": 5 * 1024 * 1024,   # 5 MB
    },
}

# ─────────────────────────────────────────────────────
# COLORES (sin dependencias externas)
# ─────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    GRAY   = "\033[90m"

def banner():
    print(f"""{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════╗
║         🔍 LOST DATA RETRIEVAL — CARVER             ║
║         Análisis Forense Digital | kaleth4          ║
╚══════════════════════════════════════════════════════╝{C.RESET}
""")

# ─────────────────────────────────────────────────────
# NÚCLEO: FILE CARVING
# ─────────────────────────────────────────────────────
def carve_files(imagen: str, salida: str, formatos: list, verbose: bool) -> list:
    """
    Escanea imagen raw byte a byte buscando Magic Numbers.
    Retorna lista de archivos recuperados con metadata.
    """
    resultados = []

    if not os.path.isfile(imagen):
        print(f"{C.RED}[✗] Archivo no encontrado: {imagen}{C.RESET}")
        sys.exit(1)

    os.makedirs(salida, exist_ok=True)
    tamano_imagen = os.path.getsize(imagen)

    print(f"{C.CYAN}[*] Imagen     : {imagen}{C.RESET}")
    print(f"{C.CYAN}[*] Tamaño     : {tamano_imagen / (1024*1024):.2f} MB{C.RESET}")
    print(f"{C.CYAN}[*] Formatos   : {', '.join(formatos).upper()}{C.RESET}")
    print(f"{C.CYAN}[*] Salida     : {salida}/{C.RESET}")
    print(f"{C.GRAY}{'─' * 54}{C.RESET}\n")

    with open(imagen, "rb") as f:
        raw = f.read()

    contador_total = 0

    for fmt in formatos:
        if fmt not in SIGNATURES:
            print(f"{C.YELLOW}[!] Formato desconocido: {fmt} — omitido{C.RESET}")
            continue

        sig    = SIGNATURES[fmt]
        header = sig["header"]
        footer = sig["footer"]
        ext    = sig["ext"]
        maxsz  = sig["max_size"]

        contador_fmt = 0
        idx = 0

        while True:
            inicio = raw.find(header, idx)
            if inicio == -1:
                break

            fin = raw.find(footer, inicio + len(header))
            if fin == -1:
                idx = inicio + len(header)
                continue

            fin += len(footer)

            # Validar tamaño para evitar falsos positivos gigantes
            tam = fin - inicio
            if tam > maxsz:
                idx = inicio + len(header)
                continue

            datos = raw[inicio:fin]
            contador_fmt  += 1
            contador_total += 1

            nombre = os.path.join(salida, f"{fmt}_recuperado_{contador_fmt}{ext}")
            with open(nombre, "wb") as out:
                out.write(datos)

            info = {
                "archivo":  nombre,
                "formato":  fmt.upper(),
                "offset":   hex(inicio),
                "tamano":   tam,
                "tamano_kb": round(tam / 1024, 2),
            }
            resultados.append(info)

            if verbose:
                print(f"  {C.GREEN}[+]{C.RESET} {fmt.upper()} → {os.path.basename(nombre)}"
                      f"  {C.GRAY}offset: {hex(inicio)}  |  {tam} bytes{C.RESET}")

            idx = fin

        if contador_fmt > 0:
            print(f"  {C.BOLD}{fmt.upper()}{C.RESET}: {C.GREEN}{contador_fmt} archivo(s) recuperado(s){C.RESET}")
        else:
            print(f"  {C.YELLOW}{fmt.upper()}: sin resultados{C.RESET}")

    print(f"\n{C.GRAY}{'─' * 54}{C.RESET}")
    print(f"{C.BOLD}[✓] Total recuperados: {C.GREEN}{contador_total}{C.RESET}")
    return resultados


# ─────────────────────────────────────────────────────
# REPORTE JSON
# ─────────────────────────────────────────────────────
def generar_reporte(resultados: list, salida: str, imagen: str):
    reporte = {
        "fecha":          datetime.now().isoformat(),
        "imagen_fuente":  imagen,
        "total_archivos": len(resultados),
        "archivos":       resultados,
    }
    ruta = os.path.join(salida, "reporte_forense.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    print(f"{C.CYAN}[*] Reporte JSON guardado: {ruta}{C.RESET}")


# ─────────────────────────────────────────────────────
# GENERADOR DE IMAGEN DE PRUEBA
# ─────────────────────────────────────────────────────
def crear_imagen_prueba(ruta: str):
    """Crea un binario sintético con JPEGs embebidos para probar el carver."""
    jpg_falso_1 = b'\xff\xd8\xff' + b'\xab\xcd\xef' * 200 + b'\xff\xd9'
    jpg_falso_2 = b'\xff\xd8\xff' + b'\x11\x22\x33' * 150 + b'\xff\xd9'

    with open(ruta, "wb") as f:
        f.write(b'\x00\x11\x22' * 500)   # basura inicial
        f.write(jpg_falso_1)
        f.write(b'\xAA\xBB\xCC' * 300)   # basura intermedia
        f.write(jpg_falso_2)
        f.write(b'\xFF\xFE\xFD' * 200)   # basura final

    print(f"{C.GREEN}[+] Imagen de prueba creada: {ruta}{C.RESET}")
    print(f"{C.GRAY}    Contiene 2 JPEGs sintéticos embebidos en datos basura.{C.RESET}\n")


# ─────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────
def main():
    banner()

    parser = argparse.ArgumentParser(
        description="Lost Data Retrieval — File Carver forense",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--imagen",
        help="Ruta de la imagen raw / archivo binario a escanear"
    )
    parser.add_argument(
        "-o", "--salida",
        default="datos_rescatados",
        help="Carpeta de salida (default: datos_rescatados)"
    )
    parser.add_argument(
        "-f", "--formatos",
        nargs="+",
        default=["jpg"],
        choices=list(SIGNATURES.keys()),
        help=f"Formatos a buscar (default: jpg)\nDisponibles: {', '.join(SIGNATURES.keys())}"
    )
    parser.add_argument(
        "-r", "--reporte",
        action="store_true",
        help="Exportar reporte JSON con metadata de archivos recuperados"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar offset y tamaño de cada archivo encontrado"
    )
    parser.add_argument(
        "--demo",
        metavar="RUTA",
        help="Generar imagen de prueba sintética en RUTA y salir"
    )

    args = parser.parse_args()

    # Modo demo
    if args.demo:
        crear_imagen_prueba(args.demo)
        sys.exit(0)

    # Modo interactivo si no se pasan argumentos
    if not args.imagen:
        print(f"{C.YELLOW}Modo interactivo — también puedes usar flags (ver --help){C.RESET}\n")
        args.imagen  = input(f"{C.GREEN}[?] Ruta del archivo/imagen a escanear: {C.RESET}").strip()
        args.salida  = input(f"{C.GREEN}[?] Carpeta de salida [{args.salida}]: {C.RESET}").strip() or args.salida
        fmt_input    = input(f"{C.GREEN}[?] Formatos a buscar [{' '.join(args.formatos)}]: {C.RESET}").strip()
        if fmt_input:
            args.formatos = fmt_input.lower().split()
        print()

    resultados = carve_files(
        imagen=args.imagen,
        salida=args.salida,
        formatos=args.formatos,
        verbose=args.verbose
    )

    if args.reporte and resultados:
        generar_reporte(resultados, args.salida, args.imagen)


if __name__ == "__main__":
    main()