import json
import tkinter as tk
from tkinter import simpledialog, filedialog, Checkbutton, BooleanVar
import os
import shutil
import docx
import PyPDF2


with open('palabras_ponderadas.json', 'r', encoding='utf-8') as f:
    diccionario = json.load(f)

# **Función para encontrar número de palabras coincidentes.
def puntaje(p_nota : list, p_clave_ponderada : dict):
    result = 0
    for palabra in p_nota:
        # .get(palabra, 0) busca la palabra.
        # Si la encuentra, devuelve su peso (ej. 10).
        # Si no la encuentra, devuelve 0.
        result += p_clave_ponderada.get(palabra, 0)
    return result

# **Función para encontrar curso con más coincidencias. Retorna nombre del curso.
def curso_mayor(p_nota, dicti : dict):
    max_puntaje = 0
    result = ""
    # 'i' ahora es el nombre del curso (ej. "Cálculo_diferencial")
    for i in dicti:
        # Pasamos solo el diccionario anidado de "palabras_clave"
        palabras_del_curso = dicti[i]["palabras_clave"]
        temp = puntaje(p_nota, palabras_del_curso)

        if max_puntaje < temp:
            max_puntaje = temp
            result = i
    return result

# **Función para remover tildes y puntuacion
def limpiar_nota(nota : str):
    actual = ['á', 'é', 'í', 'ó', 'ú', '.', ',', ':', ';', '"', '(', ')', '?', '¿', '!', '¡', '\'']
    nuevo = ['a', 'e', 'i', 'o', 'u', '', '', '', '', '', '', '', '', '', '', '', '']
    for i in range(len(actual)):
        nota = nota.replace(actual[i], nuevo[i])
    return nota

# --- Paleta de Colores ---
COLOR_FONDO = "#001233"
COLOR_BTN_1 = "#0466c8"
COLOR_BTN_2 = "#023e7d"
COLOR_BTN_3 = "#33415c"
COLOR_BTN_4 = "#5c677d"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_OK = "#90EE90"  # Verde claro
COLOR_TEXTO_ERR = "#FFB3BA" # Rojo claro

# --- Función para Limpiar la Ventana ---
def clear_window(ventana_local):
    """Destruye todos los widgets 'hijos' de la ventana para cambiar de vista."""
    # Desconfigura las filas/columnas de la cuadrícula
    ventana_local.grid_rowconfigure(0, weight=0)
    ventana_local.grid_rowconfigure(1, weight=0)
    ventana_local.grid_columnconfigure(0, weight=0)
    ventana_local.grid_columnconfigure(1, weight=0)
    
    for widget in ventana_local.winfo_children():
        widget.destroy()

# --- Lógica de Clasificación (Basada en test.py) ---
# (Esta función ahora se llama desde la nueva interfaz)
def on_clasificar_nota(entry_widget, result_label):
    """
    Toma el texto del widget de entrada, lo clasifica (simulado)
    y actualiza la etiqueta de resultado.
    """
    nota = entry_widget.get() # Obtener texto del widget Entry
    if not nota:
        result_label.config(text="Por favor, ingrese una nota.", fg=COLOR_TEXTO_ERR)
        return
    
    # --- SIMULACIÓN (para demostración) ---
    # (Reemplaza esto con tu lógica real)
    print(f"Clasificando: {nota}")
    nota = limpiar_nota(nota)  # Limpiar tildes y puntuación
    palabras_nota = nota.split()  # Separar en palabras
    curso = curso_mayor(palabras_nota, diccionario)

    if curso == "":
        resultado_texto = "No se encontró coincidencia"
        result_label.config(text=resultado_texto, fg=COLOR_TEXTO_ERR)
        
    else:
        resultado_texto = f"La nota fue clasificada en el curso: {curso}"
        result_label.config(text=resultado_texto, fg=COLOR_TEXTO_OK)


# --- "VISTA 2": Interfaz de Clasificación de Nota (Inspirada en test.py) ---
def draw_clasificar_nota_view():
    clear_window(ventana)
    
    # Usamos un Frame para centrar todo
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="both", expand=True)

    # Configurar cuadrícula interna para centrar
    frame.grid_rowconfigure(0, weight=1) # Espacio arriba
    frame.grid_rowconfigure(5, weight=1) # Espacio para el botón de volver
    frame.grid_rowconfigure(6, weight=1) # Espacio abajo
    frame.grid_columnconfigure(0, weight=1)
    
    # 1. Etiqueta de instrucciones
    instruccion = tk.Label(
        frame,
        text="Ingrese una nota académica:",
        font=("Arial", 16),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    )
    instruccion.grid(row=1, column=0, pady=10)

    # 2. Campo de entrada de texto
    # (Usamos ipady para hacerlo más alto)
    entrada_nota = tk.Entry(
        frame,
        width=60,
        font=("Arial", 14),
        bg="#FFFFFF",
        fg="#000000",
        relief="flat",
        insertbackground="#000000" # Color del cursor
    )
    entrada_nota.grid(row=2, column=0, pady=10, padx=30, ipady=10, sticky="ew")

    # 3. Etiqueta para mostrar el resultado
    resultado_label = tk.Label(
        frame,
        text="",
        font=("Arial", 14, "italic"),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    )
    resultado_label.grid(row=3, column=0, pady=10)

    # 4. Botón para clasificar
    boton_clasificar = tk.Button(
        frame,
        text="Clasificar nota",
        command=lambda: on_clasificar_nota(entrada_nota, resultado_label),
        font=("Arial", 14, "bold"),
        bg=COLOR_BTN_1,
        fg=COLOR_TEXTO,
        relief="flat",
        activebackground=COLOR_BTN_2,
        activeforeground=COLOR_TEXTO,
        pady=10
    )
    boton_clasificar.grid(row=4, column=0, pady=20)

    # 5. Botón para Volver al Menú
    boton_volver = tk.Button(
        frame,
        text="← Volver al Menú",
        command=draw_main_menu, # Vuelve a "dibujar" el menú principal
        font=("Arial", 10),
        bg=COLOR_BTN_4,
        fg=COLOR_TEXTO,
        relief="flat",
        activebackground=COLOR_BTN_3,
        activeforeground=COLOR_TEXTO,
        pady=5
    )
    boton_volver.grid(row=5, column=0, pady=20, padx=20, sticky="sw") # Abajo a la izquierda






def on_clasificar_archivo(filepath_var, check_var, result_label):
    """
    Función de lógica para leer, clasificar y (opcionalmente) copiar
    el archivo seleccionado.
    """
    
    filepath = filepath_var.get()
    if not filepath:
        result_label.config(text="Error: No se ha seleccionado ningún archivo.", fg=COLOR_TEXTO_ERR)
        return

    result_label.config(text=f"Leyendo archivo...\n{os.path.basename(filepath)}", fg=COLOR_TEXTO)
    ventana.update_idletasks() # Forzar actualización de la UI

    texto_completo = ""
    try:
        # --- 1. Extraer Texto del Archivo ---
        if filepath.lower().endswith(".pdf"):
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    texto_completo += page.extract_text()
                    
        elif filepath.lower().endswith(".docx"):
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                texto_completo += para.text + "\n"
        
        if not texto_completo:
            result_label.config(text="Error: No se pudo extraer texto del archivo.", fg=COLOR_TEXTO_ERR)
            return

        # --- 2. Clasificar (Usando tus funciones existentes) ---
        # (Asegúrate de tener 'diccionario' cargado desde tu JSON)
        # (Asegúrate de que 'limpiar_nota' y 'curso_mayor' existan)
        nota_limpia = limpiar_nota(texto_completo.lower())
        palabras_nota = nota_limpia.split()
        curso = curso_mayor(palabras_nota, diccionario)

        # --- 3. Mostrar Resultado y Manejar Copia ---
        if curso == "":
            resultado_texto = "No se encontró coincidencia."
            result_label.config(text=resultado_texto, fg=COLOR_TEXTO_ERR)
        else:
            resultado_texto = f"El archivo fue clasificado en el curso: {curso}"
            
            # --- Lógica de la Casilla de Verificación ---
            if check_var.get(): # Si la casilla está marcada
                try:
                    # Crear la carpeta del curso si no existe
                    os.makedirs(curso, exist_ok=True)
                    
                    # Copiar el archivo original a la nueva carpeta
                    shutil.copy(filepath, curso)
                    
                    resultado_texto += f"\n\nCopia guardada en la carpeta: '{curso}/'"
                except Exception as e:
                    resultado_texto += f"\n\nError al copiar archivo: {e}"

            result_label.config(text=resultado_texto, fg=COLOR_TEXTO_OK)

    except Exception as e:
        result_label.config(text=f"Error inesperado: {e}", fg=COLOR_TEXTO_ERR)


def draw_clasificar_archivo_view():
    """
    Dibuja la interfaz para seleccionar un archivo .pdf o .docx,
    clasificarlo y mostrar el resultado.
    """
    clear_window(ventana)

    # --- Variables de Tkinter ---
    # Usamos estas variables para rastrear el estado de los widgets
    
    # Almacena la ruta del archivo seleccionado
    filepath_var = tk.StringVar() 
    # Almacena el estado (True/False) de la casilla
    copy_check_var = tk.BooleanVar(value=True) # Marcada por defecto

    # --- Contenedor Principal ---
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1) # Espacio arriba
    frame.grid_rowconfigure(6, weight=1) # Espacio para el botón de volver
    frame.grid_rowconfigure(7, weight=1) # Espacio abajo
    frame.grid_columnconfigure(0, weight=1)

    # --- Widgets de la Interfaz ---

    # 1. Etiqueta de instrucciones
    instruccion = tk.Label(
        frame,
        text="Clasificar un archivo (.pdf o .docx):",
        font=("Arial", 16),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    )
    instruccion.grid(row=1, column=0, pady=10)

    # 2. Etiqueta para mostrar el archivo seleccionado
    selected_file_label = tk.Label(
        frame,
        text="Aún no se ha seleccionado ningún archivo.",
        font=("Arial", 12, "italic"),
        fg=COLOR_BTN_4, # Color gris
        bg=COLOR_FONDO
    )
    selected_file_label.grid(row=2, column=0, pady=5)

    # --- Función interna para manejar la selección de archivos ---
    def seleccionar_archivo():
        filepath = filedialog.askopenfilename(
            title="Seleccionar Archivo",
            filetypes=(("Documentos", "*.pdf *.docx"), ("Todos los archivos", "*.*")),
            parent=ventana
        )
        if filepath:
            filepath_var.set(filepath) # Guardar la ruta
            # Mostrar solo el nombre del archivo
            selected_file_label.config(text=os.path.basename(filepath), fg=COLOR_TEXTO)
        
    # 3. Botón para Seleccionar Archivo
    boton_seleccionar = tk.Button(
        frame,
        text="Seleccionar Archivo...",
        command=seleccionar_archivo,
        font=("Arial", 12, "bold"),
        bg=COLOR_BTN_2,
        fg=COLOR_TEXTO,
        relief="flat",
        pady=10
    )
    boton_seleccionar.grid(row=3, column=0, pady=10)

    # 4. Casilla de Verificación (Checkbutton) para guardar copia
    check_guardar = Checkbutton(
        frame,
        text="Crear carpeta del curso y guardar una copia del archivo",
        variable=copy_check_var, # Vinculada a nuestra variable booleana
        font=("Arial", 11),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        selectcolor=COLOR_FONDO, # Fondo del cuadradito
        activebackground=COLOR_FONDO,
        activeforeground=COLOR_TEXTO,
        highlightthickness=0,
        bd=0
    )
    check_guardar.grid(row=4, column=0, pady=10, padx=20)

    # 5. Etiqueta para mostrar el resultado
    resultado_label = tk.Label(
        frame,
        text="",
        font=("Arial", 13),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO,
        wraplength=600 # Para que el texto no se salga de la ventana
    )
    resultado_label.grid(row=5, column=0, pady=15)
    
    # 6. Botón para Clasificar
    # Este botón llama a la lógica 'on_clasificar_archivo'
    boton_clasificar = tk.Button(
        frame,
        text="Clasificar Archivo",
        command=lambda: on_clasificar_archivo(filepath_var, copy_check_var, resultado_label),
        font=("Arial", 14, "bold"),
        bg=COLOR_BTN_1,
        fg=COLOR_TEXTO,
        relief="flat",
        pady=10
    )
    boton_clasificar.grid(row=6, column=0, pady=(10, 20))

    # 7. Botón para Volver al Menú
    boton_volver = tk.Button(
        frame,
        text="← Volver al Menú",
        command=draw_main_menu,
        font=("Arial", 10),
        bg=COLOR_BTN_4,
        fg=COLOR_TEXTO,
        relief="flat",
        activebackground=COLOR_BTN_3,
        activeforeground=COLOR_TEXTO,
        pady=5
    )
    boton_volver.grid(row=7, column=0, pady=20, padx=20, sticky="sw")








# --- "VISTA 1": Menú Principal (4 botones) ---
def draw_main_menu():
    clear_window(ventana)

    # Configuración de la Cuadrícula 2x2
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_rowconfigure(1, weight=1)
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)

    # Estilo Común
    estilo_boton = {
        "font": ("Arial", 16, "bold"),
        "fg": COLOR_TEXTO,
        "relief": "flat",
        "borderwidth": 0,
        "pady": 20,
        "padx": 20
    }

    # Botón 1: Clasificar notas
    btn_notas = tk.Button(
        ventana,
        text="1. Clasificar Nota",
        command=draw_clasificar_nota_view, # <-- ESTE ES EL CAMBIO CLAVE
        bg=COLOR_BTN_1,
        activebackground=COLOR_BTN_2,
        activeforeground=COLOR_TEXTO,
        **estilo_boton
    )
    btn_notas.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Botón 2: Clasificar archivo
    btn_archivo = tk.Button(
        ventana,
        text="2. Clasificar Archivo\n(PDF, DOCX)",
        command=draw_clasificar_archivo_view, # Placeholder
        bg=COLOR_BTN_2,
        activebackground=COLOR_BTN_1,
        activeforeground=COLOR_TEXTO,
        **estilo_boton
    )
    btn_archivo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    # Botón 3: Clasificar carpeta
    btn_carpeta = tk.Button(
        ventana,
        text="3. Clasificar Carpeta",
        command=on_clasificar_carpeta, # Placeholder
        bg=COLOR_BTN_3,
        activebackground=COLOR_BTN_4,
        activeforeground=COLOR_TEXTO,
        **estilo_boton
    )
    btn_carpeta.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    # Botón 4: Clasificar foto
    btn_foto = tk.Button(
        ventana,
        text="4. Clasificar Foto (OCR)",
        command=on_clasificar_foto, # Placeholder
        bg=COLOR_BTN_4,
        activebackground=COLOR_BTN_3,
        activeforeground=COLOR_TEXTO,
        **estilo_boton
    )
    btn_foto.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

# --- Funciones (Placeholder) para botones 2, 3, 4 ---
# (Siguen abriendo diálogos por ahora)

def on_clasificar_carpeta():
    folderpath = filedialog.askdirectory(title="3. Seleccionar Carpeta", parent=ventana)
    if folderpath: print(f"Carpeta seleccionada: {folderpath}")

def on_clasificar_foto():
    filepath = filedialog.askopenfilename(
        title="4. Seleccionar Foto (OCR)",
        filetypes=(("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")),
        parent=ventana
    )
    if filepath: print(f"Foto seleccionada: {filepath}")

# --- Creación de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("Clasificador de Notas")
ventana.geometry("700x500")
ventana.config(bg=COLOR_FONDO)

# --- Iniciar la aplicación ---
draw_main_menu() # Dibuja el menú principal al iniciar
ventana.mainloop()
