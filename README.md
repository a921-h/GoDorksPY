# GoDorksPY - Herramienta OSINT con Google Dorks

![GoDorksPY Screenshot](captura.png) 

## Descripción

GoDorksPY es una aplicación de escritorio desarrollada con Python y Flet, diseñada para simplificar las búsquedas OSINT (Open Source Intelligence) utilizando Google Dorks. Proporciona una interfaz gráfica de usuario minimalista y simple que permite a los usuarios generar automáticamente una variedad de consultas de Google Dorks basadas en una única entrada de texto (como el buscador de Google), facilitando la exploración de información pública en internet.

## Características

-   **Interfaz Gráfica Intuitiva**: Desarrollada con Flet para una experiencia de usuario moderna y adpatable a cualquier dispositivo.
-   **Búsqueda Simplificada**: Un único campo de entrada para tus consultas OSINT.
-   **Generación Automática de Dorks**: Transforma tu consulta en una lista de Google Dorks comunes y efectivos (ej. búsqueda de PDFs, documentos de Word, perfiles de LinkedIn, directorios públicos, etc.).
-   **Previsualización en la Aplicación**: Visualiza los detalles de cada dork generado (nombre, consulta dork, URL de Google) dentro de la aplicación antes de abrirlo en el navegador.
-   **Apertura en Navegador Externo**: Abre la búsqueda de Google Dork seleccionada en tu navegador web predeterminado con un solo clic.
-   **Tema Oscuro**: Interfaz con fondo negro y texto blanco, inspirada en la estética de los buscadores tradicionales y herramientas de seguridad.

## Instalación

Para ejecutar GoDorksPY, necesitarás tener Python instalado en tu sistema siendo esta la ultima versión existente. Luego, puedes instalar Flet y las dependencias del proyecto:

1.  **Clona el repositorio** (si aún no lo has hecho):
    ```bash
    git clone https://github.com/makinatetanos/GoDorksPY.git 
    cd GoDorksPY
    ```
2.  **Inicia el Entorno** usa el siguiente comando:
    ```bash
    pip install -m venv venv
    ```
3. **Activa el entorno Virtual**:
   ```bash
    source .venv/bin/activate
   ```
   En el caso de Windows:
   ```
    .\venv\Scripts\Activate.ps1
   ```
4. **Instala Flet**:
   ```
    pip install 'flet[all]'
   ```
5. **Verifica la istalación**:
    ```
    flet --version
    ```
    Recuerda actualizar flet a su ultima versión de la siguiente forma:
    ```
    pip install 'flet[all]' --upgrade
    ```
    Puedes consultar la documentación de flet aqui: [Documentación de Flet](https://docs.flet.dev/)

## Uso

Una vez instalado, puedes iniciar la aplicación ejecutando el script principal:

```bash
python main.py
```

### Cómo funciona:

1.  **Introduce tu término de búsqueda**: En el campo de entrada principal, escribe el nombre, la empresa, el tema o cualquier término que desees investigar.
2.  **Genera las búsquedas Dork**: Haz clic en el botón "Generate Dork Searches".
3.  **Explora los resultados**: Aparecerá una lista de Google Dorks generados automáticamente. Cada elemento representa una búsqueda OSINT específica.
4.  **Previsualiza y Abre**: Haz clic en cualquier dork de la lista para ver sus detalles en una pantalla de previsualización dentro de la aplicación. Desde esta pantalla, puedes hacer clic en "Open in Browser" para ejecutar la búsqueda en Google.

## Contribución

¡Si deseas contribiri, puedes hacerlo! Si tienes ideas para mejorar la herramienta, por favor, abre un 'issue' o envía un 'pull request'.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
