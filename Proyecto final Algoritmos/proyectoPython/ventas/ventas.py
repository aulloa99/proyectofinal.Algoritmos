import psycopg2


class Ventas:
    def __init__(self, config):
        self.config = config
        self.cnx = psycopg2.connect(**config)
        self.cursor = self.cnx.cursor()

    def listar(self):
        try:
            self.cursor.execute("SELECT * FROM ventas")
            ventas = self.cursor.fetchall()
            for venta in ventas:
                print(
                    "Codigo de Producto: {}, Codigo de Cliente: {}, Cantidad: {}, Total de Venta: {}".format(
                        venta[1], venta[2], venta[3], venta[4]
                    )
                )
        except psycopg2.Error as err:
            print("Error: {}".format(err))

    def crear(self, codigo_producto, codigo_cliente, cantidad, total_venta):
        try:
            self.cursor.execute(
                "SELECT existencia FROM public.inventario WHERE codigo = %s",
                (codigo_producto,),
            )
            existencia = self.cursor.fetchone()
            if existencia is None:
                print("El producto no existe en el inventario.")
            elif existencia[0] < cantidad:
                print("No hay suficientes existencias para realizar la venta.")
            else:
                # Realiza la venta
                self.cursor.execute(
                    "INSERT INTO public.ventas (codigo_producto, codigo_cliente, cantidad, total_venta) "
                    "VALUES (%s, %s, %s, %s)",
                    (codigo_producto, codigo_cliente, cantidad, total_venta),
                )
                self.cursor.connection.commit()
                print("Venta creada con exito.")

                # Actualiza las existencias en el inventario restando la cantidad vendida
                self.cursor.execute(
                    "UPDATE public.inventario SET existencia = existencia - %s WHERE codigo = %s",
                    (cantidad, codigo_producto),
                )
                self.cursor.connection.commit()
                print("Existencias actualizadas en el inventario.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def anular(self, codigo_venta):
        try:
            # Consulta la cantidad de productos vendidos en la venta a anular
            self.cursor.execute(
                "SELECT codigo_producto, cantidad FROM ventas WHERE codigo_venta = %s",
                (codigo_venta,),
            )
            venta = self.cursor.fetchone()

            if venta is None:
                print("La venta no existe.")
            else:
                codigo_producto, cantidad = venta
                # Anula la venta eliminando el registro de la venta
                self.cursor.execute(
                    "DELETE FROM ventas WHERE codigo_venta = %s", (codigo_venta,)
                )
                self.cursor.connection.commit()
                print("Venta anulada con exito.")

                # Actualiza las existencias en el inventario sumando la cantidad anulada
                self.cursor.execute(
                    "UPDATE inventario SET existencia = existencia + %s WHERE codigo = %s",
                    (cantidad, codigo_producto),
                )
                self.cursor.connection.commit()
                print("Existencias actualizadas en el inventario.")
        except psycopg2.Error as err:
            print("Error: {err}")

    def cerrar_conexion(self):
        self.cursor.close()
        self.cnx.close()
