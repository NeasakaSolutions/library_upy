# Importaciones
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPResponseException
from dotenv import load_dotenv
from django.core.paginator import Paginator

# Función para el correo de verificación:
def sendMail(html, asunto, para):

    load_dotenv()

    # Configuración SMTP
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "0"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Validar configuración
    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        raise ValueError("Falta configurar alguna variable SMTP")

    # Cabecera del correo
    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"] = smtp_user
    msg["To"] = para
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(
                smtp_server, smtp_port, timeout=20
            ) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

        else:
            with smtplib.SMTP(
                smtp_server, smtp_port, timeout=20
            ) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

    except (smtplib.SMTPException, OSError, ValueError) as e:
        print(f"Error al enviar correo: {type(e).__name__}: {e}")
        raise


# Dividir la informacion:
def paginar(request, queryset, limite=9):

    page = request.GET.get("page", 1)

    paginator = Paginator(queryset, limite)

    registros = paginator.get_page(page)

    return {
        "data": registros,
        "pagina_actual": registros.number,
        "total_paginas": paginator.num_pages,
        "total_registros": paginator.count,
        "hay_siguiente": registros.has_next(),
        "hay_anterior": registros.has_previous()
    }