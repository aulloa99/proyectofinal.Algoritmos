import psycopg2


class Clientes:
    def __init__(self, config):
        self.config = config
        self.cnx = psycopg2.connect(**config)
        self.cursor = self.cnx.cursor()

    def listar(self):
        try:
            self.cursor.execute("SELECT * FROM clientes")
            clientes = self.cursor.fetchall()
            for cliente in clientes:
                print(
                    "Codigo: {}, Nombre: {}, Direccion: {}".format(
                        cliente[1], cliente[2], cliente[3]
                    )
                )
        except psycopg2.Error as err:
            print("Error: {}".format(err))

    def crear(self, codigo, nombre, direccion):
        try:
            self.cursor.execute(
                "INSERT INTO clientes (codigo, nombre, direccion) VALUES (%s, %s, %s)",
                (codigo, nombre, direccion),
            )
            self.cursor.connection.commit()
            print("Cliente creado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def editar(self, codigo, nombre, direccion):
        try:
            self.cursor.execute(
                "UPDATE clientes SET nombre = %s, direccion = %s WHERE codigo = %s",
                (nombre, direccion, codigo),
            )
            self.cursor.connection.commit()
            print("Cliente actualizado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def eliminar(self, codigo):
        try:
            self.cursor.execute(
                "DELETE FROM clientes WHERE codigo = %s", (codigo,)
            )
            self.cursor.connection.commit()
            print("Cliente eliminado con exito.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def cerrar_conexion(self):
        self.cursor.close()
        self.cnx.close()
