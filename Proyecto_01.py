import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.styles import Font
import os
from datetime import datetime

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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                nombre TEXT NOT NULL,
                apellidos TEXT,
                dpi TEXT,
                edad TEXT,
                direccion TEXT,
                telefono TEXT,
                cv_path TEXT,
                puesto TEXT,
                usuario TEXT,
                contrasena TEXT,
                sueldo_base REAL
            );
        """)

        try:
            conn.execute("ALTER TABLE colaboradores ADD COLUMN sueldo_base REAL")
        except sqlite3.OperationalError:
            pass
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                total REAL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                corriente TEXT NOT NULL,
                estado_financiero TEXT NOT NULL DEFAULT 'Balance general',
                valor REAL NOT NULL DEFAULT 0.0
            );
        """)
        try:
            conn.execute("ALTER TABLE cuentas ADD COLUMN estado_financiero TEXT NOT NULL DEFAULT 'Balance general'")
        except sqlite3.OperationalError:
            pass
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
                """INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor) VALUES (?, ?, ?, ?, ?, ?, ?)""",(nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor))
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
                """UPDATE productos SET nombre = ?, codigo = ?, precio_compra = ?, precio_venta = ?, categoria = ?, cantidad = ?, proveedor = ? WHERE id_num = ?""",(nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor, id_num))
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


class ColaboradoresDB:
    @staticmethod
    def agregar(nombre, apellidos, dpi, edad, direccion, telefono, cv_path=""):
        conn = TablasDB._conn()
        try:
            conn.execute(
                """INSERT INTO colaboradores
                   (codigo, nombre, apellidos, dpi, edad, direccion, telefono, cv_path, puesto, usuario, contrasena, sueldo_base)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("", nombre, apellidos, dpi, edad, direccion, telefono, cv_path, "", "", "", 0.0)
            )
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    @staticmethod
    def _fila_a_dict(row):
        keys = ["id", "codigo", "nombre", "apellidos", "dpi", "edad",
                "direccion", "telefono", "cv_path", "puesto", "usuario", "contrasena", "sueldo_base"]
        d = {}
        for k in keys:
            try:
                d[k] = row[k] or ""
            except Exception:
                d[k] = ""
        return d

    @staticmethod
    def obtener_todos():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT * FROM colaboradores ORDER BY nombre")
            return [ColaboradoresDB._fila_a_dict(r) for r in cursor]
        finally:
            conn.close()

    @staticmethod
    def obtener_sin_puesto():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute(
                "SELECT * FROM colaboradores WHERE (puesto IS NULL OR puesto='') AND (codigo IS NULL OR codigo='') ORDER BY nombre"
            )
            return [ColaboradoresDB._fila_a_dict(r) for r in cursor]
        finally:
            conn.close()

    @staticmethod
    def obtener_con_puesto():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute(
                "SELECT * FROM colaboradores WHERE puesto!='' AND codigo!='' ORDER BY nombre"
            )
            return [ColaboradoresDB._fila_a_dict(r) for r in cursor]
        finally:
            conn.close()

    @staticmethod
    def obtener_siguiente_secuencia(puesto):
        conn = TablasDB._conn()
        try:
            cur = conn.execute("SELECT codigo FROM colaboradores WHERE puesto=?", (puesto,))
            max_sec = 0
            for row in cur:
                cod = row["codigo"]
                if cod and len(cod) >= 3:
                    sufijo = cod[-3:]
                    if sufijo.isdigit():
                        val = int(sufijo)
                        if val > max_sec:
                            max_sec = val
            return max_sec + 1
        except Exception as e:
            print(f"Error calculando secuencia: {e}")
            return 1
        finally:
            conn.close()

    @staticmethod
    def asignar_puesto_codigo(id_col, puesto, codigo, sueldo_base):
        conn = TablasDB._conn()
        try:
            conn.execute("UPDATE colaboradores SET puesto=?, codigo=?, sueldo_base=? WHERE id=?",
                         (puesto, codigo, sueldo_base, id_col))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    @staticmethod
    def asignar_credenciales(id_col, usuario, contrasena):
        conn = TablasDB._conn()
        try:
            conn.execute("UPDATE colaboradores SET usuario=?, contrasena=? WHERE id=?", (usuario, contrasena, id_col))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    @staticmethod
    def usuario_existe(usuario):
        conn = TablasDB._conn()
        try:
            cur = conn.execute("SELECT COUNT(*) FROM colaboradores WHERE usuario=?", (usuario,))
            return cur.fetchone()[0] > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_num):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("DELETE FROM colaboradores WHERE id = ?", (id_num,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class PuestosDB:
    @staticmethod
    def crear_tabla():
        conn = TablasDB._conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS puestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                abreviatura TEXT
            )
        """)
        try:
            conn.execute("ALTER TABLE puestos ADD COLUMN abreviatura TEXT")
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()

    @staticmethod
    def agregar(nombre, abreviatura):
        PuestosDB.crear_tabla()
        conn = TablasDB._conn()
        try:
            conn.execute("INSERT INTO puestos (nombre, abreviatura) VALUES (?, ?)", (nombre, abreviatura))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos():
        PuestosDB.crear_tabla()
        conn = TablasDB._conn()
        try:
            cur = conn.execute("SELECT nombre, abreviatura FROM puestos ORDER BY nombre")
            return [{"nombre": r["nombre"], "abreviatura": r["abreviatura"]} for r in cur]
        finally:
            conn.close()


class CuentasDB:
    @staticmethod
    def agregar(nombre, tipo, corriente, estado_financiero, valor):
        conn = TablasDB._conn()
        try:
            conn.execute(
                "INSERT INTO cuentas (nombre, tipo, corriente, estado_financiero, valor) VALUES (?, ?, ?, ?, ?)",
                (nombre, tipo, corriente, estado_financiero, valor)
            )
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todas():
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("SELECT * FROM cuentas ORDER BY nombre")
            return [{"id": r["id"], "nombre": r["nombre"], "tipo": r["tipo"],
                     "corriente": r["corriente"], "estado_financiero": r["estado_financiero"],
                     "valor": r["valor"]} for r in cursor]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_cuenta):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute("DELETE FROM cuentas WHERE id = ?", (id_cuenta,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_cuenta, nombre, tipo, corriente, estado_financiero, valor):
        conn = TablasDB._conn()
        try:
            cursor = conn.execute(
                "UPDATE cuentas SET nombre=?, tipo=?, corriente=?, estado_financiero=?, valor=? WHERE id=?",
                (nombre, tipo, corriente, estado_financiero, valor, id_cuenta)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class GeneradorRecibos:
    @staticmethod
    def generar_recibo(carrito, total, nit_receptor="C/F"):
        carpeta_recibos = "recibos"
        if not os.path.exists(carpeta_recibos):
            os.makedirs(carpeta_recibos)

        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.join(carpeta_recibos, f"recibo_{fecha_str}.pdf")

        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter

        margen_izq = 40
        margen_der = width - 40
        y = height - 40

        c.setFillColorRGB(0.2, 0.4, 0.7)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, y, "Factura")
        y -= 25

        c.setStrokeColorRGB(0.2, 0.4, 0.7)
        c.setLineWidth(2)
        c.line(margen_izq, y, margen_der, y)
        y -= 25

        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margen_izq, y, "GEOS HERRAMIENTAS Y EQUIPOS")
        y -= 15

        c.setFont("Helvetica", 9)
        c.drawString(margen_izq, y, "NIT Emisor: 505303K")
        y -= 12
        c.drawString(margen_izq, y, "7 CALLE 2-27 zona 2, QUETZALTENANGO, QUETZALTENANGO")
        y -= 12
        c.drawString(margen_izq, y, f"NIT Receptor: {nit_receptor}")
        y -= 12
        c.drawString(margen_izq, y, "Nombre Receptor: CLIENTE FINAL")
        y -= 25

        fecha_actual = datetime.now()
        fecha_emision = fecha_actual.strftime("%d-%b-%Y %H:%M:%S")
        numero_factura = fecha_actual.strftime("%Y%m%d%H%M%S")

        info_y = height - 90
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(margen_der, info_y, "NÚMERO DE AUTORIZACIÓN:")
        info_y -= 10
        c.setFont("Helvetica", 8)
        c.drawRightString(margen_der, info_y, "C0DB78AF-8E1A-4310-EB91-B232BA85F45")
        info_y -= 12
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(margen_der, info_y, "Serie: C0DB78AF-8E1A")
        info_y -= 10
        c.drawRightString(margen_der, info_y, f"Número Acceso: {numero_factura}")
        info_y -= 12
        c.setFont("Helvetica", 8)
        c.drawRightString(margen_der, info_y, f"Fecha y hora de emisión: {fecha_emision}")
        info_y -= 10
        c.drawRightString(margen_der, info_y, f"Fecha y hora de certificación: {fecha_emision}")
        info_y -= 10
        c.drawRightString(margen_der, info_y, "Moneda: GTQ")
        y -= 10

        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(margen_izq, y, margen_der, y)
        y -= 20

        tabla_y = y
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(margen_izq, tabla_y - 15, margen_der - margen_izq, 15, fill=1, stroke=0)

        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 9)
        col_no = margen_izq + 5
        col_bs = margen_izq + 35
        col_cant = margen_izq + 75
        col_desc = margen_izq + 135
        col_precio = margen_der - 180
        col_desc_q = margen_der - 120
        col_otros = margen_der - 80
        col_total = margen_der - 10

        c.drawString(col_no, tabla_y - 10, "P. U")
        c.drawString(col_bs, tabla_y - 10, "IVA (Q)")
        c.drawString(col_cant, tabla_y - 10, "Cantidad")
        c.drawString(col_desc, tabla_y - 10, "Descripcion")
        c.drawRightString(col_precio + 50, tabla_y - 10, "Precio(Q)")
        c.drawRightString(col_desc_q + 30, tabla_y - 10, "Otros")
        c.drawRightString(col_total + 30, tabla_y - 10, "Total (Q)")

        y = tabla_y - 20

        c.setLineWidth(0.5)
        c.line(margen_izq, y, margen_der, y)
        y -= 15

        c.setFont("Helvetica", 9)
        item_num = 1

        for item in carrito:
            if y < 150:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)

            c.drawString(col_no, y, str(item_num))

            c.drawString(col_bs, y, "Bien")

            c.drawString(col_cant, y, f"{item['cantidad']:.0f}")

            descripcion = f"{item['nombre']}"
            if len(descripcion) > 35:
                descripcion = descripcion[:32] + "..."
            c.drawString(col_desc, y, descripcion)
            c.setFont("Helvetica", 8)
            c.drawString(col_desc, y - 8, f"Código: {item['codigo']}")
            c.setFont("Helvetica", 9)

            c.drawRightString(col_precio + 50, y, f"{item['precio']:.2f}")

            c.drawRightString(col_desc_q + 30, y, "0.00")

            c.drawRightString(col_otros + 30, y, "0.00")

            subtotal = item['cantidad'] * item['precio']
            c.drawRightString(col_total + 30, y, f"{subtotal:.2f}")

            y -= 25
            item_num += 1

        y -= 10
        c.setLineWidth(1)
        c.line(margen_izq, y, margen_der, y)
        y -= 20

        c.setFont("Helvetica-Bold", 11)
        c.drawString(col_desc, y, "TOTALES:")
        c.drawRightString(col_desc_q + 30, y, "0.00")
        c.drawRightString(col_otros + 30, y, "0.00")
        c.drawRightString(col_total + 30, y, f"{total:.2f}")

        y -= 30

        c.setLineWidth(1)
        c.rect(margen_izq, y - 80, margen_der - margen_izq, 80)

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, y - 15, "COMPLEMENTO FACTURA")

        c.setFont("Helvetica", 9)
        c.drawString(margen_izq + 10, y - 35, "Número de abono")
        c.drawString(margen_izq + 150, y - 35, "Fecha de vencimiento")
        c.drawString(margen_izq + 330, y - 35, "Monto del abono (Q)")

        c.drawString(margen_izq + 60, y - 55, "1")
        fecha_venc = (fecha_actual + timedelta(days=30)).strftime("%d/%m/%Y")
        c.drawString(margen_izq + 180, y - 55, fecha_venc)
        c.drawRightString(margen_der - 90, y - 55, f"{total:.2f}")

        c.drawString(margen_izq + 150, y - 70, "TOTALES:")
        c.drawRightString(margen_der - 90, y - 70, f"{total:.2f}")

        y -= 100

        c.setFont("Helvetica", 7)
        c.drawCentredString(width / 2, 50, "* Sujeto a pagos trimestrales ISR")
        c.drawCentredString(width / 2, 40, "Datos del certificador")
        c.drawCentredString(width / 2, 30, "Superintendencia de Administracion Tributaria NIT: 16693949")

        c.save()
        return nombre_archivo


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
            tk.Label(frame_superior, text="GEOS", font=("Arial", 36, "bold"), bg=self.COLOR_FONDO,
                     fg=self.COLOR_AZUL).pack(pady=(10, 0))
            tk.Label(frame_superior, text="Herramientas y Equipos", font=("Arial", 12), bg=self.COLOR_FONDO,
                     fg=self.COLOR_AZUL).pack()

        frame_nav = tk.Frame(self.root, bg=self.COLOR_AZUL, height=50)
        frame_nav.pack(fill="x")
        frame_nav.pack_propagate(False)

        frame_pestanas = tk.Frame(frame_nav, bg=self.COLOR_AZUL)
        frame_pestanas.place(relx=0.5, rely=0.5, anchor="center")

        pestanas = ["Inventario", "Ventas", "Proveedores", "Clientes", "Reportes", "RRHH", "Finanzas"]
        self.botones_pestanas = {}

        for i, pestana in enumerate(pestanas):
            color_bg = self.COLOR_AZUL_CLARO if i == 0 else self.COLOR_AZUL
            btn = tk.Button(frame_pestanas, text=pestana, font=("Arial", 11, "bold"), bg=color_bg, fg="white",
                            relief="flat", cursor="hand2", padx=20, pady=10,
                            command=lambda p=pestana: self.cambiar_pestana(p))
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
        elif pestana == "RRHH":
            self.mostrar_rrhh()
        elif pestana == "Finanzas":
            self.mostrar_finanzas()
        else:
            for widget in self.frame_contenido.winfo_children(): widget.destroy()
            tk.Label(self.frame_contenido, text=f"Sección {pestana} en construcción", font=("Arial", 14),
                     bg="white").pack(pady=50)

    def mostrar_ventas(self):
        for widget in self.frame_contenido.winfo_children(): widget.destroy()

        frame_nit = tk.Frame(self.frame_contenido, bg=self.COLOR_FONDO)
        frame_nit.pack(fill="x", pady=5, padx=20)
        tk.Label(frame_nit, text="NIT Receptor:", font=("Arial", 10, "bold"), bg=self.COLOR_FONDO).pack(side="left",
                                                                                                        padx=5)
        self.entry_nit_receptor = tk.Entry(frame_nit, font=("Arial", 10), width=15)
        self.entry_nit_receptor.pack(side="left", padx=5)
        self.entry_nit_receptor.insert(0, "C/F")
        tk.Label(frame_nit, text="(C/F para consumidor final)", font=("Arial", 8, "italic"), bg=self.COLOR_FONDO,
                 fg="#666").pack(side="left", padx=5)

        paned = tk.PanedWindow(self.frame_contenido, orient="horizontal", bg="#DDDDDD", sashwidth=5)
        paned.pack(fill="both", expand=True)

        frame_izq = tk.Frame(paned, bg="white", width=600)
        paned.add(frame_izq)

        tk.Label(frame_izq, text="CATÁLOGO DE PRODUCTOS", font=("Arial", 12, "bold"), bg="white",
                 fg=self.COLOR_AZUL).pack(pady=10)

        frame_busqueda_v = tk.Frame(frame_izq, bg="white")
        frame_busqueda_v.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_busqueda_v, text="Buscar (Nombre, Código, Categ.):", font=("Arial", 10), bg="white").pack(
            side="left")
        self.entry_buscar_venta = tk.Entry(frame_busqueda_v, font=("Arial", 10), width=30)
        self.entry_buscar_venta.pack(side="left", padx=5)

        self.entry_buscar_venta.bind("<KeyRelease>", self.filtrar_productos_venta)

        col_v = ("ID", "Codigo", "Nombre", "Precio", "Stock", "Categoria")
        self.tabla_prod_venta = ttk.Treeview(frame_izq, columns=col_v, show="headings", height=15)
        self.tabla_prod_venta.heading("ID", text="ID")
        self.tabla_prod_venta.heading("Codigo", text="Código")
        self.tabla_prod_venta.heading("Nombre", text="Producto")
        self.tabla_prod_venta.heading("Precio", text="Precio")
        self.tabla_prod_venta.heading("Stock", text="Stock")
        self.tabla_prod_venta.heading("Categoria", text="Categoria")

        self.tabla_prod_venta.column("ID", width=40)
        self.tabla_prod_venta.column("Codigo", width=80)
        self.tabla_prod_venta.column("Nombre", width=200)
        self.tabla_prod_venta.column("Precio", width=80)
        self.tabla_prod_venta.column("Stock", width=60)
        self.tabla_prod_venta.column("Categoria", width=100)

        self.tabla_prod_venta.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla_prod_venta.bind("<Double-1>", self.agregar_al_carrito)

        self.cargar_productos_venta()

        frame_agregar = tk.Frame(frame_izq, bg="#F0F8FF", pady=10)
        frame_agregar.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_agregar, text="Cantidad:", bg="#F0F8FF", font=("Arial", 11)).pack(side="left", padx=10)
        self.spin_cantidad = tk.Spinbox(frame_agregar, from_=1, to=100, width=5, font=("Arial", 11))
        self.spin_cantidad.pack(side="left", padx=5)

        btn_add = tk.Button(frame_agregar, text="AGREGAR AL CARRITO >>", bg="#28A745", fg="white",
                            font=("Arial", 10, "bold"), command=self.agregar_al_carrito, cursor="hand2")
        btn_add.pack(side="right", padx=20)

        frame_der = tk.Frame(paned, bg="white", width=400)
        paned.add(frame_der)

        tk.Label(frame_der, text="CARRITO DE COMPRAS", font=("Arial", 12, "bold"), bg="white", fg=self.COLOR_AZUL).pack(
            pady=10)

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

        self.lbl_total_pagar = tk.Label(frame_totales, text="TOTAL: Q0.00", font=("Arial", 12, "bold"), bg="#F8F9FA",
                                        fg="#333333")
        self.lbl_total_pagar.pack()

        btn_cobrar = tk.Button(frame_totales, text="REALIZAR VENTA", bg=self.COLOR_AZUL, fg="white",
                               font=("Arial", 14, "bold"), width=20, command=self.finalizar_venta, cursor="hand2")
        btn_cobrar.pack(pady=15)

        tk.Button(frame_totales, text="Limpiar Carrito", command=self.limpiar_carrito).pack()

    def cargar_productos_venta(self):
        for item in self.tabla_prod_venta.get_children():
            self.tabla_prod_venta.delete(item)

        productos = ProductosDB.obtener_todos()
        for p in productos:
            if p["cantidad"] > 0:
                self.tabla_prod_venta.insert("", "end",
                                             values=(p["id_num"], p["codigo"], p["nombre"], f"${p['precio_venta']}",
                                                     p["cantidad"], p["categoria"]))

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
                self.tabla_prod_venta.insert("", "end",
                                             values=(p["id_num"], p["codigo"], p["nombre"], f"${p['precio_venta']}",
                                                     p["cantidad"], p["categoria"]))

    def agregar_al_carrito(self, event=None):
        if event and not hasattr(self, 'tabla_prod_venta'): return
        if event and not self.tabla_prod_venta.identify_row(event.y): return

        seleccion = self.tabla_prod_venta.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto de la lista izquierda.")
            return

        item = self.tabla_prod_venta.item(seleccion[0])
        valores = item["values"]
        id_prod = valores[0]
        codigo = valores[1]
        nombre = valores[2]
        precio = float(str(valores[3]).replace("$", ""))
        stock_disp = float(valores[4])

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
            "codigo": codigo,
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
                total = sum(item["cantidad"] * item["precio"] for item in self.carrito_compras)

                nit_receptor = self.entry_nit_receptor.get().strip()
                if not nit_receptor:
                    nit_receptor = "C/F"

                try:
                    archivo_recibo = GeneradorRecibos.generar_recibo(self.carrito_compras, total, nit_receptor)
                    messagebox.showinfo("Venta Exitosa",
                                        f"La venta se ha registrado y el inventario actualizado.\n\n" +
                                        f"Recibo generado: {archivo_recibo}")
                except Exception as e:
                    messagebox.showinfo("Venta Exitosa",
                                        "La venta se ha registrado y el inventario actualizado.\n\n" +
                                        f"(No se pudo generar el recibo PDF: {str(e)})")

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
        self.tabla.bind("<Double-1>", self.editar_item)

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

    def editar_item(self, event=None):
        if event and not hasattr(self, 'tabla'): return
        if event and not self.tabla.identify_row(event.y): return

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
        productos = ProductosDB.obtener_todos()

        if not productos:
            messagebox.showwarning("Vacío", "No hay productos para exportar.")
            return

        ruta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(ruta_base, "inventarios")

        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ahora = datetime.now().strftime("%Y%m%d-%H%M%S")
        nombre_archivo = f"inventario-{ahora}.xlsx"
        ruta_completa = os.path.join(carpeta, nombre_archivo)

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Inventario"

            headers = ["ID", "Código", "Nombre", "Categoría", "Cantidad", "Precio Compra", "Precio Venta", "Proveedor"]
            ws.append(headers)

            for col in ws[1]:
                col.font = Font(bold=True)

            # Datos
            for p in productos:
                ws.append([
                    p["id_num"],
                    p["codigo"],
                    p["nombre"],
                    p["categoria"],
                    p["cantidad"],
                    p["precio_compra"],
                    p["precio_venta"],
                    p["proveedor"]
                ])

            for col in ws.columns:
                max_length = 0
                col_letter = col[0].column_letter
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                ws.column_dimensions[col_letter].width = max_length + 2

            wb.save(ruta_completa)

            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{ruta_completa}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
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
            tk.Button(frame_border, text=text, font=("Arial", 10, "bold"), bg="white", fg=self.COLOR_AZUL,
                      relief="flat", cursor="hand2", command=command).pack(fill="both", expand=True)

        crear_boton_azul("Agregar Producto", self.agregar_item)
        crear_boton_azul("Agregar Categoría", self.agregar_categoria)
        crear_boton_azul("Eliminar Categoría", self.eliminar_categoria)

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

        tk.Button(frame_herramientas, text="Agregar Proveedor", font=("Arial", 10, "bold"), bg="white",
                  fg=self.COLOR_AZUL, relief="solid", borderwidth=2, cursor="hand2", padx=15, pady=5,
                  command=self.agregar_proveedor).pack(side="left", padx=5)
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
        for col, width in zip(columnas, [50, 200, 100, 100, 150, 250]):
            self.tabla_proveedores.heading(col, text=col)
            self.tabla_proveedores.column(col, width=width)

        self.tabla_proveedores.pack(fill="both", expand=True, padx=5, pady=5)
        self.tabla_proveedores.bind("<Double-1>", self.editar_proveedor)
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
            if (termino in str(prov["nombre"]).lower() or termino in str(prov["codigo"]).lower() or termino in str(
                    prov["telefono"]).lower()):
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

    def editar_proveedor(self, event=None):
        if not hasattr(self, 'tabla_proveedores'): return
        if event and not self.tabla_proveedores.identify_row(event.y): return

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

    def mostrar_rrhh(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        paned = tk.PanedWindow(self.frame_contenido, orient="horizontal", bg="#DDDDDD", sashwidth=4)
        paned.pack(fill="both", expand=True)

        frame_izq = tk.Frame(paned, bg=self.COLOR_FONDO, width=210)
        paned.add(frame_izq, minsize=180)

        tk.Label(frame_izq, text="RRHH", font=("Arial", 13, "bold"), bg=self.COLOR_FONDO,
                 fg=self.COLOR_AZUL).pack(pady=(15, 10), padx=10)

        btn_style = dict(font=("Arial", 9, "bold"), bg=self.COLOR_AZUL, fg="white",
                         relief="flat", cursor="hand2", padx=8, pady=7, anchor="w")

        botones_rrhh = [
            ("Ingresar Postulante", self._rrhh_contratar),
            ("Ver colaboradores por contratar", self._rrhh_ver_postulantes),
            ("Generar Puesto", self._rrhh_generar_puesto),
            ("Asignar puesto a colaborador", self._rrhh_asignar_puesto),
            ("Generar credenciales para empleado", self._rrhh_generar_credenciales),
            ("Nómina", self._rrhh_nomina),
            ("Eliminar colaborador", self._rrhh_eliminar_colaborador),
        ]

        self.botones_rrhh_lateral = {}

        for texto, cmd in botones_rrhh:
            btn = tk.Button(frame_izq, text=texto, **btn_style)
            btn.config(command=lambda c=cmd, t=texto: self._seleccionar_boton_rrhh(t, c))
            btn.pack(fill="x", padx=10, pady=3)
            self.botones_rrhh_lateral[texto] = btn

        self.frame_rrhh_der = tk.Frame(paned, bg=self.COLOR_FONDO)
        paned.add(self.frame_rrhh_der, minsize=400)

        self._rrhh_mostrar_bienvenida()

    def _seleccionar_boton_rrhh(self, texto_boton, comando_accion):
        for btn in self.botones_rrhh_lateral.values():
            btn.config(bg=self.COLOR_AZUL)

        self.botones_rrhh_lateral[texto_boton].config(bg=self.COLOR_AZUL_CLARO)

        comando_accion()

    def _rrhh_limpiar_der(self):
        for widget in self.frame_rrhh_der.winfo_children():
            widget.destroy()

    def _rrhh_mostrar_bienvenida(self):
        self._rrhh_limpiar_der()

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_rrhh = os.path.join(ruta_script, "RRHH.png")

        try:
            from PIL import Image, ImageTk
            img_pil = Image.open(ruta_rrhh)
            img_ancho, img_alto = img_pil.size

            self._foto_rrhh = ImageTk.PhotoImage(img_pil)

            frame_img = tk.Frame(self.frame_rrhh_der, bg="#F0F4FA", highlightbackground="#CCCCCC", highlightthickness=1,
                                 width=img_ancho, height=img_alto)
            frame_img.place(relx=0.5, rely=0.5, anchor="center")
            frame_img.pack_propagate(False)

            lbl_img = tk.Label(frame_img, image=self._foto_rrhh, bg="#F0F4FA")
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")

        except ImportError:
            try:
                self._foto_rrhh = tk.PhotoImage(file=ruta_rrhh)
                img_ancho = self._foto_rrhh.width()
                img_alto = self._foto_rrhh.height()

                frame_img = tk.Frame(self.frame_rrhh_der, bg="#F0F4FA", highlightbackground="#CCCCCC",
                                     highlightthickness=1, width=img_ancho, height=img_alto)
                frame_img.place(relx=0.5, rely=0.5, anchor="center")
                frame_img.pack_propagate(False)

                lbl_img = tk.Label(frame_img, image=self._foto_rrhh, bg="#F0F4FA")
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")

            except Exception:
                tk.Label(self.frame_rrhh_der, text="[ Imagen RRHH ]", font=("Arial", 18), bg="#F0F4FA",
                         fg="#AAAAAA").place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            tk.Label(self.frame_rrhh_der, text="[ Imagen RRHH ]", font=("Arial", 18), bg="#F0F4FA", fg="#AAAAAA").place(
                relx=0.5, rely=0.5, anchor="center")

    def _rrhh_nomina(self):
        self._rrhh_limpiar_der()

        tk.Label(self.frame_rrhh_der, text="GEOS Herramientas y Equipos",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(20, 5))

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]
        mes_actual = f"{meses[datetime.now().month - 1]} de {datetime.now().year}"

        tk.Label(self.frame_rrhh_der, text=f"Nómina de {mes_actual}",
                 font=("Arial", 11, "italic"), bg=self.COLOR_FONDO, fg="#666666").pack(anchor="w", padx=30, pady=5)

        frame_tabla = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("Empleado", "Puesto", "Salario Bruto", "IGSS (4.83%)", "Cuota Patronal (12.67%)", "Anticipos", "Total")

        style = ttk.Style()
        style.configure("Nomina.Treeview", background="white", fieldbackground="white", rowheight=30)

        self._tabla_nomina = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                          yscrollcommand=sb.set, height=18, style="Nomina.Treeview")
        sb.config(command=self._tabla_nomina.yview)

        anchos = [160, 120, 100, 100, 150, 100, 100]
        for col, w in zip(cols, anchos):
            self._tabla_nomina.heading(col, text=col)
            self._tabla_nomina.column(col, width=w, anchor="center")

        self._tabla_nomina.column("Empleado", anchor="w")
        self._tabla_nomina.pack(fill="both", expand=True)

        self._tabla_nomina.tag_configure('oddrow', background='#F8D7E3')
        self._tabla_nomina.tag_configure('evenrow', background='#FFFFFF')

        empleados = ColaboradoresDB.obtener_con_puesto()

        fila_idx = 0
        for emp in empleados:
            if not emp.get("usuario"):
                continue

            try:
                sueldo_base = float(emp.get("sueldo_base", 0.0) or 0.0)
            except ValueError:
                sueldo_base = 0.0

            if sueldo_base <= 0:
                continue

            igss = sueldo_base * 0.0483
            cuota_patronal = sueldo_base * 0.1267
            anticipos = 0.0

            total = sueldo_base - igss - anticipos

            nombre_completo = f"{emp['nombre']} {emp['apellidos']}"

            tag = 'evenrow' if fila_idx % 2 == 0 else 'oddrow'

            self._tabla_nomina.insert("", "end", values=(
                nombre_completo,
                emp["puesto"],
                f"Q{sueldo_base:,.2f}",
                f"Q{igss:,.2f}",
                f"Q{cuota_patronal:,.2f}",
                f"Q{anticipos:,.2f}",
                f"Q{total:,.2f}"
            ), tags=(tag,))

            fila_idx += 1

        tk.Button(self.frame_rrhh_der, text="Imprimir Nómina", font=("Arial", 11, "bold"),
                  bg=self.COLOR_AZUL, fg="white", relief="flat", cursor="hand2", padx=25, pady=8).pack(pady=10)

    def _rrhh_contratar(self):
        self._rrhh_limpiar_der()

        canvas_scroll = tk.Canvas(self.frame_rrhh_der, bg=self.COLOR_FONDO, highlightthickness=0)
        sb = ttk.Scrollbar(self.frame_rrhh_der, orient="vertical", command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas_scroll, bg=self.COLOR_FONDO)
        win_id = canvas_scroll.create_window((0, 0), window=inner, anchor="nw")

        def _on_resize(e):
            canvas_scroll.itemconfig(win_id, width=e.width)

        canvas_scroll.bind("<Configure>", _on_resize)
        inner.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))

        tk.Label(inner, text="Ingresar Postulante", font=("Arial", 15, "bold"),
                 bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(20, 10))

        frame_form = tk.Frame(inner, bg=self.COLOR_FONDO)
        frame_form.pack(padx=60, pady=5, fill="x")
        frame_form.columnconfigure(1, weight=1)

        campos_labels = ["Nombre:", "Apellidos:", "DPI:", "Edad:", "Dirección:", "Teléfono:"]
        self._rrhh_entries = {}
        for i, label in enumerate(campos_labels):
            tk.Label(frame_form, text=label, font=("Arial", 10, "bold"),
                     bg=self.COLOR_FONDO, anchor="e", width=12).grid(row=i, column=0, sticky="e", pady=7, padx=5)
            entry = tk.Entry(frame_form, font=("Arial", 10), width=35)
            entry.grid(row=i, column=1, sticky="ew", pady=7, padx=5)
            self._rrhh_entries[label] = entry

        tk.Label(frame_form, text="Importar CV:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO, anchor="e", width=12).grid(row=6, column=0, sticky="e", pady=7, padx=5)
        frame_cv = tk.Frame(frame_form, bg=self.COLOR_FONDO)
        frame_cv.grid(row=6, column=1, sticky="ew", pady=7, padx=5)
        self._rrhh_cv_path = tk.StringVar(value="")
        self._lbl_cv = tk.Label(frame_cv, text="Ningún archivo seleccionado",
                                font=("Arial", 9), bg=self.COLOR_FONDO, fg="#666666")
        self._lbl_cv.pack(side="left", padx=(0, 10))
        tk.Button(frame_cv, text="Seleccionar PDF", font=("Arial", 9, "bold"),
                  bg="white", fg=self.COLOR_AZUL, relief="solid", borderwidth=2,
                  cursor="hand2", padx=8, pady=3,
                  command=self._rrhh_seleccionar_cv).pack(side="left")

        frame_btns = tk.Frame(inner, bg=self.COLOR_FONDO)
        frame_btns.pack(pady=20)
        tk.Button(frame_btns, text="Confirmar", font=("Arial", 11, "bold"),
                  bg="#28A745", fg="white", relief="flat", cursor="hand2", padx=30, pady=8,
                  command=self._rrhh_confirmar_contratacion).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Cancelar", font=("Arial", 11, "bold"),
                  bg="#6C757D", fg="white", relief="flat", cursor="hand2", padx=30, pady=8,
                  command=self._rrhh_limpiar_contratacion).pack(side="left", padx=10)

    def _rrhh_seleccionar_cv(self):
        from tkinter import filedialog
        ruta = filedialog.askopenfilename(
            title="Seleccionar CV (PDF, máx. 5 MB)",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if not ruta:
            return
        if os.path.getsize(ruta) > 5 * 1024 * 1024:
            messagebox.showerror("Archivo muy grande", "El PDF no debe superar 5 MB.")
            return
        self._rrhh_cv_path.set(ruta)
        nombre_corto = os.path.basename(ruta)
        if len(nombre_corto) > 40:
            nombre_corto = nombre_corto[:37] + "..."
        self._lbl_cv.config(text=nombre_corto, fg="#333333")

    def _rrhh_limpiar_contratacion(self):
        for entry in self._rrhh_entries.values():
            entry.delete(0, "end")
        self._rrhh_cv_path.set("")
        if hasattr(self, "_lbl_cv"):
            self._lbl_cv.config(text="Ningún archivo seleccionado", fg="#666666")

    def _rrhh_confirmar_contratacion(self):
        vals = {k: v.get().strip() for k, v in self._rrhh_entries.items()}
        if not vals["Nombre:"]:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        cv_path = self._rrhh_cv_path.get()
        if ColaboradoresDB.agregar(vals["Nombre:"], vals["Apellidos:"], vals["DPI:"],
                                   vals["Edad:"], vals["Dirección:"], vals["Teléfono:"], cv_path):
            self._rrhh_limpiar_contratacion()
            messagebox.showinfo("Éxito", "Empleado registrado con éxito")
        else:
            messagebox.showerror("Error", "No se pudo registrar el empleado.")

    def _rrhh_ver_postulantes(self):
        self._rrhh_limpiar_der()
        tk.Label(self.frame_rrhh_der, text="Colaboradores por Contratar",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(15, 5))
        tk.Label(self.frame_rrhh_der,
                 text="Postulantes sin puesto ni código asignado. Haga doble clic para ver el CV.",
                 font=("Arial", 9, "italic"), bg=self.COLOR_FONDO, fg="#666666").pack()

        frame_tabla = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("ID", "Nombre", "Apellidos", "DPI", "Edad", "Dirección", "Teléfono", "CV")
        self._tabla_postulantes = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                               yscrollcommand=sb.set, height=18)
        sb.config(command=self._tabla_postulantes.yview)
        anchos = [40, 150, 150, 110, 50, 180, 100, 200]
        for col, w in zip(cols, anchos):
            self._tabla_postulantes.heading(col, text=col)
            self._tabla_postulantes.column(col, width=w)
        self._tabla_postulantes.column("ID", width=0, stretch=False)
        self._tabla_postulantes.pack(fill="both", expand=True)
        self._tabla_postulantes.bind("<Double-1>", self._rrhh_ver_cv_postulante)
        self._cargar_postulantes()

    def _cargar_postulantes(self):
        if not hasattr(self, '_tabla_postulantes'):
            return
        for item in self._tabla_postulantes.get_children():
            self._tabla_postulantes.delete(item)
        for col in ColaboradoresDB.obtener_sin_puesto():
            self._tabla_postulantes.insert("", "end", values=(
                col["id"], col["nombre"], col["apellidos"], col["dpi"],
                col["edad"], col["direccion"], col["telefono"], col["cv_path"]
            ))

    def _rrhh_ver_cv_postulante(self, event=None):
        if not hasattr(self, '_tabla_postulantes'): return
        if event and not self._tabla_postulantes.identify_row(event.y): return

        sel = self._tabla_postulantes.selection()
        if not sel:
            return
        vals = self._tabla_postulantes.item(sel[0])["values"]
        cv_path = vals[7] if len(vals) > 7 else ""
        if not cv_path or not os.path.exists(str(cv_path)):
            messagebox.showinfo("Sin CV", "Este postulante no tiene CV adjunto o el archivo no existe.")
            return
        import subprocess, sys
        try:
            if sys.platform.startswith("win"):
                os.startfile(cv_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", cv_path])
            else:
                subprocess.call(["xdg-open", cv_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF:\n{e}")

    def _rrhh_generar_puesto(self):
        self._rrhh_limpiar_der()
        outer = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="Generar Puesto", font=("Arial", 16, "bold"),
                 bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(0, 20))

        frame_inp = tk.Frame(outer, bg=self.COLOR_FONDO)
        frame_inp.pack()

        tk.Label(frame_inp, text="Nombre del puesto:", font=("Arial", 11, "bold"),
                 bg=self.COLOR_FONDO).grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self._entry_puesto = tk.Entry(frame_inp, font=("Arial", 11), width=30)
        self._entry_puesto.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(frame_inp, text="Abreviatura:", font=("Arial", 11, "bold"),
                 bg=self.COLOR_FONDO).grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self._entry_abrev = tk.Entry(frame_inp, font=("Arial", 11), width=30)
        self._entry_abrev.grid(row=1, column=1, padx=10, pady=8)

        tk.Button(outer, text="Guardar Puesto", font=("Arial", 11, "bold"),
                  bg="#28A745", fg="white", relief="flat", cursor="hand2", padx=25, pady=8,
                  command=self._rrhh_guardar_puesto).pack(pady=15)

        tk.Label(outer, text="Puestos creados:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(10, 2))
        self._lista_puestos = tk.Listbox(outer, font=("Arial", 10), width=40, height=8,
                                         selectbackground=self.COLOR_AZUL)
        self._lista_puestos.pack(pady=5)
        self._actualizar_lista_puestos()

    def _actualizar_lista_puestos(self):
        if not hasattr(self, '_lista_puestos'):
            return
        self._lista_puestos.delete(0, "end")
        for p in PuestosDB.obtener_todos():
            abrev = p["abreviatura"] if p["abreviatura"] else ""
            mostrar = f"{p['nombre']} ({abrev})" if abrev else p['nombre']
            self._lista_puestos.insert("end", mostrar)

    def _rrhh_guardar_puesto(self):
        nombre = self._entry_puesto.get().strip()
        abrev = self._entry_abrev.get().strip()

        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre para el puesto.")
            return
        if not abrev:
            messagebox.showerror("Error", "Ingrese una abreviatura para el puesto.")
            return

        if PuestosDB.agregar(nombre, abrev):
            self._entry_puesto.delete(0, "end")
            self._entry_abrev.delete(0, "end")
            self._actualizar_lista_puestos()
            messagebox.showinfo("Éxito", f"Puesto '{nombre}' creado correctamente.")
        else:
            messagebox.showerror("Error", "El puesto ya existe.")

    def _rrhh_asignar_puesto(self):
        self._rrhh_limpiar_der()
        tk.Label(self.frame_rrhh_der, text="Asignar Puesto a Colaborador",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(15, 5))

        frame_busq = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_busq.pack(fill="x", padx=15, pady=5)
        tk.Label(frame_busq, text="Buscar aspirante por nombre o DPI:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO).pack(side="left", padx=5)
        self._entry_busq_asignar = tk.Entry(frame_busq, font=("Arial", 10), width=30)
        self._entry_busq_asignar.pack(side="left", padx=5)
        self._entry_busq_asignar.bind("<KeyRelease>", self._filtrar_asignar)

        frame_tabla = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("ID", "Nombre", "Apellidos", "DPI", "Edad", "Dirección", "Teléfono")
        self._tabla_asignar = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                           yscrollcommand=sb.set, height=15)
        sb.config(command=self._tabla_asignar.yview)
        anchos = [0, 160, 160, 120, 55, 180, 110]
        for col, w in zip(cols, anchos):
            self._tabla_asignar.heading(col, text=col)
            self._tabla_asignar.column(col, width=w)
        self._tabla_asignar.column("ID", width=0, stretch=False)
        self._tabla_asignar.pack(fill="both", expand=True)

        self._tabla_asignar.bind("<Double-1>", self._click_asignar)

        self._datos_asignar = ColaboradoresDB.obtener_sin_puesto()
        self._filtrar_asignar()

    def _filtrar_asignar(self, event=None):
        if not hasattr(self, '_tabla_asignar'):
            return
        termino = self._entry_busq_asignar.get().strip().lower()
        for item in self._tabla_asignar.get_children():
            self._tabla_asignar.delete(item)

        for col in self._datos_asignar:
            nombre_completo = (col["nombre"] + " " + col["apellidos"]).lower()
            if not termino or termino in nombre_completo or termino in col["dpi"].lower():
                self._tabla_asignar.insert("", "end", values=(
                    col["id"], col["nombre"], col["apellidos"], col["dpi"],
                    col["edad"], col["direccion"], col["telefono"]
                ))

    def _click_asignar(self, event=None):
        if not hasattr(self, '_tabla_asignar'): return
        if event and not self._tabla_asignar.identify_row(event.y): return

        sel = self._tabla_asignar.selection()
        if not sel:
            return
        vals = self._tabla_asignar.item(sel[0])["values"]
        col_id = vals[0]
        col_data = next((c for c in self._datos_asignar if str(c["id"]) == str(col_id)), None)
        if not col_data:
            return
        self._abrir_ventana_asignar(col_data)

    def _abrir_ventana_asignar(self, col_data):
        vent = tk.Toplevel(self.root)
        vent.title("Asignar Puesto")
        vent.configure(bg="#FFFFFF")
        vent.transient(self.root)
        vent.grab_set()
        vent.update_idletasks()
        w, h = 480, 560
        x = (vent.winfo_screenwidth() // 2) - (w // 2)
        y = (vent.winfo_screenheight() // 2) - (h // 2)
        vent.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(vent, text="Datos del Colaborador", font=("Arial", 14, "bold"),
                 bg="#FFFFFF", fg=self.COLOR_AZUL).pack(pady=(15, 5))

        frame_datos = tk.Frame(vent, bg="#FFFFFF")
        frame_datos.pack(padx=30, pady=5, fill="x")

        datos_mostrar = [
            ("Nombre:", col_data["nombre"]),
            ("Apellidos:", col_data["apellidos"]),
            ("DPI:", col_data["dpi"]),
            ("Edad:", col_data["edad"]),
            ("Dirección:", col_data["direccion"]),
            ("Teléfono:", col_data["telefono"])
        ]
        for i, (lbl, val) in enumerate(datos_mostrar):
            tk.Label(frame_datos, text=lbl, font=("Arial", 10, "bold"),
                     bg="#FFFFFF", anchor="e", width=12).grid(row=i, column=0, sticky="e", pady=5, padx=5)
            tk.Label(frame_datos, text=val, font=("Arial", 10),
                     bg="#F0F4FA", anchor="w", width=28, relief="groove", pady=3).grid(row=i, column=1, sticky="ew",
                                                                                       pady=5, padx=5)

        tk.Frame(vent, bg="#CCCCCC", height=1).pack(fill="x", padx=20, pady=8)

        frame_asig = tk.Frame(vent, bg="#FFFFFF")
        frame_asig.pack(padx=30, fill="x")

        tk.Label(frame_asig, text="Seleccionar Puesto:", font=("Arial", 10, "bold"),
                 bg="#FFFFFF", anchor="e", width=18).grid(row=0, column=0, sticky="e", pady=8, padx=5)

        todos_los_puestos = PuestosDB.obtener_todos()
        puestos_lista = [p["nombre"] for p in todos_los_puestos]

        combo_puesto = ttk.Combobox(frame_asig, values=puestos_lista, font=("Arial", 10), width=22)
        combo_puesto.grid(row=0, column=1, sticky="ew", pady=8, padx=5)

        tk.Label(frame_asig, text="Código de Empleado:", font=("Arial", 10, "bold"),
                 bg="#FFFFFF", anchor="e", width=18).grid(row=1, column=0, sticky="e", pady=8, padx=5)
        entry_codigo = tk.Entry(frame_asig, font=("Arial", 10), width=24)
        entry_codigo.grid(row=1, column=1, sticky="ew", pady=8, padx=5)

        tk.Label(frame_asig, text="Sueldo Base (Q):", font=("Arial", 10, "bold"),
                 bg="#FFFFFF", anchor="e", width=18).grid(row=2, column=0, sticky="e", pady=8, padx=5)
        entry_sueldo = tk.Entry(frame_asig, font=("Arial", 10), width=24)
        entry_sueldo.grid(row=2, column=1, sticky="ew", pady=8, padx=5)

        def autocompletar_codigo(event=None):
            puesto_seleccionado = combo_puesto.get().strip()
            if not puesto_seleccionado:
                return

            abreviatura = ""
            for p in todos_los_puestos:
                if p["nombre"] == puesto_seleccionado:
                    abreviatura = p["abreviatura"] if p["abreviatura"] else puesto_seleccionado[:3].upper()
                    break

            primer_nombre = col_data["nombre"].strip().split()[0].upper()
            siguiente_num = ColaboradoresDB.obtener_siguiente_secuencia(puesto_seleccionado)
            nuevo_codigo = f"{primer_nombre}-{abreviatura.upper()}{siguiente_num:03d}"

            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, nuevo_codigo)

        combo_puesto.bind("<<ComboboxSelected>>", autocompletar_codigo)

        frame_btns = tk.Frame(vent, bg="#FFFFFF")
        frame_btns.pack(pady=15)

        def contratar():
            puesto = combo_puesto.get().strip()
            codigo = entry_codigo.get().strip()
            sueldo_str = entry_sueldo.get().strip()

            if not puesto or not codigo:
                messagebox.showerror("Error", "Debe seleccionar un puesto y asignar un código.", parent=vent)
                return

            if not sueldo_str:
                messagebox.showerror("Error", "Debe ingresar el sueldo base del empleado.", parent=vent)
                return

            try:
                sueldo_base = float(sueldo_str)
            except ValueError:
                messagebox.showerror("Error", "El sueldo base debe ser un número válido.", parent=vent)
                return

            if ColaboradoresDB.asignar_puesto_codigo(col_data["id"], puesto, codigo, sueldo_base):
                nombre_completo = f"{col_data['nombre']} {col_data['apellidos']}"
                messagebox.showinfo("Éxito", f"{nombre_completo} contratado correctamente", parent=vent)
                self._datos_asignar = ColaboradoresDB.obtener_sin_puesto()
                self._filtrar_asignar()
                vent.destroy()
            else:
                messagebox.showerror("Error", "No se pudo completar la asignación.", parent=vent)

        tk.Button(frame_btns, text="Contratar", font=("Arial", 11, "bold"),
                  bg="#28A745", fg="white", relief="flat", cursor="hand2", padx=25, pady=8,
                  command=contratar).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Regresar", font=("Arial", 11, "bold"),
                  bg="#6C757D", fg="white", relief="flat", cursor="hand2", padx=25, pady=8,
                  command=vent.destroy).pack(side="left", padx=10)

    def _rrhh_generar_credenciales(self):
        self._rrhh_limpiar_der()
        tk.Label(self.frame_rrhh_der, text="Generar Credenciales para Empleado",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(pady=(15, 5))
        tk.Label(self.frame_rrhh_der,
                 text="Haga clic en un empleado para generar sus credenciales automáticamente.",
                 font=("Arial", 9, "italic"), bg=self.COLOR_FONDO, fg="#666666").pack()

        frame_busq = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_busq.pack(fill="x", padx=15, pady=5)
        tk.Label(frame_busq, text="Buscar aspirante por nombre o DPI:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO).pack(side="left", padx=5)
        self._entry_busq_cred = tk.Entry(frame_busq, font=("Arial", 10), width=30)
        self._entry_busq_cred.pack(side="left", padx=5)
        self._entry_busq_cred.bind("<KeyRelease>", self._filtrar_credenciales)

        frame_tabla = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("ID", "Código", "Nombre", "Apellidos", "DPI", "Puesto", "Usuario")
        self._tabla_cred = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                        yscrollcommand=sb.set, height=15)
        sb.config(command=self._tabla_cred.yview)
        anchos = [0, 80, 140, 140, 110, 120, 130]
        for col, w in zip(cols, anchos):
            self._tabla_cred.heading(col, text=col)
            self._tabla_cred.column(col, width=w)
        self._tabla_cred.column("ID", width=0, stretch=False)
        self._tabla_cred.pack(fill="both", expand=True)

        self._tabla_cred.bind("<Double-1>", self._click_generar_credencial)

        self._datos_cred = ColaboradoresDB.obtener_con_puesto()
        self._filtrar_credenciales()

    def _filtrar_credenciales(self, event=None):
        if not hasattr(self, '_tabla_cred'):
            return
        termino = self._entry_busq_cred.get().strip().lower()
        for item in self._tabla_cred.get_children():
            self._tabla_cred.delete(item)

        for col in self._datos_cred:
            nombre_completo = (col["nombre"] + " " + col["apellidos"]).lower()
            if not termino or termino in nombre_completo or termino in col["dpi"].lower():
                self._tabla_cred.insert("", "end", values=(
                    col["id"], col["codigo"], col["nombre"], col["apellidos"],
                    col["dpi"], col["puesto"], col["usuario"]
                ))

    def _click_generar_credencial(self, event=None):
        if not hasattr(self, '_tabla_cred'): return
        if event and not self._tabla_cred.identify_row(event.y): return

        sel = self._tabla_cred.selection()
        if not sel:
            return
        vals = self._tabla_cred.item(sel[0])["values"]
        col_id = vals[0]
        col_data = next((c for c in self._datos_cred if str(c["id"]) == str(col_id)), None)
        if not col_data:
            return

        if col_data["usuario"]:
            messagebox.showinfo("Credenciales ya generadas",
                                f"Credenciales actuales del empleado:\n\n"
                                f"Usuario: {col_data['usuario']}\n"
                                f"Contraseña: {col_data['contrasena']}")
            return

        usuario = col_data["codigo"]

        if not usuario:
            messagebox.showerror("Error", "Este empleado no tiene un código asignado.")
            return

        contrasena = usuario[::-1]

        if ColaboradoresDB.asignar_credenciales(col_id, usuario, contrasena):
            self._datos_cred = ColaboradoresDB.obtener_con_puesto()
            self._filtrar_credenciales()
            messagebox.showinfo("Credenciales generadas",
                                f"Usuario: {usuario}\nContraseña: {contrasena}\n\n"
                                f"(Contraseña = código al revés)")
        else:
            messagebox.showerror("Error", "No se pudieron guardar las credenciales.")

    def _rrhh_eliminar_colaborador(self):
        self._rrhh_limpiar_der()
        tk.Label(self.frame_rrhh_der, text="Eliminar Colaborador",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO, fg="#DC3545").pack(pady=(15, 5))
        tk.Label(self.frame_rrhh_der,
                 text="Seleccione un colaborador y presione Eliminar (o doble clic).",
                 font=("Arial", 9, "italic"), bg=self.COLOR_FONDO, fg="#666666").pack()

        frame_tabla = tk.Frame(self.frame_rrhh_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("ID", "Código", "Nombre", "Apellidos", "DPI", "Puesto")
        self._tabla_elim = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                        yscrollcommand=sb.set, height=16)
        sb.config(command=self._tabla_elim.yview)
        anchos = [0, 80, 180, 180, 120, 150]
        for col, w in zip(cols, anchos):
            self._tabla_elim.heading(col, text=col)
            self._tabla_elim.column(col, width=w)
        self._tabla_elim.column("ID", width=0, stretch=False)
        self._tabla_elim.pack(fill="both", expand=True)

        self._tabla_elim.bind("<Double-1>", self._click_eliminar_colaborador)

        for col in ColaboradoresDB.obtener_todos():
            self._tabla_elim.insert("", "end", values=(
                col["id"], col["codigo"], col["nombre"], col["apellidos"], col["dpi"], col["puesto"]
            ))

        tk.Button(self.frame_rrhh_der, text="Eliminar Seleccionado",
                  font=("Arial", 11, "bold"), bg="#DC3545", fg="white",
                  relief="flat", cursor="hand2", padx=25, pady=8,
                  command=self._click_eliminar_colaborador).pack(pady=10)

    def _click_eliminar_colaborador(self, event=None):
        if not hasattr(self, '_tabla_elim'): return
        if event and not self._tabla_elim.identify_row(event.y): return

        sel = self._tabla_elim.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un colaborador para eliminar.")
            return
        vals = self._tabla_elim.item(sel[0])["values"]
        self._abrir_ventana_eliminar(vals, sel[0])

    def _abrir_ventana_eliminar(self, vals, item_id):
        vent = tk.Toplevel(self.root)
        vent.title("Eliminar Colaborador")
        vent.configure(bg="#FFFFFF")
        vent.transient(self.root)
        vent.grab_set()
        vent.update_idletasks()
        w, h = 450, 400
        x = (vent.winfo_screenwidth() // 2) - (w // 2)
        y = (vent.winfo_screenheight() // 2) - (h // 2)
        vent.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(vent, text="Desvincular Colaborador", font=("Arial", 14, "bold"),
                 bg="#FFFFFF", fg="#DC3545").pack(pady=(15, 5))

        nombre_completo = f"{vals[2]} {vals[3]}"
        tk.Label(vent, text=f"Empleado: {nombre_completo}", font=("Arial", 11, "bold"), bg="#FFFFFF").pack(pady=5)
        tk.Label(vent, text=f"DPI: {vals[4]} | Puesto: {vals[5]}", font=("Arial", 10), bg="#FFFFFF", fg="#666666").pack(
            pady=5)

        tk.Frame(vent, bg="#CCCCCC", height=1).pack(fill="x", padx=20, pady=10)

        frame_cv = tk.Frame(vent, bg="#FFFFFF")
        frame_cv.pack(pady=10)

        tk.Label(frame_cv, text="Carta de renuncia/despido (PDF):", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(
            anchor="center")

        frame_btn_pdf = tk.Frame(frame_cv, bg="#FFFFFF")
        frame_btn_pdf.pack(pady=8)

        ruta_pdf = tk.StringVar(value="")
        lbl_pdf = tk.Label(frame_btn_pdf, text="Ningún archivo seleccionado", font=("Arial", 9), bg="#FFFFFF",
                           fg="#666666")
        lbl_pdf.pack(side="left", padx=(0, 10))

        def seleccionar_pdf():
            from tkinter import filedialog
            ruta = filedialog.askopenfilename(
                title="Seleccionar Documento PDF",
                filetypes=[("Archivos PDF", "*.pdf")]
            )
            if ruta:
                ruta_pdf.set(ruta)
                nombre_corto = os.path.basename(ruta)
                if len(nombre_corto) > 30:
                    nombre_corto = nombre_corto[:27] + "..."
                lbl_pdf.config(text=nombre_corto, fg="#333333")

        tk.Button(frame_btn_pdf, text="Adjuntar PDF", font=("Arial", 9, "bold"),
                  bg="white", fg=self.COLOR_AZUL, relief="solid", borderwidth=2,
                  cursor="hand2", padx=8, pady=3, command=seleccionar_pdf).pack(side="left")

        frame_sec = tk.Frame(vent, bg="#FFFFFF")
        frame_sec.pack(pady=15)
        tk.Label(frame_sec, text="Código de seguridad:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left",
                                                                                                        padx=5)
        entry_codigo = tk.Entry(frame_sec, font=("Arial", 10), show="*", width=15)
        entry_codigo.pack(side="left", padx=5)

        frame_btns = tk.Frame(vent, bg="#FFFFFF")
        frame_btns.pack(pady=20)

        def confirmar():
            if not ruta_pdf.get():
                messagebox.showerror("Error", "Debe adjuntar la carta (PDF).", parent=vent)
                return
            if entry_codigo.get() != "admin123":
                messagebox.showerror("Error", "Código de seguridad incorrecto.", parent=vent)
                return

            if ColaboradoresDB.eliminar(vals[0]):
                self._tabla_elim.delete(item_id)
                messagebox.showinfo("Éxito", "Colaborador eliminado correctamente.", parent=vent)
                vent.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el colaborador.", parent=vent)

        tk.Button(frame_btns, text="Eliminar", font=("Arial", 11, "bold"),
                  bg="#DC3545", fg="white", relief="flat", cursor="hand2", padx=25, pady=8,
                  command=confirmar).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Cancelar", font=("Arial", 11, "bold"),
                  bg="#6C757D", fg="white", relief="flat", cursor="hand2", padx=25, pady=8,
                  command=vent.destroy).pack(side="left", padx=10)

    def mostrar_finanzas(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        paned = tk.PanedWindow(self.frame_contenido, orient="horizontal", bg="#DDDDDD", sashwidth=4)
        paned.pack(fill="both", expand=True)

        frame_izq = tk.Frame(paned, bg=self.COLOR_FONDO, width=210)
        paned.add(frame_izq, minsize=180)

        tk.Label(frame_izq, text="Finanzas", font=("Arial", 13, "bold"), bg=self.COLOR_FONDO,
                 fg=self.COLOR_AZUL).pack(pady=(15, 10), padx=10)

        btn_style = dict(font=("Arial", 9, "bold"), bg=self.COLOR_AZUL, fg="white",
                         relief="flat", cursor="hand2", padx=8, pady=7, anchor="w")

        botones_finanzas = [
            ("Cuentas", self._finanzas_cuentas),
            ("Balance General", self._finanzas_balance_general),
            ("Estado de resultados", self._finanzas_estado_resultados),
        ]

        self.botones_finanzas_lateral = {}
        for texto, cmd in botones_finanzas:
            btn = tk.Button(frame_izq, text=texto, **btn_style)
            btn.config(command=lambda c=cmd, t=texto: self._seleccionar_boton_finanzas(t, c))
            btn.pack(fill="x", padx=10, pady=3)
            self.botones_finanzas_lateral[texto] = btn

        self.frame_finanzas_der = tk.Frame(paned, bg=self.COLOR_FONDO)
        paned.add(self.frame_finanzas_der, minsize=400)

        self._finanzas_mostrar_bienvenida()

    def _seleccionar_boton_finanzas(self, texto_boton, comando_accion):
        for btn in self.botones_finanzas_lateral.values():
            btn.config(bg=self.COLOR_AZUL)
        self.botones_finanzas_lateral[texto_boton].config(bg=self.COLOR_AZUL_CLARO)
        comando_accion()

    def _finanzas_limpiar_der(self):
        for widget in self.frame_finanzas_der.winfo_children():
            widget.destroy()

    # ── ÚNICO MÉTODO MODIFICADO ──────────────────────────────────────────────
    def _finanzas_mostrar_bienvenida(self):
        self._finanzas_limpiar_der()

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_finanzas = os.path.join(ruta_script, "Finanzas.png")

        try:
            from PIL import Image, ImageTk
            img_pil = Image.open(ruta_finanzas)
            img_ancho, img_alto = img_pil.size

            self._foto_finanzas = ImageTk.PhotoImage(img_pil)

            frame_img = tk.Frame(self.frame_finanzas_der, bg="#F0F4FA",
                                 highlightbackground="#CCCCCC", highlightthickness=1,
                                 width=img_ancho, height=img_alto)
            frame_img.place(relx=0.5, rely=0.5, anchor="center")
            frame_img.pack_propagate(False)

            lbl_img = tk.Label(frame_img, image=self._foto_finanzas, bg="#F0F4FA")
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")

        except ImportError:
            try:
                self._foto_finanzas = tk.PhotoImage(file=ruta_finanzas)
                img_ancho = self._foto_finanzas.width()
                img_alto = self._foto_finanzas.height()

                frame_img = tk.Frame(self.frame_finanzas_der, bg="#F0F4FA",
                                     highlightbackground="#CCCCCC", highlightthickness=1,
                                     width=img_ancho, height=img_alto)
                frame_img.place(relx=0.5, rely=0.5, anchor="center")
                frame_img.pack_propagate(False)

                lbl_img = tk.Label(frame_img, image=self._foto_finanzas, bg="#F0F4FA")
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")

            except Exception:
                tk.Label(self.frame_finanzas_der, text="[ Imagen Finanzas ]",
                         font=("Arial", 18), bg="#F0F4FA", fg="#AAAAAA").place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            tk.Label(self.frame_finanzas_der, text="[ Imagen Finanzas ]",
                     font=("Arial", 18), bg="#F0F4FA", fg="#AAAAAA").place(relx=0.5, rely=0.5, anchor="center")
    # ── FIN DEL MÉTODO MODIFICADO ────────────────────────────────────────────

    def _finanzas_proximamente(self):
        self._finanzas_limpiar_der()
        tk.Label(self.frame_finanzas_der, text="Funcionalidad próximamente disponible",
                 font=("Arial", 13), bg=self.COLOR_FONDO, fg="#888888").pack(pady=80)

    def _finanzas_cuentas(self):
        self._finanzas_limpiar_der()

        tk.Label(self.frame_finanzas_der, text="Gestión de Cuentas",
                 font=("Arial", 14, "bold"), bg=self.COLOR_FONDO,
                 fg=self.COLOR_AZUL).pack(pady=(15, 5))

        frame_form_outer = tk.Frame(self.frame_finanzas_der, bg=self.COLOR_FONDO,
                                    highlightbackground="#AAAAAA", highlightthickness=2)
        frame_form_outer.pack(fill="x", padx=20, pady=5)

        frame_cols = tk.Frame(frame_form_outer, bg=self.COLOR_FONDO)
        frame_cols.pack(padx=20, pady=15, fill="x")
        frame_cols.columnconfigure(0, weight=1)
        frame_cols.columnconfigure(1, weight=1)

        frame_izq = tk.Frame(frame_cols, bg=self.COLOR_FONDO)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        tk.Label(frame_izq, text="INGRESE EL NOMBRE DE LA CUENTA:",
                 font=("Arial", 10, "bold"), bg=self.COLOR_FONDO).pack(anchor="w", pady=(0, 4))

        self._entry_cuenta_nombre = tk.Entry(frame_izq, font=("Arial", 11))
        self._entry_cuenta_nombre.pack(fill="x", ipady=4, pady=(0, 14))

        tk.Label(frame_izq, text="CARACTERÍSTICAS DE LA CUENTA",
                 font=("Arial", 10, "bold"), bg=self.COLOR_FONDO).pack(anchor="w", pady=(0, 6))

        tk.Label(frame_izq, text="Estado financiero:", font=("Arial", 9, "bold"),
                 bg=self.COLOR_FONDO).pack(anchor="w")

        self._lb_estado_financiero = ttk.Combobox(frame_izq, font=("Arial", 10), width=22,
                                                  values=["Balance general", "Estado de resultados"],
                                                  state="readonly")
        self._lb_estado_financiero.current(0)
        self._lb_estado_financiero.pack(anchor="w", pady=4)
        self._lb_estado_financiero.bind("<<ComboboxSelected>>", self._finanzas_on_estado_change)

        self._frame_der_dinamico = tk.Frame(frame_cols, bg=self.COLOR_FONDO)
        self._frame_der_dinamico.grid(row=0, column=1, sticky="nsew")

        self._finanzas_render_columna_der("Balance general")

        frame_btns = tk.Frame(self.frame_finanzas_der, bg=self.COLOR_FONDO)
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="Guardar Cuenta", font=("Arial", 10, "bold"),
                  bg="#28A745", fg="white", relief="flat", cursor="hand2",
                  padx=20, pady=6, command=self._finanzas_guardar_cuenta).pack(side="left", padx=8)

        tk.Button(frame_btns, text="Limpiar", font=("Arial", 10, "bold"),
                  bg="#6C757D", fg="white", relief="flat", cursor="hand2",
                  padx=20, pady=6, command=self._finanzas_limpiar_form_cuenta).pack(side="left", padx=8)

        tk.Button(frame_btns, text="Eliminar Seleccionada", font=("Arial", 10, "bold"),
                  bg="#DC3545", fg="white", relief="flat", cursor="hand2",
                  padx=20, pady=6, command=self._finanzas_eliminar_cuenta).pack(side="left", padx=8)

        tk.Label(self.frame_finanzas_der, text="Cuentas registradas",
                 font=("Arial", 11, "bold"), bg=self.COLOR_FONDO,
                 fg=self.COLOR_AZUL).pack(anchor="w", padx=20)

        frame_tabla = tk.Frame(self.frame_finanzas_der, bg=self.COLOR_FONDO)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(4, 10))

        sb = ttk.Scrollbar(frame_tabla)
        sb.pack(side="right", fill="y")

        cols = ("ID", "Nombre", "Tipo", "Corriente", "Estado financiero", "Valor (Q)")
        self._tabla_cuentas = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                                           yscrollcommand=sb.set, height=8)
        sb.config(command=self._tabla_cuentas.yview)

        anchos = [0, 200, 80, 100, 150, 100]
        for col, w in zip(cols, anchos):
            self._tabla_cuentas.heading(col, text=col)
            self._tabla_cuentas.column(col, width=w)
        self._tabla_cuentas.column("ID", width=0, stretch=False)
        self._tabla_cuentas.pack(fill="both", expand=True)

        self._finanzas_cargar_tabla_cuentas()

    def _finanzas_on_estado_change(self, event=None):
        estado = self._lb_estado_financiero.get()
        self._finanzas_render_columna_der(estado)

    def _finanzas_render_columna_der(self, estado):
        for w in self._frame_der_dinamico.winfo_children():
            w.destroy()

        if estado == "Balance general":
            tk.Label(self._frame_der_dinamico, text="Tipo:", font=("Arial", 9, "bold"),
                     bg=self.COLOR_FONDO).pack(anchor="w")
            self._lb_tipo = ttk.Combobox(self._frame_der_dinamico, font=("Arial", 10), width=18,
                                         values=["Activo", "Pasivo"], state="readonly")
            self._lb_tipo.current(0)
            self._lb_tipo.pack(anchor="w", pady=(4, 10))

            tk.Label(self._frame_der_dinamico, text="Clasificación:", font=("Arial", 9, "bold"),
                     bg=self.COLOR_FONDO).pack(anchor="w")
            self._lb_corriente = ttk.Combobox(self._frame_der_dinamico, font=("Arial", 10), width=18,
                                              values=["Corriente", "No corriente"], state="readonly")
            self._lb_corriente.current(0)
            self._lb_corriente.pack(anchor="w", pady=(4, 10))

        else:
            tk.Label(self._frame_der_dinamico, text="Tipo:", font=("Arial", 9, "bold"),
                     bg=self.COLOR_FONDO).pack(anchor="w")
            self._lb_tipo = ttk.Combobox(self._frame_der_dinamico, font=("Arial", 10), width=18,
                                         values=["Gasto", "Ingreso"], state="readonly")
            self._lb_tipo.current(0)
            self._lb_tipo.pack(anchor="w", pady=(4, 10))

            self._lb_corriente = ttk.Combobox(self._frame_der_dinamico, values=["N/A"], state="readonly")
            self._lb_corriente.current(0)
            self._lb_corriente.pack_forget()

        frame_valor = tk.Frame(self._frame_der_dinamico, bg=self.COLOR_FONDO)
        frame_valor.pack(anchor="w", pady=(6, 0))

        tk.Label(frame_valor, text="Valor de la cuenta:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO).pack(side="left", padx=(0, 6))
        tk.Label(frame_valor, text="Q.", font=("Arial", 10, "bold"),
                 bg=self.COLOR_FONDO, fg=self.COLOR_AZUL).pack(side="left")

        valor_prev = "0.00"
        if hasattr(self, "_entry_cuenta_valor"):
            try:
                valor_prev = self._entry_cuenta_valor.get().strip() or "0.00"
            except Exception:
                valor_prev = "0.00"

        self._entry_cuenta_valor = tk.Entry(frame_valor, font=("Arial", 11), width=18)
        self._entry_cuenta_valor.pack(side="left", ipady=4)
        self._entry_cuenta_valor.insert(0, valor_prev)

    def _finanzas_guardar_cuenta(self):
        nombre = self._entry_cuenta_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre de la cuenta.")
            return

        estado_financiero = self._lb_estado_financiero.get()
        tipo = self._lb_tipo.get()
        corriente = self._lb_corriente.get() if estado_financiero == "Balance general" else "N/A"

        if not estado_financiero or not tipo:
            messagebox.showerror("Error", "Seleccione el estado financiero y el tipo de cuenta.")
            return

        try:
            valor = float(self._entry_cuenta_valor.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El valor debe ser un número válido.")
            return

        if CuentasDB.agregar(nombre, tipo, corriente, estado_financiero, valor):
            self._finanzas_limpiar_form_cuenta()
            self._finanzas_cargar_tabla_cuentas()
            messagebox.showinfo("Éxito", f"Cuenta '{nombre}' guardada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo guardar la cuenta.")

    def _finanzas_limpiar_form_cuenta(self):
        self._entry_cuenta_nombre.delete(0, "end")
        self._entry_cuenta_valor.delete(0, "end")
        self._entry_cuenta_valor.insert(0, "0.00")
        self._lb_estado_financiero.current(0)
        self._finanzas_render_columna_der("Balance general")

    def _finanzas_cargar_tabla_cuentas(self):
        if not hasattr(self, '_tabla_cuentas'):
            return
        for item in self._tabla_cuentas.get_children():
            self._tabla_cuentas.delete(item)
        for c in CuentasDB.obtener_todas():
            self._tabla_cuentas.insert("", "end", values=(
                c["id"], c["nombre"], c["tipo"], c["corriente"], c["estado_financiero"], f"{c['valor']:.2f}"
            ))

    def _finanzas_eliminar_cuenta(self):
        if not hasattr(self, '_tabla_cuentas'):
            return
        sel = self._tabla_cuentas.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta para eliminar.")
            return
        vals = self._tabla_cuentas.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"¿Eliminar la cuenta '{vals[1]}'?"):
            if CuentasDB.eliminar(vals[0]):
                self._finanzas_cargar_tabla_cuentas()
                messagebox.showinfo("Éxito", "Cuenta eliminada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cuenta.")

    def _finanzas_balance_general(self):
        self._finanzas_limpiar_der()

        COLOR = self.COLOR_FONDO
        AZUL  = self.COLOR_AZUL

        tk.Label(self.frame_finanzas_der, text="Balance de Situación General",
                 font=("Arial", 13, "bold"), bg=COLOR, fg=AZUL).pack(pady=(14, 0))
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        tk.Label(self.frame_finanzas_der, text=f"fecha: {fecha_hoy}",
                 font=("Arial", 10, "italic"), bg=COLOR).pack(pady=(0, 8))

        frame_wrap = tk.Frame(self.frame_finanzas_der, bg=COLOR)
        frame_wrap.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(frame_wrap, bg=COLOR, highlightthickness=0)
        sb = ttk.Scrollbar(frame_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame_rpt = tk.Frame(canvas, bg=COLOR)
        win_id = canvas.create_window((0, 0), window=frame_rpt, anchor="nw")

        def _on_resize(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _on_resize)
        frame_rpt.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        cuentas = CuentasDB.obtener_todas()
        bg = COLOR

        COL_SUBTOTAL = "#E8F0FB"
        COL_TOTAL    = "#D0E4FF"

        def fila(parent, nombre, valor_izq=None, valor_der=None,
                 bold=False, underline=False, bg_color=None, indent=0):
            f = tk.Frame(parent, bg=bg_color or bg)
            f.pack(fill="x", pady=0)
            style = "bold" if bold else ""
            font_n = ("Arial", 9, style) if not underline else ("Arial", 9, "bold underline")
            pad_left = 8 + indent * 20
            tk.Label(f, text=nombre, font=font_n, bg=bg_color or bg,
                     anchor="w").place(x=pad_left, y=2)
            if valor_izq is not None:
                tk.Label(f, text=f"Q  {valor_izq:,.2f}", font=("Arial", 9), bg=bg_color or bg,
                         anchor="e").place(relx=0.70, y=2, anchor="ne")
            if valor_der is not None:
                tk.Label(f, text=f"Q  {valor_der:,.2f}", font=("Arial", 9, "bold"), bg=bg_color or bg,
                         anchor="e").place(relx=0.99, y=2, anchor="ne")
            tk.Frame(f, bg=bg_color or bg, height=20).pack()

        def separador(parent):
            tk.Frame(parent, bg="#AAAAAA", height=1).pack(fill="x", padx=4, pady=1)

        tk.Label(frame_rpt, text="ACTIVO", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))

        activos = [c for c in cuentas if c["tipo"] == "Activo"]
        corrientes_a  = [c for c in activos if c["corriente"] == "Corriente"]
        no_corr_a     = [c for c in activos if c["corriente"] == "No corriente"]

        suma_corr_a = sum(c["valor"] for c in corrientes_a)
        suma_no_corr_a = sum(c["valor"] for c in no_corr_a)
        suma_activo = suma_corr_a + suma_no_corr_a

        fila(frame_rpt, "Corriente", bold=True, underline=True)
        for c in corrientes_a:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "", valor_der=suma_corr_a, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        fila(frame_rpt, "No Corriente", bold=True, underline=True)
        for c in no_corr_a:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "", valor_der=suma_no_corr_a, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        fila(frame_rpt, "Suma del Activo", valor_der=suma_activo, bold=True, bg_color=COL_TOTAL)
        separador(frame_rpt)

        tk.Label(frame_rpt, text="PATRIMONIO NETO Y PASIVO",
                 font=("Arial", 10, "bold underline"), bg=bg).pack(anchor="center", pady=(8, 2))
        tk.Label(frame_rpt, text="PASIVO", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(0, 2))

        pasivos = [c for c in cuentas if c["tipo"] == "Pasivo"]
        corrientes_p  = [c for c in pasivos if c["corriente"] == "Corriente"]
        no_corr_p     = [c for c in pasivos if c["corriente"] == "No corriente"]

        suma_corr_p   = sum(c["valor"] for c in corrientes_p)
        suma_no_corr_p = sum(c["valor"] for c in no_corr_p)
        suma_pasivo   = suma_corr_p + suma_no_corr_p

        fila(frame_rpt, "Corriente", bold=True, underline=True)
        for c in corrientes_p:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "", valor_der=suma_corr_p, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        fila(frame_rpt, "No Corriente", bold=True, underline=True)
        for c in no_corr_p:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "", valor_der=suma_no_corr_p, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        patrimonio = suma_activo - suma_pasivo
        tk.Label(frame_rpt, text="PATRIMONIO NETO", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))
        fila(frame_rpt, "Capital", valor_der=patrimonio, indent=1)
        separador(frame_rpt)

        suma_pasivo_patrimonio = suma_pasivo + patrimonio
        fila(frame_rpt, "Suma del Pasivo y Patrimonio Neto",
             valor_der=suma_pasivo_patrimonio, bold=True, bg_color=COL_TOTAL)

    def _finanzas_estado_resultados(self):
        self._finanzas_limpiar_der()

        COLOR = self.COLOR_FONDO
        AZUL  = self.COLOR_AZUL

        tk.Label(self.frame_finanzas_der, text="Estado de Resultados",
                 font=("Arial", 13, "bold"), bg=COLOR, fg=AZUL).pack(pady=(14, 8))

        frame_wrap = tk.Frame(self.frame_finanzas_der, bg=COLOR)
        frame_wrap.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(frame_wrap, bg=COLOR, highlightthickness=0)
        sb = ttk.Scrollbar(frame_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame_rpt = tk.Frame(canvas, bg=COLOR)
        win_id = canvas.create_window((0, 0), window=frame_rpt, anchor="nw")

        def _on_resize(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _on_resize)
        frame_rpt.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        bg = COLOR
        COL_SUBTOTAL = "#E8F0FB"
        COL_TOTAL    = "#D0E4FF"
        COL_NEG      = "#FDE8E8"

        def fila(parent, nombre, valor_izq=None, valor_der=None,
                 bold=False, underline=False, bg_color=None, indent=0):
            f = tk.Frame(parent, bg=bg_color or bg)
            f.pack(fill="x", pady=0)
            style = "bold" if bold else ""
            font_n = ("Arial", 9, style) if not underline else ("Arial", 9, "bold underline")
            pad_left = 8 + indent * 20
            tk.Label(f, text=nombre, font=font_n, bg=bg_color or bg,
                     anchor="w").place(x=pad_left, y=2)
            if valor_izq is not None:
                tk.Label(f, text=f"Q  {valor_izq:,.2f}", font=("Arial", 9), bg=bg_color or bg,
                         anchor="e").place(relx=0.70, y=2, anchor="ne")
            if valor_der is not None:
                tk.Label(f, text=f"Q  {valor_der:,.2f}", font=("Arial", 9, "bold"), bg=bg_color or bg,
                         anchor="e").place(relx=0.99, y=2, anchor="ne")
            tk.Frame(f, bg=bg_color or bg, height=20).pack()

        def separador(parent):
            tk.Frame(parent, bg="#AAAAAA", height=1).pack(fill="x", padx=4, pady=1)

        cuentas = CuentasDB.obtener_todas()
        er = [c for c in cuentas if c["estado_financiero"] == "Estado de resultados"]
        gastos   = [c for c in er if c["tipo"] == "Gasto"]
        ingresos_er = [c for c in er if c["tipo"] == "Ingreso"]

        tk.Label(frame_rpt, text="Ingresos", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))

        ventas          = 900000.00
        devoluciones    = 3914.00
        utilidad_neta   = ventas - devoluciones

        fila(frame_rpt, "Ventas",                                valor_der=ventas)
        fila(frame_rpt, "(-) Devoluciones y Rebajas sobre Ventas", valor_der=devoluciones)
        fila(frame_rpt, "Utilidad Neta",                         valor_der=utilidad_neta, bold=True, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        tk.Label(frame_rpt, text="Gastos", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))

        suma_gastos = sum(c["valor"] for c in gastos)
        for c in gastos:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "Total de Gastos", valor_der=suma_gastos, bold=True, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        resultado_operacion = utilidad_neta - suma_gastos
        fila(frame_rpt, "Resultado de Operación", valor_der=resultado_operacion, bold=True, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        tk.Label(frame_rpt, text="Otros Ingresos", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))

        suma_otros_ing = sum(c["valor"] for c in ingresos_er)
        for c in ingresos_er:
            fila(frame_rpt, c["nombre"], valor_izq=c["valor"], indent=1)
        fila(frame_rpt, "", valor_der=suma_otros_ing, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        diferencia_positiva = resultado_operacion + suma_otros_ing
        fila(frame_rpt, "Diferencia Positiva", valor_der=diferencia_positiva, bold=True, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        tk.Label(frame_rpt, text="Otros Gastos", font=("Arial", 10, "bold underline"),
                 bg=bg).pack(anchor="center", pady=(6, 2))

        otros_gastos = 0.0
        fila(frame_rpt, "", valor_der=otros_gastos, bg_color=COL_SUBTOTAL)
        separador(frame_rpt)

        ganancia_antes = diferencia_positiva - otros_gastos
        isr = ganancia_antes * 0.25
        ganancia_despues = ganancia_antes - isr

        fila(frame_rpt, "Ganancia Antes del Impuesto",            valor_der=ganancia_antes,   bold=True, bg_color=COL_SUBTOTAL)
        fila(frame_rpt, "(-) ISR por Pagar (25% sobre ganancia)", valor_der=isr,              bg_color=COL_NEG)
        fila(frame_rpt, "Ganancia Después del Impuesto y Reserva",valor_der=ganancia_despues, bold=True, bg_color=COL_TOTAL)


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

        tk.Label(self.ventana, text="Nueva Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#0055A5").pack(
            pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)
        tk.Label(frame_form, text="Nombre:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.entry_nombre.pack(side="left", padx=5)
        self.entry_nombre.focus()
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar", font=("Arial", 10, "bold"), bg="#0055A5", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

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

        tk.Label(self.ventana, text="Eliminar Categoría", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#0055A5").pack(
            pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5)
        tk.Label(frame_form, text="Seleccione:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        categorias = CategoriasDB.obtener_todas()
        self.combo_categorias = ttk.Combobox(frame_form, values=categorias, state="readonly", width=27)
        self.combo_categorias.pack(side="left", padx=5)
        if categorias: self.combo_categorias.current(0)
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Eliminar", font=("Arial", 10, "bold"), bg="#DC3545", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.eliminar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=5, command=self.ventana.destroy).pack(side="left", padx=10)

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

        tk.Label(self.ventana, text="Agregar Nuevo Producto", font=("Arial", 16, "bold"), bg="#FFFFFF",
                 fg="#0055A5").pack(pady=15)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)
        frame_form.columnconfigure(1, weight=1)

        labels = ["Código:", "Nombre:", "Categoría:", "Cantidad:", "Precio Compra:", "Precio Venta:", "Proveedor:"]
        self.widgets = {}

        for i, label in enumerate(labels):
            tk.Label(frame_form, text=label, font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="e",
                                                                                            pady=5, padx=5)
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
        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg="#0055A5", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

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
        if not all([vals["Código:"], vals["Nombre:"], vals["Cantidad:"], vals["Precio Compra:"], vals["Precio Venta:"],
                    prov]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            if ProductosDB.agregar(vals["Nombre:"], vals["Código:"], float(vals["Precio Compra:"]),
                                   float(vals["Precio Venta:"]), cat, float(vals["Cantidad:"]), prov):
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

        tk.Label(self.ventana, text="Editar Producto", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#0055A5").pack(
            pady=15)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=20, pady=5, fill="both", expand=True)
        frame_form.columnconfigure(1, weight=1)

        self.widgets = {}
        campos = [("ID:", item["id_num"]), ("Código:", item["codigo"]), ("Nombre:", item["nombre"]),
                  ("Cantidad:", item["cantidad"]), ("Precio Compra:", item["precio_compra"]),
                  ("Precio Venta:", item["precio_venta"])]

        for i, (label, val) in enumerate(campos):
            tk.Label(frame_form, text=label, font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="e",
                                                                                            pady=5, padx=5)
            entry = tk.Entry(frame_form, font=("Arial", 10))
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            entry.insert(0, val)
            if label == "ID:": entry.config(state="disabled")
            self.widgets[label] = entry

        tk.Label(frame_form, text="Categoría:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=6, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        self.combo_categoria = ttk.Combobox(frame_form, values=CategoriasDB.obtener_todas())
        self.combo_categoria.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        self.combo_categoria.set(item["categoria"])

        tk.Label(frame_form, text="Proveedor:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=7, column=0,
                                                                                               sticky="e", pady=5,
                                                                                               padx=5)
        self.combo_proveedor = ttk.Combobox(frame_form, values=ProveedoresDB.obtener_nombres())
        self.combo_proveedor.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        self.combo_proveedor.set(item["proveedor"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg="#0055A5", fg="white",
                  relief="flat", cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho, alto = 550, 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def guardar(self):
        vals = {k: v.get().strip() for k, v in self.widgets.items()}
        try:
            if ProductosDB.actualizar(self.item_original["id_num"], vals["Nombre:"], vals["Código:"],
                                      float(vals["Precio Compra:"]), float(vals["Precio Venta:"]),
                                      self.combo_categoria.get(), float(vals["Cantidad:"]), self.combo_proveedor.get()):
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

        tk.Label(self.ventana, text="Agregar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#0055A5").pack(
            pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        self.widgets = {}
        for i, label in enumerate(["Nombre:", "Código:", "Teléfono:", "Encargado:"]):
            tk.Label(frame_form, text=label, font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="w",
                                                                                            pady=10)
            entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.widgets[label] = entry

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                                 sticky="nw", pady=10)
        self.text_info = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_info.grid(row=4, column=1, pady=10, padx=10)
        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar", font=("Arial", 11, "bold"), bg="#0055A5", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

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
        if ProveedoresDB.agregar(vals["Nombre:"], vals["Código:"], vals["Teléfono:"], vals["Encargado:"],
                                 self.text_info.get("1.0", "end-1c").strip()):
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

        tk.Label(self.ventana, text="Editar Proveedor", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#0055A5").pack(
            pady=20)
        frame_form = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_form.pack(padx=40, pady=10, fill="both", expand=True)

        self.widgets = {}
        campos = [("Nombre:", proveedor["nombre"]), ("Código:", proveedor["codigo"]),
                  ("Teléfono:", proveedor["telefono"]), ("Encargado:", proveedor["encargado"])]

        for i, (label, val) in enumerate(campos):
            tk.Label(frame_form, text=label, font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=i, column=0, sticky="w",
                                                                                            pady=10)
            entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
            entry.grid(row=i, column=1, pady=10, padx=10)
            entry.insert(0, val)
            if label == "Código:": entry.config(state="readonly")
            self.widgets[label] = entry

        tk.Label(frame_form, text="Información:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,
                                                                                                 sticky="nw", pady=10)
        self.text_info = tk.Text(frame_form, font=("Arial", 11), width=30, height=5)
        self.text_info.grid(row=4, column=1, pady=10, padx=10)
        self.text_info.insert("1.0", proveedor["informacion"])

        frame_botones = tk.Frame(self.ventana, bg="#FFFFFF")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 11, "bold"), bg="#0055A5", fg="white",
                  relief="flat", cursor="hand2", padx=30, pady=8, command=self.guardar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 11, "bold"), bg="#6C757D", fg="white", relief="flat",
                  cursor="hand2", padx=30, pady=8, command=self.ventana.destroy).pack(side="left", padx=10)

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
        if ProveedoresDB.actualizar(self.proveedor_original["id_num"], vals["Nombre:"],
                                    self.proveedor_original["codigo"], vals["Teléfono:"], vals["Encargado:"],
                                    self.text_info.get("1.0", "end-1c").strip()):
            self.sistema.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor actualizado")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()

