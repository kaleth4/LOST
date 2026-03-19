<div align="center">

```
██╗      ██████╗ ███████╗████████╗    ██████╗  █████╗ ████████╗ █████╗ 
██║     ██╔═══██╗██╔════╝╚══██╔══╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
██║     ██║   ██║███████╗   ██║       ██║  ██║███████║   ██║   ███████║
██║     ██║   ██║╚════██║   ██║       ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗╚██████╔╝███████║   ██║       ██████╔╝██║  ██║   ██║   ██║  ██║
╚══════╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
              R E T R I E V A L   —   F I L E   C A R V I N G
```

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Category](https://img.shields.io/badge/Category-Forense%20Digital-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge&logo=linux)
![Deps](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Estable-success?style=for-the-badge)

> **Herramienta de análisis forense digital para recuperar archivos eliminados o corruptos.**  
> Ignora el sistema de archivos — busca directamente las firmas hexadecimales en el raw data.

</div>

---

## 🧠 ¿Cómo funciona realmente?

Cuando "eliminas" un archivo, el sistema operativo **no borra los datos** — solo elimina la referencia en la tabla de asignación. Los bytes siguen ahí hasta ser sobrescritos.

```
DISCO EN RAW:
┌──────────────────────────────────────────────────────┐
│ ...basura... FF D8 FF [datos JPEG] FF D9 ...basura.. │
│              ▲ INICIO                ▲ FIN           │
│              └──────── CARVING ──────┘               │
└──────────────────────────────────────────────────────┘
                          │
                          ▼
                recuperado_1.jpg ✅
```

La técnica se llama **File Carving**: escanea el disco byte a byte buscando **Magic Numbers** (firmas hexadecimales) que identifican el inicio y fin de cada tipo de archivo.

---

## ✨ Características

| Feature | Descripción |
|---------|-------------|
| 🔍 **Sin dependencias del FS** | Extrae datos por contenido, no por tabla de asignación |
| 🔢 **Magic Numbers** | Detecta cabeceras y footers hexadecimales de tipos de archivo |
| 📸 **Soporte JPEG** | Busca firmas `FF D8 FF` (inicio) y `FF D9` (fin) |
| ⚡ **Sin dependencias externas** | Solo librerías estándar de Python |
| 📂 **Organización automática** | Guarda archivos recuperados en carpeta de salida nombrada |

---

## 🚀 Uso

```bash
# Clonar el repositorio
git clone https://github.com/kaleth4/lost-data-retrieval.git
cd lost-data-retrieval

# Ejecutar (no requiere pip install)
python3 carver.py
```

El script te pedirá dos inputs:

```
Introduce la ruta del archivo/imagen a escanear: disco_corrupto.img
Introduce el nombre de la carpeta de salida: datos_rescatados
```

### Output esperado

```
========================================
   🔍 LOST DATA RETRIEVAL (CARVER) 🔍
========================================

[*] Carpeta de salida creada: datos_rescatados
[*] Iniciando escaneo profundo en: disco_corrupto.img...

  [+] ¡Archivo recuperado! → recuperado_1.jpg  (Tamaño: 48320 bytes)
  [+] ¡Archivo recuperado! → recuperado_2.jpg  (Tamaño: 71204 bytes)
  [+] ¡Archivo recuperado! → recuperado_3.jpg  (Tamaño: 29847 bytes)

--------------------------------------------------
[*] Escaneo completado. Total recuperados: 3
```

---

## 🧪 ¿Cómo generar un archivo de prueba?

**Linux — volcado real de USB:**
```bash
# Crear imagen raw de un pendrive (reemplaza sdX con tu dispositivo)
sudo dd if=/dev/sdX of=disco_prueba.img bs=512 status=progress
python3 carver.py
# → Imagen: disco_prueba.img
```

**Cualquier plataforma — archivo sintético:**
```python
# Genera un binario de prueba con imágenes mezcladas en basura
with open("test.img", "wb") as f:
    f.write(b'\x00' * 1024)                    # basura inicial
    f.write(open("foto.jpg", "rb").read())     # JPEG real embebido
    f.write(b'\x00' * 512)                     # basura intermedia
    f.write(open("otra.jpg", "rb").read())     # segundo JPEG
```

---

## 📁 Estructura del proyecto

```
lost-data-retrieval/
├── carver.py          # Script principal de file carving
├── README.md          # Documentación
└── datos_rescatados/  # Carpeta generada automáticamente al ejecutar
    ├── recuperado_1.jpg
    ├── recuperado_2.jpg
    └── ...
```

---

## 🗺️ Roadmap — Próximos formatos

- [x] JPEG (`FF D8 FF` → `FF D9`)
- [ ] PNG (`89 50 4E 47` → `49 45 4E 44 AE 42 60 82`)
- [ ] PDF (`25 50 44 46` → `25 25 45 4F 46`)
- [ ] ZIP / DOCX (`50 4B 03 04` → `50 4B 05 06`)
- [ ] MP4 / MOV (atom `ftyp`)
- [ ] Exportación de reporte en JSON
- [ ] Soporte para escaneo por sectores (optimización RAM)
- [ ] Interfaz de línea de comandos con `argparse`

---

## 📚 Conceptos que aprenderás

```
✔ Estructura interna de archivos a nivel de bytes
✔ Magic Numbers y firmas hexadecimales
✔ Manipulación de datos binarios en Python
✔ Fundamentos de análisis forense digital
✔ Cómo los SO gestionan la eliminación de archivos
✔ Técnica de File Carving usada por herramientas como Autopsy y Foremost
```

---

## ⚠️ Aviso legal

> Esta herramienta fue desarrollada con fines estrictamente educativos y de investigación forense.  
> Úsala únicamente en dispositivos de tu propiedad o con autorización explícita por escrito.  
> El autor no se responsabiliza por uso indebido.

---

<div align="center">

**Kaled Corcho** — [github.com/kaleth4](https://github.com/kaleth4)  
`Cybersecurity Analyst Jr.` · `Digital Forensics` · `Blue Team`

</div>
