import flet as ft
import webbrowser

def main(page: ft.Page):
    page.title = "GoDorksPY - OSINT Search"
    page.bgcolor = ft.Colors.BLACK
    
    # State variable to hold search results across view changes
    page.results_data = []

    def open_in_browser(url):
        webbrowser.open(url)
        page.update()

    def search_clicked(search_field, results_view):
        raw_query = search_field.value
        if not raw_query:
            search_field.error_text = "Search query cannot be empty"
            page.update()
            return
        else:
            search_field.error_text = None

        results_view.controls.clear()
        page.results_data.clear()

        generated_dorks = {
            f'PDF Documents': f'"{raw_query}" filetype:pdf',
            f'Word Documents': f'"{raw_query}" filetype:docx',
            f'Excel Spreadsheets': f'"{raw_query}" filetype:xlsx',
            f'LinkedIn Profiles': f'site:linkedin.com "{raw_query}"',
            f'Public Directories': f'intitle:"index of" "{raw_query}"',
            f'Resumes/CVs': f'("{raw_query}" AND (intitle:"resume" OR intitle:"CV"))',
            f'Email Addresses': f'"{raw_query}" intext:@',
        }

        # Store results in the persistent state variable
        for i, (name, dork) in enumerate(generated_dorks.items()):
            google_url = f"https://www.google.com/search?q={dork}"
            page.results_data.append({"index": i, "name": name, "dork": dork, "url": google_url})

        # Populate the UI from the state variable
        for item in page.results_data:
            results_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LINK, color=ft.Colors.WHITE70),
                    title=ft.Text(item['name'], color="white", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(item['dork'], color=ft.Colors.WHITE54, size=11),
                    data=item['index'],
                    on_click=lambda e: page.go(f"/preview/{e.control.data}")
                )
            )
        page.update()

    def route_change(route):
        page.views.clear()

        # --- Main View (Search) ---
        search_field = ft.TextField(
            hint_text="Enter a name, company, topic...",
            width=600, border_color="white", color="white",
            hint_style=ft.TextStyle(color=ft.Colors.WHITE54),
        )
        results_view = ft.ListView(expand=1, spacing=5, auto_scroll=True)
        search_field.on_submit = lambda e: search_clicked(search_field, results_view)

        # If results already exist (e.g., navigating back), populate the list
        if page.results_data:
            for item in page.results_data:
                results_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LINK, color=ft.Colors.WHITE70),
                        title=ft.Text(item['name'], color="white", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(item['dork'], color=ft.Colors.WHITE54, size=11),
                        data=item['index'],
                        on_click=lambda e: page.go(f"/preview/{e.control.data}")
                    )
                )

        page.views.append(
            ft.View(
                route="/",
                bgcolor=ft.Colors.BLACK,
                padding=20,
                controls=[
                    ft.Column([
                        ft.Text("GoDorksPY", size=40, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Container(height=15),
                        search_field,
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            text="Generate Dork Searches",
                            on_click=lambda e: search_clicked(search_field, results_view),
                            bgcolor=ft.Colors.BLUE_GREY_700, color="white", width=600
                        ),
                        ft.Divider(color=ft.Colors.WHITE24, height=20),
                        ft.Text("Suggested Dork Searches", color=ft.Colors.WHITE70)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    results_view
                ]
            )
        )

        # --- Preview View ---
        if page.route.startswith("/preview"):
            preview_index = int(page.route.split("/")[-1])
            clicked_data = next((item for item in page.results_data if item["index"] == preview_index), None)

            if clicked_data:
                page.views.append(
                    ft.View(
                        route=page.route,
                        bgcolor=ft.Colors.BLACK,
                        appbar=ft.AppBar(
                            title=ft.Text("Preview", color="white"),
                            bgcolor=ft.Colors.BLUE_GREY_900,
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/"))
                        ),
                        padding=20,
                        controls=[
                            ft.Text(clicked_data['name'], size=24, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text(clicked_data['dork'], selectable=True, color=ft.Colors.WHITE70),
                            ft.Container(height=30),
                            ft.ElevatedButton(
                                "Open in Browser",
                                icon=ft.Icons.OPEN_IN_NEW,
                                width=300,
                                bgcolor=ft.Colors.BLUE_500,
                                color="white",
                                on_click=lambda _, url=clicked_data['url']: open_in_browser(url)
                            )
                        ],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
