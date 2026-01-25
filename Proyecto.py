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

class ProveedooresDB:
    DB_NAME = "proveedores.db"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(ProveedooresDB.DB_NAME)
        conn.row_factory = sqlite3.Row

        # 1. Tabla de proveedores
        conn.execute("""
                    CREATE TABLE IF NOT EXISTS proveedores (
                        id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        tipo_producto TEXT NOT NULL,
                        informacion REAL
                    );
                """)