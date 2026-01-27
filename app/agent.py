def decide_tool(user_input: str):
    if "get" in user_input.lower():
        return {
            "tool": "get_last_emails",
            "arguments": {
                "num_emails": 3
            }
        }

    if "send" in user_input.lower():
        return {
            "tool": "send_email",
            "arguments": {
                "destinatario": "jon8gs8@gmail.com",
                "asunto": "Demo Helia",
                "cuerpo": "Correo enviado desde el agent"
            }
        }

    return None
