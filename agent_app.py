import asyncio
import os
from qwen_agent.agents import Assistant
from qwen_agent.tools import CodeInterpreter, WebSearch, Retrieval
from langchain_tool import LangChainTool

# Configuration for the LLM (Qwen3 model via FastAPI proxy)
# Uses environment variables for flexibility, defaulting to local proxy
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'qwen') 
LLM_API_BASE = os.getenv('LLM_API_BASE', 'http://localhost:80/v1')
LLM_API_KEY = os.getenv('LLM_API_KEY', 'EMPTY') 

# Super Assistant Persona Definition
SUPER_ASSISTANT_PERSONA = """
You are a Super Assistant — highly intelligent, proactive, and fully dedicated to helping me achieve my goals efficiently. Your core traits are:

1. Always ready to assist me promptly with clear, actionable, and precise responses.
2. Continuously looking for new tools, techniques, and methods that can improve your ability to support me better.
3. Proactively suggesting better alternatives or optimizations without waiting to be asked.
4. Keeping my priorities and preferences in mind, tailoring your help to my needs.
5. Approaching every problem as an opportunity to provide the best possible assistance, including research, tool integration, or step-by-step guidance.
6. Communicating in an encouraging, confident, and respectful tone.
7. When unsure, you transparently explain the limits and propose ways to explore further or learn more.

Whenever I give you a task or ask a question, you respond not only with an answer but also with suggestions on how to improve the process or outcome.

Begin every interaction with a readiness mindset: "I’m here to help you achieve your goals—let’s make it happen!"

You have the following tools available: a Python execution environment, a web browser for searching and accessing URLs, a document knowledge base (like ChromaDB) for information retrieval, and a LangChainTool for accessing various LangChain functionalities.
"""

async def run_agent_task():
    print("--- Initializing Qwen-Agent ---")

    # Configure the LLM settings
    llm_cfg = {
        'model': LLM_MODEL_NAME,
        'model_server': LLM_API_BASE,
        'api_key': LLM_API_KEY,
        'generate_cfg': {
            'top_p': 0.8,
        },
        'system_message': SUPER_ASSISTANT_PERSONA 
    }

    # Initialize tools
    tools = [
        CodeInterpreter(),
        WebSearch(),
        Retrieval(),
        LangChainTool()
    ]

    # Initialize the Assistant agent with the LLM config and tools
    try:
        print('--- Initializing Qwen-Agent ---')
        agent = Assistant(
            llm=llm_cfg,
            system_message=SUPER_ASSISTANT_PERSONA,
            function_list=tools
        )
        print("LLM and Tools initialized successfully.")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    print("Agent initialized successfully. Running test query...")

    # Main interaction loop
    print("--- Super Assistant Interactive Chat ---")
    print("Type 'exit' to end the chat.")
    while True:
        try:
            query = input('User> ')
            if query.lower() == 'exit':
                print("Exiting...")
                break
            
            messages = [{'role': 'user', 'content': query}]
            response_iterator = agent.run(messages=messages)
            
            print("Assistant> ", end="")
            full_response = ""
            for chunk in response_iterator:
                content_to_print = ""
                if hasattr(chunk, 'content') and chunk.content and isinstance(chunk.content, str):
                    content_to_print = chunk.content
                elif isinstance(chunk, list):
                    assistant_content = ''
                    for msg in reversed(chunk):
                        if isinstance(msg, dict) and msg.get('role') == 'assistant':
                            assistant_content = msg.get('content', '')
                            break
                    if isinstance(assistant_content, str) and assistant_content.startswith(full_response):
                        content_to_print = assistant_content[len(full_response):]

                if content_to_print:
                    print(content_to_print, end="", flush=True)
                    full_response += content_to_print
            print() # Newline after assistant's full response

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run_agent_task())
