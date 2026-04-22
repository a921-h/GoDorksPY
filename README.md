# GoDorks — Advanced OSINT CLI Tool

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge&logo=go)](https://golang.org)
[![Download](https://img.shields.io/badge/⬇️_Descargar-GoDorks.exe-brightgreen?style=for-the-badge&logo=windows)](https://github.com/a921-h/GoDorksPY/releases/latest/download/GoDorks.exe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

```
  ██████╗  ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗
 ██╔════╝ ██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
 ██║  ███╗██║   ██║██║  ██║██║   ██║██████╔╝█████╔╝ ███████╗
 ██║   ██║██║   ██║██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚════██║
 ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝██║  ██║██║  ██╗███████║
  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
          Advanced OSINT CLI Tool · Built with Go
```

---

## 🇪🇸 Descripción

**GoDorks** es una herramienta CLI OSINT de alto rendimiento desarrollada en **Go**, diseñada para investigadores de seguridad y analistas digitales. Genera automáticamente consultas avanzadas de **Google Dorks** organizadas por categorías a partir de un único término de búsqueda.

El ejecutable resultante pesa **menos de 5MB**, no requiere ningún runtime, y puede automatizarse en scripts.

### ✨ Características:
- ⚡ **Ultra rápido**: Binario nativo compilado en Go — arranque instantáneo.
- 🗂️ **5 Categorías, +40 Dorks**: Archivos, Social, Infraestructura, Inteligencia de Empresa y Búsqueda Avanzada.
- 🌐 **Multiplataforma**: Windows, Linux y macOS — un solo binario.
- 🤖 **Automatizable**: Ideal para pipelines de OSINT con flags CLI.
- 💾 **Exportación**: Guarda todos los resultados en un archivo `.txt` con un solo comando.
- 📂 **Menú interactivo**: Selecciona categorías, abre dorks en el navegador y exporta resultados en tiempo real.
- 📦 **Sin dependencias**: Un único ejecutable, sin instalar nada más.

---

## 🇺🇸 Description

**GoDorks** is a high-performance OSINT CLI tool built in **Go**, designed for security researchers and digital analysts. It auto-generates advanced **Google Dork** queries organized by category from a single search term.

### Features:
- ⚡ **Ultra fast**: Native Go binary — instant startup.
- 🗂️ **5 Categories, 40+ Dorks**: Files, Social, Infrastructure, Business Intel & Advanced Search.
- 🌐 **Cross-platform**: Windows, Linux and macOS.
- 🤖 **Scriptable**: Perfect for OSINT pipelines using CLI flags.
- 💾 **Export**: Save all results to a `.txt` file with one flag.
- 📂 **Interactive Menu**: Select categories, open results in browser, export on-the-fly.
- 📦 **Zero dependencies**: Single binary, nothing to install.

---

## ⬇️ Descarga Rápida / Quick Download

> No necesitas tener Go instalado. Descarga el `.exe` directamente y ejecútalo.

👉 **[Descargar GoDorks.exe para Windows](https://github.com/a921-h/GoDorksPY/releases/latest/download/GoDorks.exe)**

---

## 🚀 Uso / Usage

### Modo Interactivo (menú completo)
```bash
./GoDorks
```
El programa te pedirá el término y te permitirá elegir la categoría.

### Modo Directo con flags
```bash
# Búsqueda simple
./GoDorks -q "tesla.com"

# Elegir categoría directamente (1=Archivos, 2=Social, 3=Infra, 4=Empresa, 5=Avanzado, 6=Todas)
./GoDorks -q "tesla.com" -cat 2

# Exportar resultados a un archivo
./GoDorks -q "tesla.com" -export resultados.txt

# Abrir todos los dorks en el navegador automáticamente
./GoDorks -q "tesla.com" -open
```

### Flags disponibles / Available flags
| Flag | Descripción / Description |
|------|--------------------------|
| `-q <term>` | Término de búsqueda (dominio, nombre, empresa) |
| `-cat <n>` | Seleccionar categoría por número (1-5, 6=Todas) |
| `-export <file>` | Exportar resultados al archivo especificado |
| `-open` | Abrir todos los dorks en el navegador automáticamente |

---

## 🐳 Docker / Uso en Servidor

También puedes ejecutar GoDorks como servidor web accesible desde el navegador:

```bash
# Construir imagen
docker build -t godorks .

# Ejecutar (accesible en http://localhost:8550)
docker run -p 8550:8550 godorks
```

---

## 🔨 Compilar desde el código fuente / Build from source

### Requisitos
- [Go 1.21+](https://go.dev/dl/)

### Compilar para tu sistema
```bash
git clone https://github.com/a921-h/GoDorksPY.git
cd GoDorksPY
go build -o GoDorks .
./GoDorks
```

### Cross-compilar para múltiples plataformas
```bash
# Windows (64-bit)
GOOS=windows GOARCH=amd64 go build -o GoDorks.exe .

# Linux (64-bit)
GOOS=linux GOARCH=amd64 go build -o GoDorks_linux .

# macOS (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o GoDorks_mac .
```

---

## 🤝 Contribuir / Contributing

¡Las contribuciones son bienvenidas! Para añadir nuevos patrones de dorks:

1. Haz un Fork del proyecto.
2. Crea tu rama: `git checkout -b feature/NuevoDork`
3. Añade tu dork en la función `getCategories()` de `main.go`.
4. Abre un Pull Request.

---

## ⚖️ Licencia / License

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

> **Disclaimer**: Esta herramienta es para fines educativos e investigación de seguridad ética. El uso indebido es responsabilidad exclusiva del usuario.
