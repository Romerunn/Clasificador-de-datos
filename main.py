import tkinter as tk
from tkinter import filedialog, messagebox
from logic.classification_logic import cargar_diccionario, clasificar_nota

# --- Paleta de Colores ---
COLOR_FONDO = "#001233"
COLOR_BTN_1 = "#0466c8"
COLOR_BTN_2 = "#023e7d"
COLOR_BTN_3 = "#33415c"
COLOR_BTN_4 = "#5c677d"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_OK = "#90EE90"  # Verde claro
COLOR_TEXTO_ERR = "#FFB3BA" # Rojo claro

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clasificador de Notas")
        self.geometry("700x500")
        self.config(bg=COLOR_FONDO)
        self.diccionario = cargar_diccionario()
        self.draw_main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def on_clasificar_nota(self, entry_widget, result_label):
        nota = entry_widget.get()
        if not nota:
            result_label.config(text="Por favor, ingrese una nota.", fg=COLOR_TEXTO_ERR)
            return

        curso = clasificar_nota(nota, self.diccionario)

        if curso:
            resultado_texto = f"La nota fue clasificada en el curso: {curso}"
            result_label.config(text=resultado_texto, fg=COLOR_TEXTO_OK)
            messagebox.showinfo("Resultado", resultado_texto)
        else:
            resultado_texto = "No se encontró coincidencia"
            result_label.config(text=resultado_texto, fg=COLOR_TEXTO_ERR)
            messagebox.showinfo("Resultado", resultado_texto)

    def on_clasificar_archivo(self):
        filepath = filedialog.askopenfilename(
            title="2. Seleccionar Archivo",
            filetypes=(("Documentos", "*.pdf *.docx"), ("Todos los archivos", "*.*")),
        )
        if filepath: print(f"Archivo seleccionado: {filepath}")

    def on_clasificar_carpeta(self):
        folderpath = filedialog.askdirectory(title="3. Seleccionar Carpeta")
        if folderpath: print(f"Carpeta seleccionada: {folderpath}")

    def on_clasificar_foto(self):
        filepath = filedialog.askopenfilename(
            title="4. Seleccionar Foto (OCR)",
            filetypes=(("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")),
        )
        if filepath: print(f"Foto seleccionada: {filepath}")

    def draw_main_menu(self):
        self.clear_window()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        estilo_boton = {
            "font": ("Arial", 16, "bold"),
            "fg": COLOR_TEXTO,
            "relief": "flat",
            "borderwidth": 0,
            "pady": 20,
            "padx": 20
        }

        btn_notas = tk.Button(self, text="1. Clasificar Nota", command=self.draw_clasificar_nota_view, bg=COLOR_BTN_1, activebackground=COLOR_BTN_2, activeforeground=COLOR_TEXTO, **estilo_boton)
        btn_notas.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        btn_archivo = tk.Button(self, text="2. Clasificar Archivo\n(PDF, DOCX)", command=self.on_clasificar_archivo, bg=COLOR_BTN_2, activebackground=COLOR_BTN_1, activeforeground=COLOR_TEXTO, **estilo_boton)
        btn_archivo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        btn_carpeta = tk.Button(self, text="3. Clasificar Carpeta", command=self.on_clasificar_carpeta, bg=COLOR_BTN_3, activebackground=COLOR_BTN_4, activeforeground=COLOR_TEXTO, **estilo_boton)
        btn_carpeta.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        btn_foto = tk.Button(self, text="4. Clasificar Foto (OCR)", command=self.on_clasificar_foto, bg=COLOR_BTN_4, activebackground=COLOR_BTN_3, activeforeground=COLOR_TEXTO, **estilo_boton)
        btn_foto.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def draw_clasificar_nota_view(self):
        self.clear_window()
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(fill="both", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        instruccion = tk.Label(frame, text="Ingrese una nota académica:", font=("Arial", 16), fg=COLOR_TEXTO, bg=COLOR_FONDO)
        instruccion.grid(row=1, column=0, pady=10)

        entrada_nota = tk.Entry(frame, width=60, font=("Arial", 14), bg="#FFFFFF", fg="#000000", relief="flat", insertbackground="#000000")
        entrada_nota.grid(row=2, column=0, pady=10, padx=30, ipady=10, sticky="ew")

        resultado_label = tk.Label(frame, text="", font=("Arial", 14, "italic"), fg=COLOR_TEXTO, bg=COLOR_FONDO)
        resultado_label.grid(row=3, column=0, pady=10)

        boton_clasificar = tk.Button(frame, text="Clasificar nota", command=lambda: self.on_clasificar_nota(entrada_nota, resultado_label), font=("Arial", 14, "bold"), bg=COLOR_BTN_1, fg=COLOR_TEXTO, relief="flat", activebackground=COLOR_BTN_2, activeforeground=COLOR_TEXTO, pady=10)
        boton_clasificar.grid(row=4, column=0, pady=20)

        boton_volver = tk.Button(frame, text="← Volver al Menú", command=self.draw_main_menu, font=("Arial", 10), bg=COLOR_BTN_4, fg=COLOR_TEXTO, relief="flat", activebackground=COLOR_BTN_3, activeforeground=COLOR_TEXTO, pady=5)
        boton_volver.grid(row=5, column=0, pady=20, padx=20, sticky="sw")

if __name__ == "__main__":
    app = App()
    app.mainloop()
