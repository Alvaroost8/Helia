from email_logic.gmail_client import get_last_emails, send_email

def tool_get_last_emails(max_results: int = 5):
    return get_last_emails(max_results=max_results)

def tool_send_email(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    ind_ia: bool = True,
    ind_enviar: bool = False
    ):
    return send_email(
        destinatario=destinatario,
        asunto=asunto,
        cuerpo=cuerpo,
        ind_ia=ind_ia,
        ind_enviar=ind_enviar)