
🔍 Lost Data Retrieval (Recuperación de Datos Perdidos)
Bienvenido a Lost Data Retrieval, una herramienta de análisis forense digital diseñada para recuperar archivos perdidos, eliminados o corruptos de dispositivos de almacenamiento. Este proyecto utiliza la técnica de File Carving, la cual ignora el sistema de archivos principal y busca directamente las "firmas" (Magic Numbers) de los archivos en crudo (raw data).

Este proyecto es ideal para aprender sobre la estructura profunda de los archivos, la manipulación de bytes y los fundamentos de la recuperación de datos en ciberseguridad.

✨ Características
Recuperación sin Sistema de Archivos: Extrae datos basándose en el contenido del archivo, no en la tabla de asignación.

Detección por Magic Numbers: Identifica cabeceras (headers) y pies (footers) específicos de tipos de archivos.

Soporte inicial para imágenes JPEG: Busca las firmas hexadecimales FF D8 FF (Inicio) y FF D9 (Fin).

Código ligero y educativo: Perfecto para entender cómo los sistemas operativos almacenan los datos a nivel de bytes.

🚀 ¿Cómo funciona?
Cuando "eliminas" un archivo de una unidad USB o disco duro, el sistema operativo generalmente solo borra la referencia a ese archivo, dejando los datos reales (los bytes) intactos hasta que sean sobrescritos por nueva información. Esta herramienta lee la imagen del disco byte a byte, buscando las firmas que indican el comienzo y el final de un archivo, y los "esculpe" (extrae) para guardarlos de forma segura.

🛠️ Requisitos Previos
Python 3.8 o superior.

Una imagen de disco en formato RAW (.img, .dd o .iso) o un archivo binario corrupto que contenga imágenes.

💻 El Código del Programa (Python)
A continuación se presenta el código fuente completo del proyecto (carver.py). No requiere dependencias externas, ya que utiliza las bibliotecas estándar de Python.

Python
import os
import sys

def recuperar_archivos(archivo_imagen, carpeta_salida):
    """
    Escanea un archivo binario o imagen de disco buscando firmas de archivos JPEG
    y los recupera (File Carving).
    """
    # Firmas hexadecimales (Magic Numbers) para archivos JPEG
    JPEG_INICIO = b'\xff\xd8\xff'
    JPEG_FIN = b'\xff\xd9'

    # Verificar si la imagen existe
    if not os.path.isfile(archivo_imagen):
        print(f"[x] Error: No se encontró el archivo {archivo_imagen}")
        return

    # Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"[*] Carpeta de salida creada: {carpeta_salida}")

    print(f"[*] Iniciando escaneo profundo en: {archivo_imagen}...")
    
    try:
        # Abrir el archivo en modo lectura binaria
        with open(archivo_imagen, "rb") as f:
            contenido_raw = f.read()

        indice_actual = 0
        archivos_recuperados = 0

        while True:
            # Buscar el inicio de un archivo JPEG
            indice_inicio = contenido_raw.find(JPEG_INICIO, indice_actual)
            
            # Si no hay más inicios, terminamos
            if indice_inicio == -1:
                break

            # Buscar el final del archivo JPEG desde donde encontramos el inicio
            indice_fin = contenido_raw.find(JPEG_FIN, indice_inicio)
            
            if indice_fin == -1:
                # Se encontró un inicio pero no un final (archivo incompleto o corrupto)
                break

            # Ajustar el índice para incluir los bytes de cierre de la firma (\xff\xd9)
            indice_fin += len(JPEG_FIN)

            # Extraer los bytes correspondientes al archivo
            datos_archivo = contenido_raw[indice_inicio:indice_fin]

            # Guardar el archivo recuperado
            nombre_archivo = os.path.join(carpeta_salida, f"recuperado_{archivos_recuperados + 1}.jpg")
            with open(nombre_archivo, "wb") as out_file:
                out_file.write(datos_archivo)

            print(f"  [+] ¡Archivo recuperado! Guardado como: {nombre_archivo} (Tamaño: {len(datos_archivo)} bytes)")
            
            # Actualizar contadores y continuar la búsqueda
            archivos_recuperados += 1
            indice_actual = indice_fin

        print("-" * 50)
        print(f"[*] Escaneo completado. Total de archivos recuperados: {archivos_recuperados}")

    except Exception as e:
        print(f"[x] Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    print("========================================")
    print("   🔍 LOST DATA RETRIEVAL (CARVER) 🔍")
    print("========================================\n")
    
    # Datos de ejemplo para la ejecución
    print("Para probar este script, necesitas un archivo binario (ej. 'disco_corrupto.img')")
    archivo_objetivo = input("Introduce la ruta del archivo/imagen a escanear: ")
    directorio_salida = input("Introduce el nombre de la carpeta para guardar lo recuperado (ej. 'datos_rescatados'): ")
    
    print("\n")
    recuperar_archivos(archivo_objetivo, directorio_salida)
⚙️ Uso del Programa
Guarda el código anterior en un archivo llamado carver.py.

Para probarlo, puedes crear un archivo binario falso que contenga texto basura y un par de imágenes reales mezcladas, o usar un volcado de un pendrive USB antiguo (usando herramientas como dd en Linux).

Ejecuta el script desde tu terminal:

Bash
python carver.py
El programa te pedirá la ruta del archivo a escanear y la carpeta donde quieres guardar los resultados.

Revisa la carpeta de salida para ver tus imágenes recuperadas. 🖼️

⚠️ Aviso Legal y Ético
Propósito Educativo: Esta herramienta ha sido desarrollada estrictamente con fines educativos y de investigación en ciberseguridad y análisis forense. No utilices herramientas de recuperación en dispositivos de los cuales no seas propietario o no tengas permiso explícito para auditar.
