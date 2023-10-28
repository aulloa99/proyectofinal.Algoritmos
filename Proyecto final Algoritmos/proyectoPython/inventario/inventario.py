import psycopg2


class Inventario:
    def __init__(self, config):
        self.config = config
        self.cnx = psycopg2.connect(**config)
        self.cursor = self.cnx.cursor()

    def listar(self):
        try:
            self.cursor.execute("SELECT * FROM public.inventario")
            productos = self.cursor.fetchall()
            for producto in productos:
                print(
                    "Producto: {}, Nombre: {}, Existencia: {}, Proveedor: {}, Precio: {}".format(
                        producto[1],
                        producto[2],
                        producto[3],
                        producto[4],
                        producto[5],
                    )
                )
        except psycopg2.Error as err:
            print("Error: {}".format(err))

    def crear(self, codigo, nombre, existencia, proveedor, precio):
        try:
            self.cursor.execute(
                "INSERT INTO inventario (codigo, nombre, existencia, proveedor, precio) "
                "VALUES (%s, %s, %s, %s, %s)",
                (codigo, nombre, existencia, proveedor, precio),
            )
            self.cursor.connection.commit()
            print("Producto creado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def actualizar(self, codigo, nombre, existencia, proveedor, precio):
        try:
            self.cursor.execute(
                "UPDATE inventario "
                "SET nombre = %s, existencia = %s, proveedor = %s, precio = %s "
                "WHERE codigo = %s",
                (nombre, existencia, proveedor, precio, codigo),
            )
            self.cursor.connection.commit()
            print("Producto actualizado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def editar_existencias(self, codigo, nueva_existencia):
        try:
            self.cursor.execute(
                "UPDATE inventario " "SET existencia = %s " "WHERE codigo = %s",
                (nueva_existencia, codigo),
            )
            self.cursor.connection.commit()
            print("Existencias actualizadas con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def eliminar(self, codigo):
        try:
            self.cursor.execute(
                "DELETE FROM inventario " "WHERE codigo = %s", (codigo,)
            )
            self.cursor.connection.commit()
            print("Producto eliminado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def cerrar_conexion(self):
        self.cursor.close()
        self.cnx.close()
