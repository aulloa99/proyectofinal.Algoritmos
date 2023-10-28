import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Reportes:
    def __init__(self, config):
        self.config = config
        self.cnx = psycopg2.connect(**config)
        self.cursor = self.cnx.cursor()
        # self.smtp_config = smtp_config

    def ventas_por_cliente(self):
        try:
            self.cursor.execute(
                "SELECT codigo_cliente, SUM(total_venta) FROM ventas GROUP BY codigo_cliente"
            )
            ventas_por_cliente = self.cursor.fetchall()

            # Genera un archivo PDF con los resultados
            self.generar_pdf(
                "reporte_ventas_cliente.pdf", ventas_por_cliente, "Ventas por Cliente"
            )

        except psycopg2.Error as err:
            print("Error: {}".format(err))

    def ventas_por_producto(self):
        try:
            self.cursor.execute(
                "SELECT codigo_producto, SUM(cantidad) FROM ventas GROUP BY codigo_producto"
            )
            ventas_por_producto = self.cursor.fetchall()

            # Genera un archivo PDF con los resultados
            self.generar_pdf(
                "reporte_ventas_producto.pdf",
                ventas_por_producto,
                "Ventas por Producto",
            )

        except psycopg2.Error as err:
            print("Error: {}".format(err))

    def generar_pdf(self, file_name, data, report_type):
        c = canvas.Canvas(file_name, pagesize=letter)
        c.drawString(100, 750, "Reporte de {}".format(report_type))
        y = 700
        for row in data:
            c.drawString(
                100, y, "Item: {}, Cantidad Vendida: {}".format(row[0], row[1])
            )
            y -= 20
        c.save()
        print("Reporte creado correctamente :)")

    def enviar_email(self, subject, message, file_name):
        msg = MIMEMultipart()
        msg["From"] = self.smtp_config["from_email"]
        msg["To"] = self.smtp_config["to_email"]
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        with open(file_name, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header(
                "Content-Disposition", "attachment", filename=str(file_name)
            )
            msg.attach(attach)

        server = smtplib.SMTP(
            self.smtp_config["smtp_server"], self.smtp_config["smtp_port"]
        )
        server.starttls()
        server.login(self.smtp_config["from_email"], self.smtp_config["email_password"])
        server.sendmail(
            self.smtp_config["from_email"],
            self.smtp_config["to_email"],
            msg.as_string(),
        )
        server.quit()

    def cerrar_conexion(self):
        self.cursor.close()
        self.cnx.close()
