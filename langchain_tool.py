from qwen_agent.tools import BaseTool
import json
import importlib

class LangChainTool(BaseTool):
    name = "LangChainTool"
    description = "A tool to access various functionalities provided by the LangChain library. " \
                  "Specify the LangChain module, function/class name, and arguments in JSON format. " \
                  "Example: {'module_name': 'langchain.chains', 'function_or_class_name': 'LLMChain', 'args': {'llm': 'your_llm', 'prompt': 'your_prompt'}}"
    parameters = [
        {
            "name": "module_name",
            "type": "string",
            "description": "The full path to the LangChain module (e.g., 'langchain.chains', 'langchain.document_loaders')."
        },
        {
            "name": "function_or_class_name",
            "type": "string",
            "description": "The name of the function or class within the specified module to use (e.g., 'LLMChain', 'TextLoader')."
        },
        {
            "name": "args",
            "type": "string",
            "description": "A JSON string of arguments to pass to the LangChain function or class constructor. " \
                           "If the function/class requires an LLM, assume 'llm' is already configured by the agent."
        }
    ]

    def call(self, module_name: str, function_or_class_name: str, args: str, **kwargs) -> str:
        try:
            parsed_args = json.loads(args)

            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Get the function or class from the module
            target_callable = getattr(module, function_or_class_name)

            # If it's a class, instantiate it. If it's a function, call it directly.
            if isinstance(target_callable, type): # It's a class
                # Assuming 'llm' might be a common argument for many LangChain classes/functions
                # You might need more sophisticated LLM handling here, e.g., passing the agent's LLM
                # For now, let's assume the LLM is configured within the LangChain component itself or passed as an arg.
                instance = target_callable(**parsed_args)
                # If the instantiated object has a 'run' or '__call__' method, you might want to call it.
                # This part needs more specific guidance on what you expect from a LangChain "functionality".
                # For now, we'll just return a confirmation of instantiation.
                return f"Successfully instantiated {function_or_class_name} from {module_name}. Instance: {instance}"
            else: # It's a function
                result = target_callable(**parsed_args)
                return str(result)

        except json.JSONDecodeError:
            return "Error: 'args' must be a valid JSON string."
        except ImportError:
            return f"Error: Could not import module '{module_name}'. Please check the module name."
        except AttributeError:
            return f"Error: '{function_or_class_name}' not found in module '{module_name}'. Please check the function/class name."
        except Exception as e:
            return f"An error occurred in LangChainTool: {e}"
