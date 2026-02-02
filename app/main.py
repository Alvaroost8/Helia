from app.agent import plan_step, execute_step, summarize_step
from app.tool_runner import run_tool

def main():
    user_input = input("Usuario: ")

    plan = plan_step(user_input)

    if 'respuesta' in plan:
        if not plan['predefinida']:
            plan['respuesta'] += ("\n\nDisclaimer: esta respuesta ha sido generada " 
            "usando los conocimientos previos de Helia y podría ser errónea. ")

        print("\nRespuesta:\n")
        print(plan['respuesta'])
        return

    tool_results = []

    steps = plan["steps"]

    tool_name, arguments = steps[0]["tool"], steps[0]["arguments"]

    output = run_tool(tool_name, arguments)

    tool_results.append({
        "tool": tool_name,
        "arguments": arguments,
        "output": output,
    })

    previous_output = output

    if len(steps) > 1:
        for step in steps[1:]:
            tool_name = step["tool"]

            arguments = execute_step(
                user_prompt=user_input,
                steps=steps,
                previous_output=previous_output,
                tool_name=tool_name,
            )

            output = run_tool(tool_name, arguments)

            tool_results.append({
                "tool": tool_name,
                "arguments": arguments,
                "output": output,
            })

            previous_output = output

    final_response = summarize_step(tool_results)
    print("\nRespuesta:\n")
    print(final_response)

if __name__ == "__main__":
    main()