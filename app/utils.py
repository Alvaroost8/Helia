import yaml
import os

TOOLS_PATH = r".\config\tools.yaml"
PROMPTS_PATH = r".\config\config.yaml"

def load_prompts():
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    

def build_tools_definition() -> str:
    with open(TOOLS_PATH, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    lines = []

    for tool in schema["tools"]:
        lines.append(f"- {tool['name']}: {tool['description']}")

        if "inputs" in tool:
            lines.append("  inputs:")
            for name, meta in tool["inputs"].items():
                lines.append(
                    f"    - {name} ({meta['type']}): {meta['description']}"
                )
        
        if "reglas" in tool:
            lines.append("  Reglas de la herramienta:")
            lines.append(tool["reglas"])

    return "\n".join(lines)