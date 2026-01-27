from app.tool_runner import run_tool

print(
    run_tool(
        "send_email",
        {"destinatario": "jon8gs8@gmail.com",
        "asunto": "Prueba final día 3",
        "cuerpo": "Si este mail te llega con disclaimer, he terminado el día 3.",
        "ind_ia": True,
        "ind_enviar": True}
    )
)