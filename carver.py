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