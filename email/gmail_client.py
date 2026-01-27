from googleapiclient.discovery import build
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import auth
import os
from email.mime.text import MIMEText

import auth

def get_gmail_service():
    creds = auth.get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service

def decode(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

def is_html(text: str) -> bool:
    soup = BeautifulSoup(text, "html.parser")
    return bool(soup.find())

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Elimina scripts y estilos
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Limpieza básica
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)

def _get_body_from_payload(payload):
    """
    Extrae el cuerpo del email desde el payload de Gmail.
    Prioriza text/plain y si no existe convierte text/html a texto plano.
    """

    # Caso simple
    if payload.get("body", {}).get("data"):
        print("joder")
        return decode(payload["body"]["data"])

    # Caso multipart
    parts = payload.get("parts", [])
    html_body = None

    for part in parts:
        if "parts" in part.keys():
            for p in part.get("parts", []):
                part=p
                break

        mime_type = part.get("mimeType")
        data = part.get("body", {}).get("data")

        if not data:
            continue

        decoded = decode(data)

        if mime_type == "text/plain":
            if(is_html(decoded)):
                return html_to_text(decoded)
            return decoded

        if mime_type == "text/html":
            return html_to_text(decoded)

    return ""

def get_last_emails(max_results=5):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me", maxResults=max_results).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full").execute()

        headers = msg_data["payload"]["headers"]
        header_dict = {h["name"]: h["value"] for h in headers}

        body = _get_body_from_payload(msg_data["payload"])

        email = {
            "id": msg["id"],
            "remitente": header_dict.get("From"),
            "destinatario": header_dict.get("To"),
            "asunto": header_dict.get("Subject"),
            "fecha": header_dict.get("Date"),
            "cuerpo": body,
        }

        emails.append(email)

    return emails

def send_email(destinatario, asunto, cuerpo, ind_ia=True, ind_enviar=True):
    service = get_gmail_service()

    if ind_ia:
        cuerpo += (
            "\n\nDisclaimer: Este email ha sido generado usando Helia, "
            "un chatbot creado por Sistemas Helion.")

    message = MIMEText(cuerpo)
    message["to"] = destinatario
    message["subject"] = asunto

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    if ind_enviar:
        result = service.users().messages().send(
            userId="me", body=body).execute()

        return {
            "status": "sent",
            "message_id": result["id"],
            "ind_ia": ind_ia,
            "ind_enviado": True
        }

    else:
        result = service.users().drafts().create(
            userId="me", body={"message": body}).execute()

        return {
            "status": "draft",
            "draft_id": result["id"],
            "ind_ia": ind_ia,
            "ind_enviado": False
        }
