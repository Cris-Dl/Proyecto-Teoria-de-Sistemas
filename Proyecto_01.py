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

        # Tabla Proveedores
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

        # Tabla Productos
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

        # Tabla Categorías
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            );
        """)

        # Tabla Historial Ventas
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                total REAL
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
    def actualizar_stock(id_num, cantidad_vendida):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT cantidad FROM productos WHERE id_num = ?", (id_num,))
            row = cursor.fetchone()
            if row:
                stock_actual = row["cantidad"]
                nuevo_stock = stock_actual - cantidad_vendida
                conn.execute("UPDATE productos SET cantidad = ? WHERE id_num = ?", (nuevo_stock, id_num))
                conn.commit()
                return True
            return False
        except Exception as e:
            print(e)
            return False
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

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos.png")

        try:
            self.imagen = tk.PhotoImage(file=ruta_logo)
            self.label_logo = tk.Label(self.root, image=self.imagen, bg=self.COLOR_FONDO)
            self.label_logo.pack(pady=(60, 80))
        except:
            tk.Label(self.root, text="GEOS", font=("Arial", 48, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(60, 20))
            tk.Label(self.root, text="Herramientas y Equipos", font=("Arial", 14), bg=self.COLOR_FONDO,fg=self.COLOR_AZUL).pack(pady=(0, 60))

        self.frame_login = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_login.pack()

        self.frame_user = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG, highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_user.pack(pady=(0, 20))
        tk.Label(self.frame_user, text="👤", font=("Arial", 14), bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))
        self.entry_user = tk.Entry(self.frame_user, font=("Arial", 12), bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_user.pack(side="left", padx=(5, 15), pady=15)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.clear_placeholder_user)
        self.entry_user.bind("<FocusOut>", self.restore_placeholder_user)
        self.entry_user.bind("<Return>", lambda event: self.login())

        self.frame_pass = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG, highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_pass.pack(pady=(0, 40))
        tk.Label(self.frame_pass, text="🔒", font=("Arial", 14), bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))
        self.entry_password = tk.Entry(self.frame_pass, font=("Arial", 12), bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_password.pack(side="left", padx=(5, 15), pady=15)
        self.entry_password.insert(0, "Contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_placeholder_pass)
        self.entry_password.bind("<FocusOut>", self.restore_placeholder_pass)
        self.entry_password.bind("<Return>", lambda event: self.login())

        self.boton_login = tk.Button(self.frame_login, text="INICIAR SESIÓN", bg=self.COLOR_AZUL, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=32, height=2,command=self.login)
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

    def restore_placeholder_pass(self, event):
        if self.entry_password.get() == "":
            self.entry_password.config(show="")
            self.entry_password.insert(0, "Contraseña")
            self.entry_password.config(fg="#666666")

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

        self.carrito_compras = []

        self.pestana_actual = "Inventario"
        self.crear_interfaz()

    def confirmar_cierre(self):
        respuesta = messagebox.askyesno("Confirmar Salida", "¿Está seguro que desea cerrar el programa?")
        if respuesta:
            self.root.destroy()

    def crear_interfaz(self):
        self.frame_estado = tk.Frame(self.root, bg="#F0F0F0", height=30)
        self.frame_estado.pack(fill="x", side="bottom")
        self.frame_estado.pack_propagate(False)
        self.label_estado = tk.Label(self.frame_estado, text="Listo", font=("Arial", 9), bg="#F0F0F0", fg="#333333")
        self.label_estado.pack(side="left", padx=20, pady=5)

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
            tk.Label(frame_superior, text="GEOS", font=("Arial", 36, "bold"), bg=self.COLOR_FONDO,fg=self.COLOR_AZUL).pack(pady=(10, 0))
            tk.Label(frame_superior, text="Herramientas y Equipos", font=("Arial", 12), bg=self.COLOR_FONDO,fg=self.COLOR_AZUL).pack()

        frame_nav = tk.Frame(self.root, bg=self.COLOR_AZUL, height=50)
        frame_nav.pack(fill="x")
        frame_nav.pack_propagate(False)

        frame_pestanas = tk.Frame(frame_nav, bg=self.COLOR_AZUL)
        frame_pestanas.place(relx=0.5, rely=0.5, anchor="center")

        pestanas = ["Inventario", "Ventas", "Proveedores", "Clientes", "Reportes"]
        self.botones_pestanas = {}

        for i, pestana in enumerate(pestanas):
            color_bg = self.COLOR_AZUL_CLARO if i == 0 else self.COLOR_AZUL
            btn = tk.Button(frame_pestanas, text=pestana, font=("Arial", 11, "bold"), bg=color_bg, fg="white",relief="flat", cursor="hand2", padx=20, pady=10,command=lambda p=pestana: self.cambiar_pestana(p))
            btn.pack(side="left", padx=2, pady=5, fill="y")
            self.botones_pestanas[pestana] = btn

        self.frame_contenido = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=10)

        self.mostrar_inventario()

    def cambiar_pestana(self, pestana):
        if pestana == self.pestana_actual: return

        self.pestana_actual = pestana
        for nombre, boton in self.botones_pestanas.items():
            boton.config(bg=self.COLOR_AZUL_CLARO if nombre == pestana else self.COLOR_AZUL)

        if pestana == "Inventario":
            self.mostrar_inventario()
        elif pestana == "Ventas":
            self.mostrar_ventas()
        elif pestana == "Proveedores":
            self.mostrar_proveedores()
        else:
            for widget in self.frame_contenido.winfo_children(): widget.destroy()
            tk.Label(self.frame_contenido, text=f"Sección {pestana} en construcción", font=("Arial", 14),bg="white").pack(pady=50)


    def mostrar_ventas(self):
        for widget in self.frame_contenido.winfo_children(): widget.destroy()

        paned = tk.PanedWindow(self.frame_contenido, orient="horizontal", bg="#DDDDDD", sashwidth=5)
        paned.pack(fill="both", expand=True)

        frame_izq = tk.Frame(paned, bg="white", width=600)
        paned.add(frame_izq)

        tk.Label(frame_izq, text="CATÁLOGO DE PRODUCTOS", font=("Arial", 12, "bold"), bg="white",fg=self.COLOR_AZUL).pack(pady=10)

        frame_busqueda_v = tk.Frame(frame_izq, bg="white")
        frame_busqueda_v.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_busqueda_v, text="Buscar (Nombre, Código, Categ.):", font=("Arial", 10), bg="white").pack(side="left")
        self.entry_buscar_venta = tk.Entry(frame_busqueda_v, font=("Arial", 10), width=30)
        self.entry_buscar_venta.pack(side="left", padx=5)

        self.entry_buscar_venta.bind("<KeyRelease>", self.filtrar_productos_venta)

        col_v = ("ID", "Nombre", "Precio", "Stock", "Categoria")
        self.tabla_prod_venta = ttk.Treeview(frame_izq, columns=col_v, show="headings", height=15)
        self.tabla_prod_venta.heading("ID", text="ID")
        self.tabla_prod_venta.heading("Nombre", text="Producto")
        self.tabla_prod_venta.heading("Precio", text="Precio")
        self.tabla_prod_venta.heading("Stock", text="Stock")
        self.tabla_prod_venta.heading("Categoria", text="Categoria")

        self.tabla_prod_venta.column("ID", width=40)
        self.tabla_prod_venta.column("Nombre", width=200)
        self.tabla_prod_venta.column("Precio", width=80)
        self.tabla_prod_venta.column("Stock", width=60)
        self.tabla_prod_venta.column("Categoria", width=100)

        self.tabla_prod_venta.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla_prod_venta.bind("<Double-1>", lambda event: self.agregar_al_carrito())

        self.cargar_productos_venta()

        frame_agregar = tk.Frame(frame_izq, bg="#F0F8FF", pady=10)
        frame_agregar.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_agregar, text="Cantidad:", bg="#F0F8FF", font=("Arial", 11)).pack(side="left", padx=10)
        self.spin_cantidad = tk.Spinbox(frame_agregar, from_=1, to=100, width=5, font=("Arial", 11))
        self.spin_cantidad.pack(side="left", padx=5)

        btn_add = tk.Button(frame_agregar, text="AGREGAR AL CARRITO >>", bg="#28A745", fg="white",font=("Arial", 10, "bold"),command=self.agregar_al_carrito, cursor="hand2")
        btn_add.pack(side="right", padx=20)

        frame_der = tk.Frame(paned, bg="white", width=400)
        paned.add(frame_der)

        tk.Label(frame_der, text="CARRITO DE COMPRAS", font=("Arial", 12, "bold"), bg="white", fg=self.COLOR_AZUL).pack(pady=10)

        col_c = ("Prod", "Cant", "Total")
        self.tabla_carrito = ttk.Treeview(frame_der, columns=col_c, show="headings")
        self.tabla_carrito.heading("Prod", text="Producto")
        self.tabla_carrito.heading("Cant", text="Cant.")
        self.tabla_carrito.heading("Total", text="Subtotal")

        self.tabla_carrito.column("Prod", width=150)
        self.tabla_carrito.column("Cant", width=50)
        self.tabla_carrito.column("Total", width=80)

        self.tabla_carrito.pack(fill="both", expand=True, padx=10, pady=5)

        frame_totales = tk.Frame(frame_der, bg="#F8F9FA", pady=20)
        frame_totales.pack(fill="x", side="bottom")

        self.lbl_total_pagar = tk.Label(frame_totales, text="TOTAL: $0.00", font=("Arial", 20, "bold"), bg="#F8F9FA",fg="#333333")
        self.lbl_total_pagar.pack()

        btn_cobrar = tk.Button(frame_totales, text="REALIZAR VENTA", bg=self.COLOR_AZUL, fg="white",font=("Arial", 14, "bold"), width=20, command=self.finalizar_venta, cursor="hand2")
        btn_cobrar.pack(pady=15)

        tk.Button(frame_totales, text="Limpiar Carrito", command=self.limpiar_carrito).pack()

    def cargar_productos_venta(self):
        for item in self.tabla_prod_venta.get_children():
            self.tabla_prod_venta.delete(item)

        productos = ProductosDB.obtener_todos()
        for p in productos:
            if p["cantidad"] > 0:
                self.tabla_prod_venta.insert("", "end",values=(p["id_num"], p["nombre"], f"${p['precio_venta']}", p["cantidad"],p["categoria"]))

    def filtrar_productos_venta(self, event):
        filtro = self.entry_buscar_venta.get().lower()
        for item in self.tabla_prod_venta.get_children():
            self.tabla_prod_venta.delete(item)

        productos = ProductosDB.obtener_todos()
        for p in productos:
            coincide_nombre = filtro in p["nombre"].lower()
            coincide_codigo = filtro in p["codigo"].lower()
            coincide_categoria = filtro in p["categoria"].lower()

            if (p["cantidad"] > 0 and (coincide_nombre or coincide_codigo or coincide_categoria)):
                self.tabla_prod_venta.insert("", "end",values=(p["id_num"], p["nombre"], f"${p['precio_venta']}", p["cantidad"],p["categoria"]))

    def agregar_al_carrito(self):
        seleccion = self.tabla_prod_venta.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto de la lista izquierda.")
            return

        item = self.tabla_prod_venta.item(seleccion[0])
        valores = item["values"]
        id_prod = valores[0]
        nombre = valores[1]
        precio = float(str(valores[2]).replace("$", ""))
        stock_disp = float(valores[3])

        try:
            cantidad = float(self.spin_cantidad.get())
        except:
            cantidad = 1.0

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return

        if cantidad > stock_disp:
            messagebox.showerror("Stock Insuficiente", f"Solo hay {stock_disp} unidades disponibles.")
            return

        subtotal = precio * cantidad

        self.carrito_compras.append({
            "id": id_prod,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal
        })

        self.actualizar_vista_carrito()

    def actualizar_vista_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        total_global = 0.0
        for item in self.carrito_compras:
            self.tabla_carrito.insert("", "end", values=(item["nombre"], item["cantidad"], f"${item['subtotal']:.2f}"))
            total_global += item["subtotal"]

        self.lbl_total_pagar.config(text=f"TOTAL: ${total_global:.2f}")

    def limpiar_carrito(self):
        self.carrito_compras = []
        self.actualizar_vista_carrito()

    def finalizar_venta(self):
        if not self.carrito_compras:
            messagebox.showwarning("Vacío", "El carrito está vacío.")
            return

        respuesta = messagebox.askyesno("Confirmar Venta", "¿Desea procesar la venta y descontar del inventario?")
        if respuesta:
            exito = True
            for item in self.carrito_compras:
                if not ProductosDB.actualizar_stock(item["id"], item["cantidad"]):
                    exito = False

            if exito:
                messagebox.showinfo("Venta Exitosa", "La venta se ha registrado y el inventario actualizado.")
                self.limpiar_carrito()
                self.cargar_productos_venta()
            else:
                messagebox.showerror("Error", "Hubo un problema al actualizar algunos productos.")

    def crear_tabla(self):
        frame_tabla = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#333333", rowheight=30, fieldbackground="white",font=("Arial", 10))
        style.configure("Treeview.Heading", background=self.COLOR_AZUL, foreground="white", font=("Arial", 10, "bold"),relief="flat")
        style.map("Treeview", background=[("selected", self.COLOR_AZUL_CLARO)])

        columnas = ("ID_NUM", "Codigo", "Nombre", "Categoria", "Cantidad", "P.Compra", "P.Venta", "Proveedor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

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
        for item in self.tabla.get_children(): self.tabla.delete(item)
        productos = ProductosDB.obtener_todos()
        for item in productos:
            self.tabla.insert("", "end", values=(
                item["id_num"], item["codigo"], item["nombre"], item["categoria"], item["cantidad"],
                f"${item['precio_compra']:.2f}", f"${item['precio_venta']:.2f}", item["proveedor"]
            ))
        self.actualizar_estado(len(productos))

    def actualizar_estado(self, total):
        if hasattr(self, 'label_estado') and self.label_estado.winfo_exists():
            fecha_hora = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            self.label_estado.config(text=f"Total de productos: {total} | Última sincronización: {fecha_hora}")

    def clear_buscar(self, event):
        if self.entry_buscar.get() == "Buscar...": self.entry_buscar.delete(0, 'end')

    def restore_buscar(self, event):
        if self.entry_buscar.get() == "": self.entry_buscar.insert(0, "Buscar...")

    def buscar_item(self, event):
        termino = self.entry_buscar.get().lower()
        if termino == "buscar...":
            self.cargar_datos()
            return
        for item in self.tabla.get_children(): self.tabla.delete(item)
        productos = ProductosDB.obtener_todos()
        for item in productos:
            if (termino in str(item["codigo"]).lower() or termino in str(item["nombre"]).lower() or
                    termino in str(item["categoria"]).lower() or termino in str(item["proveedor"]).lower()):
                self.tabla.insert("", "end", values=(
                    item["id_num"], item["codigo"], item["nombre"], item["categoria"], item["cantidad"],
                    f"${item['precio_compra']:.2f}", f"${item['precio_venta']:.2f}", item["proveedor"]
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
            p_compra, p_venta = 0.0, 0.0
        item_completo = {
            "id_num": item_values[0], "codigo": item_values[1], "nombre": item_values[2],
            "categoria": item_values[3], "cantidad": item_values[4], "precio_compra": p_compra,
            "precio_venta": p_venta, "proveedor": item_values[7]
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
        messagebox.showinfo("Exportar","Funcionalidad de exportación a Excel\n(Requiere librería openpyxl o xlsxwriter)")

    def agregar_categoria(self):
        VentanaAgregarCategoria(self.root, self)

    def eliminar_categoria(self):
        VentanaEliminarCategoria(self.root, self)

    def mostrar_inventario(self):
        for widget in self.frame_contenido.winfo_children(): widget.destroy()
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

        def crear_boton_azul(text, command):
            frame_border = tk.Frame(frame_herramientas, bg=self.COLOR_AZUL, padx=2, pady=2)
            frame_border.pack(side="left", padx=5)
            tk.Button(frame_border, text=text, font=("Arial", 10, "bold"), bg="white", fg=self.COLOR_AZUL,relief="flat", cursor="hand2", command=command).pack(fill="both", expand=True)

        crear_boton_azul("Agregar Producto", self.agregar_item)
        crear_boton_azul("Agregar Categoría", self.agregar_categoria)
        crear_boton_azul("Eliminar Categoría", self.eliminar_categoria)

        tk.Button(frame_herramientas, text="Editar", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL, fg="white",relief="flat", cursor="hand2", padx=20, pady=5, command=self.editar_item).pack(side="left", padx=5)
        tk.Button(frame_herramientas, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white",relief="flat", cursor="hand2", padx=20, pady=5, command=self.eliminar_item).pack(side="left", padx=5)
        tk.Button(frame_herramientas, text="📊 Exportar a Excel", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL,fg="white", relief="flat", cursor="hand2", padx=15, pady=5, command=self.exportar_excel).pack(side="right", padx=5)

        self.crear_tabla()
        self.cargar_datos()

    def mostrar_proveedores(self):
        for widget in self.frame_contenido.winfo_children(): widget.destroy()
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

        tk.Button(frame_herramientas, text="Agregar Proveedor", font=("Arial", 10, "bold"), bg="white",fg=self.COLOR_AZUL, relief="solid", borderwidth=2, cursor="hand2", padx=15, pady=5,command=self.agregar_proveedor).pack(side="left", padx=5)
        tk.Button(frame_herramientas, text="Editar", font=("Arial", 10, "bold"), bg=self.COLOR_AZUL, fg="white",relief="flat", cursor="hand2", padx=20, pady=5, command=self.editar_proveedor).pack(side="left",padx=5)
        tk.Button(frame_herramientas, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white",relief="flat", cursor="hand2", padx=20, pady=5, command=self.eliminar_proveedor).pack(side="left",padx=5)

        frame_tabla = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("ID", "Nombre", "Código", "Teléfono", "Encargado", "Información")
        self.tabla_proveedores = ttk.Treeview(frame_tabla, columns=columnas, show="headings",yscrollcommand=scrollbar.set, height=20)
        scrollbar.config(command=self.tabla_proveedores.yview)
        for col, width in zip(columnas, [50, 200, 100, 100, 150, 250]):
            self.tabla_proveedores.heading(col, text=col)
            self.tabla_proveedores.column(col, width=width)

        self.tabla_proveedores.pack(fill="both", expand=True, padx=5, pady=5)
        self.tabla_proveedores.bind("<Double-1>", lambda e: self.editar_proveedor())
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
        if not hasattr(self, 'tabla_proveedores'): return
        termino = self.entry_buscar_proveedor.get().lower()
        if termino == "buscar proveedor...":
            self.cargar_proveedores()
            return
        for item in self.tabla_proveedores.get_children(): self.tabla_proveedores.delete(item)
        proveedores = ProveedoresDB.obtener_todos()
        for prov in proveedores:
            if (termino in str(prov["nombre"]).lower() or termino in str(prov["codigo"]).lower() or termino in str(prov["telefono"]).lower()):
                self.tabla_proveedores.insert("", "end", values=(
                    prov["id_num"], prov["nombre"], prov["codigo"], prov["telefono"],
                    prov["encargado"], prov["informacion"]))

    def cargar_proveedores(self):
        if hasattr(self, 'tabla_proveedores'):
            for item in self.tabla_proveedores.get_children(): self.tabla_proveedores.delete(item)
            proveedores = ProveedoresDB.obtener_todos()
            for prov in proveedores:
                self.tabla_proveedores.insert("", "end", values=(
                    prov["id_num"], prov["nombre"], prov["codigo"], prov["telefono"],
                    prov["encargado"], prov["informacion"]))

    def agregar_proveedor(self):
        VentanaAgregarProveedor(self.root, self)

    def editar_proveedor(self):
        if not hasattr(self, 'tabla_proveedores'): return
        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para editar")
            return
        valores = self.tabla_proveedores.item(seleccion[0])["values"]
        proveedor = {
            "id_num": valores[0], "nombre": valores[1], "codigo": valores[2],
            "telefono": valores[3], "encargado": valores[4], "informacion": valores[5]
        }
        VentanaEditarProveedor(self.root, self, proveedor)

    def eliminar_proveedor(self):
        if not hasattr(self, 'tabla_proveedores'): return
        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")
            return
        valores = self.tabla_proveedores.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar el proveedor '{valores[1]}'?")
        if respuesta and ProveedoresDB.eliminar(valores[0]):
            self.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")

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

        tk.Label(self.ventana, text="Nueva Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#0055A5").pack(pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)
        tk.Label(frame_form, text="Nombre:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.entry_nombre.pack(side="left", padx=5)
        self.entry_nombre.focus()
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar", font=("Arial", 10, "bold"), bg="#0055A5", fg="white", relief="flat",cursor="hand2", padx=20, pady=5, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 400, 200
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre: return
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
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.centrar_ventana()

        tk.Label(self.ventana, text="Eliminar Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#0055A5").pack(pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)
        tk.Label(frame_form, text="Seleccione:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        categorias = CategoriasDB.obtener_todas()
        self.combo_categorias = ttk.Combobox(frame_form, values=categorias, state="readonly", width=27)
        self.combo_categorias.pack(side="left", padx=5)
        if categorias: self.combo_categorias.current(0)
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white", relief="flat",cursor="hand2", padx=20, pady=5, command=self.eliminar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 400, 200
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def eliminar(self):
        nombre = self.combo_categorias.get().strip()
        if not nombre: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?"):
            if CategoriasDB.eliminar(nombre):
                messagebox.showinfo("Éxito", "Categoría eliminada")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")


class VentanaAgregar:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Nuevo Producto")
        self.ventana.geometry("550x500")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.centrar_ventana()

        tk.Label(self.ventana, text="Agregar Nuevo Producto", font=("Arial", 16, "bold"), bg="#FFFFFF",fg="#0055A5").pack(pady=15)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)
        frame_form.columnconfigure(1, weight=1)

        labels = ["Código:", "Nombre:", "Categoría:", "Cantidad:", "Precio Compra:", "Precio Venta:", "Proveedor:"]
        self.widgets = {}

        for i, label in enumerate(labels):
            tk.Label(frame_form, text=label, font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="e",pady=5, padx=5)
            if label == "Categoría:":
                self.combo_categoria = ttk.Combobox(frame_form, values=CategoriasDB.obtener_todas(), state="readonly")
                self.combo_categoria.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                if self.combo_categoria['values']: self.combo_categoria.current(0)
            elif label == "Proveedor:":
                self.combo_proveedor = ttk.Combobox(frame_form, values=ProveedoresDB.obtener_nombres())
                self.combo_proveedor.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            else:
                entry = tk.Entry(frame_form, font=("Arial", 10))
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.widgets[label] = entry

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg="#0055A5", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 550, 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        vals = {k: v.get().strip() for k, v in self.widgets.items()}
        cat = self.combo_categoria.get()
        prov = self.combo_proveedor.get()
        if not all([vals["Código:"], vals["Nombre:"], vals["Cantidad:"], vals["Precio Compra:"], vals["Precio Venta:"],prov]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            if ProductosDB.agregar(vals["Nombre:"], vals["Código:"], float(vals["Precio Compra:"]),float(vals["Precio Venta:"]), cat, float(vals["Cantidad:"]), prov):
                self.sistema.cargar_datos()
                messagebox.showinfo("Éxito", "Producto agregado")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "El Código ya existe")
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos")


class VentanaEditar:
    def __init__(self, parent, sistema, item):
        self.sistema = sistema
        self.item_original = item
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Producto")
        self.ventana.geometry("550x500")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.centrar_ventana()

        tk.Label(self.ventana, text="Editar Producto", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#0055A5").pack(pady=15)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)
        frame_form.columnconfigure(1, weight=1)

        self.widgets = {}
        campos = [("ID:", item["id_num"]), ("Código:", item["codigo"]), ("Nombre:", item["nombre"]),
                  ("Cantidad:", item["cantidad"]), ("Precio Compra:", item["precio_compra"]),
                  ("Precio Venta:", item["precio_venta"])]

        for i, (label, val) in enumerate(campos):
            tk.Label(frame_form, text=label, font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="e",pady=5, padx=5)
            entry = tk.Entry(frame_form, font=("Arial", 10))
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            entry.insert(0, val)
            if label == "ID:": entry.config(state="disabled")
            self.widgets[label] = entry

        tk.Label(frame_form, text="Categoría:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=6, column=0,sticky="e", pady=5,padx=5)
        self.combo_categoria = ttk.Combobox(frame_form, values=CategoriasDB.obtener_todas())
        self.combo_categoria.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        self.combo_categoria.set(item["categoria"])

        tk.Label(frame_form, text="Proveedor:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=7, column=0,sticky="e", pady=5,padx=5)
        self.combo_proveedor = ttk.Combobox(frame_form, values=ProveedoresDB.obtener_nombres())
        self.combo_proveedor.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        self.combo_proveedor.set(item["proveedor"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg="#0055A5", fg="white",relief="flat",cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 550, 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        vals = {k: v.get().strip() for k, v in self.widgets.items()}
        try:
            if ProductosDB.actualizar(self.item_original["id_num"], vals["Nombre:"], vals["Código:"],float(vals["Precio Compra:"]), float(vals["Precio Venta:"]),self.combo_categoria.get(), float(vals["Cantidad:"]), self.combo_proveedor.get()):
                self.sistema.cargar_datos()
                messagebox.showinfo("Éxito", "Producto actualizado")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar")
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos")


class VentanaAgregarProveedor:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Proveedor")
        self.ventana.geometry("500x550")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.centrar_ventana()

        tk.Label(self.ventana, text="Agregar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#0055A5").pack(pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        self.widgets = {}
        for i, label in enumerate(["Nombre:", "Código:", "Teléfono:", "Encargado:"]):
            tk.Label(frame_form, text=label, font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="w",pady=10)
            entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.widgets[label] = entry

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,sticky="nw", pady=10)
        self.text_info = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_info.grid(row=4, column=1, pady=10, padx=10)
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg="#0055A5", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 500, 550
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        vals = {k: v.get().strip() for k, v in self.widgets.items()}
        if not all([vals["Nombre:"], vals["Código:"], vals["Teléfono:"]]):
            messagebox.showerror("Error", "Campos obligatorios vacíos")
            return
        if ProveedoresDB.agregar(vals["Nombre:"], vals["Código:"], vals["Teléfono:"], vals["Encargado:"],self.text_info.get("1.0", "end-1c").strip()):
            self.sistema.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor agregado")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "El código ya existe")


class VentanaEditarProveedor:
    def __init__(self, parent, sistema, proveedor):
        self.sistema = sistema
        self.proveedor_original = proveedor
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Proveedor")
        self.ventana.geometry("500x550")
        self.ventana.configure(bg="#FFFFFF")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.centrar_ventana()

        tk.Label(self.ventana, text="Editar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#0055A5").pack(pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        self.widgets = {}
        campos = [("Nombre:", proveedor["nombre"]), ("Código:", proveedor["codigo"]),("Teléfono:", proveedor["telefono"]), ("Encargado:", proveedor["encargado"])]

        for i, (label, val) in enumerate(campos):
            tk.Label(frame_form, text=label, font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="w",pady=10)
            entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, pady=10, padx=10)
            entry.insert(0, val)
            if label == "Código:": entry.config(state="readonly")
            self.widgets[label] = entry

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0, sticky="nw", pady=10)
        self.text_info = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_info.grid(row=4, column=1, pady=10, padx=10)
        self.text_info.insert("1.0", proveedor["informacion"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg="#0055A5", fg="white",relief="flat", cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 500, 550
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        vals = {k: v.get().strip() for k, v in self.widgets.items()}
        if not all([vals["Nombre:"], vals["Teléfono:"]]):
            messagebox.showerror("Error", "Nombre y teléfono obligatorios")
            return
        if ProveedoresDB.actualizar(self.proveedor_original["id_num"], vals["Nombre:"],self.proveedor_original["codigo"],vals["Teléfono:"], vals["Encargado:"], self.text_info.get("1.0", "end-1c").strip()):
            self.sistema.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor actualizado")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar")


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()