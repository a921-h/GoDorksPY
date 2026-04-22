import flet as ft
import webbrowser
import urllib.parse

class DorkEngine:
    """Clase para generar dorks de Google basados en una consulta."""
    
    @staticmethod
    def get_categories():
        return {
            "Archivos": [
                {"name": "Documentos PDF", "template": '"{query}" filetype:pdf'},
                {"name": "Documentos Word", "template": '"{query}" filetype:docx'},
                {"name": "Hojas de Excel", "template": '"{query}" filetype:xlsx'},
                {"name": "Presentaciones PPT", "template": '"{query}" filetype:pptx'},
                {"name": "Archivos de Texto", "template": '"{query}" filetype:txt'},
                {"name": "Archivos de Registro (Log)", "template": '"{query}" filetype:log'},
                {"name": "Bases de Datos SQL", "template": '"{query}" filetype:sql'},
            ],
            "Social & Perfiles": [
                {"name": "Perfiles de LinkedIn", "template": 'site:linkedin.com/in/ "{query}"'},
                {"name": "Perfiles de Twitter/X", "template": 'site:twitter.com "{query}"'},
                {"name": "Perfiles de Instagram", "template": 'site:instagram.com "{query}"'},
                {"name": "Perfiles de Facebook", "template": 'site:facebook.com "{query}"'},
                {"name": "Perfiles de GitHub", "template": 'site:github.com "{query}"'},
            ],
            "Infraestructura": [
                {"name": "Directorios Públicos", "template": 'intitle:"index of" "{query}"'},
                {"name": "Servidores Apache", "template": 'intitle:"index of" "Apache" "{query}"'},
                {"name": "Páginas de Login", "template": '"{query}" (inurl:login | inurl:signin)'},
                {"name": "Configuraciones PHP", "template": '"{query}" "phpinfo()"'},
                {"name": "Archivos Env / Config", "template": '"{query}" extension:env | extension:conf | extension:config'},
            ],
            "Búsqueda Avanzada": [
                {"name": "Correos Electrónicos", "template": '"{query}" intext:@gmail.com | intext:@outlook.com | intext:@yahoo.com'},
                {"name": "Menciones en Noticias", "template": 'site:news.google.com "{query}"'},
                {"name": "Documentos en Pastebin", "template": 'site:pastebin.com "{query}"'},
                {"name": "Caché de Google", "template": 'cache:"{query}"'},
            ]
        }

    @staticmethod
    def generate_dorks(query):
        results = []
        categories = DorkEngine.get_categories()
        for cat_name, dorks in categories.items():
            for dork in dorks:
                dork_query = dork["template"].format(query=query)
                google_url = f"https://www.google.com/search?q={urllib.parse.quote(dork_query)}"
                results.append({
                    "category": cat_name,
                    "name": dork["name"],
                    "dork": dork_query,
                    "url": google_url
                })
        return results

def main(page: ft.Page):
    page.title = "GoDorksPY - OSINT Tool"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 900
    page.window_height = 800
    page.window_resizable = True
    
    # Fuentes y Colores
    PRIMARY_COLOR = "#00FF41" # Matrix Green
    BG_COLOR = "#0D0D0D"
    SURFACE_COLOR = "#1A1A1A"
    
    page.bgcolor = BG_COLOR
    
    # Estado de la aplicación
    results_data = []

    def copy_to_clipboard(text):
        page.set_clipboard(text)
        page.show_snack_bar(
            ft.SnackBar(ft.Text(f"Copiado al portapapeles: {text}"), bgcolor=ft.Colors.GREEN_700)
        )

    # --- Internal Browser Modal ---
    wv_container = ft.Container(expand=True, bgcolor=ft.Colors.WHITE)
    
    def close_dlg(e):
        page.close(browser_dlg)

    browser_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [ft.Text("Navegador OSINT Interno", color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD), 
             ft.IconButton(ft.Icons.CLOSE, on_click=close_dlg)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        content=ft.Container(
            content=wv_container,
            width=1200,
            height=800,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        ),
        bgcolor=SURFACE_COLOR,
    )

    def open_url(url):
        try:
            # Intenta importar el WebView nativo de Flet
            import flet.webview as webview
            wv_container.content = webview.WebView(
                url=url,
                expand=True,
            )
            page.open(browser_dlg)
        except ImportError:
            # Si no está instalado flet-webview, usa el navegador del sistema
            page.show_snack_bar(
                ft.SnackBar(ft.Text("Módulo 'flet-webview' no encontrado. Abriendo en navegador externo..."), bgcolor=ft.Colors.ORANGE_700)
            )
            webbrowser.open(url)

    def on_search(e):
        query = search_input.value.strip()
        if not query:
            search_input.error_text = "Por favor, introduce un término de búsqueda."
            page.update()
            return
        
        search_input.error_text = None
        results_list.controls.clear()
        
        # Animación de carga (opcional, pero mejora UX)
        loading_indicator.visible = True
        page.update()
        
        nonlocal results_data
        results_data = DorkEngine.generate_dorks(query)
        
        # Agrupar por categoría
        categories = {}
        for item in results_data:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
            
        for cat_name, items in categories.items():
            results_list.controls.append(
                ft.Container(
                    content=ft.Text(cat_name, size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    padding=ft.padding.only(top=20, bottom=10)
                )
            )
            for item in items:
                results_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(item["name"], weight=ft.FontWeight.W_600, size=16, color="white"),
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.COPY,
                                        icon_size=18,
                                        icon_color=ft.Colors.WHITE54,
                                        tooltip="Copiar Dork",
                                        on_click=lambda e, d=item["dork"]: copy_to_clipboard(d)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.OPEN_IN_NEW,
                                        icon_size=18,
                                        icon_color=PRIMARY_COLOR,
                                        tooltip="Abrir en Google",
                                        on_click=lambda e, u=item["url"]: open_url(u)
                                    ),
                                ], spacing=0)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(item["dork"], size=12, color=ft.Colors.WHITE38, italic=True)
                        ], spacing=2),
                        padding=15,
                        bgcolor=SURFACE_COLOR,
                        border_radius=10,
                        border=ft.border.all(1, ft.Colors.WHITE10),
                        on_hover=lambda e: (setattr(e.control, "border", ft.border.all(1, PRIMARY_COLOR)) if e.data == "true" else setattr(e.control, "border", ft.border.all(1, ft.Colors.WHITE10)), e.control.update())
                    )
                )
        
        loading_indicator.visible = False
        page.update()

    # --- UI Components ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Text("GoDorksPY", size=48, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Text("ADVANCED OSINT SEARCH ENGINE", size=12, color=ft.Colors.WHITE54),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=40,
        width=page.window_width,
    )
    
    search_input = ft.TextField(
        hint_text="Nombre, empresa, dominio...",
        width=500,
        height=50,
        border_radius=25,
        border_color=ft.Colors.WHITE24,
        focused_border_color=PRIMARY_COLOR,
        color="white",
        prefix_icon=ft.Icons.SEARCH,
        on_submit=on_search,
    )
    
    search_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.BOLT, color=BG_COLOR),
            ft.Text("GENERAR DORKS", color=BG_COLOR, weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        bgcolor=PRIMARY_COLOR,
        border_radius=25,
        padding=15,
        on_click=on_search,
        ink=True,
    )
    
    loading_indicator = ft.ProgressBar(width=500, color=PRIMARY_COLOR, visible=False)
    
    results_list = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
    )
    
    footer = ft.Container(
        content=ft.Row([
            ft.Text("© 2024 GoDorksPY - OSINT Tools", color=ft.Colors.WHITE24, size=12),
            ft.Row([
                ft.Container(content=ft.Text("GitHub", color=ft.Colors.WHITE24), on_click=lambda _: open_url("https://github.com/a921-h/GoDorksPY"), padding=5, ink=True),
                ft.Container(content=ft.Text("Docs", color=ft.Colors.WHITE24), on_click=lambda _: open_url("https://docs.flet.dev/"), padding=5, ink=True),
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(left=40, right=40, bottom=20, top=10)
    )
    
    # Main Layout
    page.add(
        ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    ft.Row([search_input, search_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    loading_indicator,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=20)
            ),
            ft.Divider(color=ft.Colors.WHITE10, height=1),
            ft.Container(
                content=results_list,
                expand=True,
                padding=ft.padding.only(left=20, right=20)
            ),
            footer
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except AttributeError:
        # Fallback for newer flet versions where app might be completely deprecated/removed in the future
        ft.run(main)
