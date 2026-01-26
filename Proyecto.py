import sqlite3

class Proveedores:
    def __init__(self, nombre, codigo, telefono, informacion):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__telefono = telefono
        self.__informacion = informacion

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, new_nombre):
        if new_nombre:
            self.__nombre = new_nombre
        else:
            print("El campo no puede estar vacio")

    @property
    def codigo(self):
        return self.__codigo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, new_telefono):
        if new_telefono:
            self.__telefono = new_telefono
        else:
            print("El campo no puede estar vacio")

    @property
    def informacion(self):
        return self.__informacion

    @informacion.setter
    def informacion(self, new_informacion):
        if new_informacion:
            self.__informacion = new_informacion
        else:
            print("El campo no puede estar vacio")

class Productos:
    def __init__(self, nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__precio_compra = precio_compra
        self.__precio_venta = precio_venta
        self.__categoria = categoria
        self.__cantidad = cantidad
        self.__proveedor = proveedor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, new_nombre):
        if new_nombre:
            self.__nombre = new_nombre
        else:
            print("El campo no puede estar vacio")

    @property
    def codigo(self):
        return self.__codigo

    @property
    def precio_compra(self):
        return self.__precio_compra

    @precio_compra.setter
    def precio_compra(self, new_precio_compra):
        if new_precio_compra:
            self.__precio_compra = new_precio_compra
        else:
            print("El campo no puede estar vacio")

    @property
    def precio_venta(self):
        return self.__precio_venta

    @precio_venta.setter
    def precio_venta(self, new_precio_venta):
        if new_precio_venta:
            self.__precio_venta = new_precio_venta
        else:
            print("El campo no puede estar vacio")

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, new_categoria):
        if new_categoria:
            self.__categoria = new_categoria
        else:
            print("El campo no puede estar vacio")

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, new_cantidad):
        if new_cantidad:
            self.__cantidad = new_cantidad
        else:
            print("El campo no puede estar vacio")

    @property
    def proveedor(self):
        return self.__proveedor

    @proveedor.setter
    def proveedor(self, new_proveedor):
        if new_proveedor:
            self.__proveedor = new_proveedor
        else:
            print("El campo no puede estar vacio")

class TablasDB:
    DB_NAME = "proveedores.db"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(TablasDB.DB_NAME)
        conn.row_factory = sqlite3.Row

        # 1. Tabla de proveedores
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS proveedores (
                            id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            codigo TEXT UNIQUE NOT NULL,  
                            telefono TEXT NOT NULL,
                            informacion TEXT              
                        );
                    """)

        #2. Tabla de productos
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

        conn.commit()
        return conn


class AgregarProveedor:
    def agregar_proveedor(self, proveedor):
        if not isinstance(proveedor, Proveedores):
            print("Error: El objeto no es un proveedor válido.")
            return False
        conn = TablasDB._conn()
        try:
            query = """
                INSERT INTO proveedores (nombre, codigo, telefono, informacion)
                VALUES (?, ?, ?, ?)
            """
            datos = (proveedor.nombre,proveedor.codigo,proveedor.telefono,proveedor.informacion)
            conn.execute(query, datos)
            conn.commit()
            print(f"Proveedor '{proveedor.nombre}' guardado exitosamente.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: El código '{proveedor.codigo}' ya existe en la base de datos.")
            return False
        except Exception as e:
            print(f"Ocurrió un error al guardar: {e}")
            return False
        finally:
            conn.close()

class ModificarProveedor:
    def modificar_proveedor(self, proveedor):
        if not isinstance(proveedor, Proveedores):
            print("Error: El objeto no es un proveedor válido.")
            return False
        conn = TablasDB._conn()
        try:
            query = """UPDATE proveedores
                SET nombre = ?, telefono = ?, informacion = ?
                WHERE codigo = ?
            """
            datos = (proveedor.nombre, proveedor.telefono, proveedor.informacion,proveedor.codigo)
            cursor = conn.execute(query, datos)
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Proveedor con código '{proveedor.codigo}' modificado exitosamente.")
                return True
            else:
                print(f"No se encontró ningún proveedor con el código '{proveedor.codigo}'.")
                return False
        except Exception as e:
            print(f"Error al modificar: {e}")
            return False
        finally:
            conn.close()


class EliminarProveedor:
    def eliminar_proveedor(self, codigo_proveedor):
        conn = TablasDB._conn()
        try:
            codigo_a_borrar = codigo_proveedor
            if isinstance(codigo_proveedor, Proveedores):
                codigo_a_borrar = codigo_proveedor.codigo
            query = "DELETE FROM proveedores WHERE codigo = ?"
            cursor = conn.execute(query, (codigo_a_borrar,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"ÉXITO: Proveedor con código '{codigo_a_borrar}' eliminado.")
                return True
            else:
                print(f"ADVERTENCIA: No se encontró ningún proveedor con el código '{codigo_a_borrar}'.")
                return False
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            conn.close()

class AgregarProducto:
    def agregar_producto(self, producto):
        if not isinstance(producto, Productos):
            print("Error: El objeto no es un producto válido.")
            return False
        conn = TablasDB._conn()
        try:
            query = """
                INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, categoria, cantidad, proveedor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            datos = (producto.nombre,producto.codigo,producto.precio_compra,producto.precio_venta,producto.categoria,producto.cantidad, producto.proveedor)
            conn.execute(query, datos)
            conn.commit()
            print(f"Producto '{producto.nombre}' guardado exitosamente.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: El código '{producto.codigo}' ya existe en la base de datos.")
            return False
        except Exception as e:
            print(f"Ocurrió un error al guardar el producto: {e}")
            return False
        finally:
            conn.close()


class ModificarProducto:
    def modificar_producto(self, producto):
        if not isinstance(producto, Productos):
            print("Error: El objeto no es un producto válido.")
            return False
        dato_proveedor = producto.proveedor
        if isinstance(dato_proveedor, Proveedores):
            dato_proveedor = dato_proveedor.nombre
        conn = TablasDB._conn()
        try:
            query = """
                UPDATE productos
                SET nombre = ?, precio_compra = ?, precio_venta = ?, categoria = ?, cantidad = ?, proveedor = ?
                WHERE codigo = ?
            """
            datos = (producto.nombre, producto.precio_compra, producto.precio_venta, producto.categoria, producto.cantidad, dato_proveedor, producto.codigo)
            cursor = conn.execute(query, datos)
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Producto con código '{producto.codigo}' modificado exitosamente.")
                return True
            else:
                print(f"No se encontró ningún producto con el código '{producto.codigo}'.")
                return False
        except Exception as e:
            print(f"Error al modificar producto: {e}")
            return False
        finally:
            conn.close()


class EliminarProducto:
    def eliminar_producto(self, codigo_producto):
        conn = TablasDB._conn()
        try:
            codigo_a_borrar = codigo_producto
            if isinstance(codigo_producto, Productos):
                codigo_a_borrar = codigo_producto.codigo
            query = "DELETE FROM productos WHERE codigo = ?"
            cursor = conn.execute(query, (codigo_a_borrar,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"ÉXITO: Producto con código '{codigo_a_borrar}' eliminado.")
                return True
            else:
                print(f"ADVERTENCIA: No se encontró producto con código '{codigo_a_borrar}'.")
                return False
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            conn.close()