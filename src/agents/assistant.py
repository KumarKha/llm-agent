from ollama import chat
from ollama import ChatResponse

from src.memory import load_history, save_message
from src.tools import tools, tool_registry


def conductor(
    user_message: str, session_id: str = "default_user", model: str = "llama3.2"
) -> str:
    """
    The Core Agent Conductor. Manages the conversation state and executes an autonomous perception loop to fulfill user goals.
    """
    # Log the incoming user message to long-term memory
    save_message(session_id=session_id, role="user", content=user_message)

    running = True
    iterations = 0
    max_iterations = 5
    final_output = ""

    while running:
        iterations += 1
        if iterations > max_iterations:
            print(f"⚠️ Safety brake triggered: Exceeded {max_iterations} iterations")
            final_output = "I apologize, but processing this request took too many steps. Could you try rephrasing"
            break

        messages = load_history(
            session_id=session_id, limit_turns=10, include_tools=True
        )
        print(f"🧠 Conductor Thinking (Iteration {iterations})...")

        response: ChatResponse = chat(model=model, messages=messages, tools=tools)
        assistant_msg = response["message"]

        if "tool_calls" in assistant_msg:
            print("🔧 Action Required: Model requested tool execution.")
            save_message(
                session_id=session_id,
                role="assistant",
                content=assistant_msg.get("content") or "",
            )

            for tool_call in assistant_msg["tool_calls"]:
                tool_call_id = tool_call.get("id") or tool_call.get("id", "fallback_id")
                name = tool_call["function"]["name"]
                args = tool_call["function"]["arguments"]

                tool_fn = tool_registry.get(name)
                if tool_fn:
                    print(f"⚙️ Executing {name} with arguments: {args}")
                    tool_result = tool_fn(**args)
                    print(f"📥 Tool Output Caught: {tool_result[:100]}...")
                else:
                    tool_result = f"Error: Tool '{name}' not found"

                save_message(
                    session_id=session_id,
                    role="tool",
                    name=name,
                    content=str(tool_result),
                    tool_call_id=tool_call_id,
                )
        else:
            final_output = assistant_msg["content"]

            save_message(session_id=session_id, role="assistant", content=final_output)
            running = False
    return final_output


if __name__ == "__main__":
    TEST_SESSION = "search_verification_chat"

    print("🧹 Wiping previous test history...")
    from src.memory import clear_session

    clear_session(TEST_SESSION)

    print("\n💬 --- TRIGGERING SEARCH TOOL TEST ---")
    # This prompt forces the model to realize it doesn't know the answer
    # internally and must use 'execute_web_search'
    prompt = "What were the major technology headlines or announcements made yesterday?"
    print(f"User: {prompt}\n")

    reply = conductor(user_message=prompt, session_id=TEST_SESSION)

    print("\n--- Final Agent Reply ---")
    print(reply)
    print("-------------------------")
