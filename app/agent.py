import os
import json
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from app.utils import load_prompts, build_tools_definition

load_dotenv()

PROMPTS = load_prompts()
TOOLS_DEFINITION = build_tools_definition()
OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

def plan_step(user_prompt: str) -> list:
    prompt = PROMPTS["planificador"].format(
        tools_definition=TOOLS_DEFINITION
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return json.loads(response.choices[0].message.content)

def execute_step(user_prompt, steps, previous_output, tool_name):
    prompt = PROMPTS["ejecutor"].format(
        tools_definition=TOOLS_DEFINITION,
        prompt_inicial=user_prompt,
        steps=json.dumps(steps, indent=2),
        output=json.dumps(previous_output, indent=2),
        tool=tool_name,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0,
    )

    return json.loads(response.choices[0].message.content)["arguments"]

def summarize_step(tool_results):
    prompt = PROMPTS["redactor"].format(
        tool_results=json.dumps(tool_results, indent=2)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3,
    )

    return json.loads(response.choices[0].message.content)["response"]
