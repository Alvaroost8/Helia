# Helia

Asistente inteligente  para asesorías fiscales y financieras. Helia utiliza GPT-4o-mini como motor de lenguaje y un sistema de agentes (planificador → ejecutor → redactor) para interpretar instrucciones en lenguaje natural, ejecutar herramientas y devolver respuestas claras al usuario.

---

## Características

- **Planificación automática** – Un agente LLM analiza la petición del usuario y decide qué herramientas ejecutar y en qué orden.
- **Ejecución encadenada** – Cada paso recibe el output del anterior para construir argumentos contextuales.
- **Redacción natural** – Los resultados técnicos se transforman en respuestas comprensibles para usuarios no técnicos.
- **Integración con Gmail** – Lectura de correos recientes y envío/borrador de emails vía la API de Gmail (OAuth 2.0).
- **Interfaz web** – Frontend con Flask para interactuar con Helia desde el navegador.
- **CLI** – Modo consola para pruebas rápidas.

---

## Estructura del proyecto

```
Helia/
├── app/
│   ├── agent.py          # Agentes LLM: planificador, ejecutor y redactor
│   ├── main.py           # Orquestador principal (función helia())
│   ├── tool_runner.py    # Registro y ejecución de herramientas
│   └── utils.py          # Carga de prompts y definiciones de tools
│
├── config/
│   ├── config.yaml       # Prompts del sistema (planificador, ejecutor, redactor)
│   ├── tools.yaml        # Definición de herramientas disponibles
│   ├── data_structures.yaml  # Esquemas de datos (Mail, etc.)
│   ├── settings.py       # Configuración adicional
│   ├── credentials.json  # Credenciales OAuth de Google (no versionado)
│   └── token.json        # Token de sesión Gmail (no versionado)
│
├── email_logic/
│   ├── auth.py           # Autenticación OAuth 2.0 con Gmail
│   └── gmail_client.py   # Cliente Gmail: lectura y envío de correos
│
├── frontend/
│   ├── app.py            # Servidor Flask (rutas / y /helia)
│   ├── templates/
│   │   └── index.html    # Interfaz web
│   └── static/
│       └── style.css     # Estilos
│
├── scripts/
│   └── test.py           # Scripts de prueba
│
├── ui/
│   └── web.py            # (reservado)
│
├── logs/                  # Directorio de logs
├── requirements.txt       # Dependencias Python
└── LICENSE.txt            # Licencia MIT
```

---

## Herramientas disponibles

| Herramienta | Descripción |
|---|---|
| `get_last_emails` | Devuelve los últimos *n* emails recibidos |
| `send_email` | Envía un email o lo guarda como borrador |

---

## Requisitos previos

- **Python 3.10+**
- Una cuenta de Google con la **API de Gmail habilitada** y un archivo `credentials.json` de OAuth 2.0.
- Una **API key de OpenAI** con acceso a `gpt-4o-mini`.

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Alvaroost8/Helia.git
cd Helia

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Configuración

1. **Variables de entorno** – Crea un archivo `.env` en la raíz:

   ```env
   OPENAI_KEY=sk-...
   ```

2. **Credenciales de Gmail** – Coloca tu archivo `credentials.json` de Google Cloud en `config/`. La primera ejecución abrirá el navegador para autorizar el acceso y generará `config/token.json` automáticamente.

---

## Uso

### Interfaz web

```bash
python -m frontend.app
```

Abre `http://127.0.0.1:5000` en el navegador.

### Línea de comandos

```bash
python -m app.main
```

Escribe tu instrucción y Helia planificará, ejecutará las herramientas necesarias y te devolverá una respuesta.

### Ejemplos de prompts

- *"¿Cuáles son mis últimos 3 correos?"*
- *"Responde a mi último correo diciendo que mañana a las 11 le llamo"*
- *"Envía un email a ejemplo@mail.com con el asunto Reunión y dile que confirmo asistencia"*

---

## Arquitectura

```
Usuario ──► Planificador (LLM)
                 │
                 ▼
            ┌─ Step 1 ─► Ejecutor (LLM) ─► Tool Runner ─► Gmail API
            │
            ├─ Step 2 ─► Ejecutor (LLM) ─► Tool Runner ─► ...
            │
            └─ ...
                 │
                 ▼
           Redactor (LLM) ──► Respuesta final
```

1. **Planificador** – Recibe el prompt del usuario y genera un plan de ejecución (lista de steps con herramientas y argumentos) o responde directamente si no se requieren herramientas.
2. **Ejecutor** – Para cada step posterior al primero, genera los argumentos basándose en el output del paso anterior.
3. **Tool Runner** – Ejecuta la herramienta correspondiente y devuelve el resultado.
4. **Redactor** – Toma todos los resultados y genera una respuesta clara en lenguaje natural.

---

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE.txt).

---

*Desarrollado por [Sistemas Helion](https://github.com/Alvaroost8)*
