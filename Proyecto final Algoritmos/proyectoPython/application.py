import psycopg2
import sys
from inventario.inventario import Inventario
from ventas.ventas import Ventas
from clientes.clientes import Clientes
from reportes.reportes import Reportes

config = {
    "user": "postgres",
    "password": "pwd2023",
    "host": "localhost",
    "dbname": "ventas",
}

if len(sys.argv) < 2:
    print(
        "Uso: python3 application.py [--inventario | --clientes | --ventas] <comando> [...]"
    )
else:
    try:
        if sys.argv[1] == "--inventario":
            inventario = Inventario(config)
            subcomando = sys.argv[2]
            if subcomando == "listar":
                inventario.listar()
            elif subcomando == "crear":
                codigo, nombre, existencia, proveedor, precio = (
                    sys.argv[3],
                    sys.argv[4],
                    int(sys.argv[5]),
                    sys.argv[6],
                    float(sys.argv[7]),
                )
                inventario.crear(codigo, nombre, existencia, proveedor, precio)
            elif subcomando == "actualizar":
                codigo, nombre, existencia, proveedor, precio = (
                    sys.argv[3],
                    sys.argv[4],
                    int(sys.argv[5]),
                    sys.argv[6],
                    float(sys.argv[7]),
                )
                inventario.actualizar(codigo, nombre, existencia, proveedor, precio)
            elif subcomando == "editar_existencias":
                codigo, nueva_existencia = sys.argv[3], int(sys.argv[4])
                inventario.editar_existencias(codigo, nueva_existencia)
            elif subcomando == "eliminar":
                codigo = sys.argv[3]
                inventario.eliminar(codigo)
            else:
                print("Comando no valido para inventario.")
            inventario.cerrar_conexion()

        elif sys.argv[1] == "--clientes":
            clientes = Clientes(config)

            subcomando = sys.argv[2]
            if subcomando == "listar":
                clientes.listar()
            elif subcomando == "crear":
                codigo, nombre, direccion = sys.argv[3], sys.argv[4], sys.argv[5]
                clientes.crear(codigo, nombre, direccion)
            elif subcomando == "editar":
                codigo, nombre, direccion = sys.argv[3], sys.argv[4], sys.argv[5]
                clientes.editar(codigo, nombre, direccion)
            elif subcomando == "eliminar":
                codigo = sys.argv[3]
                clientes.eliminar(codigo)

            clientes.cerrar_conexion()
        elif sys.argv[1] == "--ventas":
            ventas = Ventas(config)

            subcomando = sys.argv[2]
            if subcomando == "listar":
                ventas.listar()
            elif subcomando == "crear":
                codigo_producto, codigo_cliente, cantidad, total_venta = (
                    sys.argv[3],
                    sys.argv[4],
                    int(sys.argv[5]),
                    float(sys.argv[6]),
                )
                ventas.crear(codigo_producto, codigo_cliente, cantidad, total_venta)
            elif subcomando == "anular":
                id_venta = sys.argv[3]
                ventas.anular(id_venta)

            ventas.cerrar_conexion()
        elif sys.argv[1] == "--reportes":
            reportes = Reportes(config)

            subcomando = sys.argv[2]
            if subcomando == "ventas_por_cliente":
                reportes.ventas_por_cliente()
            elif subcomando == "ventas_por_producto":
                reportes.ventas_por_producto()
            else:
                print("Comando no valido para reportes.")

            reportes.cerrar_conexion()

        else:
            print("Comando no valido.")
    except psycopg2.Error as err:
        print("Error de conexion: {err}")
