from app.agent import decide_tool
from app.tool_runner import run_tool

def main():
    user_input = input("Usuario: ")

    tool_call = decide_tool(user_input)

    if not tool_call:
        print("No se decidió ninguna tool")
        return

    result = run_tool(
        tool_call["tool"],
        tool_call["arguments"]
    )

    print("Resultado:")
    print(result)


if __name__ == "__main__":
    main()