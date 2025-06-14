import sys
import os
import asyncio
import json

# Add the project directory to the Python path to allow importing langchain_tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from langchain_tool import LangChainTool

async def run_test():
    print("--- Testing LangChainTool directly ---")

    tool = LangChainTool()

    # Test case 1: Instantiate ChatOpenAI
    # Note: This requires 'langchain-openai' to be installed and potentially an OpenAI API key
    # If you don't have an OpenAI API key, this might fail, but it will confirm the tool's
    # ability to attempt the import and instantiation.
    print("\nAttempting to instantiate ChatOpenAI...")
    result_openai = tool.call(
        module_name='langchain_openai.chat_models',
        function_or_class_name='ChatOpenAI',
        args=json.dumps({}) # Empty dictionary as JSON string
    )
    print(f"Result (ChatOpenAI): {result_openai}")

    # Test case 2: Attempt to import a non-existent module/class
    print("\nAttempting to call a non-existent module/class...")
    result_fail = tool.call(
        module_name='non_existent_module',
        function_or_class_name='NonExistentClass',
        args=json.dumps({})
    )
    print(f"Result (Fail Test): {result_fail}")

    # Test case 3: Call a function (example: a simple string manipulation from a dummy module)
    # For this to work, you'd need a module like 'my_dummy_module.py' with a function 'reverse_string'
    # For now, this will likely fail with ImportError or AttributeError, but tests the path.
    print("\nAttempting to call a dummy function (will likely fail without dummy module)...")
    result_func = tool.call(
        module_name='os.path', # Using a standard library module for demonstration
        function_or_class_name='join',
        args=json.dumps({"path1": "dir", "path2": "file.txt"})
    )
    print(f"Result (os.path.join): {result_func}")


if __name__ == "__main__":
    asyncio.run(run_test())
