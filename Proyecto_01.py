import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("GEOS - Herramientas y Equipos")
        self.root.geometry("500x600")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.COLOR_FONDO = "#FFFFFF"
        self.COLOR_AZUL = "#0055A5"
        self.COLOR_INPUT_BG = "#F0F8FF"
        self.COLOR_TEXTO = "#333333"

        self.centrar_ventana(500, 600)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos.png")

        self.imagen = tk.PhotoImage(file=ruta_logo)
        self.label_logo = tk.Label(self.root, image=self.imagen, bg=self.COLOR_FONDO)
        self.label_logo.pack(pady=(60, 80))

        self.frame_login = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_login.pack()

        self.frame_user = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG,highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_user.pack(pady=(0, 20))

        tk.Label(self.frame_user, text="👤", font=("Arial", 14),bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))

        self.entry_user = tk.Entry(self.frame_user, font=("Arial", 12),bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_user.pack(side="left", padx=(5, 15), pady=15)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.clear_placeholder_user)
        self.entry_user.bind("<FocusOut>", self.restore_placeholder_user)
        self.entry_user.bind("<Return>", lambda event: self.login())

        self.frame_pass = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG,highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_pass.pack(pady=(0, 40))

        tk.Label(self.frame_pass, text="🔒", font=("Arial", 14),bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))

        self.entry_password = tk.Entry(self.frame_pass, font=("Arial", 12),bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_password.pack(side="left", padx=(5, 15), pady=15)
        self.entry_password.insert(0, "Contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_placeholder_pass)
        self.entry_password.bind("<FocusOut>", self.restore_placeholder_pass)
        self.entry_password.bind("<Return>", lambda event: self.login())
        self.password_hidden = False

        self.boton_login = tk.Button(self.frame_login, text="INICIAR SESIÓN",bg=self.COLOR_AZUL, fg="white",font=("Arial", 12, "bold"),relief="flat", cursor="hand2",width=32, height=2,command=self.login)
        self.boton_login.pack()

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def clear_placeholder_user(self, event):
        if self.entry_user.get() == "Usuario":
            self.entry_user.delete(0, 'end')
            self.entry_user.config(fg="#000000")

    def restore_placeholder_user(self, event):
        if self.entry_user.get() == "":
            self.entry_user.insert(0, "Usuario")
            self.entry_user.config(fg="#666666")

    def clear_placeholder_pass(self, event):
        if self.entry_password.get() == "Contraseña":
            self.entry_password.delete(0, 'end')
            self.entry_password.config(show="*", fg="#000000")
            self.password_hidden = True

    def restore_placeholder_pass(self, event):
        if self.entry_password.get() == "":
            self.entry_password.config(show="")
            self.entry_password.insert(0, "Contraseña")
            self.entry_password.config(fg="#666666")
            self.password_hidden = False

    def login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()

        if user == "ADMIN" and password == "1234":
            messagebox.showinfo("Login", "Bienvenido Admin")
            self.root.destroy()
            ventana_principal = tk.Tk()
            app2 = App(ventana_principal)
            ventana_principal.mainloop()
        else:
            messagebox.showerror("ERROR", "Error en sus credenciales, inténtelo de nuevo.")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GEOS - Sistema Principal")
        self.root.geometry("1200x700")
        self.root.configure(bg="#FFFFFF")

        self.COLOR_AZUL = "#0055A5"
        self.COLOR_FONDO = "#FFFFFF"

        #ejemplo
        self.inventario = [
            {"id": "ID", "nombre": "GEOS-001", "cantidad": 45, "precio": 84.50, "fecha": "2026-01-24"},
            {"id": "1", "nombre": "GEOS-001", "cantidad": 45, "precio": 84.50, "fecha": "2026-01-24"}
        ]

        self.crear_interfaz()

    def crear_interfaz(self):
        header_frame = tk.Frame(self.root, bg=self.COLOR_FONDO, height=150)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos.png")

        try:
            logo_img = tk.PhotoImage(file=ruta_logo)
            logo_label = tk.Label(header_frame, image=logo_img, bg=self.COLOR_FONDO)
            logo_label.image = logo_img
            logo_label.pack()
        except:
            tk.Label(header_frame, text="GEOS\nHerramientas y Equipos",font=("Arial", 24, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack()

        # Menú de navegación
        menu_frame = tk.Frame(self.root, bg=self.COLOR_AZUL, height=50)
        menu_frame.pack(fill="x")
        menu_frame.pack_propagate(False)

        botones_menu = ["Inventario", "Proveedores", "Clientes", "Reportes", "Configuración"]
        for i, texto in enumerate(botones_menu):
            bg_color = "white" if i == 0 else "#0066CC"
            fg= self.COLOR_AZUL if i == 0 else "white"

            btn = tk.Button(menu_frame, text=texto, bg=bg_color, fg=fg, font=("Arial", 11, "bold"), relief="flat",cursor="hand2", width=15, height=2)
            btn.pack(side="left", padx=2, pady=5)

        # Frame de contenido
        contenido_frame = tk.Frame(self.root, bg=self.COLOR_FONDO)
        contenido_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame superior con búsqueda y botones
        top_frame = tk.Frame(contenido_frame, bg=self.COLOR_FONDO)
        top_frame.pack(fill="x", pady=(0, 10))

        # Búsqueda
        search_frame = tk.Frame(top_frame, bg=self.COLOR_FONDO)
        search_frame.pack(side="left")

        tk.Label(search_frame, text="🔍", font=("Arial", 12),bg=self.COLOR_FONDO).pack(side="left", padx=(0, 5))

        self.entry_buscar = tk.Entry(search_frame, font=("Arial", 11), width=30, relief="solid", borderwidth=1)
        self.entry_buscar.pack(side="left")
        self.entry_buscar.insert(0, "Buscar...")
        self.entry_buscar.bind("<FocusIn>", self.clear_buscar)
        self.entry_buscar.bind("<FocusOut>", self.restore_buscar)

        # Botones de acción
        btn_frame = tk.Frame(top_frame, bg=self.COLOR_FONDO)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="Exportar a Excel", bg=self.COLOR_AZUL,fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=15, command=self.exportar_excel).pack(side="right", padx=5)

        # Botones de gestión
        btn_frame2 = tk.Frame(contenido_frame, bg=self.COLOR_FONDO)
        btn_frame2.pack(fill="x", pady=(0, 10))

        tk.Button(btn_frame2, text="Agregar Nuevo", bg="white", fg=self.COLOR_AZUL,font=("Arial", 10, "bold"), relief="solid", borderwidth=0.5, cursor="hand2", width=12, command=self.agregar_nuevo).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="Actualizar", bg="white", fg=self.COLOR_AZUL,font=("Arial", 10, "bold"), relief="solid",borderwidth=0.5, cursor="hand2", width=12, command=self.actualizar).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="Eleminar", bg="white", fg=self.COLOR_AZUL,font=("Arial", 10, "bold"), relief="solid", borderwidth=0.5, cursor="hand2", width=12, command=self.eliminar).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="Exportar a Excel", bg=self.COLOR_AZUL, fg="white",font=("Arial", 10, "bold"), relief="flat",cursor="hand2", width=15, command=self.exportar_excel).pack(side="right", padx=5)

        # Tabla de inventario
        tabla_frame = tk.Frame(contenido_frame, bg=self.COLOR_FONDO)
        tabla_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side="right", fill="y")

        # TABLA
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        font=("Arial", 10))
        style.configure("Treeview.Heading",
                        background=self.COLOR_AZUL,
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", "#0066CC")])

        columnas = ("ID", "Nombre", "Tuable", "Precio Uio 1", "Última Actualización")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                                 yscrollcommand=scrollbar.set, height=15)

        # Configurar colores alternados DESPUÉS de crear el tree
        self.tree.tag_configure('oddrow', background='#E6F2FF')  # Azul pálido
        self.tree.tag_configure('evenrow', background='white')  # Blanco

        # Colmn
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Equipo/Heremienta")
        self.tree.heading("Tuable", text="Cantidad Disponible")
        self.tree.heading("Precio Uio 1", text="Pecio Uio 1")
        self.tree.heading("Última Actualización", text="Última Actualización")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=300, anchor="w")
        self.tree.column("Tuable", width=150, anchor="center")
        self.tree.column("Precio Uio 1", width=150, anchor="center")
        self.tree.column("Última Actualización", width=200, anchor="center")

        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill="both", expand=True)

        # Llenar tabla con datos
        self.actualizar_tabla()

        footer_frame = tk.Frame(self.root, bg=self.COLOR_FONDO)
        footer_frame.pack(fill="x", padx=20, pady=10)

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(footer_frame,
                 text=f"Total de ítems: 125  |  Última sinciniación: 208-25 17:35 PM CST",
                 font=("Arial", 9), bg=self.COLOR_FONDO, fg="#666666").pack(side="left")

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, item in enumerate(self.inventario):
            # Alternar etiquetas entre filas pares e impares
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'

            self.tree.insert("", "end", values=(
                item["id"],
                item["nombre"],
                item["cantidad"],
                f"${item['precio']:.2f}" if isinstance(item['precio'], (int, float)) else item['precio'],
                item["fecha"]
            ), tags=(tag,))

    def clear_buscar(self, event):
        if self.entry_buscar.get() == "Buscar...":
            self.entry_buscar.delete(0, 'end')

    def restore_buscar(self, event):
        if self.entry_buscar.get() == "":
            self.entry_buscar.insert(0, "Buscar...")

    def agregar_nuevo(self):
        messagebox.showinfo("Agregar", "Funcionalidad de agregar nuevo item")

    def actualizar(self):
        messagebox.showinfo("Actualizar", "Funcionalidad de agregar nuevo item")

    def eliminar(self):
        selection= self.tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Desea eliminar el item seleccionado?"):
                self.tree.delete(selection)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un item para eliminar")

    def exportar_excel(self):
        messagebox.showinfo("Exportar", "Exportando datos a Excel...")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()