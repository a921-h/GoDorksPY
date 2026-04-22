package main

import (
	"bufio"
	"flag"
	"fmt"
	"net/url"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"strings"
	"time"
)

// ANSI Color Codes
const (
	Reset   = "\033[0m"
	Red     = "\033[31m"
	Green   = "\033[32m"
	Yellow  = "\033[33m"
	Blue    = "\033[34m"
	Magenta = "\033[35m"
	Cyan    = "\033[36m"
	White   = "\033[37m"
	Bold    = "\033[1m"
	Dim     = "\033[2m"
	BgDark  = "\033[40m"
)

type Dork struct {
	Name     string
	Template string
}

type Category struct {
	Name  string
	Icon  string
	Dorks []Dork
}

var reader = bufio.NewReader(os.Stdin)

func main() {
	queryFlag := flag.String("q", "", "Término de búsqueda (dominio, nombre, empresa)")
	openFlag := flag.Bool("open", false, "Abrir todos los resultados en el navegador")
	exportFlag := flag.String("export", "", "Exportar resultados a un archivo (ej: -export resultados.txt)")
	catFlag := flag.Int("cat", 0, "Seleccionar categoría directamente por número (ej: -cat 1)")
	flag.Parse()

	clearScreen()
	printBanner()

	query := *queryFlag
	if query == "" {
		fmt.Print(Cyan + "  ❯ " + Bold + "Introduce el término de búsqueda" + Reset + Cyan + " (dominio, nombre, empresa): " + Reset)
		input, _ := reader.ReadString('\n')
		query = strings.TrimSpace(input)
		if query == "" {
			fmt.Println(Red + "\n  [✗] Búsqueda cancelada. Saliendo..." + Reset)
			return
		}
	}

	categories := getCategories()

	// Selección de categoría
	selectedCat := *catFlag
	if selectedCat == 0 {
		selectedCat = selectCategory(categories)
	}

	// Recopilar dorks a procesar
	var dorksToProcess []Category
	if selectedCat == len(categories)+1 {
		// Todas las categorías
		dorksToProcess = categories
	} else if selectedCat >= 1 && selectedCat <= len(categories) {
		dorksToProcess = []Category{categories[selectedCat-1]}
	} else {
		dorksToProcess = categories
	}

	// Generar y mostrar resultados
	var allResults []string
	printSeparator()
	fmt.Printf("\n%s%s  [+] Generando dorks para: %s\"%s\"%s\n\n",
		Bold, Green, Reset+Yellow, query, Reset)

	for _, cat := range dorksToProcess {
		fmt.Printf("\n%s%s %s %s%s\n", Bold, Magenta, cat.Icon, cat.Name, Reset)
		printThinLine()
		for i, dork := range cat.Dorks {
			dorkQuery := strings.ReplaceAll(dork.Template, "{query}", query)
			googleURL := fmt.Sprintf("https://www.google.com/search?q=%s", url.QueryEscape(dorkQuery))

			fmt.Printf("\n  %s%s[%d]%s %s%s%s\n", Bold, Cyan, i+1, Reset, Bold, dork.Name, Reset)
			fmt.Printf("  %s  Dork:%s %s\n", Dim, Reset, dorkQuery)
			fmt.Printf("  %s  URL: %s%s%s\n", Dim, Reset+Blue, googleURL, Reset)

			allResults = append(allResults,
				fmt.Sprintf("[%s] %s\n  Dork: %s\n  URL:  %s\n", cat.Name, dork.Name, dorkQuery, googleURL))

			if *openFlag {
				openBrowser(googleURL)
				time.Sleep(200 * time.Millisecond) // Evitar spam al navegador
			}
		}
	}

	// Exportar si se solicitó
	if *exportFlag != "" {
		exportResults(*exportFlag, query, allResults)
	}

	// Menú post-generación
	if !*openFlag {
		postMenu(allResults, *exportFlag)
	}
}

func selectCategory(categories []Category) int {
	printSeparator()
	fmt.Printf("\n%s%s  📂 Selecciona una categoría:%s\n\n", Bold, Yellow, Reset)
	for i, cat := range categories {
		fmt.Printf("  %s%s[%d]%s %s %s\n", Bold, Cyan, i+1, Reset, cat.Icon, cat.Name)
	}
	fmt.Printf("  %s%s[%d]%s 🌐 Todas las categorías\n", Bold, Green, len(categories)+1, Reset)
	fmt.Printf("\n%s  ❯ Elige una opción [1-%d]: %s", Cyan, len(categories)+1, Reset)

	input, _ := reader.ReadString('\n')
	choice, err := strconv.Atoi(strings.TrimSpace(input))
	if err != nil || choice < 1 || choice > len(categories)+1 {
		fmt.Println(Yellow + "\n  [~] Opción no válida. Mostrando todas las categorías..." + Reset)
		return len(categories) + 1
	}
	return choice
}

func postMenu(results []string, exportedTo string) {
	printSeparator()
	fmt.Printf("\n%s%s  ⚡ ¿Qué quieres hacer ahora?%s\n\n", Bold, Yellow, Reset)
	fmt.Printf("  %s[1]%s 🌐 Abrir un dork específico en el navegador\n", Cyan+Bold, Reset)
	fmt.Printf("  %s[2]%s 💾 Exportar todos los resultados a un archivo\n", Cyan+Bold, Reset)
	fmt.Printf("  %s[3]%s 🔄 Nueva búsqueda\n", Cyan+Bold, Reset)
	fmt.Printf("  %s[4]%s 🚪 Salir\n", Cyan+Bold, Reset)
	fmt.Printf("\n%s  ❯ Opción: %s", Cyan, Reset)

	input, _ := reader.ReadString('\n')
	choice := strings.TrimSpace(input)

	switch choice {
	case "1":
		fmt.Printf("\n%s  ❯ Número de dork a abrir (1-%d): %s", Cyan, len(results), Reset)
		numInput, _ := reader.ReadString('\n')
		num, err := strconv.Atoi(strings.TrimSpace(numInput))
		if err != nil || num < 1 || num > len(results) {
			fmt.Println(Red + "  [✗] Número inválido." + Reset)
			return
		}
		// Extraer la URL del resultado
		lines := strings.Split(results[num-1], "\n")
		for _, line := range lines {
			if strings.HasPrefix(strings.TrimSpace(line), "URL:") {
				urlPart := strings.TrimPrefix(strings.TrimSpace(line), "URL:  ")
				openBrowser(strings.TrimSpace(urlPart))
				fmt.Println(Green + "\n  [✓] Abriendo en el navegador..." + Reset)
			}
		}
	case "2":
		if exportedTo != "" {
			fmt.Printf(Green+"  [✓] Ya exportado a: %s\n"+Reset, exportedTo)
		} else {
			fmt.Printf("\n%s  ❯ Nombre del archivo (ej: resultados.txt): %s", Cyan, Reset)
			nameInput, _ := reader.ReadString('\n')
			filename := strings.TrimSpace(nameInput)
			if filename == "" {
				filename = fmt.Sprintf("godorks_%d.txt", time.Now().Unix())
			}
			exportResults(filename, "", results)
		}
	case "3":
		clearScreen()
		main()
	case "4":
		fmt.Println(Green + "\n  [✓] ¡Hasta pronto! Stay stealthy. 🕵️" + Reset + "\n")
	default:
		fmt.Println(Yellow + "\n  [~] Opción no reconocida. Saliendo..." + Reset)
	}
}

func exportResults(filename, query string, results []string) {
	f, err := os.Create(filename)
	if err != nil {
		fmt.Printf(Red+"  [✗] Error al crear el archivo: %v\n"+Reset, err)
		return
	}
	defer f.Close()

	header := fmt.Sprintf("========================================\n  GoDorks - Resultados OSINT\n  Búsqueda: %s\n  Fecha: %s\n========================================\n\n",
		query, time.Now().Format("2006-01-02 15:04:05"))
	f.WriteString(header)
	for _, r := range results {
		f.WriteString(r + "\n")
	}
	fmt.Printf(Green+"\n  [✓] Resultados exportados a: %s%s%s (%d dorks)\n"+Reset,
		Bold, filename, Reset+Green, len(results))
}

func printBanner() {
	banner := Green + Bold + `
  ██████╗  ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗
 ██╔════╝ ██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
 ██║  ███╗██║   ██║██║  ██║██║   ██║██████╔╝█████╔╝ ███████╗
 ██║   ██║██║   ██║██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚════██║
 ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝██║  ██║██║  ██╗███████║
  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝` + Reset

	subtitle := Dim + `
          Advanced OSINT CLI Tool · Built with Go
` + Reset

	fmt.Println(banner)
	fmt.Println(subtitle)
}

func printSeparator() {
	fmt.Println(Dim + "  " + strings.Repeat("─", 60) + Reset)
}

func printThinLine() {
	fmt.Println(Dim + "  " + strings.Repeat("·", 50) + Reset)
}

func clearScreen() {
	if runtime.GOOS == "windows" {
		cmd := exec.Command("cmd", "/c", "cls")
		cmd.Stdout = os.Stdout
		cmd.Run()
	} else {
		fmt.Print("\033[H\033[2J")
	}
}

func openBrowser(rawURL string) {
	var err error
	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", rawURL).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", rawURL).Start()
	case "darwin":
		err = exec.Command("open", rawURL).Start()
	}
	if err != nil {
		fmt.Printf(Red+"  [✗] Error abriendo el navegador: %v\n"+Reset, err)
	}
}

func getCategories() []Category {
	return []Category{
		{
			Name: "Archivos Sensibles",
			Icon: "📄",
			Dorks: []Dork{
				{"Documentos PDF", `"{query}" filetype:pdf`},
				{"Hojas de Cálculo (Excel)", `"{query}" filetype:xlsx OR filetype:csv`},
				{"Documentos Word", `"{query}" filetype:docx OR filetype:doc`},
				{"Presentaciones PowerPoint", `"{query}" filetype:pptx`},
				{"Archivos de Registro (Log)", `"{query}" filetype:log`},
				{"Bases de Datos SQL", `"{query}" filetype:sql`},
				{"Archivos de Configuración", `"{query}" filetype:conf OR filetype:cfg OR filetype:ini`},
				{"Archivos de Variables de Entorno", `"{query}" filetype:env`},
				{"Volcados de Base de Datos", `"{query}" filetype:sql intext:INSERT INTO`},
				{"Archivos de Backup", `"{query}" filetype:bak OR filetype:old OR filetype:backup`},
			},
		},
		{
			Name: "Social & Perfiles",
			Icon: "👤",
			Dorks: []Dork{
				{"Perfiles de LinkedIn", `site:linkedin.com/in/ "{query}"`},
				{"Publicaciones de LinkedIn", `site:linkedin.com "{query}"`},
				{"Perfiles de Twitter/X", `site:twitter.com "{query}"`},
				{"Perfiles de GitHub", `site:github.com "{query}"`},
				{"Repositorios de GitHub", `site:github.com/repos "{query}"`},
				{"Perfiles de Instagram", `site:instagram.com "{query}"`},
				{"Perfiles de Facebook", `site:facebook.com "{query}"`},
				{"Perfiles de Reddit", `site:reddit.com "{query}"`},
				{"Perfiles de Telegram", `site:t.me "{query}"`},
			},
		},
		{
			Name: "Infraestructura & Servidores",
			Icon: "🖥️",
			Dorks: []Dork{
				{"Directorios Públicos Expuestos", `intitle:"index of" "{query}"`},
				{"Páginas de Login/Admin", `"{query}" (inurl:login OR inurl:admin OR inurl:signin)`},
				{"Paneles de Control", `"{query}" (inurl:dashboard OR inurl:panel OR inurl:cpanel)`},
				{"APIs Expuestas", `"{query}" (inurl:/api/ OR inurl:/v1/ OR inurl:/v2/)`},
				{"Archivos .htaccess", `"{query}" filetype:htaccess`},
				{"Errores de Servidor", `"{query}" (intext:"SQL syntax" OR intext:"Warning: mysql")`},
				{"Instalaciones WordPress", `"{query}" inurl:wp-content OR inurl:wp-admin`},
				{"phpMyAdmin", `"{query}" inurl:phpmyadmin`},
				{"Cámaras IP Expuestas", `inurl:"/view/index.shtml" "{query}"`},
			},
		},
		{
			Name: "Inteligencia de Empresa",
			Icon: "🏢",
			Dorks: []Dork{
				{"Empleados y Personal", `site:linkedin.com/in/ "{query}" employees`},
				{"Comunicados de Prensa", `"{query}" filetype:pdf intext:"press release"`},
				{"Informes Anuales", `"{query}" filetype:pdf "annual report"`},
				{"Contratos y Licitaciones", `"{query}" filetype:pdf (contrato OR licitacion OR contract)`},
				{"Documentos Judiciales", `"{query}" (intext:"vs." OR intext:"demanda" OR intext:"lawsuit") filetype:pdf`},
				{"Patentes", `site:patents.google.com "{query}"`},
			},
		},
		{
			Name: "Búsqueda Avanzada",
			Icon: "🔍",
			Dorks: []Dork{
				{"Correos Electrónicos Filtrados", `"{query}" intext:"@gmail.com" OR intext:"@yahoo.com" OR intext:"@outlook.com"`},
				{"Documentos en Pastebin", `site:pastebin.com "{query}"`},
				{"Datos en GitHub Gist", `site:gist.github.com "{query}"`},
				{"Caché de Google", `cache:"{query}"`},
				{"Subdominios Expuestos", `site:*.{query}`},
				{"Menciones en Foros", `"{query}" site:forum.* OR site:*.forum.*`},
				{"Credenciales Filtradas", `"{query}" intext:password OR intext:passwd filetype:txt`},
				{"Claves API en Código", `"{query}" intext:"api_key" OR intext:"apikey" site:github.com`},
				{"Tokens de Acceso", `"{query}" intext:"access_token" OR intext:"bearer" site:github.com`},
			},
		},
	}
}
