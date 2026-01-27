import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os
import sqlite3


class TablasDB:
    DB_NAME = "geos_inventario.db"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(TablasDB.DB_NAME)
        conn.row_factory = sqlite3.Row

        conn.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                telefono TEXT NOT NULL,
                encargado TEXT,
                informacion TEXT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                precio_compra REAL,
                precio_venta REAL,
                categoria TEXT NOT NULL,
                cantidad REAL,
                proveedor TEXT NOT NULL
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            );
        """)

        conn.commit()
        return conn


class CategoriasDB:
    @staticmethod
    def obtener_todas():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT nombre FROM categorias ORDER BY nombre")
            return [row["nombre"] for row in cursor]
        finally:
            conn.close()

    @staticmethod
    def agregar(nombre):
        conn = TablasDB._conn()
        try:
            conn.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(nombre):
        conn = TablasDB._conn()
        try:
            conn.execute("DELETE FROM categorias WHERE nombre = ?", (nombre,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()


class ProductosDB:
    @staticmethod
    def obtener_todos():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT * FROM productos ORDER BY codigo")
            items = []
            for row in cursor:
                items.append({
                    "id_num": row["id_num"],
                    "nombre": row["nombre"],
                    "codigo": row["codigo"],
                    "precio_compra": row["precio_compra"],
                    "precio_venta": row["precio_venta"],
                    "categoria": row["categoria"],
                    "cantidad": row["cantidad"],
                    "proveedor": row["proveedor"]
                })
            return items
        finally:
            conn.close()

    @staticmethod
    def agregar(nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor):
        conn = TablasDB._conn()
        try:
            conn.execute(
                """INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_num, nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute(
                """UPDATE productos SET nombre = ?, codigo = ?, precio_compra = ?, precio_venta = ?, 
                   categoria = ?, cantidad = ?, proveedor = ? WHERE id_num = ?""",
                (nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor, id_num)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_num):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("DELETE FROM productos WHERE id_num = ?", (id_num,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class ProveedoresDB:
    @staticmethod
    def obtener_todos():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT * FROM proveedores ORDER BY nombre")
            proveedores = []
            for row in cursor:
                proveedores.append({
                    "id_num": row["id_num"],
                    "nombre": row["nombre"],
                    "codigo": row["codigo"],
                    "telefono": row["telefono"],
                    "encargado": row["encargado"] or "",
                    "informacion": row["informacion"] or ""
                })
            return proveedores
        finally:
            conn.close()

    @staticmethod
    def obtener_nombres():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT nombre FROM proveedores ORDER BY nombre")
            return [row["nombre"] for row in cursor]
        finally:
            conn.close()

    @staticmethod
    def agregar(nombre, codigo, telefono, encargado="", informacion=""):
        conn = TablasDB._conn()
        try:
            conn.execute(
                "INSERT INTO proveedores (nombre, codigo, telefono, encargado, informacion) VALUES (?, ?, ?, ?, ?)",
                (nombre, codigo, telefono, encargado, informacion)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_num):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("DELETE FROM proveedores WHERE id_num = ?", (id_num,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_num, nombre, codigo, telefono, encargado="", informacion=""):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute(
                "UPDATE proveedores SET nombre = ?, codigo = ?, telefono = ?, encargado = ?, informacion = ? WHERE id_num = ?",
                (nombre, codigo, telefono, encargado, informacion, id_num)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


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

        # Ruta segura para logos
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos.png")

        try:
            self.imagen = tk.PhotoImage(file=ruta_logo)
            self.label_logo = tk.Label(self.root, image=self.imagen, bg=self.COLOR_FONDO)
            self.label_logo.pack(pady=(60, 80))
        except:
            tk.Label(self.root, text="GEOS", font=("Arial", 48, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(
                pady=(60, 20))
            tk.Label(self.root, text="Herramientas y Equipos", font=("Arial", 14), bg=self.COLOR_FONDO,
                     fg=self.COLOR_AZUL).pack(pady=(0, 60))

        self.frame_login = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_login.pack()

        self.frame_user = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG, highlightbackground=self.COLOR_AZUL,
                                   highlightthickness=2)
        self.frame_user.pack(pady=(0, 20))

        tk.Label(self.frame_user, text="👤", font=("Arial", 14), bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(
            side="left", padx=(15, 5))

        self.entry_user = tk.Entry(self.frame_user, font=("Arial", 12), bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,
                                   relief="flat", width=28)
        self.entry_user.pack(side="left", padx=(5, 15), pady=15)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.clear_placeholder_user)
        self.entry_user.bind("<FocusOut>", self.restore_placeholder_user)
        self.entry_user.bind("<Return>", lambda event: self.login())

        self.frame_pass = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG, highlightbackground=self.COLOR_AZUL,
                                   highlightthickness=2)
        self.frame_pass.pack(pady=(0, 40))

        tk.Label(self.frame_pass, text="🔒", font=("Arial", 14), bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(
            side="left", padx=(15, 5))

        self.entry_password = tk.Entry(self.frame_pass, font=("Arial", 12), bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,
                                       relief="flat", width=28)
        self.entry_password.pack(side="left", padx=(5, 15), pady=15)
        self.entry_password.insert(0, "Contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_placeholder_pass)
        self.entry_password.bind("<FocusOut>", self.restore_placeholder_pass)
        self.entry_password.bind("<Return>", lambda event: self.login())
        self.password_hidden = False

        self.boton_login = tk.Button(self.frame_login, text="INICIAR SESIÓN", bg=self.COLOR_AZUL, fg="white",
                                     font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=32, height=2,
                                     command=self.login)
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

        self.crear_interfaz()

    def confirmar_cierre(self):
        respuesta = messagebox.askyesno("Confirmar Salida", "¿Está seguro que desea cerrar el programa?")
        if respuesta:
            self.root.destroy()

    def crear_interfaz(self):
        # 1. Crear BARRA DE ESTADO PRIMERO para evitar el error AttributeError
        self.frame_estado = tk.Frame(self.root, bg="#F0F0F0", height=30)
        self.frame_estado.pack(fill="x", side="bottom")
        self.frame_estado.pack_propagate(False)

        self.label_estado = tk.Label(self.frame_estado, text="Total de ítems: 0", font=("Arial", 9), bg="#F0F0F0",
                                     fg="#333333")
        self.label_estado.pack(side="left", padx=20, pady=5)

        # 2. Header
        frame_superior = tk.Frame(self.root, bg=self.COLOR_FONDO, height=150)
        frame_superior.pack(fill="x", padx=20, pady=(10, 0))
        frame_superior.pack_propagate(False)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos_2.png")

        try:
            self.imagen = tk.PhotoImage(file=ruta_logo)
            label_logo = tk.Label(frame_superior, image=self.imagen, bg=self.COLOR_FONDO)
            label_logo.pack(pady=20)
        except:
            tk.Label(frame_superior, text="GEOS", font=("Arial", 36, "bold"), bg=self.COLOR_FONDO,
                     fg=self.COLOR_AZUL).pack(pady=(10, 0))
            tk.Label(frame_superior, text="Herramientas y Equipos", font=("Arial", 12), bg=self.COLOR_FONDO,
                     fg=self.COLOR_AZUL).pack()

        # 3. Navegación
        frame_nav = tk.Frame(self.root, bg=self.COLOR_AZUL, height=50)
        frame_nav.pack(fill="x")
        frame_nav.pack_propagate(False)

        frame_pestanas = tk.Frame(frame_nav, bg=self.COLOR_AZUL)
        frame_pestanas.place(relx=0.5, rely=0.5, anchor="center")

        pestanas = ["Inventario", "Proveedores", "Clientes", "Reportes", "Configuración"]
        self.botones_pestanas = {}

        for i, pestana in enumerate(pestanas):
            color_bg = self.COLOR_AZUL_CLARO if i == 0 else self.COLOR_AZUL
            btn = tk.Button(frame_pestanas, text=pestana, font=("Arial", 11, "bold"), bg=color_bg, fg="white",
                            relief="flat", cursor="hand2", padx=20, pady=10,
                            command=lambda p=pestana: self.cambiar_pestana(p))
            btn.pack(side="left", padx=2, pady=5, fill="y")
            self.botones_pestanas[pestana] = btn

        # 4. Contenido Principal
        self.frame_contenido = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=10)

        # 5. Vista Inicial
        self.mostrar_inventario()

    def crear_tabla(self):
        frame_tabla = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#333333", rowheight=30, fieldbackground="white",
                        font=("Arial", 10))
        style.configure("Treeview.Heading", background=self.COLOR_AZUL, foreground="white", font=("Arial", 10, "bold"),
                        relief="flat")
        style.map("Treeview", background=[("selected", self.COLOR_AZUL_CLARO)])

        columnas = ("ID_NUM", "Codigo", "Nombre", "Categoria", "Cantidad", "P.Compra", "P.Venta", "Proveedor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scroll_y.set,
                                  xscrollcommand=scroll_x.set)

        self.tabla.heading("ID_NUM", text="ID")
        self.tabla.heading("Codigo", text="Código")
        self.tabla.heading("Nombre", text="Nombre Producto")
        self.tabla.heading("Categoria", text="Categoría")
        self.tabla.heading("Cantidad", text="Stock")
        self.tabla.heading("P.Compra", text="P. Compra")
        self.tabla.heading("P.Venta", text="P. Venta")
        self.tabla.heading("Proveedor", text="Proveedor")

        self.tabla.column("ID_NUM", width=50, anchor="center")
        self.tabla.column("Codigo", width=100, anchor="center")
        self.tabla.column("Nombre", width=300, anchor="w")
        self.tabla.column("Categoria", width=120, anchor="center")
        self.tabla.column("Cantidad", width=80, anchor="center")
        self.tabla.column("P.Compra", width=100, anchor="center")
        self.tabla.column("P.Venta", width=100, anchor="center")
        self.tabla.column("Proveedor", width=150, anchor="w")

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.pack(fill="both", expand=True)

        self.tabla.bind("<Double-1>", lambda e: self.editar_item())

    def cargar_datos(self):
        if not hasattr(self, 'tabla'): return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        productos = ProductosDB.obtener_todos()

        for item in productos:
            self.tabla.insert("", "end", values=(
                item["id_num"],
                item["codigo"],
                item["nombre"],
                item["categoria"],
                item["cantidad"],
                f"${item['precio_compra']:.2f}",
                f"${item['precio_venta']:.2f}",
                item["proveedor"]
            ))

        self.actualizar_estado(len(productos))

    def actualizar_estado(self, total):
        # FIX DE SEGURIDAD: Verificar si el label existe antes de intentar configurarlo
        if hasattr(self, 'label_estado') and self.label_estado.winfo_exists():
            fecha_hora = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            self.label_estado.config(text=f"Total de productos: {total} | Última sincronización: {fecha_hora}")

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

        productos = ProductosDB.obtener_todos()

        for item in productos:
            if (termino in str(item["codigo"]).lower() or
                    termino in str(item["nombre"]).lower() or
                    termino in str(item["categoria"]).lower() or
                    termino in str(item["proveedor"]).lower()):
                self.tabla.insert("", "end", values=(
                    item["id_num"],
                    item["codigo"],
                    item["nombre"],
                    item["categoria"],
                    item["cantidad"],
                    f"${item['precio_compra']:.2f}",
                    f"${item['precio_venta']:.2f}",
                    item["proveedor"]
                ))

    def agregar_item(self):
        VentanaAgregar(self.root, self)

    def editar_item(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ítem para editar")
            return

        item_values = self.tabla.item(seleccion[0])["values"]

        try:
            p_compra = float(str(item_values[5]).replace("$", ""))
            p_venta = float(str(item_values[6]).replace("$", ""))
        except:
            p_compra = 0.0
            p_venta = 0.0

        item_completo = {
            "id_num": item_values[0],
            "codigo": item_values[1],
            "nombre": item_values[2],
            "categoria": item_values[3],
            "cantidad": item_values[4],
            "precio_compra": p_compra,
            "precio_venta": p_venta,
            "proveedor": item_values[7]
        }

        VentanaEditar(self.root, self, item_completo)

    def eliminar_item(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ítem para eliminar")
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        respuesta = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{valores[2]}'?")
        if respuesta:
            if ProductosDB.eliminar(valores[0]):
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")

    def exportar_excel(self):
        messagebox.showinfo("Exportar",
                            "Funcionalidad de exportación a Excel\n(Requiere librería openpyxl o xlsxwriter)")

    def agregar_categoria(self):
        VentanaAgregarCategoria(self.root, self)

    def eliminar_categoria(self):
        VentanaEliminarCategoria(self.root, self)

    def cambiar_pestana(self, pestana):
        if pestana == self.pestana_actual:
            return

        self.pestana_actual = pestana

        for nombre, boton in self.botones_pestanas.items():
            if nombre == pestana:
                boton.config(bg=self.COLOR_AZUL_CLARO)
            else:
                boton.config(bg=self.COLOR_AZUL)

        if pestana == "Inventario":
            self.mostrar_inventario()
        elif pestana == "Proveedores":
            self.mostrar_proveedores()
        else:
            for widget in self.frame_contenido.winfo_children():
                widget.destroy()
            tk.Label(self.frame_contenido, text=f"Sección {pestana} en construcción",
                     font=("Arial", 14), bg="white").pack(pady=50)

    def mostrar_inventario(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        frame_herramientas = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_herramientas.pack(fill="x", pady=(0, 15))

        frame_busqueda = tk.Frame(frame_herramientas, bg="white", highlightbackground="#CCCCCC", highlightthickness=1)
        frame_busqueda.pack(side="left", padx=(0, 10))

        tk.Label(frame_busqueda, text="🔍", font=("Arial", 12), bg="white").pack(side="left", padx=(10, 5))
        self.entry_buscar = tk.Entry(frame_busqueda, font=("Arial", 11), relief="flat", width=30, bg="white")
        self.entry_buscar.pack(side="left", padx=(0, 10), pady=8)
        self.entry_buscar.insert(0, "Buscar...")
        self.entry_buscar.bind("<FocusIn>", self.clear_buscar)
        self.entry_buscar.bind("<FocusOut>", self.restore_buscar)
        self.entry_buscar.bind("<KeyRelease>", self.buscar_item)

        # ---------------------------------------------------------
        # FUNCIÓN AUXILIAR PARA BOTONES CON BORDE AZUL PERSONALIZADO
        # ---------------------------------------------------------
        def crear_boton_azul(text, command):
            # Frame contenedor que actúa como el borde de 2px
            frame_border = tk.Frame(frame_herramientas, bg=self.COLOR_AZUL, padx=2, pady=2)
            frame_border.pack(side="left", padx=5)

            # Botón interior blanco con letras azules
            btn = tk.Button(frame_border, text=text, font=("Arial", 10, "bold"),
                            bg="white", fg=self.COLOR_AZUL,
                            relief="flat", cursor="hand2", command=command)
            btn.pack(fill="both", expand=True)
            return btn

        # 1. Agregar Producto
        crear_boton_azul("Agregar Producto", self.agregar_item)

        # 2. Agregar Categoría
        crear_boton_azul("Agregar Categoría", self.agregar_categoria)

        # 3. Eliminar Categoría
        crear_boton_azul("Eliminar Categoría", self.eliminar_categoria)

        # ---------------------------------------------------------

        tk.Button(frame_herramientas, text="Editar", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL, fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=5, command=self.editar_item).pack(side="left", padx=5)

        tk.Button(frame_herramientas, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=5, command=self.eliminar_item).pack(side="left", padx=5)

        tk.Button(frame_herramientas, text="📊 Exportar a Excel", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL,
                  fg="white", relief="flat", cursor="hand2", padx=15, pady=5, command=self.exportar_excel).pack(
            side="right", padx=5)

        self.crear_tabla()
        self.cargar_datos()

    def mostrar_proveedores(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        frame_herramientas = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_herramientas.pack(fill="x", pady=(0, 15))

        frame_busqueda = tk.Frame(frame_herramientas, bg="white", highlightbackground="#CCCCCC", highlightthickness=1)
        frame_busqueda.pack(side="left", padx=(0, 10))

        tk.Label(frame_busqueda, text="🔍", font=("Arial", 12), bg="white").pack(side="left", padx=(10, 5))
        self.entry_buscar_proveedor = tk.Entry(frame_busqueda, font=("Arial", 11), relief="flat", width=30, bg="white")
        self.entry_buscar_proveedor.pack(side="left", padx=(0, 10), pady=8)
        self.entry_buscar_proveedor.insert(0, "Buscar proveedor...")
        self.entry_buscar_proveedor.bind("<FocusIn>", self.clear_buscar_proveedor)
        self.entry_buscar_proveedor.bind("<FocusOut>", self.restore_buscar_proveedor)
        self.entry_buscar_proveedor.bind("<KeyRelease>", self.buscar_proveedor)

        tk.Button(frame_herramientas, text="Agregar Proveedor", font=("Arial", 10, "bold"), bg="white",
                  fg=self.COLOR_AZUL,
                  relief="solid", borderwidth=2, cursor="hand2", padx=15, pady=5, command=self.agregar_proveedor).pack(
            side="left", padx=5)

        tk.Button(frame_herramientas, text="Editar", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL, fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=5, command=self.editar_proveedor).pack(side="left",
                                                                                                      padx=5)

        tk.Button(frame_herramientas, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=5, command=self.eliminar_proveedor).pack(side="left",
                                                                                                        padx=5)

        frame_tabla = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("ID", "Nombre", "Código", "Teléfono", "Encargado", "Información")
        self.tabla_proveedores = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                              yscrollcommand=scrollbar.set, height=20)
        scrollbar.config(command=self.tabla_proveedores.yview)

        self.tabla_proveedores.heading("ID", text="ID")
        self.tabla_proveedores.heading("Nombre", text="Nombre")
        self.tabla_proveedores.heading("Código", text="Código")
        self.tabla_proveedores.heading("Teléfono", text="Teléfono")
        self.tabla_proveedores.heading("Encargado", text="Encargado")
        self.tabla_proveedores.heading("Información", text="Información")

        self.tabla_proveedores.column("ID", width=50, anchor="center")
        self.tabla_proveedores.column("Nombre", width=200, anchor="w")
        self.tabla_proveedores.column("Código", width=100, anchor="center")
        self.tabla_proveedores.column("Teléfono", width=100, anchor="center")
        self.tabla_proveedores.column("Encargado", width=150, anchor="w")
        self.tabla_proveedores.column("Información", width=250, anchor="w")

        self.tabla_proveedores.pack(fill="both", expand=True, padx=5, pady=5)
        self.tabla_proveedores.bind("<Double-1>", lambda e: self.editar_proveedor())

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        self.cargar_proveedores()

    def clear_buscar_proveedor(self, event):
        if self.entry_buscar_proveedor.get() == "Buscar proveedor...":
            self.entry_buscar_proveedor.delete(0, 'end')
            self.entry_buscar_proveedor.config(fg="#000000")

    def restore_buscar_proveedor(self, event):
        if self.entry_buscar_proveedor.get() == "":
            self.entry_buscar_proveedor.insert(0, "Buscar proveedor...")
            self.entry_buscar_proveedor.config(fg="#666666")

    def buscar_proveedor(self, event=None):
        if not hasattr(self, 'tabla_proveedores'):
            return

        termino = self.entry_buscar_proveedor.get().lower()

        if termino == "buscar proveedor...":
            self.cargar_proveedores()
            return

        for item in self.tabla_proveedores.get_children():
            self.tabla_proveedores.delete(item)

        proveedores = ProveedoresDB.obtener_todos()
        for prov in proveedores:
            if (termino in str(prov["nombre"]).lower() or
                    termino in str(prov["codigo"]).lower() or
                    termino in str(prov["telefono"]).lower() or
                    termino in str(prov["encargado"]).lower() or
                    termino in str(prov["informacion"]).lower()):
                self.tabla_proveedores.insert("", "end", values=(
                    prov["id_num"],
                    prov["nombre"],
                    prov["codigo"],
                    prov["telefono"],
                    prov["encargado"],
                    prov["informacion"]
                ))

    def cargar_proveedores(self):
        if hasattr(self, 'tabla_proveedores'):
            for item in self.tabla_proveedores.get_children():
                self.tabla_proveedores.delete(item)

            proveedores = ProveedoresDB.obtener_todos()
            for prov in proveedores:
                self.tabla_proveedores.insert("", "end", values=(
                    prov["id_num"],
                    prov["nombre"],
                    prov["codigo"],
                    prov["telefono"],
                    prov["encargado"],
                    prov["informacion"]
                ))

    def agregar_proveedor(self):
        VentanaAgregarProveedor(self.root, self)

    def editar_proveedor(self):
        if not hasattr(self, 'tabla_proveedores'):
            return

        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para editar")
            return

        valores = self.tabla_proveedores.item(seleccion[0])["values"]
        proveedor = {
            "id_num": valores[0],
            "nombre": valores[1],
            "codigo": valores[2],
            "telefono": valores[3],
            "encargado": valores[4],
            "informacion": valores[5]
        }
        VentanaEditarProveedor(self.root, self, proveedor)

    def eliminar_proveedor(self):
        if not hasattr(self, 'tabla_proveedores'):
            return

        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")
            return

        valores = self.tabla_proveedores.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar el proveedor '{valores[1]}'?")

        if respuesta:
            if ProveedoresDB.eliminar(valores[0]):
                self.cargar_proveedores()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor")


class VentanaAgregarCategoria:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Categoría")
        self.ventana.geometry("400x200")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Nueva Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF",
                 fg=COLOR_AZUL).pack(pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.entry_nombre.pack(side="left", padx=5)
        self.entry_nombre.focus()

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar", font=("Arial", 10, "bold"), bg=COLOR_AZUL, fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 400
        alto = 200
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        if CategoriasDB.agregar(nombre):
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "La categoría ya existe")


class VentanaEliminarCategoria:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Eliminar Categoría")
        self.ventana.geometry("400x200")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Eliminar Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF",
                 fg=COLOR_AZUL).pack(pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)

        tk.Label(frame_form, text="Seleccione:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)

        categorias = CategoriasDB.obtener_todas()
        self.combo_categorias = ttk.Combobox(frame_form, values=categorias, state="readonly", width=27)
        self.combo_categorias.pack(side="left", padx=5)
        if categorias:
            self.combo_categorias.current(0)

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.eliminar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 400
        alto = 200
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def eliminar(self):
        nombre = self.combo_categorias.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Seleccione una categoría")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar la categoría '{nombre}'?")
        if respuesta:
            if CategoriasDB.eliminar(nombre):
                messagebox.showinfo("Éxito", "Categoría eliminada")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")


class VentanaAgregar:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Nuevo Producto")
        self.ventana.geometry("550x500")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Agregar Nuevo Producto", font=("Arial", 16, "bold"), bg="#FFFFFF",
                 fg=COLOR_AZUL).pack(
            pady=15)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)

        frame_form.columnconfigure(1, weight=1)

        tk.Label(frame_form, text="Código:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="e",
                                                                                            pady=5, padx=5)
        self.entry_codigo = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_codigo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="e",
                                                                                            pady=5, padx=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Categoría:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=2, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        # --- CARGAR CATEGORIAS DESDE DB ---
        categorias_lista = CategoriasDB.obtener_todas()
        self.combo_categoria = ttk.Combobox(frame_form, values=categorias_lista, state="readonly")
        self.combo_categoria.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        if categorias_lista:
            self.combo_categoria.current(0)

        tk.Label(frame_form, text="Cantidad:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=3, column=0,
                                                                                              sticky="e", pady=5,
                                                                                              padx=5)
        self.entry_cantidad = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_cantidad.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Precio Compra:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                                   sticky="e", pady=5,
                                                                                                   padx=5)
        self.entry_pcompra = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_pcompra.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Precio Venta:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=5, column=0,
                                                                                                  sticky="e", pady=5,
                                                                                                  padx=5)
        self.entry_pventa = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_pventa.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(frame_form, text="Proveedor:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=6, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        proveedores_lista = ProveedoresDB.obtener_nombres()
        self.combo_proveedor = ttk.Combobox(frame_form, values=proveedores_lista)
        self.combo_proveedor.grid(row=6, column=1, sticky="ew", pady=5, padx=5)

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg=COLOR_AZUL, fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 550
        alto = 500
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get()
        cantidad = self.entry_cantidad.get().strip()
        pcompra = self.entry_pcompra.get().strip()
        pventa = self.entry_pventa.get().strip()
        proveedor = self.combo_proveedor.get().strip()

        if not all([codigo, nombre, cantidad, pcompra, pventa, proveedor]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = float(cantidad)
            pcompra = float(pcompra)
            pventa = float(pventa)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precios deben ser numéricos")
            return

        if ProductosDB.agregar(nombre, codigo, pcompra, pventa, categoria, cantidad, proveedor):
            self.sistema.cargar_datos()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "El Código ya existe en la base de datos")


class VentanaEditar:
    def __init__(self, parent, sistema, item):
        self.sistema = sistema
        self.item_original = item
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Producto")
        self.ventana.geometry("550x500")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Editar Producto", font=("Arial", 16, "bold"), bg="#FFFFFF", fg=COLOR_AZUL).pack(
            pady=15)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)
        frame_form.columnconfigure(1, weight=1)

        tk.Label(frame_form, text="ID:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="e",
                                                                                        pady=5, padx=5)
        self.entry_id = tk.Entry(frame_form, font=("Arial", 10), state="disabled")
        self.entry_id.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.entry_id.config(state="normal")
        self.entry_id.insert(0, item["id_num"])
        self.entry_id.config(state="disabled")

        tk.Label(frame_form, text="Código:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="e",
                                                                                            pady=5, padx=5)
        self.entry_codigo = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_codigo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.entry_codigo.insert(0, item["codigo"])

        tk.Label(frame_form, text="Nombre:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=2, column=0, sticky="e",
                                                                                            pady=5, padx=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_nombre.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        self.entry_nombre.insert(0, item["nombre"])

        tk.Label(frame_form, text="Categoría:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=3, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        # --- CARGAR CATEGORIAS DESDE DB ---
        categorias_lista = CategoriasDB.obtener_todas()
        self.combo_categoria = ttk.Combobox(frame_form, values=categorias_lista)
        self.combo_categoria.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        self.combo_categoria.set(item["categoria"])

        tk.Label(frame_form, text="Cantidad:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                              sticky="e", pady=5,
                                                                                              padx=5)
        self.entry_cantidad = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_cantidad.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        self.entry_cantidad.insert(0, item["cantidad"])

        tk.Label(frame_form, text="Precio Compra:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=5, column=0,
                                                                                                   sticky="e", pady=5,
                                                                                                   padx=5)
        self.entry_pcompra = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_pcompra.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
        self.entry_pcompra.insert(0, item["precio_compra"])

        tk.Label(frame_form, text="Precio Venta:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=6, column=0,
                                                                                                  sticky="e", pady=5,
                                                                                                  padx=5)
        self.entry_pventa = tk.Entry(frame_form, font=("Arial", 10))
        self.entry_pventa.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        self.entry_pventa.insert(0, item["precio_venta"])

        tk.Label(frame_form, text="Proveedor:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=7, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        proveedores_lista = ProveedoresDB.obtener_nombres()
        self.combo_proveedor = ttk.Combobox(frame_form, values=proveedores_lista)
        self.combo_proveedor.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        self.combo_proveedor.set(item["proveedor"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg=COLOR_AZUL, fg="white",
                  relief="flat", cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 550
        alto = 500
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get()
        cantidad = self.entry_cantidad.get().strip()
        pcompra = self.entry_pcompra.get().strip()
        pventa = self.entry_pventa.get().strip()
        proveedor = self.combo_proveedor.get().strip()

        if not all([codigo, nombre, cantidad, pcompra, pventa]):
            messagebox.showerror("Error", "Todos los campos principales son obligatorios")
            return

        try:
            cantidad = float(cantidad)
            pcompra = float(pcompra)
            pventa = float(pventa)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precios deben ser valores numéricos")
            return

        if ProductosDB.actualizar(self.item_original["id_num"], nombre, codigo, pcompra, pventa, categoria, cantidad,
                                  proveedor):
            self.sistema.cargar_datos()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el producto (posible código duplicado)")


class VentanaAgregarProveedor:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Proveedor")
        self.ventana.geometry("500x550")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Agregar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg=COLOR_AZUL).pack(
            pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w",
                                                                                            pady=10)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Código:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w",
                                                                                            pady=10)
        self.entry_codigo = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_codigo.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Teléfono:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0,
                                                                                              sticky="w", pady=10)
        self.entry_telefono = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_telefono.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Encargado:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0,
                                                                                               sticky="w", pady=10)
        self.entry_encargado = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_encargado.grid(row=3, column=1, pady=10, padx=10)

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                                 sticky="nw", pady=10)
        self.text_informacion = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_informacion.grid(row=4, column=1, pady=10, padx=10)

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg=COLOR_AZUL, fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 500
        alto = 550
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        telefono = self.entry_telefono.get().strip()
        encargado = self.entry_encargado.get().strip()
        informacion = self.text_informacion.get("1.0", "end-1c").strip()

        if not all([nombre, codigo, telefono]):
            messagebox.showerror("Error", "Nombre, Código y Teléfono son obligatorios")
            return

        if ProveedoresDB.agregar(nombre, codigo, telefono, encargado, informacion):
            self.sistema.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "El código ya existe en la base de datos")


class VentanaEditarProveedor:
    def __init__(self, parent, sistema, proveedor):
        self.sistema = sistema
        self.proveedor_original = proveedor
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Proveedor")
        self.ventana.geometry("500x550")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.centrar_ventana()

        COLOR_AZUL = "#0055A5"

        tk.Label(self.ventana, text="Editar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg=COLOR_AZUL).pack(
            pady=20)

        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w",
                                                                                            pady=10)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)
        self.entry_nombre.insert(0, proveedor["nombre"])

        tk.Label(frame_form, text="Código:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w",
                                                                                            pady=10)
        self.entry_codigo = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_codigo.grid(row=1, column=1, pady=10, padx=10)
        self.entry_codigo.insert(0, proveedor["codigo"])
        self.entry_codigo.config(state="readonly")

        tk.Label(frame_form, text="Teléfono:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0,
                                                                                              sticky="w", pady=10)
        self.entry_telefono = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_telefono.grid(row=2, column=1, pady=10, padx=10)
        self.entry_telefono.insert(0, proveedor["telefono"])

        tk.Label(frame_form, text="Encargado:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0,
                                                                                               sticky="w", pady=10)
        self.entry_encargado = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.entry_encargado.grid(row=3, column=1, pady=10, padx=10)
        self.entry_encargado.insert(0, proveedor["encargado"])

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                                 sticky="nw", pady=10)
        self.text_informacion = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_informacion.grid(row=4, column=1, pady=10, padx=10)
        self.text_informacion.insert("1.0", proveedor["informacion"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg=COLOR_AZUL, fg="white",
                  relief="flat", cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 500
        alto = 550
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        encargado = self.entry_encargado.get().strip()
        informacion = self.text_informacion.get("1.0", "end-1c").strip()

        if not all([nombre, telefono]):
            messagebox.showerror("Error", "Nombre y Teléfono son obligatorios")
            return

        if ProveedoresDB.actualizar(self.proveedor_original["id_num"], nombre,
                                    self.proveedor_original["codigo"], telefono, encargado, informacion):
            self.sistema.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el proveedor")


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()