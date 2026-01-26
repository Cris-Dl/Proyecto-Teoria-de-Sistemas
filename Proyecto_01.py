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
            self.root.destroy()
            ventana_principal = tk.Tk()
            app = SistemaGEOS(ventana_principal)
            ventana_principal.mainloop()
        else:
            messagebox.showerror("ERROR", "Error en sus credenciales, inténtelo de nuevo.")


class SistemaGEOS:
    def __init__(self, root):
        self.root = root
        self.root.title("GEOS - Herramientas y Equipos")
        self.root.state('zoomed')
        self.root.configure(bg="#FFFFFF")

        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)

        self.COLOR_AZUL = "#0055A5"
        self.COLOR_AZUL_CLARO = "#1E88E5"
        self.COLOR_FONDO = "#FFFFFF"

        self.pestana_actual = "Inventario"

        self.inventario = [
            {"id": "GEOS-001", "nombre": "Taladro Percutor XP150", "cantidad": 45, "precio": 84.50,
             "fecha": "2026-01-24"},
            {"id": "GEOS-002", "nombre": "Sierra Circular CS300", "cantidad": 28, "precio": 120.00,
             "fecha": "2026-01-23"},
            {"id": "GEOS-003", "nombre": "Llave de Impacto IW200", "cantidad": 60, "precio": 49.99,
             "fecha": "2026-01-24"},
            {"id": "GEOS-004", "nombre": "Llave de Impacto Pasill 5", "cantidad": 60, "precio": 49.99,
             "fecha": "2026-01-24"},
            {"id": "GEOS-005", "nombre": "Llave de Juceniería", "cantidad": 60, "precio": 40.00, "fecha": "2026-01-24"},
            {"id": "GEOS-006", "nombre": "Pieer edex perfena", "cantidad": 60, "precio": 40.50, "fecha": "2026-01-24"},
        ]

        self.crear_interfaz()
        self.cargar_datos()

    def confirmar_cierre(self):
        respuesta = messagebox.askyesno("Confirmar Salida","¿Está seguro que desea cerrar el programa?")
        if respuesta:
            self.root.destroy()

    def crear_interfaz(self):
        frame_superior = tk.Frame(self.root, bg=self.COLOR_FONDO, height=150)
        frame_superior.pack(fill="x", padx=20, pady=(10, 0))
        frame_superior.pack_propagate(False)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos_2.png")
        self.imagen = tk.PhotoImage(file=ruta_logo)
        label_logo = tk.Label(frame_superior, image=self.imagen, bg=self.COLOR_FONDO)
        label_logo.pack(pady=20)

        frame_nav = tk.Frame(self.root, bg=self.COLOR_AZUL, height=50)
        frame_nav.pack(fill="x")
        frame_nav.pack_propagate(False)

        frame_pestanas = tk.Frame(frame_nav, bg=self.COLOR_AZUL)
        frame_pestanas.place(relx=0.5, rely=0.5, anchor="center")

        pestanas = ["Inventario", "Proveedores", "Clientes", "Reportes", "Configuración"]
        self.botones_pestanas = {}

        for i, pestana in enumerate(pestanas):
            color_bg = self.COLOR_AZUL_CLARO if i == 0 else self.COLOR_AZUL
            btn = tk.Button(frame_pestanas, text=pestana, font=("Arial", 11, "bold"),bg=color_bg, fg="white", relief="flat",cursor="hand2", padx=20, pady=10,command=lambda p=pestana: self.cambiar_pestana(p))
            btn.pack(side="left", padx=2, pady=5, fill="y")
            self.botones_pestanas[pestana] = btn

        self.frame_contenido = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=10)

        frame_herramientas = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_herramientas.pack(fill="x", pady=(0, 15))

        frame_busqueda = tk.Frame(frame_herramientas, bg="white",highlightbackground="#CCCCCC", highlightthickness=1)
        frame_busqueda.pack(side="left", padx=(0, 10))

        tk.Label(frame_busqueda, text="🔍", font=("Arial", 12),bg="white").pack(side="left", padx=(10, 5))
        self.entry_buscar = tk.Entry(frame_busqueda, font=("Arial", 11),relief="flat", width=30, bg="white")
        self.entry_buscar.pack(side="left", padx=(0, 10), pady=8)
        self.entry_buscar.insert(0, "Buscar...")
        self.entry_buscar.bind("<FocusIn>", self.clear_buscar)
        self.entry_buscar.bind("<FocusOut>", self.restore_buscar)
        self.entry_buscar.bind("<KeyRelease>", self.buscar_item)

        tk.Button(frame_herramientas, text="Agregar Nuevo", font=("Arial", 10, "bold"),bg="white", fg=self.COLOR_AZUL, relief="solid",borderwidth=2, cursor="hand2", padx=15, pady=5,command=self.agregar_item).pack(side="left", padx=5)

        tk.Button(frame_herramientas, text="Editar", font=("Arial", 10, "bold"),bg=self.COLOR_AZUL, fg="white", relief="flat",cursor="hand2", padx=20, pady=5,command=self.editar_item).pack(side="left", padx=5)

        tk.Button(frame_herramientas, text="Eliminar", font=("Arial", 10, "bold"),bg="#DC3545", fg="white", relief="flat",cursor="hand2", padx=20, pady=5,command=self.eliminar_item).pack(side="left", padx=5)

        tk.Button(frame_herramientas, text="📊 Exportar a Excel", font=("Arial", 10, "bold"),bg=self.COLOR_AZUL, fg="white", relief="flat",cursor="hand2", padx=15, pady=5,command=self.exportar_excel).pack(side="right", padx=5)

        self.crear_tabla()

        self.frame_estado = tk.Frame(self.root, bg="#F0F0F0", height=30)
        self.frame_estado.pack(fill="x", side="bottom")
        self.frame_estado.pack_propagate(False)

        self.label_estado = tk.Label(self.frame_estado, text="Total de ítems: 0",font=("Arial", 9), bg="#F0F0F0", fg="#333333")
        self.label_estado.pack(side="left", padx=20, pady=5)

    def crear_tabla(self):
        frame_tabla = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="white",foreground="#333333",rowheight=30,fieldbackground="white",font=("Arial", 10))
        style.configure("Treeview.Heading",background=self.COLOR_AZUL,foreground="white",font=("Arial", 10, "bold"),relief="flat")
        style.map("Treeview", background=[("selected", self.COLOR_AZUL_CLARO)])

        columnas = ("ID", "Nombre", "Cantidad", "Precio", "Última Actualización")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre del Equipo/Herramienta")
        self.tabla.heading("Cantidad", text="Cantidad Disponible")
        self.tabla.heading("Precio", text="Precio Unitario")
        self.tabla.heading("Última Actualización", text="Última Actualización")

        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Nombre", width=350, anchor="w")
        self.tabla.column("Cantidad", width=150, anchor="center")
        self.tabla.column("Precio", width=120, anchor="center")
        self.tabla.column("Última Actualización", width=180, anchor="center")

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.pack(fill="both", expand=True)

        self.tabla.bind("<Double-1>", lambda e: self.editar_item())

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for item in self.inventario:
            self.tabla.insert("", "end", values=(
                item["id"],
                item["nombre"],
                item["cantidad"],
                f"${item['precio']:.2f}",
                item["fecha"]
            ))

        self.actualizar_estado()

    def actualizar_estado(self):
        total = len(self.inventario)
        fecha_hora = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        self.label_estado.config(text=f"Total de ítems: {total} | Última sincronización: {fecha_hora}")

    def clear_buscar(self, event):
        if self.entry_buscar.get() == "Buscar...":
            self.entry_buscar.delete(0, 'end')

    def restore_buscar(self, event):
        if self.entry_buscar.get() == "":
            self.entry_buscar.insert(0, "Buscar...")

    def buscar_item(self, event):
        termino = self.entry_buscar.get().lower()
        if termino == "buscar...":
            self.cargar_datos()
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for item in self.inventario:
            if (termino in item["id"].lower() or
                    termino in item["nombre"].lower()):
                self.tabla.insert("", "end", values=(
                    item["id"],
                    item["nombre"],
                    item["cantidad"],
                    f"${item['precio']:.2f}",
                    item["fecha"]
                ))

    def agregar_item(self):
        VentanaAgregar(self.root, self)

    def editar_item(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ítem para editar")
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        item_completo = None
        for i in self.inventario:
            if i["id"] == valores[0]:
                item_completo = i
                break

        if item_completo:
            VentanaEditar(self.root, self, item_completo)

    def eliminar_item(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ítem para eliminar")
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        respuesta = messagebox.askyesno("Confirmar",f"¿Está seguro de eliminar el ítem {valores[0]} - {valores[1]}?")
        if respuesta:
            self.inventario = [i for i in self.inventario if i["id"] != valores[0]]
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Ítem eliminado correctamente")

    def exportar_excel(self):
        messagebox.showinfo("Exportar","Funcionalidad de exportación a Excel\n(Requiere librería openpyxl o xlsxwriter)")

    def cambiar_pestana(self, pestana):
        if pestana == self.pestana_actual:
            return

        self.pestana_actual = pestana

        for nombre, boton in self.botones_pestanas.items():
            if nombre == pestana:
                boton.config(bg=self.COLOR_AZUL_CLARO)
            else:
                boton.config(bg=self.COLOR_AZUL)

        if pestana != "Inventario":
            messagebox.showinfo("Navegación", f"Navegando a: {pestana}\n(Funcionalidad pendiente)")


class VentanaAgregar:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Nuevo Ítem")
        self.ventana.geometry("500x450")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Agregar Nuevo Ítem", font=("Arial", 18, "bold"),bg="#FFFFFF", fg=COLOR_AZUL).pack(pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(frame_form, text="ID:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=10)
        self.entry_id = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_id.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=10)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_nombre.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Cantidad:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=10)
        self.entry_cantidad = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_cantidad.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Precio:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=10)
        self.entry_precio = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_precio.grid(row=3, column=1, pady=10, padx=10)

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"),bg=COLOR_AZUL, fg="white", relief="flat",cursor="hand2", padx=30, pady=8,command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"),bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8,command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 500
        alto = 450
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        id_item = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        precio = self.entry_precio.get().strip()

        if not all([id_item, nombre, cantidad, precio]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser valores numéricos")
            return

        for item in self.sistema.inventario:
            if item["id"] == id_item:
                messagebox.showerror("Error", "El ID ya existe")
                return

        nuevo_item = {
            "id": id_item,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }

        self.sistema.inventario.append(nuevo_item)
        self.sistema.cargar_datos()
        messagebox.showinfo("Éxito", "Ítem agregado correctamente")
        self.ventana.destroy()


class VentanaEditar:
    def __init__(self, parent, sistema, item):
        self.sistema = sistema
        self.item_original = item
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Ítem")
        self.ventana.geometry("500x450")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Editar Ítem", font=("Arial", 18, "bold"),bg="#FFFFFF", fg=COLOR_AZUL).pack(pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(frame_form, text="ID:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=10)
        self.entry_id = tk.Entry(frame_form, font=("Arial", 11), width=30, state="disabled")
        self.entry_id.grid(row=0, column=1, pady=10, padx=10)
        self.entry_id.insert(0, item["id"])

        tk.Label(frame_form, text="Nombre:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=10)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_nombre.grid(row=1, column=1, pady=10, padx=10)
        self.entry_nombre.insert(0, item["nombre"])

        tk.Label(frame_form, text="Cantidad:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=10)
        self.entry_cantidad = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_cantidad.grid(row=2, column=1, pady=10, padx=10)
        self.entry_cantidad.insert(0, item["cantidad"])

        tk.Label(frame_form, text="Precio:", font=("Arial", 11, "bold"),bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=10)
        self.entry_precio = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_precio.grid(row=3, column=1, pady=10, padx=10)
        self.entry_precio.insert(0, item["precio"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"),bg=COLOR_AZUL, fg="white", relief="flat",cursor="hand2", padx=30, pady=8,command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"),bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8,command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 500
        alto = 450
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        precio = self.entry_precio.get().strip()

        if not all([nombre, cantidad, precio]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser valores numéricos")
            return

        self.item_original["nombre"] = nombre
        self.item_original["cantidad"] = cantidad
        self.item_original["precio"] = precio
        self.item_original["fecha"] = datetime.now().strftime("%Y-%m-%d")

        self.sistema.cargar_datos()
        messagebox.showinfo("Éxito", "Ítem actualizado correctamente")
        self.ventana.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()