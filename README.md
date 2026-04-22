# GoDorksPY - Advanced OSINT Search Engine

![GoDorksPY Screenshot](captura.png) 

## 🇪🇸 Descripción

GoDorksPY es una potente herramienta OSINT (Open Source Intelligence) desarrollada en Python con Flet. Su objetivo es simplificar y automatizar la generación de **Google Dorks** avanzados para investigaciones digitales. Con una interfaz moderna inspirada en la estética "Cybersecurity", permite extraer información valiosa de internet con un solo clic.

### Características Principales:
- **Interfaz Hacker Estética**: Diseño oscuro y minimalista optimizado para investigadores.
- **Navegador Interno**: Abre los resultados de búsqueda en un modal flotante sin salir de la app (requiere `flet-webview`).
- **Categorización Inteligente**: Dorks agrupados por Archivos, Social, Infraestructura y Búsqueda Avanzada.
- **+20 Patrones de Dorks**: Incluye búsquedas de archivos sensibles, perfiles sociales, directorios expuestos y más.
- **Versión Ejecutable**: Permite generar un `.exe` independiente para usar sin dependencias.

---

## 🇺🇸 Description

GoDorksPY is a powerful OSINT (Open Source Intelligence) tool developed in Python using Flet. It simplifies and automates the generation of advanced **Google Dorks** for digital investigations. Featuring a modern "Cybersecurity" aesthetic, it allows you to extract valuable information from the internet with a single click.

### Key Features:
- **Cybersecurity Aesthetic**: Dark, minimalist design optimized for investigators.
- **Internal Browser**: Open search results directly within the app using a floating modal (requires `flet-webview`).
- **Smart Categorization**: Dorks grouped by Files, Social, Infrastructure, and Advanced Search.
- **20+ Dork Patterns**: Includes searches for sensitive files, social profiles, exposed directories, and more.
- **Standalone Executable**: Easily compile to a standalone `.exe` file.

---

## 🚀 Instalación / Installation

### Requisitos / Prerequisites
- Python 3.10+
- Pip

### Pasos / Steps

1. **Clonar el repositorio / Clone repository**:
   ```bash
   git clone https://github.com/a921-h/GoDorksPY.git
   cd GoDorksPY
   ```

2. **Crear entorno virtual / Create virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias / Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📦 Crear Ejecutable / Build `.exe`

Puedes convertir esta herramienta en un archivo ejecutable portable para Windows utilizando el empaquetador de Flet (que utiliza PyInstaller):

1. **Asegúrate de tener PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Ejecuta el empaquetado**:
   ```bash
   python -m flet pack main.py --name "GoDorksPY" --icon "captura.png"
   ```
   *(Nota: si el comando anterior falla en Windows por problemas del PATH, puedes llamar a flet directamente desde su ruta de instalación con `ruta\a\flet.exe pack main.py`)*

¡Encontrarás tu ejecutable listo para usar dentro de la carpeta `dist/`!

---

## 🛠️ Uso / Usage

Ejecuta la aplicación con / Run the app with:
```bash
python main.py
```

1. Introduce un término (nombre, empresa, dominio) en el buscador.
2. Haz clic en **GENERAR DORKS**.
3. Usa los iconos para copiar el dork o abrirlo en el navegador interno.

---

## 🤝 Contribuir / Contributing

¡Las contribuciones son bienvenidas! Si tienes nuevos patrones de dorks o mejoras visuales:
1. Haz un Fork del proyecto.
2. Crea tu rama (`git checkout -b feature/MejoraDork`).
3. Haz commit de tus cambios (`git commit -m 'Añadir dork para log de servidores'`).
4. Push a la rama (`git push origin feature/MejoraDork`).
5. Abre un Pull Request.

---

## ⚖️ Licencia / License

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
